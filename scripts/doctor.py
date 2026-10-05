#!/usr/bin/env python3
"""Read-only setup report. Model size checks are not a replacement for SHA256 verification."""
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
ROOT=Path(__file__).resolve().parents[1]
models=json.loads((ROOT/'config/models.lock.json').read_text())['models']
rows=[]
for m in models:
    missing=[f['path'] for f in m['files'] if not (ROOT/'models'/m['id']/f['path']).is_file() or (ROOT/'models'/m['id']/f['path']).stat().st_size!=f['bytes']]
    rows.append({'id':m['id'],'backend':m['backend'],'bytes':m['total_bytes'],'size_check_complete':not missing,'missing_or_partial_files':len(missing)})
report={'python':platform.python_version(),'architecture':platform.machine(),
        'chip':subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip(),
        'os_version':subprocess.check_output(['sw_vers','-productVersion'],text=True).strip(),
        'os_build':subprocess.check_output(['sw_vers','-buildVersion'],text=True).strip(),
        'free_disk_gib':round(shutil.disk_usage(ROOT).free/1024**3,1),
        'packages':{p:importlib.metadata.version(p) for p in ['mlx','mlx-lm','mlx-metal','transformers','huggingface-hub']},
        'native_binaries_present':all((ROOT/'vendor/dwarfstar'/f).is_file() for f in ['ds4','ds4-bench','ds4-server']),
        'models':rows}
print(json.dumps(report,indent=2))
