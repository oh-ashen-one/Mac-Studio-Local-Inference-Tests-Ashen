#!/usr/bin/env python3
"""M5 first-look campaign: one model at a time, fixed-token probes + real streamed request."""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import socket
import statistics
import subprocess
import sys
import threading
import time
import urllib.request
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from models import digest
from bench import preflight
PROMPT='Write a Python function moving_average(values, window) that returns the simple moving average for every complete window. Reject nonpositive window sizes. Include an example with values [2, 4, 6, 8, 10] and window 3, show the expected result, and explain the time complexity. Keep the whole answer under 350 words.'


def write_json(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(path)


def stop(process):
    if process and process.poll() is None:
        import psutil
        try:children=psutil.Process(process.pid).children(recursive=True)
        except psutil.Error:children=[]
        # Stop the driver first, then only its own descendants. Allow graceful GPU shutdown.
        process.terminate()
        for child in children:
            try:child.terminate()
            except psutil.Error:pass
        _,alive=psutil.wait_procs(children,timeout=60)
        for child in alive:
            try:child.kill()
            except psutil.Error:pass
        try:process.wait(timeout=1)
        except subprocess.TimeoutExpired:process.kill();process.wait()


def safety():
    state=preflight('studio-new',True)
    console=subprocess.check_output(['stat','-f','%Su','/dev/console'],text=True).strip()
    if console in ('root','loginwindow',''):raise RuntimeError('Desktop session is not active')
    for line in subprocess.check_output(['ps','-axo','stat=,comm='],text=True).splitlines():
        parts=line.strip().split(None,1)
        if len(parts)!=2:continue
        status,name=parts
        if any(x in name.lower() for x in ('unrealeditor.app/','unity.app/','blender.app/','godot.app/')):
            raise RuntimeError('Another renderer is present on this host; preserve it and reserve a test window')
    return state


@contextlib.contextmanager
def shared_gpu_slot():
    # Interoperates with the existing shared protocol: perf.lock SH + capture.N.lock EX.
    base=Path(os.environ.get('GPU_SLOT_DIR',str(Path.home()/'.cache/gpu-slot')))
    if (base/'PAUSED').exists():raise RuntimeError('Shared GPU protocol is paused')
    for name in ['locks','holders','queue']:(base/name).mkdir(parents=True,exist_ok=True)
    if any((base/'queue').iterdir()):raise RuntimeError('Existing shared GPU waiters have priority')
    held=[];slot=None;holder=base/'holders'/f'{os.getpid()}.json'
    try:
        perf=(base/'locks/perf.lock').open('a+')
        fcntl.flock(perf,fcntl.LOCK_SH|fcntl.LOCK_NB);held.append(perf)
        for index in range(2):
            candidate=(base/'locks'/f'capture.{index}.lock').open('a+')
            try:fcntl.flock(candidate,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:candidate.close();continue
            held.append(candidate);slot=str(index);break
        if slot is None:raise RuntimeError('Both shared GPU slots are occupied')
        write_json(holder,{'pid':os.getpid(),'start':subprocess.check_output(['ps','-o','lstart=','-p',str(os.getpid())],text=True).strip(),'class':'capture','label':'ashen-m5-inference-firstlook','slot':slot,'state':'running','cmd':'scripts/first_test.py','since':datetime.datetime.now().astimezone().isoformat()})
        yield {'directory':'~/.cache/gpu-slot','slot':slot,'mode':'shared capture slot; not quiet-exclusive performance'}
    finally:
        if slot is not None:holder.unlink(missing_ok=True)
        for fd in reversed(held):fd.close()


class Telemetry:
    def __init__(self,pid):self.pid=pid;self.rows=[];self.done=threading.Event()
    def sample(self):
        import psutil
        while not self.done.is_set():
            try:
                proc=psutil.Process(self.pid)
                rss=sum(p.memory_info().rss for p in [proc]+proc.children(recursive=True) if p.is_running())
                text=subprocess.check_output(['ioreg','-r','-d','1','-c','AGXAccelerator'],text=True,timeout=5)
                matches=re.findall(r'"Device Utilization %"\s*=\s*(\d+)',text)
                self.rows.append({'elapsed_s':time.monotonic()-self.start,'rss_bytes':rss,'available_bytes':psutil.virtual_memory().available,'swap_bytes':psutil.swap_memory().used,'gpu_util_pct':max(map(int,matches)) if matches else None})
            except Exception:pass
            self.done.wait(1)
    def __enter__(self):
        self.start=time.monotonic();self.thread=threading.Thread(target=self.sample,daemon=True);self.thread.start();return self
    def __exit__(self,*args):self.done.set();self.thread.join(timeout=6)


def summarize(rows):
    speeds=[r['decode_tok_s'] for r in rows if r.get('kind')=='initial_speed_test' and not r.get('cell',{}).get('warmup') and r.get('status')=='ok' and r.get('decode_tok_s')]
    return {'measured_repeats':len(speeds),'fastest_decode_tok_s':max(speeds) if speeds else None,'median_decode_tok_s':statistics.median(speeds) if speeds else None}


def transaction(spec,out,live,update):
    safety()
    port=18183
    with socket.socket() as check:
        if check.connect_ex(('127.0.0.1',port))==0:raise RuntimeError('Test server port is already occupied; will not take it over')
    environment=os.environ.copy();environment.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
    if spec['backend']=='mlx':
        cmd=[sys.executable,'-m','mlx_lm.server','--model',str(ROOT/'models'/spec['id']),'--host','127.0.0.1','--port',str(port),'--prompt-cache-size','0','--prompt-concurrency','1']
        cwd=ROOT
    else:
        cwd=ROOT/'vendor/dwarfstar'
        cmd=[str(cwd/'ds4-server'),'-m',str(ROOT/'models'/spec['id']/spec['files'][0]['path']),'--host','127.0.0.1','--port',str(port),'--metal','--ctx','8192','--prefill-chunk','2048']
    start=time.perf_counter();process=None
    with (out/(spec['id']+'-server.log')).open('w') as log:
        try:
            process=subprocess.Popen(cmd,cwd=cwd,env=environment,stdout=log,stderr=log,start_new_session=True)
            with Telemetry(process.pid) as telemetry:
                for _ in range(900):
                    if process.poll() is not None:raise RuntimeError('Model server exited during startup; inspect its saved log')
                    try:
                        with urllib.request.urlopen(f'http://127.0.0.1:{port}/v1/models',timeout=2) as response:
                            if response.status==200:break
                    except Exception:time.sleep(1)
                else:raise TimeoutError('Model server startup exceeded 15 minutes')
                ready_s=time.perf_counter()-start
                payload={'model':'default_model' if spec['backend']=='mlx' else spec['repo'],'messages':[{'role':'user','content':PROMPT}],'temperature':0,'max_tokens':512,'stream':True,'stream_options':{'include_usage':True}}
                if spec['backend']=='mlx':payload['chat_template_kwargs']={'enable_thinking':False}
                else:payload['thinking']={'type':'disabled'}
                request=urllib.request.Request(f'http://127.0.0.1:{port}/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                begin=time.perf_counter();first=None;first_visible=None;last=None;usage=None;content='';reasoning='';chunks=[];finish=None;last_write=0
                with urllib.request.urlopen(request,timeout=600) as response:
                    for raw in response:
                        if time.perf_counter()-begin>600:raise TimeoutError('Transaction time budget exceeded')
                        line=raw.decode().strip()
                        if not line.startswith('data: '):continue
                        if line[6:]=='[DONE]':break
                        body=json.loads(line[6:]);elapsed=time.perf_counter()-begin
                        if body.get('usage'):usage=body['usage']
                        for choice in body.get('choices',[]):
                            delta=choice.get('delta',{})
                            text=delta.get('content') or '';think=delta.get('reasoning_content') or delta.get('reasoning') or ''
                            if text or think:
                                if first is None:first=elapsed
                                if text and first_visible is None:first_visible=elapsed
                                last=elapsed;chunks.append({'elapsed_s':elapsed,'content_chars':len(text),'reasoning_chars':len(think)})
                                content+=text;reasoning+=think
                            if choice.get('finish_reason'):finish=choice['finish_reason']
                        if elapsed-last_write>.5:
                            live['stream']={'model_id':spec['id'],'content':content,'reasoning':reasoning,'elapsed_s':elapsed};update();last_write=elapsed
                wall=time.perf_counter()-begin
                if not usage or not isinstance(usage.get('completion_tokens'),int):raise RuntimeError('Backend did not provide token usage; refusing to invent tok/s')
                n=usage['completion_tokens']
                result={'kind':'real_transaction','model_id':spec['id'],'prompt':PROMPT,'request':payload,'server_ready_s':ready_s,'ttft_stream_s':first,'first_visible_output_s':first_visible,'response_wall_s':wall,'end_to_end_output_tok_s':n/wall if wall else None,'completion_tokens':n,'prompt_tokens':usage.get('prompt_tokens'),'usage':usage,'finish_reason':finish,'output':content,'reasoning':reasoning,'stream_chunks':chunks,'status':'ok'}
                # Only the fixed-token engine probe is used for precise decode tok/s.
                # HTTP chunks are never counted as tokens.
                result['peak_server_rss_bytes']=max((r['rss_bytes'] for r in telemetry.rows),default=None)
                result['telemetry']=telemetry.rows
                write_json(out/(spec['id']+'-transaction.json'),result)
                return result
        finally:stop(process)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--campaign',required=True);a=p.parse_args()
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    if not a.allow_inference:p.error('Owner authorization and --allow-inference are required')
    if not re.fullmatch(r'[a-z0-9-]+',a.campaign):p.error('Use a simple campaign identifier')
    out=ROOT/'results'/a.campaign
    out.mkdir(parents=True,exist_ok=False)
    live={'campaign':a.campaign,'machine':'M5 Ultra · 256 GB','status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'background_note':'Initial interactive measurement; Photos/iCloud background work and the live browser may affect performance. Not an absolute maximum or an M3 comparison.','configuration':'Pinned artifacts; 512-input / 256-output speed probe; one warmup and three measured repeats; no speculation. Separate real streamed request capped at 512 tokens.','models':{},'active':None}
    def update():write_json(ROOT/'work/live-results.json',live)
    update();specs=json.loads((ROOT/'config/models.lock.json').read_text())['models']
    specs.sort(key=lambda m:['qwen-27b','gemma-31b','deepseek-v4-flash'].index(m['id']))
    process=None
    try:
        with shared_gpu_slot() as slot:
            live['harness_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();live['driver_sha256']=digest(Path(__file__))
            live['slot']=slot;live['preflight']=safety();live['model_lock_sha256']=digest(ROOT/'config/models.lock.json')
            for spec in specs:
                live['active']=spec['id'];live['status']='speed_test';live['models'][spec['id']]={'status':'running','quantization':spec['quantization'],'revision':spec['revision'],'backend':spec['backend']};update()
                safety()
                raw=out/(spec['id']+'-speed.jsonl')
                command=[sys.executable,str(ROOT/'scripts/bench.py'),'--allow-inference','--machine','studio-new','--suite','firstlook','--model',spec['id'],'--output',str(raw)]
                with (out/(spec['id']+'-speed.log')).open('w') as log:
                    process=subprocess.Popen(command,cwd=ROOT,stdout=log,stderr=log,start_new_session=True)
                    with Telemetry(process.pid) as t:
                        start=time.monotonic()
                        while process.poll() is None:
                            if time.monotonic()-start>1800:raise TimeoutError('Speed test exceeded 30 minutes')
                            if raw.exists():
                                rows=[json.loads(l) for l in raw.read_text().splitlines() if l.strip()]
                                live['models'][spec['id']].update(summarize(rows));update()
                            if t.rows and (t.rows[-1]['available_bytes']<8*1024**3 or t.rows[-1]['swap_bytes']-t.rows[0]['swap_bytes']>2*1024**3):
                                raise RuntimeError('Memory pressure guard stopped this test')
                            time.sleep(2)
                    write_json(out/(spec['id']+'-speed-telemetry.json'),t.rows)
                if process.returncode:raise RuntimeError('Speed worker failed for '+spec['id']+'; no automatic retry')
                rows=[json.loads(l) for l in raw.read_text().splitlines()]
                summary=summarize(rows)
                if summary['measured_repeats']!=3:raise RuntimeError('Expected three valid measured repeats')
                live['models'][spec['id']].update(summary)
                live['models'][spec['id']]['peak_process_rss_bytes']=max((x['rss_bytes'] for x in t.rows),default=None)
                live['models'][spec['id']]['observed_system_memory_delta_bytes']=max(0,t.rows[0]['available_bytes']-min(x['available_bytes'] for x in t.rows)) if t.rows else None
                prefill=[r.get('prefill_tok_s') for r in rows if not r.get('cell',{}).get('warmup') and r.get('prefill_tok_s')]
                live['models'][spec['id']]['prefill_tok_s']=statistics.median(prefill) if prefill else None
                live['status']='real_transaction';update()
                result=transaction(spec,out,live,update)
                live['models'][spec['id']].update({'status':'complete','transaction':{k:v for k,v in result.items() if k not in ('telemetry','stream_chunks')}})
                live.pop('stream',None);update()
                print(spec['id']+' completed',flush=True)
            live['status']='complete';live['active']=None;live['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()
    except BaseException as e:
        live['status']='failed';live['error']=str(e).replace(str(ROOT),'<repo>');update();raise
    finally:
        stop(process);write_json(out/'summary.json',live)


if __name__=='__main__':main()
