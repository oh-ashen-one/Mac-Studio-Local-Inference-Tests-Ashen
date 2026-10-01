#!/usr/bin/env python3
"""Run the locked AA replay under the shared GPU protocol; never submit externally."""
import argparse,datetime,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import shared_gpu_slot,write_json,stop,Telemetry,safety
from models import digest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--run-id',required=True);p.add_argument('--condition',choices=['alone','blender-open'],default='alone');p.add_argument('--mini',action='store_true');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization and --allow-inference required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    lock=json.loads((ROOT/'config/agentperf.lock.json').read_text());ready=json.loads((ROOT/'work/AGENTPERF_READY.json').read_text())
    if ready['lock_sha256']!=digest(ROOT/'config/agentperf.lock.json'):raise RuntimeError('AA preparation lock changed')
    out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    result={'kind':'aa-agentperf','condition':a.condition,'cohort':lock['cohort'],'replay':'aa-mini-v1' if a.mini else lock['replay'],'status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lock_sha256':ready['lock_sha256'],'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'model_revision':lock['model_revision'],'artifact_sha256':lock['sha256'],'agentperf_commit':lock['agentperf_commit'],'llama_commit':lock['llama_commit'],'quality_note':'Recorded trajectory replay measures serving speed, not autonomous task success.'}
    def update():write_json(out/'run.json',result);write_json(ROOT/'work/agentperf-live.json',result)
    update();process=None
    try:
        if a.condition=='alone':result['preflight']=safety()
        else:
            from bench import preflight
            result['preflight']=preflight('studio-new',True)
            receipt=json.loads((ROOT/'work/blender-condition.json').read_text())
            import psutil
            proc=psutil.Process(receipt['pid'])
            if not proc.is_running() or 'Blender.app/Contents/MacOS/Blender' not in proc.exe():raise RuntimeError('Owned Blender condition is not running')
            result['blender']=receipt
        with shared_gpu_slot() as slot:
            result['slot']=slot
            command=[str(ROOT/'vendor/aa-agentperf-local/.venv/bin/agentperf-local'),'managed-run','--profile-id',lock['profile'],'--framework','llama-cpp','--cache-root',str(ROOT/'models/agentperf-cache'),'--output-dir',str(out/'raw'),'--port','18184','--output-token-policy','exact','--no-power','--request-timeout-seconds','1800']
            if a.mini:command+=['--replay','aa-mini-v1']
            env=dict(os.environ,PATH=str(ROOT/'vendor/llama-agentperf/build/bin')+os.pathsep+os.environ['PATH'])
            # Do not inherit a submission token into the benchmark subprocess.
            env.pop('AGENTPERF_SUBMIT_TOKEN',None)
            with (out/'agentperf.log').open('w') as log:
                process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                start=time.monotonic()
                with Telemetry(process.pid) as telemetry:
                    while process.poll() is None:
                        result.update(status='running',elapsed_s=time.monotonic()-start)
                        turns=out/'raw/turns.jsonl'
                        if turns.exists():result['recorded_turns']=sum(1 for _ in turns.open())
                        update()
                        if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):raise RuntimeError('Memory guard reached')
                        if result['elapsed_s']>14400:raise TimeoutError('Four-hour replay budget reached')
                        time.sleep(3)
                write_json(out/'telemetry.json',telemetry.rows)
            result.update(status='complete' if process.returncode==0 else 'failed',exit_code=process.returncode,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());update()
            if process.returncode:raise RuntimeError('Official replay failed; inspect retained logs, no automatic retry')
    except BaseException as exc:result.update(status='failed',error=str(exc).replace(str(ROOT),'<repo>'));update();raise
    finally:stop(process)
if __name__=='__main__':main()
