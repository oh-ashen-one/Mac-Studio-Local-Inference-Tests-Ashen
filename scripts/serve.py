#!/usr/bin/env python3
"""Launch exactly one pinned model on loopback for manual or quality testing."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from models import verify
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('model');p.add_argument('--port',type=int,default=18181)
p.add_argument('--allow-inference',action='store_true')
a=p.parse_args()
if not a.allow_inference:p.error('Preparation-only mode. Explicit owner start required before --allow-inference.')
models=json.loads((ROOT/'config/models.lock.json').read_text())['models']
m=next((x for x in models if x['id']==a.model),None)
if m is None:p.error('Unknown model')
verify(m,ROOT/'models'/m['id'])
if m['backend']=='mlx':
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'
    cmd=[sys.executable,'-m','mlx_lm.server','--model',str(ROOT/'models'/m['id']),'--host','127.0.0.1','--port',str(a.port)]
else:
    vendor=ROOT/'vendor/dwarfstar'
    lock=json.loads((ROOT/'config/dwarfstar.lock.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=vendor,text=True).strip()==lock['commit']
    cmd=[str(vendor/'ds4-server'),'-m',str(ROOT/'models'/m['id']/m['files'][0]['path']),
         '--host','127.0.0.1','--port',str(a.port),'--ctx','32768','--metal']
    os.chdir(vendor)
print('Starting task-owned loopback server for',m['id'],'on port',a.port,flush=True)
os.execv(cmd[0],cmd)
