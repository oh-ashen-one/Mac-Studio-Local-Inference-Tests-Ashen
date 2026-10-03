#!/usr/bin/env python3
"""AIPerf-style serving metrics at declared request concurrency; no CUDA needed."""
import argparse,concurrent.futures,datetime,json,signal,subprocess,sys,time,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,write_json
from models import digest,verify
from model_registry import resolve_model
from unified_server import server,chat,chat_payload,fill_to_tokens

def percentile(values,q):
    x=sorted(values);k=(len(x)-1)*q;lo=int(k);hi=min(lo+1,len(x)-1);return x[lo]+(x[hi]-x[lo])*(k-lo) if x else None

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--run-id',required=True);p.add_argument('--concurrency',type=int,choices=[1,2,4],required=True);p.add_argument('--requests',type=int,default=12);p.add_argument('--lock',default='config/unified-models.lock.json');p.add_argument('--campaign-id',default='unified-overnight-20261002');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec,folder,lock=resolve_model(a.model,a.lock);out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    r={'kind':'serving_load','campaign_id':a.campaign_id,'model_id':a.model,'machine_id':'studio-new','status':'starting','concurrency':a.concurrency,'planned_requests':a.requests,'warmup_requests':2,'input_target_tokens':8192,'output_cap':256,'temperature':0,'seed':None,'model_lock_sha256':digest(lock),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Metric definitions follow AIPerf/GenAI-Perf; this is our portable harness, not an official AIPerf submission. Actual output lengths and cache counts retained.'}
    def update():write_json(out/'result.json',r);write_json(ROOT/'work/unified-job-live.json',r)
    update()
    try:
        with shared_gpu_slot():
            r['preflight']=safety('studio-new');verify(spec,folder)
            def prepare_payloads(port=None):
                body=(ROOT/'work/context-corpus.txt').read_text();payloads=[]
                for i in range(a.requests+2):
                    messages,count=fill_to_tokens(spec,folder,'Write a useful, detailed technical summary of the supplied code.','Independent request '+str(i)+'\n',body,'\nSummarize the code and identify its main responsibilities. Aim for a thorough response.',8192,port)
                    payload=chat_payload(spec,messages,256,0);payload.pop('seed',None);payload['cache_prompt']=False;payloads.append(payload)
                return payloads
            prepared=prepare_payloads() if spec['runtime']=='dwarfstar' else None
            r['tokenizer_schedule']='before-server-v1' if prepared else 'resident-server'
            with server(spec,folder,out,context=16384,cache_sequences=0,slots=a.concurrency) as (port,telemetry):
                payloads=prepared or prepare_payloads(port)
                write_json(out/'requests.json',payloads)
                warm=[chat(port,payload,900) for payload in payloads[:2]];write_json(out/'warmup.json',warm)
                r['status']='measuring';update();start=time.perf_counter()
                with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as executor:
                    responses=list(executor.map(lambda p:chat(port,p,900),payloads[2:]))
                elapsed=time.perf_counter()-start;write_json(out/'responses.json',responses)
                if any(not 8192<=x['usage'].get('prompt_tokens',0)<=8256 for x in responses):raise RuntimeError('Actual serving input outside declared range')
                lat=[x['wall_s'] for x in responses];ttft=[x['first_output_s'] for x in responses if x['first_output_s'] is not None]
                r.update(status='complete',completed_requests=len(responses),total_output_tokens=sum(x['usage']['completion_tokens'] for x in responses),wall_s=elapsed,aggregate_output_tok_s=sum(x['usage']['completion_tokens'] for x in responses)/elapsed,requests_per_s=len(responses)/elapsed,ttft_median_s=statistics.median(ttft) if ttft else None,ttft_p95_s=percentile(ttft,.95),latency_median_s=statistics.median(lat),latency_p95_s=percentile(lat,.95),per_request_e2e_tok_s_median=statistics.median(x['end_to_end_tok_s'] for x in responses),per_request_e2e_tok_s_p25=percentile([x['end_to_end_tok_s'] for x in responses],.25))
    except BaseException as e:r.update(status='failed',error=str(e).replace(str(ROOT),'<repo>'));raise
    finally:r['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()

if __name__=='__main__':main()
