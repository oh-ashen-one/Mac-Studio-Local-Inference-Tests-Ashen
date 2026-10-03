import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from extension_qualification import require_qualified
from unified_campaign import command_for

def test_unqualified_mistral_refuses_admission():
    plan=json.loads((ROOT/'config/mistral-campaign-20261003.json').read_text())
    spec=json.loads((ROOT/plan['model_lock']).read_text())['models'][0]
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
