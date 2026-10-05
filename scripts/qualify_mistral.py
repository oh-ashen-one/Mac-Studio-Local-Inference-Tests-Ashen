#!/usr/bin/env python3
"""Separately labeled native Mistral setup; called only by the guarded driver."""
import argparse,datetime,hashlib,json,re,signal,subprocess,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,write_json
from model_registry import resolve_model
from models import digest,verify
from unified_server import server,post,chat,chat_payload,count_chat
PINNED_NATIVE='f1cee9941b0e843ea260bf8dd9a090fbd9711b6a'

def rendered_reasoning_effort(prompt):
    start='[MODEL_SETTINGS]';end='[/MODEL_SETTINGS]'
    if start not in prompt or end not in prompt:raise RuntimeError('Native template omitted explicit model settings')
    settings=json.loads(prompt.split(start,1)[1].split(end,1)[0])
    mode=settings.get('reasoning_effort')
    if mode not in ('none','high'):raise RuntimeError('Unsupported rendered reasoning effort')
    return mode

def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-inference',action='store_true');p.add_argument('--run-id',required=True);a=p.parse_args()
    if not a.allow_inference:p.error('Owner inference authorization required')
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt()))
    if not re.fullmatch(r'q20261003-mistral-qualification-r[1-9][0-9]*',a.run_id):p.error('Separate qualification run ID required')
    # The supervising driver must be live and must own this qualification run.
    import psutil
    guard=json.loads((ROOT/'work/mistral-qualification-driver.json').read_text())
    if guard.get('run_id')!=a.run_id or not psutil.pid_exists(guard['pid']):raise RuntimeError('Guarded qualification driver required')
    spec,folder,lock=resolve_model('mistral-medium35-q4','config/mistral-models.lock.json')
    out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    result={'kind':'runtime_qualification','status':'starting','run_id':a.run_id,'model_revision':spec['revision'],'model_files':spec['files'],'model_lock_sha256':digest(lock),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Setup only; excluded from all 39 measured groups. Short exact-token probe and common task interface. Long-context stored metadata/load interpretation checked; full200K measurements remain separately declared.'}
    def save():write_json(out/'qualification.json',result)
    save()
    try:
        with shared_gpu_slot():
            result['preflight']=safety('studio-new');verify(spec,folder);result['artifact_hashes_verified']=True;save()
            vendor=ROOT/'vendor/llama-agentperf';commit=subprocess.check_output(['git','-C',str(vendor),'rev-parse','HEAD'],text=True).strip()
            if commit!=PINNED_NATIVE:raise RuntimeError('Reviewed native source revision changed')
            paths=[vendor/'build/bin/llama-server',*sorted((vendor/'build/bin').glob('*.dylib'))]
            files=[]
            for path in paths:
                if not path.resolve().is_relative_to(ROOT):raise RuntimeError('Native file resolves outside task checkout')
                files.append({'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':digest(path)})
            native={'commit':commit,'server':str(paths[0].relative_to(ROOT)),'lock':str((out/'native-runtime-lock.json').relative_to(ROOT)),'files':files}
            write_json(out/'native-runtime-lock.json',native);spec=dict(spec,native_runtime=native)
            result.update(native_runtime=native,runtime_files=files,runtime_source_commit=commit,native_server_sha256=files[0]['sha256'],runtime_lock_sha256=digest(ROOT/native['lock']));save()
            with server(spec,folder,out,port=18186,context=16384,cache_sequences=0) as (port,telemetry):
                result['runtime_load_passed']=True;save()
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/v1/models',timeout=10) as response:model_info=json.load(response)
                write_json(out/'native-model-info.json',model_info)
                tokens=post(port,'/tokenize',{'content':(ROOT/'work/context-corpus.txt').read_text(),'add_special':False,'parse_special':False},120)['tokens']
                if len(tokens)<8192:raise RuntimeError('Qualification corpus too short')
                payload={'prompt':tokens[:8192],'n_predict':32,'temperature':0,'seed':1729,'ignore_eos':True,'cache_prompt':False,'stream':False,'return_tokens':True}
                write_json(out/'exact-token-request.json',payload);response=post(port,'/completion',payload,900);write_json(out/'exact-token-response.json',response)
                timing=response.get('timings',{});actual=response.get('tokens_evaluated',timing.get('prompt_n'));generated=response.get('tokens_predicted',timing.get('predicted_n'))
                if (actual,generated)!=(8192,32):raise RuntimeError('Exact native qualification token counts mismatch')
                result.update(exact_token_count_passed=True,actual_probe_input_tokens=actual,actual_probe_output_tokens=generated);save()
                messages=[{'role':'system','content':'Respond directly without reasoning.'},{'role':'user','content':'Reply with the JSON object {"ready": true}.'}]
                templates={}
                for effort in ['none','high']:
                    rendered=post(port,'/apply-template',{'messages':messages,'add_generation_prompt':True,'chat_template_kwargs':{'reasoning_effort':effort}})
                    if rendered_reasoning_effort(rendered['prompt'])!=effort:raise RuntimeError('Native renderer ignored explicit reasoning effort')
                    templates[effort]=rendered
                write_json(out/'reasoning-template-evidence.json',templates);result['reasoning_control_passed']=True;save()
                count=count_chat(spec,folder,messages,port);result['task_preflight_input_tokens']=count;save();request=chat_payload(spec,messages,128,0,1729);write_json(out/'task-request.json',request)
                reply=chat(port,request,900);write_json(out/'task-response.json',reply)
                if reply['usage'].get('prompt_tokens')!=count or not reply['output'] or reply['reasoning'] or '[THINK]' in reply['output'] or '<think>' in reply['output']:raise RuntimeError('Common no-reasoning task interface or exact template usage mismatch')
                result.update(task_interface_passed=True,actual_task_input_tokens=count,task_output_tokens=reply['usage']['completion_tokens']);save()
                metadata=json.loads((ROOT/'hardware/mistral-gguf-metadata-20261003.json').read_text())
                if not metadata.get('metadata_crosschecks') or not all(metadata['metadata_crosschecks'].values()):raise RuntimeError('Long-context fixed metadata crosscheck missing')
                entries=model_info.get('data',[])
                if len(entries)!=1 or entries[0].get('meta',{}).get('n_ctx_train')!=262144:raise RuntimeError('Native model metadata did not confirm declared262144 training context')
                result.update(long_context_metadata_passed=True,long_context_evidence='Verified stored corrected settings plus native model endpoint declared training context; no full200K qualification claim',status='complete');save()
    except BaseException as error:
        result.update(status='failed',error=(str(error) or type(error).__name__).replace(str(ROOT),'<repo>').replace(str(Path.home()),'<home>'));save();raise
    finally:
        result['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

if __name__=='__main__':main()
