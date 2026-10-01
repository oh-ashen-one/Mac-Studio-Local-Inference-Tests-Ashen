#!/usr/bin/env python3
"""Finite, resumable, sequential M5 additional-model campaign. No retries on failure."""
import argparse,datetime,fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,stop,Telemetry,write_json

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');a=p.parse_args()
    if not a.allow_inference:p.error('Explicit owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    lock=(ROOT/'work/additional-campaign.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    python=str(ROOT/'vendor/vlm-runtime/.venv/bin/python');model_lock='config/additional-models.lock.json'
    jobs=[]
    for short,model,pilot in [('qwen36','qwen3.6-35b-a3b-vl-mtp-mxfp8','m5-qwen36-pilot-vlm-20261001'),('mimo','mimo-v2.6-flash-mopd','m5-mimo-pilot-vlm-base-20261001')]:
        validation=json.loads((ROOT/'results'/pilot/'result.json').read_text())
        # MiMo answered both checks correctly but fenced the JSON; preserve its
        # format failure while accepting explicitly reviewed runtime coherence.
        if not validation.get('passed'):
            assessment=ROOT/'results'/pilot/'assessment.json'
            if not assessment.exists() or not json.loads(assessment.read_text()).get('runtime_coherent'):raise RuntimeError('Runtime validation has not been accepted')
        common=['--allow-inference','--model',model,'--lock',model_lock]
        for repeat in range(1,4):
            run=f'm5-{short}-200k-20261001-{repeat}'
            jobs.append((run,'result.json',[python,'scripts/long_context.py',*common,'--backend','mlx-vlm','--run-id',run],7500))
        for index in range(1,6):
            base=f'm5-repo-{short}-20261001';run=f'{base}-{index}'
            jobs.append((run,'result.json',[python,'scripts/run_repo_task.py',*common,'--backend','mlx-vlm','--run-id',base,'--start-at',str(index)],4200))
        for mini in [True,False]:
            run=f'm5-aa-{short}-'+('mini' if mini else 'full')+'-recorded-20261001'
            jobs.append((run,'run.json',[python,'scripts/additional_replay.py',*common,'--run-id',run]+(['--mini'] if mini else []),15000))
    state={'pid':os.getpid(),'status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobs':[{'run_id':j[0],'status':'pending'} for j in jobs]}
    def save():write_json(ROOT/'work/additional-campaign.json',state)
    save();process=None
    try:
        for index,(run,file,command,budget) in enumerate(jobs):
            result_file=ROOT/'results'/run/file
            if result_file.exists():
                saved=json.loads(result_file.read_text())
                if saved.get('status')!='complete':raise RuntimeError('Existing incomplete/failed job needs review: '+run)
                state['jobs'][index]['status']='already complete';save();continue
            # Respect a new download or another session before every next cell.
            cache=Path.home()/'.cache/huggingface/hub'
            if any(p.is_file() and p.name.endswith(('.part','.incomplete')) or p.is_dir() and 'staging' in p.name for p in cache.rglob('*')):
                raise RuntimeError('A model download is incomplete; postpone subsequent cells')
            import psutil
            for holder in (Path.home()/'.cache/gpu-slot/holders').glob('*.json'):
                record=json.loads(holder.read_text());pid=record.get('pid')
                if pid and psutil.pid_exists(pid):raise RuntimeError('Another GPU slot holder is active; preserve its work')
            safety('studio-new')
            state.update(status='running',active=run);state['jobs'][index]['status']='running';save()
            env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
            with (ROOT/'work'/f'{run}.log').open('w') as log:
                process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                started=time.monotonic()
                with Telemetry(process.pid) as telemetry:
                    while process.poll() is None:
                        state['elapsed_s']=time.monotonic()-started;save()
                        if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):raise RuntimeError('Campaign memory guard reached')
                        if state['elapsed_s']>budget:raise TimeoutError('Job deadline reached: '+run)
                        time.sleep(3)
                if (ROOT/'results'/run).exists():write_json(ROOT/'results'/run/'campaign-telemetry.json',telemetry.rows)
            if process.returncode:raise RuntimeError('Job failed and was not retried: '+run)
            state['jobs'][index]['status']='complete';save();process=None
        state.update(status='complete',active=None,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save()
    except BaseException as exc:state.update(status='stopped',error=str(exc));save();raise
    finally:stop(process)

if __name__=='__main__':main()
