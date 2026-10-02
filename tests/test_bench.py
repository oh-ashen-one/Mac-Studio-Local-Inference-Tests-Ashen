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


def test_gemma_channel_diagnostic_parsing():
    from quality_smoke import final_json
    assert final_json('<|channel>thought\nCompute.\n<channel|>{"answer": 3}')=={'answer':3}


def test_comparison_cli_pairs_results_and_reports_failure(tmp_path):
    import subprocess
    base={'kind':'hardware_microbenchmark','model_id':'fixture','session':0,'model_revision':'test',
          'cell':{'id':'small','repeat':0,'warmup':False},'status':'ok','decode_tok_s':10}
    old=tmp_path/'old.jsonl';new=tmp_path/'new.jsonl';out=tmp_path/'comparison.json'
    old.write_text(json.dumps({**base,'machine_id':'studio-old'})+'\n')
    new.write_text(json.dumps({**base,'machine_id':'studio-new','decode_tok_s':20})+'\n')
    subprocess.run([sys.executable,str(ROOT/'scripts/compare.py'),str(old),str(new),'--output',str(out)],check=True,capture_output=True)
    report=json.loads(out.read_text())
    assert report['rows'][0]['median_paired_speedup']==2
    assert report['rows'][0]['matched_pairs']==1
    assert report['rows'][0]['bootstrap_95_low'] is None
    assert out.with_suffix('.csv').exists()
    new.write_text(json.dumps({**base,'machine_id':'studio-new','status':'error'})+'\n')
    result=subprocess.run([sys.executable,str(ROOT/'scripts/compare.py'),str(old),str(new),'--output',str(out)],capture_output=True)
    assert result.returncode!=0
    assert json.loads(out.read_text())['excluded_pairs']
    assert not out.with_suffix('.csv').exists()


@pytest.mark.parametrize('script,args',[
    ('bench.py',['--machine','studio-old','--output','work/guard-test.jsonl']),
    ('serve.py',['qwen-27b']),
    ('quality_smoke.py',['--model','qwen-27b','--output','work/guard-test.jsonl'])
])
def test_inference_requires_explicit_start_flag(script,args):
    import subprocess
    run=subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],capture_output=True,text=True)
    assert run.returncode==2
    assert 'Preparation-only mode' in run.stderr


def test_preview_serves_only_saved_data_without_gpu(tmp_path):
    from preview import ThreadingHTTPServer,handler_for
    import threading,urllib.request,urllib.error
    server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(tmp_path/'absent.json'))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        base='http://127.0.0.1:'+str(server.server_address[1])
        with urllib.request.urlopen(base+'/api/state') as response:payload=json.load(response)
        assert len([m for m in payload['models'] if not m.get('additional')])==3
        assert {m['id'] for m in payload['models'] if m.get('additional')}=={m['id'] for m in json.loads((ROOT/'config/additional-models.lock.json').read_text())['models']}
        assert payload['comparison'] is None
        with urllib.request.urlopen(base+'/') as response:assert b'Mac Studio Local Inference Tests Ashen' in response.read()
        for asset,mime in [('/style.css','text/css'),('/app.js','text/javascript')]:
            with urllib.request.urlopen(base+asset) as response:
                assert response.status==200 and response.headers['Content-Type'].startswith(mime)
                assert len(response.read())>100
        with pytest.raises(urllib.error.HTTPError):urllib.request.urlopen(base+'/../README.md')
    finally:server.shutdown();server.server_close();thread.join()


def test_ready_receipt_rejects_missing_native_runtime(tmp_path):
    from finish_prepare import verify_runtime
    (tmp_path/'requirements-macos-arm64.lock').write_text('')
    with pytest.raises(RuntimeError,match='Missing native runtime binary'):
        verify_runtime(tmp_path)


def test_ready_receipt_rejects_dependency_drift(tmp_path,monkeypatch):
    import finish_prepare
    (tmp_path/'requirements-macos-arm64.lock').write_text('mlx==0.32.3\n')
    monkeypatch.setattr(finish_prepare.importlib.metadata,'version',lambda _: 'different')
    with pytest.raises(RuntimeError,match='Runtime version mismatch'):
        finish_prepare.verify_runtime(tmp_path)


