#!/usr/bin/env python3
"""Install the separate pinned AA cohort. Never loads a model or starts a server."""
import json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from models import digest
from first_test import write_json

def main():
    lock=json.loads((ROOT/'config/agentperf.lock.json').read_text())
    uv=str(ROOT/'.tools/uv') if (ROOT/'.tools/uv').exists() else shutil.which('uv')
    if not uv:raise RuntimeError('Run the standard preparation first to install uv')
    def run(args,**kw):subprocess.run(list(map(str,args)),check=True,**kw)
    def checkout(name,url,commit):
        folder=ROOT/'vendor'/name
        if not folder.exists():run(['git','clone','--depth','1',url,folder])
        current=subprocess.check_output(['git','rev-parse','HEAD'],cwd=folder,text=True).strip()
        if current!=commit:
            if subprocess.check_output(['git','status','--porcelain'],cwd=folder,text=True).strip():raise RuntimeError('Preserve modified vendor checkout: '+name)
            run(['git','fetch','--depth','1','origin',commit],cwd=folder);run(['git','checkout','--detach',commit],cwd=folder)
        return folder
    aa=checkout('aa-agentperf-local',lock['agentperf_repository'],lock['agentperf_commit'])
    run([uv,'sync','--locked','--no-dev','--python','3.12.13'],cwd=aa)
    llama=checkout('llama-agentperf',lock['llama_repository'],lock['llama_commit'])
    buildenv=ROOT/'.tools/aa-build'
    if not buildenv.exists():run([uv,'venv','--python','3.12.13',buildenv])
    run([uv,'pip','install','--python',buildenv/'bin/python','cmake=='+lock['cmake'],'ninja=='+lock['ninja']])
    env=dict(os.environ,PATH=str(buildenv/'bin')+os.pathsep+os.environ['PATH'])
    run([buildenv/'bin/cmake','-S',llama,'-B',llama/'build','-G','Ninja','-DCMAKE_BUILD_TYPE=Release','-DGGML_METAL=ON','-DGGML_NATIVE=OFF','-DLLAMA_BUILD_TESTS=OFF','-DLLAMA_CURL=OFF'],env=env)
    run([buildenv/'bin/cmake','--build',llama/'build','--target','llama-server','-j','4'],env=env)
    from huggingface_hub import hf_hub_download
    cache=ROOT/'models/agentperf-cache'
    path=Path(hf_hub_download(lock['model_repository'],lock['filename'],revision=lock['model_revision'],cache_dir=cache))
    if path.stat().st_size!=lock['size_bytes'] or digest(path)!=lock['sha256']:raise RuntimeError('AA artifact hash mismatch')
    write_json(ROOT/'work/AGENTPERF_READY.json',{'status':'prepared_not_loaded','lock_sha256':digest(ROOT/'config/agentperf.lock.json'),'model_sha256':lock['sha256'],'agentperf_commit':lock['agentperf_commit'],'llama_commit':lock['llama_commit']})
    print('AA cohort prepared and verified; no model was loaded.',flush=True)
if __name__=='__main__':main()
