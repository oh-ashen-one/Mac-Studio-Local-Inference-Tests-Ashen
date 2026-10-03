"""Pinned, loopback-only server adapters. Caller owns GPU slot and budgets."""
import contextlib,json,os,socket,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from first_test import stop,Telemetry
_native_server_active = False

def post(port,path,payload,timeout=60):
    request=urllib.request.Request(f'http://127.0.0.1:{port}{path}',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=timeout) as response:return json.load(response)

def model_name(spec):
    return 'default_model' if spec['runtime'].startswith('mlx') else spec['id'] if spec['runtime']=='llama-cpp' else spec['repo']

def template_kwargs(spec):
    return {'reasoning_effort':'none'} if spec['id']=='mistral-medium35-q4' else {'enable_thinking':False}

def chat_payload(spec,messages,max_tokens=2048,temperature=0,seed=1729):
    payload={'model':model_name(spec),'messages':messages,'max_tokens':max_tokens,'temperature':temperature,'seed':seed,'stream':True,'stream_options':{'include_usage':True}}
    if spec['runtime']=='dwarfstar':payload['thinking']={'type':'disabled'}
    else:payload['chat_template_kwargs']=template_kwargs(spec)
    if spec['id']=='mistral-medium35-q4':payload['reasoning_effort']='none'
    return payload

