#!/usr/bin/env python3
"""No overall deadline: execute the complete frozen all-configuration matrix."""
import argparse,datetime,fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,Telemetry,stop,write_json
from models import digest
from campaign_admission import pending_disposition, download_snapshot, extension_pending, OMITTED

def command_for(job,spec):
    python=str(ROOT/('vendor/vlm-runtime/.venv/bin/python' if spec['runtime']=='mlx-vlm' else '.venv/bin/python'))
    common=['--allow-inference','--model',job['model_id'],'--run-id',job['id']]
    if job['kind']=='speed':
        if spec['runtime']=='llama-cpp':entry=['scripts/llama_context.py',*common]
        else:entry=['scripts/long_context.py',*common,'--lock','config/unified-models.lock.json','--campaign-id','unified-overnight-20261002','--backend',spec['runtime'] if spec['runtime'].startswith('mlx') else 'mlx-lm','--wired-policy','recommended' if spec['runtime'].startswith('mlx') else 'unchanged']
        return [python,*entry,'--tokens',str(job['tokens']),'--output-tokens',str(job['output_tokens'])],7600
    if job['kind']=='repo':return [python,'scripts/unified_repo.py',*common,'--attempt',str(job['attempt']),'--max-turns',str(job['max_turns'])],7800 if job['max_turns']==20 else 4200
    if job['kind']=='replay':return [python,'scripts/unified_replay.py',*common]+(['--mini'] if job['mini'] else []),15000
    if job['kind']=='quality':return [python,'scripts/unified_quality.py',*common,'--suite',job['suite']],86400
    if job['kind']=='serving':return [python,'scripts/unified_serving.py',*common,'--concurrency',str(job['concurrency']),'--requests',str(job['requests'])],7200
    raise ValueError('Unknown frozen job type')

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    lock=(ROOT/'work/unified-campaign.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    plan=json.loads((ROOT/'config/unified-campaign.json').read_text());specs={s['id']:s for s in json.loads((ROOT/plan['model_lock']).read_text())['models']}
    state={'campaign_id':plan['id'],'pid':os.getpid(),'status':'starting','overall_deadline':None,'plan_sha256':digest(ROOT/'config/unified-campaign.json'),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobs':[{**j,'status':'pending'} for j in plan['jobs']]}
    def save():write_json(ROOT/'work/unified-campaign.json',state)
    save();process=None
    try:
        import psutil
        for j in state['jobs']:
            out=ROOT/'results'/j['id'];file=out/('run.json' if j['kind']=='replay' else 'result.json')
            if file.exists():
                result=json.loads(file.read_text())
                if result.get('status')!='complete':j['status']='needs_review';state.update(status='stopped',active=j['id'],error='Existing failed/incomplete cell requires explicit review');save();return
                j['status']='complete';save();continue
            disposition=pending_disposition(j, file.exists())
            if disposition:
                j.update(status=disposition,reason=j['disposition_reason']);save();continue
            if j.get('requires'):
                required=next(x for x in state['jobs'] if x['id']==j['requires'])
                if required['status']!='complete':j.update(status='blocked',reason='Replay qualification has not passed');save();continue
            # Require a stable, partial-free metadata interval before timed work.
            previous=None;quiet_since=None
            while True:
                signature,blockers=download_snapshot([Path.home()/'.cache/huggingface',ROOT/'models'])
                now=time.monotonic()
                if blockers or signature!=previous:quiet_since=now
                previous=signature
                hold=(ROOT/'work/campaign-hold.json').exists()
                if not blockers and not hold and quiet_since is not None and now-quiet_since>=60:break
                state.update(status='waiting_for_download_quiescence',active=None,next_job=j['id'],admission={'partial_or_scan_blocker_count':len(blockers),'owner_hold':hold,'required_quiet_seconds':60});save();time.sleep(10)
            for holder in (Path.home()/'.cache/gpu-slot/holders').glob('*.json'):
                held=json.loads(holder.read_text())
                if held.get('pid') and psutil.pid_exists(held['pid']):raise RuntimeError('Another GPU holder is active; preserve its work')
            safety('studio-new')
            command,budget=command_for(j,specs[j['model_id']]);j['status']='running';state.update(status='running',active=j['id']);save()
            with (ROOT/'work'/f'{j["id"]}.log').open('w') as log:
                process=subprocess.Popen(command,cwd=ROOT,env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1'),stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
                start=time.monotonic()
                try:
                    with Telemetry(process.pid) as telemetry:
                        while process.poll() is None:
                            state['elapsed_s']=time.monotonic()-start;save()
                            if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):
                                state['guard_sample']=telemetry.rows[-1];raise RuntimeError('Memory guard reached; no automatic retry')
                            if state['elapsed_s']>budget:raise TimeoutError('Declared individual-job budget reached; overall campaign has no cutoff')
                            time.sleep(3)
                finally:
                    if out.exists():write_json(out/'campaign-telemetry.json',telemetry.rows)
            if process.returncode:
                j['status']='needs_review';raise RuntimeError('Cell failed and was preserved: '+j['id'])
            j['status']='complete';save();process=None
        if any(j['status'] not in ('complete',OMITTED) for j in state['jobs']):state['status']='needs_review'
        elif extension_pending(ROOT,plan):state.update(status='baseline_accounted_extension_pending',active=None)
        else:state.update(status='complete',active=None,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        save()
    except BaseException as e:state.update(status='stopped',error=str(e));save();raise
    finally:stop(process)

if __name__=='__main__':main()
