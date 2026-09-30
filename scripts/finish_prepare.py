#!/usr/bin/env python3
"""Create the ready receipt from completed file verification. No ML/GPU imports."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from models import digest
report=json.loads((ROOT/'work/model-verification.json').read_text())
lock=json.loads((ROOT/'config/models.lock.json').read_text())
if report['lock_sha256']!=digest(ROOT/'config/models.lock.json'):
    raise SystemExit('Verification receipt refers to a different model lock. Run scripts/models.py verify.')
verified={m['id']:m for m in report['models']}
for m in lock['models']:
    v=verified.get(m['id'],{})
    if not v.get('sha256_verified') or v.get('revision')!=m['revision'] or v.get('verified_files')!=len(m['files']):
        raise SystemExit('Missing completed verification for '+m['id'])
    for f in m['files']:
        path=ROOT/'models'/m['id']/f['path']
        if not path.is_file() or path.stat().st_size!=f['bytes']:
            raise SystemExit('Model file changed after verification: '+m['id']+'/'+f['path'])
chip=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
machine={'Apple M3 Ultra':'studio-old','Apple M5 Ultra':'studio-new'}.get(chip)
if not machine:raise SystemExit('Unexpected machine: '+chip)
receipt={'state':'prepared_not_loaded','machine_id':machine,'chip':chip,
         'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'models_sha256_verified':True,'models':[{'id':m['id'],'revision':m['revision'],'bytes':m['total_bytes']} for m in lock['models']],
         'model_lock_sha256':report['lock_sha256'],'inference_authorized':False,
         'next_step':'Wait for the owner to explicitly say start. Review results on localhost before website publication.'}
(ROOT/'work/READY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
