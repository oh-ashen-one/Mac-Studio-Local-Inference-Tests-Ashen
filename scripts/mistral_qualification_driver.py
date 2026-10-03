#!/usr/bin/env python3
"""Idle-M5 qualification supervisor with unchanged memory/shared-slot guards."""
import argparse,datetime,fcntl,json,os,re,signal,subprocess,time
from pathlib import Path
import psutil
from first_test import safety,Telemetry,stop,write_json
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');p.add_argument('--run-id',required=True);a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    if not re.fullmatch(r'q20261003-mistral-qualification-r[1-9][0-9]*',a.run_id):p.error('Explicit separate qualification ID required')
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt()))
    mutex=(ROOT/'work/unified-campaign.lock').open('a+');fcntl.flock(mutex,fcntl.LOCK_EX|fcntl.LOCK_NB)
    for name in ['work/unified-campaign.json','work/mistral-campaign.json']:
        file=ROOT/name
        if file.exists() and psutil.pid_exists(json.loads(file.read_text())['pid']):raise RuntimeError('Existing campaign driver is alive')
    for holder in (Path.home()/'.cache/gpu-slot/holders').glob('*.json'):
        pid=json.loads(holder.read_text()).get('pid')
        if pid and psutil.pid_exists(pid):raise RuntimeError('Existing GPU holder is alive')
    safety('studio-new');out=ROOT/'results'/a.run_id
    if out.exists():raise RuntimeError('Preserve existing qualification attempt; no silent retry')
    state={'pid':os.getpid(),'run_id':a.run_id,'status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'job_budget_s':1800,'min_available_bytes':12*2**30,'max_swap_growth_bytes':2*2**30}
    def save():write_json(ROOT/'work/mistral-qualification-driver.json',state)
    child=None;rows=[];save()
    try:
        with (ROOT/'work'/f'{a.run_id}.log').open('w') as log:
            child=subprocess.Popen(['.venv/bin/python','-u','scripts/qualify_mistral.py','--allow-inference','--run-id',a.run_id],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
            start=time.monotonic()
            with Telemetry(child.pid) as telemetry:
                while child.poll() is None:
                    state.update(status='running',elapsed_s=time.monotonic()-start);save()
                    if telemetry.rows and (telemetry.rows[-1]['available_bytes']<state['min_available_bytes'] or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>state['max_swap_growth_bytes']):raise RuntimeError('Qualification memory guard reached; preserve failure')
                    if state['elapsed_s']>state['job_budget_s']:raise TimeoutError('Qualification setup budget reached')
                    time.sleep(3)
                rows=telemetry.rows
        if child.returncode:raise RuntimeError('Qualification failed; no automatic retry')
        state.update(status='complete',finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save()
    except BaseException as error:
        state.update(status='stopped',error=str(error) or type(error).__name__);save();raise
    finally:
        stop(child)
        if out.exists():write_json(out/'qualification-driver-telemetry.json',rows or (telemetry.rows if 'telemetry' in locals() else []))

if __name__=='__main__':main()
