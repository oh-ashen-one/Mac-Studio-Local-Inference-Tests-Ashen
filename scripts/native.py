"""Pinned DwarfStar adapter; retains engine CSV instead of guessing token timing."""
import csv
import datetime
import io
import json
import os
from pathlib import Path
import random
import subprocess
import time


def run_native(args, model_spec, output):
    from bench import ROOT, append, preflight
    from models import digest, verify
    import psutil
    directory=ROOT/'models'/model_spec['id']
    verify(model_spec,directory)
    state=preflight(args.machine,args.suite=='core')
    if state['available_memory_bytes'] < model_spec['total_bytes']+32*1024**3:
        raise RuntimeError('Native model needs weights plus 32 GiB free working headroom')
    runtime=json.loads((ROOT/'config/dwarfstar.lock.json').read_text())
    vendor=ROOT/'vendor/dwarfstar'
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=vendor,text=True).strip()
    if actual!=runtime['commit']:raise RuntimeError('DwarfStar source revision mismatch')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=vendor,text=True).strip():
        raise RuntimeError('DwarfStar source has unrecorded edits')
    gguf=directory/model_spec['files'][0]['path']
    offsets=[0,4,7];counts=[4,3,3]
    if args.suite=='smoke':
        cases=[{'id':'setup-reply','input_tokens':None,'output_tokens':128,'repeat':0,'warmup':False,'prompt_seed':1729}]
    elif args.suite=='firstlook':
        cases=[{'id':'decode-512-256','input_tokens':512,'output_tokens':256,'repeat':i,'warmup':i<0,'prompt_seed':1729+i+1} for i in [-1,0,1,2]]
    elif args.suite=='pilot':
        cases=[{'id':'setup-speed','input_tokens':512,'output_tokens':32,'repeat':0,'warmup':False,'prompt_seed':1729}]
    else:
        cells=json.loads((ROOT/'config/campaign.json').read_text())['core_cells']
        random.Random(702+args.session).shuffle(cells)
        cases=[]
        for cell in cells:
            cases.extend({**cell,'repeat':-i-1,'warmup':True,'prompt_seed':100+i} for i in range(2))
            cases.extend({**cell,'repeat':offsets[args.session]+i,'warmup':False,'prompt_seed':1729+offsets[args.session]+i} for i in range(counts[args.session]))
    for case in cases:
        record={'schema_version':1,'kind':'setup_smoke' if args.suite=='smoke' else ('initial_speed_test' if args.suite=='firstlook' else ('setup_pilot' if args.suite=='pilot' else 'hardware_microbenchmark')),
                'machine_id':args.machine,'model_id':model_spec['id'],'model_revision':model_spec['revision'],
                'backend':'dwarfstar-metal','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_commit':actual,'runtime_lock_sha256':digest(ROOT/'config/dwarfstar.lock.json'),
                'model_lock_sha256':digest(ROOT/'config/models.lock.json'),'campaign_sha256':digest(ROOT/'config/campaign.json'),
                'compiler':subprocess.check_output(['xcrun','clang','--version'],text=True).splitlines()[0],
                'harness_sha256':digest(Path(__file__)),'session':args.session,'cell':case,'preflight':state,
                'os_build':subprocess.check_output(['sw_vers','-buildVersion'],text=True).strip(),
                'settings':{'resident':True,'speculation':False,'power':100,'prefill_chunk':2048}}
        if args.suite=='smoke':
            command=[str(vendor/'ds4'),'-m',str(gguf),'--metal','--ctx','4096','--prefill-chunk','2048',
                     '--temp','0','--seed','1729','--nothink','-n','128','-p','Reply with the single word READY.']
        else:
            prompt=ROOT/'work'/f'native-prompt-{case["prompt_seed"]}.txt'
            prompt.write_text(('Fictional inventory seed '+str(case['prompt_seed'])+'. Please summarize all entries.\n')+
                              '\n'.join(f'Item {i}: {(i*17+case["prompt_seed"])%1000} units; status ready.' for i in range(20000)))
            record['source_prompt_sha256']=digest(prompt)
            command=[str(vendor/'ds4-bench'),'-m',str(gguf),'--metal','--prompt-file',str(prompt),
                     '--ctx-start',str(case['input_tokens']),'--ctx-max',str(case['input_tokens']),
                     '--gen-tokens',str(case['output_tokens']),'--prefill-chunk','2048']
        start=time.perf_counter();swap=psutil.swap_memory().used
        # terminate gracefully on timeout; never kill a GPU-bearing process first.
        process=subprocess.Popen(command,cwd=vendor,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            stdout,stderr=process.communicate(timeout=1800 if args.suite=='smoke' else 3600)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:stdout,stderr=process.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                process.kill();stdout,stderr=process.communicate()
            record.update({'status':'timeout','process_wall_s':time.perf_counter()-start})
            append(output,record);raise RuntimeError('Native process timed out; no automatic retry')
        record.update({'process_wall_s':time.perf_counter()-start,'exit_code':process.returncode,
                       'swap_delta_bytes':psutil.swap_memory().used-swap,
                       'stdout':stdout.replace(str(ROOT),'<repo>'),'stderr':stderr.replace(str(ROOT),'<repo>'),
                       'binary_sha256':digest(Path(command[0]))})
        record['status']='ok' if process.returncode==0 else 'error'
        if args.suite=='smoke':
            record['ready_marker_seen']='READY' in stdout
            if not record['ready_marker_seen']:record['status']='unexpected_output'
        elif process.returncode==0:
            rows=list(csv.DictReader(io.StringIO(stdout)))
            record['native_csv_rows']=rows
            if len(rows)!=1 or int(rows[0]['prefill_tokens'])!=case['input_tokens'] or int(rows[0]['gen_tokens'])!=case['output_tokens']:
                record['status']='invalid_counters'
            else:
                record['input_tokens']=case['input_tokens'];record['output_tokens']=case['output_tokens']
                record['prefill_tok_s']=float(rows[0]['prefill_tps'])
                record['decode_tok_s']=float(rows[0]['gen_steady_tps'])
                record['ttft_s']=None # gen_first_ms excludes prefill; never mislabel it as TTFT
        append(output,record)
        print(json.dumps({'model':model_spec['id'],'cell':case['id'],'status':record['status']}),flush=True)
        if record['status']!='ok':raise RuntimeError('Native check failed: '+record['status'])