def chat(port,payload,timeout=900):
    request=urllib.request.Request(f'http://127.0.0.1:{port}/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    start=time.perf_counter();text='';reasoning='';usage={};finish=None;first=None;chunks=[]
    with urllib.request.urlopen(request,timeout=timeout) as response:
        for raw in response:
            elapsed=time.perf_counter()-start
            if elapsed>timeout:raise TimeoutError('Declared per-request deadline exceeded')
            if not raw.startswith(b'data:'):continue
            raw=raw[5:].strip()
            if raw==b'[DONE]':break
            body=json.loads(raw)
            if body.get('usage'):usage=body['usage']
            for choice in body.get('choices',[]):
                delta=choice.get('delta') or {};content=delta.get('content') or '';thought=delta.get('reasoning_content') or delta.get('reasoning') or ''
                if content or thought:
                    first=elapsed if first is None else first;chunks.append({'elapsed_s':elapsed,'content_chars':len(content),'reasoning_chars':len(thought)})
                text+=content;reasoning+=thought;finish=choice.get('finish_reason') or finish
    wall=time.perf_counter()-start
    if not isinstance(usage.get('completion_tokens'),int):raise RuntimeError('Server did not provide actual token counts')
    return {'output':text,'reasoning':reasoning,'usage':usage,'finish_reason':finish,'wall_s':wall,'first_output_s':first,'end_to_end_tok_s':usage['completion_tokens']/wall,'stream_chunks':chunks,'chunk_note':'SSE chunks are not counted as tokens; exact usage is server-reported.'}

@contextlib.contextmanager
def server(spec,folder,out,port=18185,context=262144,cache_sequences=1,slots=1):
    global _native_server_active
    with socket.socket() as sock:
        if sock.connect_ex(('127.0.0.1',port))==0:raise RuntimeError('Owned benchmark port is occupied; preserve existing process')
    env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
    if spec['runtime'].startswith('mlx'):
        if spec['runtime']=='mlx-vlm':entry=[str(ROOT/'scripts/vlm_text_server.py')]
        else:entry=['-m','mlx_lm.server']
        cmd=[sys.executable,*entry,'--model',str(folder),'--host','127.0.0.1','--port',str(port),'--prompt-cache-size',str(cache_sequences),'--prompt-concurrency',str(slots),'--prefill-step-size','2048']
        if spec['id']=='mimo-v2.6-flash-mopd':cmd+=['--mimo-xml-tools']
        cwd=ROOT
    elif spec['runtime']=='llama-cpp':
        cmd=[str(ROOT/spec.get('native_runtime',{}).get('server','vendor/llama-agentperf/build/bin/llama-server')),'-m',str(folder/spec['files'][0]['path']),'--alias',spec['id'],'--jinja','--host','127.0.0.1','--port',str(port),'-c',str(context*slots),'-ngl','999','--parallel',str(slots),'--flash-attn','on','--batch-size','2048','--ubatch-size','2048','--no-context-shift']
        cwd=ROOT
    elif spec['runtime']=='dwarfstar':
        cmd=[str(ROOT/'vendor/dwarfstar/ds4-server'),'-m',str(folder/spec['files'][0]['path']),'--host','127.0.0.1','--port',str(port),'--metal','--ctx',str(context),'--prefill-chunk','2048']
        if slots>1:cmd+=['--batched-session',str(slots)]
        cwd=ROOT/'vendor/dwarfstar'
    else:raise ValueError('Unsupported pinned runtime')
    process=None;telemetry=None
    from models import digest
    runtime_lock='config/requirements-mlx-vlm.lock' if spec['runtime']=='mlx-vlm' else 'requirements-macos-arm64.lock' if spec['runtime']=='mlx-lm' else 'config/agentperf.lock.json' if spec['runtime']=='llama-cpp' else 'config/dwarfstar.lock.json'
    runtime_lock=spec.get('native_runtime',{}).get('lock',runtime_lock)
    (out/'server-config.json').write_text(json.dumps({'runtime':spec['runtime'],'runtime_lock_sha256':digest(ROOT/runtime_lock),'command':[x.replace(str(ROOT),'<repo>').replace(str(Path.home()),'<home>') for x in cmd],'requested_context_per_slot':context,'slots':slots,'prompt_cache_sequences':cache_sequences,'thinking_policy':'Requested disabled in common task payloads; official replay keeps its declared policy','native_binary_sha256':digest(Path(cmd[0])) if not spec['runtime'].startswith('mlx') else None},indent=2)+'\n')
    with (out/'server.log').open('w') as log:
        try:
            process=subprocess.Popen(cmd,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
            with Telemetry(process.pid) as telemetry:
                for _ in range(600):
                    if process.poll() is not None:raise RuntimeError('Pinned server exited during startup; inspect preserved server log')
                    try:
                        with urllib.request.urlopen(f'http://127.0.0.1:{port}/v1/models',timeout=1) as response:
                            if response.status==200:break
                    except Exception:time.sleep(1)
                else:raise TimeoutError('Server did not become ready within ten minutes')
                _native_server_active = spec['runtime']=='dwarfstar'
                yield port,telemetry
            (out/'server-telemetry.json').write_text(json.dumps(telemetry.rows,indent=2)+'\n')
        finally:
            _native_server_active = False
            if telemetry is not None:(out/'server-telemetry.json').write_text(json.dumps(telemetry.rows,indent=2)+'\n')
            stop(process)

def count_chat(spec,folder,messages,port=None):
    if spec['runtime']=='llama-cpp' and port is not None:
        rendered=post(port,'/apply-template',{'messages':messages,'add_generation_prompt':True,'chat_template_kwargs':template_kwargs(spec)})['prompt']
        return len(post(port,'/tokenize',{'content':rendered,'add_special':False,'parse_special':True})['tokens'])
    if spec['runtime']=='dwarfstar':
        if _native_server_active:raise RuntimeError('Native metadata tokenization must finish before loading the DwarfStar server')
        if len(messages)!=2 or [m['role'] for m in messages]!=['system','user']:raise ValueError('Native exact counter currently supports the initial system/user packet only')
        prompt=ROOT/'work/deepseek-tokenizer-input.txt';prompt.write_text(messages[1]['content'])
        result=subprocess.run([str(ROOT/'vendor/dwarfstar/ds4'),'-m',str(folder/spec['files'][0]['path']),'--dump-tokens','--nothink','--ctx','262144','--system',messages[0]['content'],'--prompt-file',str(prompt)],capture_output=True,text=True,timeout=120)
        if result.returncode:raise RuntimeError('Native metadata-only tokenization failed')
        return len(json.loads(result.stdout.splitlines()[0]))
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(folder,local_files_only=True,trust_remote_code=False)
    return len(tokenizer.apply_chat_template(messages,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False))

def fill_to_tokens(spec,folder,system,prefix,body,suffix,target=200000,port=None):
    def messages(n):return [{'role':'system','content':system},{'role':'user','content':prefix+body[:n]+suffix}]
    lo,hi=0,len(body);best=None
    for _ in range(25):
        n=(lo+hi)//2;m=messages(n);count=count_chat(spec,folder,m,port)
        if target<=count<=target+32:return m,count
        if count<target:lo=n+1
        else:best=(m,count);hi=n-1
    if best and best[1]<=target+32:return best
    raise RuntimeError('Could not construct exact declared input range; no silent truncation')
