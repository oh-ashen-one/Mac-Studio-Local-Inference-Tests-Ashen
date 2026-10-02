#!/usr/bin/env python3
"""Official recorded-policy AA replay, same request policy for all six backends."""
import argparse,datetime,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,stop,write_json
from model_registry import resolve_model
from models import digest,verify
from unified_server import server,model_name

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--run-id',required=True);p.add_argument('--mini',action='store_true');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec,folder,lock=resolve_model(a.model,'config/unified-models.lock.json');out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    result={'kind':'aa-agentperf','campaign_id':'unified-overnight-20261002','model_id':a.model,'machine_id':'studio-new','status':'starting','replay':'aa-mini-v1' if a.mini else 'agentperf-default-v1','condition':'alone','cohort':'unified-recorded-v1','output_token_policy':'recorded','model_revision':spec['revision'],'model_lock_sha256':digest(lock),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'agentperf_commit':json.loads((ROOT/'config/agentperf.lock.json').read_text())['agentperf_commit'],'quality_note':'Recorded serving trajectories, not autonomous tasks solved; shorter than the 200K performance cells.','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    def update():write_json(out/'run.json',result);write_json(ROOT/'work/unified-job-live.json',result)
    process=None;update()
    try:
        with shared_gpu_slot():
            result['preflight']=safety('studio-new');verify(spec,folder)
            with server(spec,folder,out,port=18184,context=262144) as (port,telemetry):
                env=dict(os.environ);env.pop('AGENTPERF_SUBMIT_TOKEN',None)
                cmd=[str(ROOT/'vendor/aa-agentperf-local/.venv/bin/agentperf-local'),'run','--replay',result['replay'],'--base-url',f'http://127.0.0.1:{port}/v1','--model',model_name(spec),'--output-dir',str(out/'raw'),'--output-token-policy','recorded','--no-power','--timeout-seconds','900','--no-progress']
                with (out/'agentperf.log').open('w') as log:
                    process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True);start=time.monotonic()
                    while process.poll() is None:
                        result.update(status='running',elapsed_s=time.monotonic()-start);update()
                        if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):raise RuntimeError('Memory guard reached')
                        if result['elapsed_s']>14400:raise TimeoutError('Declared four-hour replay budget exceeded')
                        time.sleep(2)
                summary=json.loads((out/'raw/summary.json').read_text());success=process.returncode==0 and summary['success'] and summary['totals']['failed_turns']==0
                result.update(status='complete' if success else 'failed',serving_success=success,exit_code=process.returncode,context_evidence=summary.get('config',{}).get('context'))
                if not success:raise RuntimeError('Official replay failed qualification; do not silently retry')
    except BaseException as exc:result.update(status='failed',error=str(exc).replace(str(ROOT),'<repo>'));raise
    finally:stop(process);result['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()

if __name__=='__main__':main()
