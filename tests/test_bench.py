import importlib.util
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from bench import timing_summary,synthetic_prompt,canonical_hash
from models import verify,digest


def test_decode_excludes_first_token_and_uses_wall_interval():
    result=timing_summary(10,[12,12.5,13],13.2)
    assert result['ttft_s']==2
    assert result['decode_tok_s']==2
    assert result['generation_wall_s']==pytest.approx(3.2)


def test_short_or_empty_outputs_have_no_invented_decode_rate():
    assert timing_summary(0,[],1)['ttft_s'] is None
    assert timing_summary(0,[1],1)['decode_tok_s'] is None


def test_integrity_detects_same_length_corruption(tmp_path):
    p=tmp_path/'weights';p.write_bytes(b'abc')
    spec={'files':[{'path':'weights','bytes':3,'sha256':digest(p)}]}
    assert verify(spec,tmp_path)==1
    p.write_bytes(b'abd')
    with pytest.raises(ValueError,match='SHA256 mismatch'):verify(spec,tmp_path)


def test_prompt_pairing_is_exact_and_seed_sensitive():
    class Tokenizer:
        def encode(self,text,**kwargs): return list(text.encode())
    a=synthetic_prompt(Tokenizer(),512,1729)
    assert len(a)==512
    assert a==synthetic_prompt(Tokenizer(),512,1729)
    assert canonical_hash(a)!=canonical_hash(synthetic_prompt(Tokenizer(),512,1730))


def test_model_lock_has_hashes_for_all_files():
    models=json.loads((ROOT/'config/models.lock.json').read_text())['models']
    assert len(models)==3
    for m in models:
        assert len(m['revision'])==40
        assert m['total_bytes']==sum(f['bytes'] for f in m['files'])
        assert all(len(f['sha256'])==64 for f in m['files'])


def test_comparison_rejects_changed_runtime_or_prompt():
    from compare import compatible
    a={'runtime_lock_sha256':'same','input_token_ids_sha256':'first'}
    compatible(a,dict(a))
    with pytest.raises(ValueError,match='input_token_ids_sha256'):
        compatible(a,{**a,'input_token_ids_sha256':'changed'})


def test_comparison_never_includes_smoke_or_warmup(tmp_path):
    from compare import records
    path=tmp_path/'rows.jsonl'
    path.write_text(json.dumps({'kind':'setup_smoke'})+'\n'+json.dumps({'kind':'hardware_microbenchmark','cell':{'warmup':True}})+'\n')
    assert records(path)=={}


def test_quality_diagnostic_requires_valid_exact_json():
    from quality_smoke import final_json
    assert final_json('<think>work</think>```json\n{"answer": 703}\n```')=={'answer':703}
    with pytest.raises(json.JSONDecodeError):final_json('The answer is 703.')


def test_bootstrap_lock_includes_runtime_dependencies():
    lock=(ROOT/'requirements-macos-arm64.lock').read_text()
    assert 'mlx==0.32.3' in lock
    assert 'mlx-lm==0.31.3' in lock
    assert 'transformers==5.17.0' in lock
