#!/usr/bin/env python3
"""Idle-M5-only preparation of the owner-selected pinned Mistral; no inference."""
import datetime,fcntl,json,os,shutil,subprocess,time
from pathlib import Path
import psutil
from models import digest,verify
ROOT=Path(__file__).resolve().parents[1]

def main():
    assert subprocess.check_output(['sysctl','-n','hw.model'],text=True).strip()=='Mac17,15'
    assert subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()=='Apple M5 Ultra'
    mutex=(ROOT/'work/unified-campaign.lock').open('a+');fcntl.flock(mutex,fcntl.LOCK_EX|fcntl.LOCK_NB)
    s=json.loads((ROOT/'work/unified-campaign.json').read_text());assert not psutil.pid_exists(s['pid']),'Preserve active driver'
    for p in (Path.home()/'.cache/gpu-slot/holders').glob('*.json'):
        pid=json.loads(p.read_text()).get('pid');assert not pid or not psutil.pid_exists(pid),'Preserve active GPU holder'
    lock=ROOT/'config/mistral-models.lock.json';spec=json.loads(lock.read_text())['models'][0]
    folder=ROOT/'models'/spec['id'];folder.mkdir(parents=True,exist_ok=True)
    missing=sum(f['bytes'] for f in spec['files'] if not (folder/f['path']).is_file())
    assert shutil.disk_usage(folder).free>=missing+100*2**30,'Preserve 100GiB storage headroom'
    run=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');receipt=ROOT/'work'/('mistral-preparation-'+run+'.json');state={'status':'downloading','pid':os.getpid(),'started_at_utc':run,'repo':spec['repo'],'revision':spec['revision'],'model_lock_sha256':digest(lock),'attempt_receipt':receipt.name}
    def save():
        receipt.write_text(json.dumps(state,indent=2)+'\n');(ROOT/'work/mistral-preparation.json').write_text(json.dumps(state,indent=2)+'\n')
    save()
    try:
        os.environ.setdefault('HF_XET_NUM_CONCURRENT_RANGE_GETS','4');os.environ.setdefault('HF_HUB_DOWNLOAD_TIMEOUT','120')
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id=spec['repo'],revision=spec['revision'],local_dir=folder,max_workers=2,allow_patterns=[f['path'] for f in spec['files']])
        state['status']='verifying';save();verify(spec,folder)
        state.update(status='verified',finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),verified_files=[{'path':f['path'],'bytes':f['bytes'],'sha256':f['sha256']} for f in spec['files']]);save()
    except BaseException as e:
        state.update(status='failed',error=type(e).__name__+': '+str(e).replace(str(Path.home()),'<M5_HOME>'));save();raise
    print(json.dumps({'status':'verified','files':len(spec['files']),'attempt':receipt.name}))

if __name__=='__main__':main()
