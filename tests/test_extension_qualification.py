import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from extension_qualification import require_qualified
from unified_campaign import command_for

def test_unqualified_mistral_refuses_admission():
    plan=json.loads((ROOT/'config/mistral-campaign-20261003.json').read_text())
    spec=json.loads((ROOT/plan['model_lock']).read_text())['models'][0]
    spec=dict(spec,execution_ready=False)
    with pytest.raises(RuntimeError,match='not explicitly qualified'):require_qualified(ROOT,plan,{spec['id']:spec})

def test_every_extension_command_uses_separate_lock_and_campaign_with_original_budgets():
    plan=json.loads((ROOT/'config/mistral-campaign-20261003.json').read_text());spec=json.loads((ROOT/plan['model_lock']).read_text())['models'][0]
    for job in plan['jobs']:
        cmd,budget=command_for(job,spec,plan['model_lock'],plan['id'])
        assert cmd[cmd.index('--lock')+1]==plan['model_lock']
        assert cmd[cmd.index('--campaign-id')+1]==plan['id']
        expected={'speed':7600,'repo':7800 if job.get('max_turns')==20 else 4200,'replay':15000,'quality':86400,'serving':7200}
        assert budget==expected[job['kind']]


def test_mistral_declared_no_reasoning_is_explicit_in_task_and_counting_template():
    from unified_server import chat_payload,template_kwargs
    spec={'id':'mistral-medium35-q4','runtime':'llama-cpp'}
    payload=chat_payload(spec,[{'role':'user','content':'test'}])
    assert payload['reasoning_effort']=='none'
    assert payload['chat_template_kwargs']==template_kwargs(spec)=={'reasoning_effort':'none'}
    assert template_kwargs({'id':'qwen38-q4-gguf'})=={'enable_thinking':False}


def test_modified_linked_library_refuses_an_otherwise_qualified_runtime(tmp_path):
    from extension_qualification import digest
    server=tmp_path/'server';server.write_bytes(b'launcher')
    library=tmp_path/'library.dylib';library.write_bytes(b'qualified library')
    lock=tmp_path/'runtime.json';lock.write_text('{}')
    files=[{'path':p.name,'sha256':digest(p)} for p in [server,library]]
    native={'lock':'runtime.json','server':'server','commit':'pinned-source','files':files}
    spec={'id':'mistral','extension':True,'execution_ready':True,'revision':'model-rev','files':[],
          'qualification_receipt':'qualification.json','native_runtime':native}
    q={k:True for k in ['artifact_hashes_verified','runtime_load_passed','exact_token_count_passed','task_interface_passed','reasoning_control_passed','long_context_metadata_passed']}
    q.update(status='complete',run_id='qualification-test',model_revision=spec['revision'],model_files=[],runtime_lock_sha256=digest(lock),
             native_server_sha256=digest(server),runtime_source_commit='pinned-source',runtime_files=files)
    (tmp_path/'qualification.json').write_text(json.dumps(q))
    (tmp_path/'qualification-driver.json').write_text(json.dumps({'status':'complete','run_id':'qualification-test'}))
    require_qualified(tmp_path,{}, {'mistral':spec})
    library.write_bytes(b'changed library')
    with pytest.raises(RuntimeError,match='Qualified linked runtime changed'):
        require_qualified(tmp_path,{}, {'mistral':spec})


def test_explicit_native_reasoning_settings_are_required():
    from qualify_mistral import rendered_reasoning_effort
    assert rendered_reasoning_effort('prefix[MODEL_SETTINGS]{"reasoning_effort":"none"}[/MODEL_SETTINGS]suffix')=='none'
    assert rendered_reasoning_effort('[MODEL_SETTINGS]{"reasoning_effort":"high"}[/MODEL_SETTINGS]')=='high'
    with pytest.raises(RuntimeError,match='omitted explicit model settings'):rendered_reasoning_effort('plain template')
    with pytest.raises(RuntimeError,match='Unsupported rendered'):rendered_reasoning_effort('[MODEL_SETTINGS]{"reasoning_effort":"low"}[/MODEL_SETTINGS]')


def test_failed_qualification_cannot_be_admitted_even_if_gate_flags_remain_true(tmp_path):
    spec={'id':'mistral','extension':True,'execution_ready':True,'qualification_receipt':'qualification.json'}
    q={k:True for k in ['artifact_hashes_verified','runtime_load_passed','exact_token_count_passed','task_interface_passed','reasoning_control_passed','long_context_metadata_passed']}
    q['status']='failed'
    (tmp_path/'qualification.json').write_text(json.dumps(q))
    with pytest.raises(RuntimeError,match='did not complete'):require_qualified(tmp_path,{}, {'mistral':spec})


def test_native_chat_count_includes_only_explicit_model_special_tokens(monkeypatch):
    import unified_server
    seen=[]
    def post(port,path,payload,*args):
        seen.append((path,payload))
        if path=='/apply-template':return {'prompt':'rendered Mistral chat'}
        return {'tokens':[1,2,3] if payload['add_special'] else [2,3]}
    monkeypatch.setattr(unified_server,'post',post)
    messages=[{'role':'user','content':'probe'}]
    base={'id':'qwen38-q4-gguf','runtime':'llama-cpp'}
    assert unified_server.count_chat(base,None,messages,123)==2
    assert seen[-1][1]['add_special'] is False
    mistral={'id':'mistral-medium35-q4','runtime':'llama-cpp','native_add_special_tokens':True}
    assert unified_server.count_chat(mistral,None,messages,123)==3
    assert seen[-1][1]['add_special'] is True
