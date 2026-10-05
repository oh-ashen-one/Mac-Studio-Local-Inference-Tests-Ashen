#!/usr/bin/env python3
"""CPU-only tokenizer/parser qualification. Never loads model weights or serves."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from model_registry import resolve_model
from text_runtime import tokenizer_options
from models import digest

def main():
    from mlx_lm.utils import load_tokenizer
    spec,folder,lock=resolve_model('mimo-v2.6-flash-mopd','config/additional-models.lock.json')
    config=json.loads((folder/'config.json').read_text())
    original=load_tokenizer(folder,tokenizer_config_extra=tokenizer_options(folder,config),eos_token_ids=config['eos_token_id'])
    fixed=load_tokenizer(folder,tokenizer_config_extra=tokenizer_options(folder,config,True),eos_token_ids=config['eos_token_id'])
    tools=[{'type':'function','function':{'name':'bash','parameters':{'type':'object','properties':{'command':{'type':'string'}}}}}]
    messages=[{'role':'user','content':'Read the repository listing.'}]
    args=dict(tools=tools,tokenize=True,add_generation_prompt=True)
    assert original.apply_chat_template(messages,**args)==fixed.apply_chat_template(messages,**args)
    fixture='<function=bash><parameter=command>ls src</parameter></function>'
    rejected=False
    try:original.tool_parser(fixture,tools)
    except ValueError:rejected=True
    assert rejected,'Expected the original JSON parser mismatch'
    parsed=fixed.tool_parser(fixture,tools)
    assert parsed=={'name':'bash','arguments':{'command':'ls src'}}
    record={'kind':'cpu_tokenizer_parser_validation','passed':True,'model_lock_sha256':digest(lock),'chat_template_sha256':digest(folder/'chat_template.jinja'),'original_parser':original.tool_parser.__module__,'corrected_parser':fixed.tool_parser.__module__,'original_rejects_declared_xml':rejected,'prompt_token_ids_unchanged':True,'fixture':fixture,'parsed':parsed,'no_tools_executed':True,'no_model_weights_loaded':True,'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
    out=ROOT/'work/mimo-xml-parser-validation.json';out.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))

if __name__=='__main__':main()
