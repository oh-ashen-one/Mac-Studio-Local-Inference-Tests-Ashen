#!/usr/bin/env python3
"""Exact-token corpus fill/decode through the pinned llama.cpp native endpoint."""
import argparse,datetime,json,signal,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,write_json
from model_registry import resolve_model
from models import digest,verify
from bench import canonical_hash
from unified_server import server,post

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--run-id',required=True);p.add_argument('--tokens',type=int,default=200000);p.add_argument('--output-tokens',type=int,default=256);p.add_argument('--lock',default='config/unified-models.lock.json');p.add_argument('--campaign-id',default='unified-overnight-20261002');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec,folder,lock=resolve_model(a.model,a.lock);out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    r={'kind':'long_context','campaign_id':a.campaign_id,'machine_id':'studio-new','model_id':a.model,'status':'starting','backend':'llama-cpp','model_revision':spec['revision'],'model_lock_sha256':digest(lock),'runtime_commit':spec.get('native_runtime',{}).get('commit') or json.loads((ROOT/'config/agentperf.lock.json').read_text())['llama_commit'],'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'requested_input_tokens':a.tokens,'requested_output_tokens':a.output_tokens,'condition':'alone','sample_count':1,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prefix_cache':'Fresh server/slot; cache_prompt=false','speculation':False}
    def update():write_json(out/'result.json',r);write_json(ROOT/'work/unified-job-live.json',r)
    update()
    try:
        with shared_gpu_slot():
            r['preflight']=safety('studio-new');verify(spec,folder)
            with server(spec,folder,out,port=18183,context=a.tokens+a.output_tokens+512,cache_sequences=0) as (port,telemetry):
                corpus=ROOT/'work/context-corpus.txt';r['corpus_sha256']=digest(corpus)
                ids=post(port,'/tokenize',{'content':corpus.read_text(),'add_special':False,'parse_special':False},120)['tokens']
                if len(ids)<a.tokens:raise RuntimeError('Corpus too short')
                ids=ids[:a.tokens];r['input_token_ids_sha256']=canonical_hash(ids)
                payload={'prompt':ids,'n_predict':a.output_tokens,'temperature':0,'seed':1729,'ignore_eos':True,'cache_prompt':False,'stream':True,'return_tokens':True}
                request=urllib.request.Request(f'http://127.0.0.1:{port}/completion',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                start=time.perf_counter();first=None;text='';final=None;chunks=[];r['status']='filling_context';update()
                with urllib.request.urlopen(request,timeout=7200) as response:
                    for line in response:
                        if not line.startswith(b'data:'):continue
                        line=line[5:].strip()
                        if line==b'[DONE]':break
                        body=json.loads(line);elapsed=time.perf_counter()-start
                        if body.get('content'):
                            if first is None:first=elapsed;r.update(status='decoding',context_fill_s=first);update()
                            text+=body['content'];chunks.append({'elapsed_s':elapsed,'characters':len(body['content']),'token_ids':body.get('tokens')})
                        if body.get('stop'):final=body
                        if elapsed>7200:raise TimeoutError('Two-hour measurement limit')
                if not final:raise RuntimeError('Native completion did not provide final counters')
                timings=final.get('timings',{});actual=final.get('tokens_evaluated',timings.get('prompt_n'));generated=final.get('tokens_predicted',timings.get('predicted_n'))
                if actual!=a.tokens or generated!=a.output_tokens:raise RuntimeError(f'Exact native token count mismatch: {actual}, {generated}')
                r.update(status='complete',input_tokens=actual,output_tokens=generated,context_fill_s=first,prefill_tok_s=timings.get('prompt_per_second'),decode_tok_s=timings.get('predicted_per_second'),native_timings=timings,generation_wall_s=time.perf_counter()-start,output_text=text,finish=final,settings='Native llama.cpp timings; HTTP TTFT includes loopback request overhead. Token IDs supplied directly. EOS ignored for fixed work. f16 KV, Metal/flash attention, no context shift.')
                write_json(out/'stream-chunks.json',chunks)
    except BaseException as e:r.update(status='failed',error=str(e).replace(str(ROOT),'<repo>'));raise
    finally:r['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()

if __name__=='__main__':main()
