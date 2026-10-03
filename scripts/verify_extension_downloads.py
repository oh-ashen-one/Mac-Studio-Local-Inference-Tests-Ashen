#!/usr/bin/env python3
"""Verify the selected owner downloads, only on an idle verified M5.

Reads bytes; never downloads, imports a model runtime, converts or loads weights.
"""
import datetime,fcntl,hashlib,json,os,subprocess
from pathlib import Path
import psutil
ROOT=Path(__file__).resolve().parents[1]
SELECTED=['qwen3.5-35b-a3b','gpt-oss-20b','ternary-bonsai-2-27b','nvidia-nemotron-3.5-lightning']

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(8*1024*1024):h.update(block)
    return h.hexdigest()

def main():
    host=subprocess.check_output(['sysctl','-n','hw.model'],text=True).strip()
    chip=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
    assert host=='Mac17,15' and chip=='Apple M5 Ultra','Only verified M5'
    lock=(ROOT/'work/unified-campaign.lock').open('a+')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    state=json.loads((ROOT/'work/unified-campaign.json').read_text())
    assert not psutil.pid_exists(state['pid']),'Driver must have exited'
    for p in (Path.home()/'.cache/gpu-slot/holders').glob('*.json'):
        pid=json.loads(p.read_text()).get('pid')
        assert not pid or not psutil.pid_exists(pid),'Preserve active GPU work'
    receipt={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host_model':host,'chip':chip,'status':'verifying','models':[]}
    out=ROOT/'hardware/extension-integrity-20261003.json'
    assert not out.exists(),'Preserve previous verification receipt'
    def save():out.write_text(json.dumps(receipt,indent=2)+'\n')
    save()
    try:
        for name in SELECTED:
            base=Path.home()/'.cache/huggingface/hub'/('models--'+name)
            snapshots=[p for p in (base/'snapshots').iterdir() if p.name.startswith('.revision-')]
            assert len(snapshots)==1,'Ambiguous snapshot requires review'
            folder=snapshots[0];manifest=folder/'.darkbloom-manifest.json';m=json.loads(manifest.read_text())
            entry={'id':name,'snapshot':folder.name,'artifact_version':m['version'],'manifest_sha256':digest(manifest),'files':[],'status':'verifying'}
            receipt['models'].append(entry);save()
            for f in m['files']:
                rel=Path(f['path']);assert not rel.is_absolute() and '..' not in rel.parts
                path=folder/rel;before=path.stat();actual=digest(path);after=path.stat()
                row={'path':str(rel),'bytes':after.st_size,'sha256':actual,'expected_sha256':f['sha256'],'matches':before.st_size==after.st_size==f['size_bytes'] and before.st_mtime_ns==after.st_mtime_ns and actual==f['sha256']}
                entry['files'].append(row);save()
                assert row['matches'],'Integrity or concurrent modification failure: '+name+'/'+str(rel)
            assert len(entry['files'])==m['file_count']
            entry['status']='verified';save()
        receipt['status']='verified';receipt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
    except BaseException as e:
        receipt.update(status='failed',error=type(e).__name__+': '+str(e));save();raise
    print(json.dumps({'status':receipt['status'],'models':len(receipt['models']),'files':sum(len(m['files']) for m in receipt['models'])}))

if __name__=='__main__':main()