def test_firstlook_summary_excludes_warmup_and_failed_runs():
    from first_test import summarize
    def row(rate,warmup=False,status='ok'):return {'kind':'initial_speed_test','cell':{'warmup':warmup},'status':status,'decode_tok_s':rate}
    s=summarize([row(999,True),row(20),row(30),row(25),row(1000,status='error')])
    assert s=={'measured_repeats':3,'fastest_decode_tok_s':30,'median_decode_tok_s':25}


def test_mimo_base_loader_excludes_only_the_declared_draft():
    from text_runtime import exclude_mimo_draft
    weights={f'model.mtp.layers.{i//14}.tensor{i}':i for i in range(42)}
    weights.update({'model.layers.0.weight':'keep','model.mtp_like.weight':'keep too'})
    assert exclude_mimo_draft(weights)=={'model.layers.0.weight':'keep','model.mtp_like.weight':'keep too'}
    weights.pop('model.mtp.layers.0.tensor0')
    with pytest.raises(ValueError,match='exactly 42'):exclude_mimo_draft(weights)


def test_explicit_mimo_xml_parser_keeps_files_unchanged_and_rejects_other_grammars(tmp_path):
    from text_runtime import tokenizer_options
    template=tmp_path/'chat_template.jinja'
    text="{{ '<tool_call><function=' ~ tool_call.name }}<parameter=command>"
    template.write_text(text)
    config={'model_type':'mimo_v2'}
    assert 'tool_parser_type' not in tokenizer_options(tmp_path,config)
    assert tokenizer_options(tmp_path,config,True)['tool_parser_type']=='qwen3_coder'
    assert template.read_text()==text
    with pytest.raises(ValueError):tokenizer_options(tmp_path,{'model_type':'qwen3_5'},True)
    template.write_text('{{ tool_call | tojson }}')
    with pytest.raises(ValueError):tokenizer_options(tmp_path,config,True)


def test_unified_exact_context_builder_never_returns_a_short_prompt(tmp_path,monkeypatch):
    import unified_server
    monkeypatch.setattr(unified_server,'count_chat',lambda spec,folder,messages,port:len(messages[1]['content'])//2+20)
    messages,count=unified_server.fill_to_tokens({},tmp_path,'system','prefix','x'*10000,'suffix',1000)
    assert 1000<=count<=1032
    with pytest.raises(RuntimeError,match='exact declared input range'):
        unified_server.fill_to_tokens({},tmp_path,'system','','x'*20,'',1000)


def test_unified_evaluator_restricts_escape_routes_but_accepts_math():
    from unified_quality import check_code,ARITHMETIC_EVAL
    check_code('import hashlib\ndef f(x):\n return hashlib.md5(x.encode()).hexdigest()')
    for code in ['import os','import random\nx=random._os','from random import _os','x=open("/tmp/x")','import operator\nx=operator.attrgetter("__globals__")']:
        with pytest.raises(ValueError):check_code(code)
    namespace={};exec(ARITHMETIC_EVAL,namespace)
    assert namespace['eval']('2+3*4-5')==9
    with pytest.raises(ValueError):namespace['eval']('__import__("os")')


def test_unified_matrix_covers_each_downloaded_configuration_equally():
    plan=json.loads((ROOT/'config/unified-campaign.json').read_text())
    assert plan['overall_deadline'] is None
    counts=[]
    for model in plan['models']:
        jobs=[j for j in plan['jobs'] if j['model_id']==model]
        for size in [8192,32768,131072,200000]:
            assert len([j for j in jobs if j['kind']=='speed' and j['tokens']==size and j['output_tokens']==256])==5
        assert len([j for j in jobs if j['kind']=='repo' and j['max_turns']==8])==5
        assert len([j for j in jobs if j['kind']=='repo' and j['max_turns']==20])==3
        assert {j['suite'] for j in jobs if j['kind']=='quality'}=={'structured','retrieval','humaneval'}
        counts.append(len(jobs))
    assert len(plan['models'])==6 and len(set(counts))==1
