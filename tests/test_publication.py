import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import harvest_unified


def test_invalid_utf8_does_not_bypass_private_path_redaction(monkeypatch):
    machine = {'repository': '/private/test-m5/project',
               'target': 'benchmark@192.0.2.1'}
    monkeypatch.setattr(harvest_unified, 'connection', lambda: (machine, []))
    original = (b'\xefbroken\xff /private/test-m5/project/result.json '
                b'/private/test-m5/cache benchmark@192.0.2.1 192.0.2.1\x00')
    expected = (b'\xefbroken\xff <M5_REPO>/result.json '
                b'<M5_HOME>/cache <M5_SSH_TARGET> <M5_PRIVATE_HOST>\x00')
    assert harvest_unified.sanitize(original) == expected
    assert original.startswith(b'\xefbroken\xff /private/test-m5/project')


def test_utf8_and_non_private_binary_bytes_remain_intact(monkeypatch):
    machine = {'repository': '/private/test-m5/project',
               'target': 'benchmark@192.0.2.1'}
    monkeypatch.setattr(harvest_unified, 'connection', lambda: (machine, []))
    original = 'Native output: \u03bb \u4e2d'.encode('utf-8') + b'\xff\x00\xef'
    assert harvest_unified.sanitize(original) == original


def test_mistral_harvest_uses_separate_ledger_preserves_hashes_and_does_not_touch_baseline(monkeypatch,tmp_path):
    import io,json,tarfile,hashlib
    run='u20261003-mistral35-core-8192-r1'
    original=b'{"status":"complete","input_tokens":8192,"output_tokens":256}\n'
    archive=io.BytesIO()
    with tarfile.open(fileobj=archive,mode='w') as t:
        for name,data in [('result.json',original),('campaign-telemetry.json',b'[]\n')]:
            info=tarfile.TarInfo(name);info.size=len(data);t.addfile(info,io.BytesIO(data))
    (tmp_path/'results/unified-overnight-20261002').mkdir(parents=True)
    baseline=tmp_path/'results/unified-overnight-20261002/summary.json';baseline.write_bytes(b'baseline-original')
    responses=iter([json.dumps({'ids':[run],'state':{'status':'running','active':'another-group'}}).encode(),archive.getvalue(),b'',b'{"campaign_id":"mistral-extension-20261003"}',b'# Mistral\n'])
    calls=[]
    def remote(code):
        calls.append(code)
        return next(responses)
    monkeypatch.setattr(harvest_unified,'ROOT',tmp_path)
    monkeypatch.setattr(harvest_unified,'remote',remote)
    monkeypatch.setattr(harvest_unified,'sanitize',lambda data:data)
    harvest_unified.harvest('mistral')
    assert 'work/mistral-campaign.json' in calls[0] and 'work/mistral-campaign.json' in calls[1]
    assert 'config/mistral-campaign-20261003.json' in calls[2]
    assert baseline.read_bytes()==b'baseline-original'
    assert (tmp_path/'results'/run/'result.json').read_bytes()==original
    receipt=json.loads((tmp_path/'results'/run/'publication.json').read_text())
    expected=hashlib.sha256(original).hexdigest()
    assert receipt['files']['result.json']=={'original_sha256':expected,'published_sha256':expected}
    assert (tmp_path/'results/mistral-extension-20261003/summary.json').exists()


def test_mistral_harvest_rejects_a_baseline_id_before_copying(monkeypatch,tmp_path):
    import json,pytest
    monkeypatch.setattr(harvest_unified,'ROOT',tmp_path)
    monkeypatch.setattr(harvest_unified,'remote',lambda code:json.dumps({'ids':['u20261002-gemma-core-8192-r1'],'state':{'status':'running'}}).encode())
    with pytest.raises(AssertionError):harvest_unified.harvest('mistral')
    assert not (tmp_path/'results').exists()


def test_qualification_driver_blocks_runtime_updates_after_baseline_exits(tmp_path):
    import json
    (tmp_path/'work').mkdir()
    (tmp_path/'work/unified-campaign.json').write_text(json.dumps({'pid':10}))
    (tmp_path/'work/mistral-qualification-driver.json').write_text(json.dumps({'pid':20,'status':'running'}))
    active=harvest_unified.active_controls(tmp_path,lambda pid:pid==20)
    assert active==['work/mistral-qualification-driver.json']


def test_download_verification_control_is_protected_even_without_model_worker(tmp_path):
    import json
    (tmp_path/'work').mkdir()
    (tmp_path/'work/mistral-preparation.json').write_text(json.dumps({'pid':30,'status':'verifying'}))
    assert harvest_unified.active_controls(tmp_path,lambda pid:pid==30)==['work/mistral-preparation.json']
    assert harvest_unified.active_controls(tmp_path,lambda pid:False)==[]
