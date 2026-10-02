#!/usr/bin/env python3
"""CPU-only positive/negative controls before evaluating model-generated code."""
import gzip,json,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from unified_quality import evaluate_code
from repo_task import profile,VENV

def main():
    out=ROOT/'work/unified-evaluator-validation';out.mkdir(exist_ok=False)
    cases=[json.loads(x) for x in gzip.decompress((ROOT/'config/humaneval/HumanEval.jsonl.gz').read_bytes()).decode().splitlines()]
    rows=[]
    for case in cases:
        folder=out/case['task_id'].replace('/','_');folder.mkdir();result=evaluate_code(case,case['prompt']+case['canonical_solution'],folder);rows.append({'task_id':case['task_id'],**result})
    sentinel=ROOT/'work/unified-private-sentinel.txt';sentinel.write_text('synthetic private sentinel')
    probe=out/'sandbox_probe.py'
    probe.write_text('import socket,os\nchecks=[]\ntry:\n open('+repr(str(sentinel))+').read()\n checks.append(False)\nexcept PermissionError: checks.append(True)\ntry:\n socket.socket().connect(("127.0.0.1",18765))\n checks.append(False)\nexcept PermissionError: checks.append(True)\ntry:\n os.fork()\n checks.append(False)\nexcept PermissionError: checks.append(True)\nprint(checks)\nassert checks == [True,True,True]\n')
    env={'PATH':'/usr/bin:/bin','HOME':str(out),'TMPDIR':str(out),'PYTHONDONTWRITEBYTECODE':'1','LANG':'en_US.UTF-8'}
    r=subprocess.run(['/usr/bin/sandbox-exec','-p',profile(out).replace('(allow process-fork)','(deny process-fork)'),str(VENV/'bin/python'),'-I','-B',str(probe)],cwd=out,env=env,capture_output=True,text=True,timeout=10)
    receipt={'kind':'cpu_evaluator_validation','canonical_passed':sum(x['passed'] for x in rows),'canonical_tasks':len(rows),'sandbox_negative_controls_passed':r.returncode==0,'negative_control_stdout':r.stdout,'cases':rows,'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
    (ROOT/'work/unified-evaluator-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='cases'}))
    if not all(x['passed'] for x in rows) or r.returncode:raise RuntimeError('Evaluator qualification failed; do not launch model scoring')

if __name__=='__main__':main()
