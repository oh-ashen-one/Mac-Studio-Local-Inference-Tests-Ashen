#!/usr/bin/env python3
"""Build the exact DwarfStar revision without changing existing source checkouts."""
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'config/dwarfstar.lock.json').read_text())
path=ROOT/'vendor/dwarfstar'
path.parent.mkdir(exist_ok=True)
if not path.exists():
    subprocess.run(['git','clone',lock['repository'],str(path)],check=True)
if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=path,text=True).strip():
    raise SystemExit('Refusing to modify a dirty dependency checkout')
subprocess.run(['git','fetch','origin',lock['commit']],cwd=path,check=True)
subprocess.run(['git','checkout','--detach',lock['commit']],cwd=path,check=True)
subprocess.run(lock['build_command'],cwd=path,check=True)
print('Pinned native Metal engine built.')
