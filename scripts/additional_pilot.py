#!/usr/bin/env python3
"""Bounded runtime validation for an explicitly pinned additional MLX artifact."""
import argparse,datetime,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from model_registry import resolve_model
from models import verify,digest
from first_test import shared_gpu_slot,safety,write_json
from text_runtime import load_text,runtime_lock

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--lock',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--backend',choices=['mlx-lm','mlx-vlm'],default='mlx-lm');a=p.parse_args()
    if not a.allow_inference:p.error('Owner inference authorization required')
    spec,folder,lock=resolve_model(a.model,a.lock);out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    result={'kind':'runtime_validation','model_id':a.model,'machine_id':'studio-new','status':'starting','model_revision':spec['revision'],'model_lock_sha256':digest(lock),'runtime_lock_sha256':digest(ROOT/'requirements-macos-arm64.lock'),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':[],'not_a_benchmark_result':True}
    result.update(backend=a.backend,runtime_lock_sha256=digest(runtime_lock(a.backend)),modality='text only',speculation=False)
    def save():write_json(out/'result.json',result)
    save()
    try:
        with shared_gpu_slot():
            result['preflight']=safety('studio-new');verify(spec,folder)
            config=json.loads((folder/'config.json').read_text())
            if config.get('model_file'):raise RuntimeError('Custom model code requires independent review; not executed')
            import mlx.core as mx
            from mlx_lm import generate
            mx.set_memory_limit(int(__import__('psutil').virtual_memory().total*.82))
            start=time.perf_counter();model,tokenizer,_=load_text(folder,a.backend);mx.synchronize();result['load_s']=time.perf_counter()-start
            for prompt,expected in [('Reply with exactly the word READY and nothing else.','READY'),('Return only JSON: {"result": the value of 7 times 8}.','{"result":56}')]:
                rendered=tokenizer.apply_chat_template([{'role':'user','content':prompt}],add_generation_prompt=True,tokenize=False,enable_thinking=False)
                start=time.perf_counter();text=generate(model,tokenizer,prompt=rendered,max_tokens=128,verbose=False)
                answer=text.split('</think>')[-1].strip();passed=answer==expected if expected=='READY' else False
                if expected!='READY':
                    try:passed=json.loads(answer)=={'result':56}
                    except ValueError:pass
                result['tests'].append({'prompt':prompt,'output':text,'passed':passed,'wall_s':time.perf_counter()-start});save()
            result.update(status='complete',passed=all(t['passed'] for t in result['tests']),peak_metal_bytes=mx.get_peak_memory(),finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save()
    except BaseException as exc:result.update(status='failed',error=str(exc).replace(str(folder),'<model>').replace(str(ROOT),'<repo>'));save();raise
if __name__=='__main__':main()
