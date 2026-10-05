#!/usr/bin/env python3
"""Write a ready receipt only when locked artifacts and runtimes exist. No GPU imports."""
import datetime
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from models import digest


def verify_runtime(root):
    versions={}
    for line in (root/'requirements-macos-arm64.lock').read_text().splitlines():
        if not line or line.startswith('#'):continue
        name,expected=line.split('==',1)
        actual=importlib.metadata.version(name)
        if actual!=expected:raise RuntimeError(f'Runtime version mismatch: {name}: {actual} != {expected}')
        versions[name]=actual
    if platform.python_version()!='3.12.13':raise RuntimeError('The campaign requires Python 3.12.13')
    native=root/'vendor/dwarfstar'
    for name in ['ds4','ds4-bench','ds4-server']:
        if not (native/name).is_file():raise RuntimeError('Missing native runtime binary: '+name)
    # Check without invoking a developer-tool shim that might open an installer dialog.
    if subprocess.run(['xcode-select','-p'],capture_output=True).returncode:
        raise RuntimeError('Apple developer tools remain unavailable')
    lock=json.loads((root/'config/dwarfstar.lock.json').read_text())
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=native,text=True).strip()
    if commit!=lock['commit']:raise RuntimeError('Native source revision mismatch')
    return {'python':platform.python_version(),'packages':versions,'native_commit':commit,
            'native_binary_sha256':{name:digest(native/name) for name in ['ds4','ds4-bench','ds4-server']}}


def main():
    report=json.loads((ROOT/'work/model-verification.json').read_text())
    lock=json.loads((ROOT/'config/models.lock.json').read_text())
    if report['lock_sha256']!=digest(ROOT/'config/models.lock.json'):
        raise SystemExit('Verification receipt uses a different lock; run scripts/models.py verify')
    verified={m['id']:m for m in report['models']}
    for m in lock['models']:
        v=verified.get(m['id'],{})
        if not v.get('sha256_verified') or v.get('revision')!=m['revision'] or v.get('verified_files')!=len(m['files']):
            raise SystemExit('Missing completed verification for '+m['id'])
        for f in m['files']:
            path=ROOT/'models'/m['id']/f['path']
            if not path.is_file() or path.stat().st_size!=f['bytes']:
                raise SystemExit('Model file changed after verification: '+m['id']+'/'+f['path'])
    runtime=verify_runtime(ROOT)
    chip=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
    machine={'Apple M3 Ultra':'studio-old','Apple M5 Ultra':'studio-new'}.get(chip)
    if not machine:raise SystemExit('Unexpected machine: '+chip)
    receipt={'state':'prepared_not_loaded','machine_id':machine,'chip':chip,
             'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'models_sha256_verified':True,'models':[{'id':m['id'],'revision':m['revision'],'bytes':m['total_bytes']} for m in lock['models']],
             'model_lock_sha256':report['lock_sha256'],'runtime':runtime,'inference_authorized':False,
             'next_step':'Wait for the owner to explicitly say start. Review results on localhost before website publication.'}
    (ROOT/'work/READY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
