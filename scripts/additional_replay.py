#!/usr/bin/env python3
"""Official AA replay on a separately pinned independent text configuration.

MLX HTTP does not implement ignore_eos. Use recorded output caps explicitly;
this is an exploratory serving cell, not the standard exact-output cohort.
"""
import argparse,datetime,json,os,signal,socket,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,stop,Telemetry,write_json
from models import digest,verify
from model_registry import resolve_model
from text_runtime import runtime_lock

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--lock',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--mini',action='store_true');p.add_argument('--mimo-xml-tools',action='store_true');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec,folder,lock=resolve_model(a.model,a.lock);out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    result={'kind':'aa-agentperf','machine_id':'studio-new','condition':'alone','cohort':'additional-independent-mlx-vlm-recorded','model_id':a.model,'model_revision':spec['revision'],'model_lock_sha256':digest(lock),'runtime_lock_sha256':digest(runtime_lock('mlx-vlm')),'replay':'aa-mini-v1' if a.mini else 'agentperf-default-v1','output_token_policy':'recorded','exact_policy_status':'unsupported: MLX HTTP does not implement ignore_eos','comparable_to_standard_exact_cohort':False,'quality_note':'Official recorded trajectory; measures serving, not task solving. Different output policy from the standard managed run.','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'agentperf_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'vendor/aa-agentperf-local',text=True).strip(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'starting'}
    if a.mimo_xml_tools:
        if a.model!='mimo-v2.6-flash-mopd':raise ValueError('XML parser profile is MiMo-only')
        result.update(cohort='additional-independent-mlx-vlm-mimo-xml-v2-recorded',tool_parser='explicit upstream qwen3_coder XML parser',prior_failed_qualification='m5-aa-mimo-mini-recorded-20261001',change_scope='Response parsing only; model/template/sampling/output budgets unchanged')
    def update():write_json(out/'run.json',result);write_json(ROOT/'work/agentperf-live.json',result)
    server=client=None;update();port=18184
    try:
        with shared_gpu_slot():
            result['preflight']=safety('studio-new');verify(spec,folder)
            with socket.socket() as sock:
                if sock.connect_ex(('127.0.0.1',port))==0:raise RuntimeError('Replay port is occupied; preserve existing service')
            env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1');env.pop('AGENTPERF_SUBMIT_TOKEN',None)
            with (out/'server.log').open('w') as slog,(out/'agentperf.log').open('w') as clog:
                server=subprocess.Popen([sys.executable,str(ROOT/'scripts/vlm_text_server.py'),'--model',str(folder),'--host','127.0.0.1','--port',str(port),'--prompt-cache-size','1','--prompt-concurrency','1']+(['--mimo-xml-tools'] if a.mimo_xml_tools else []),cwd=ROOT,env=env,stdout=slog,stderr=slog,start_new_session=True)
                with Telemetry(server.pid) as telemetry:
                    for _ in range(300):
                        if server.poll() is not None:raise RuntimeError('Independent server failed during startup')
                        try:urllib.request.urlopen(f'http://127.0.0.1:{port}/v1/models',timeout=1);break
                        except Exception:time.sleep(1)
                    else:raise TimeoutError('Server startup exceeded five minutes')
                    cmd=[str(ROOT/'vendor/aa-agentperf-local/.venv/bin/agentperf-local'),'run','--replay',result['replay'],'--base-url',f'http://127.0.0.1:{port}/v1','--model','default_model','--output-dir',str(out/'raw'),'--output-token-policy','recorded','--no-power','--timeout-seconds','900','--no-progress']
                    client=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=clog,stderr=clog,start_new_session=True);start=time.monotonic()
                    while client.poll() is None:
                        result.update(status='running',elapsed_s=time.monotonic()-start)
                        turns=out/'raw/turns.jsonl'
                        if turns.exists():result['recorded_turns']=sum(1 for _ in turns.open())
                        update()
                        if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):raise RuntimeError('Memory guard reached')
                        if result['elapsed_s']>14400:raise TimeoutError('Four-hour replay budget reached')
                        time.sleep(2)
                write_json(out/'telemetry.json',telemetry.rows)
            summary_file=out/'raw/summary.json'
            summary=json.loads(summary_file.read_text()) if summary_file.exists() else {}
            serving_success=client.returncode==0 and summary.get('success') is True and summary.get('totals',{}).get('failed_turns')==0
            result.update(status='complete' if serving_success else 'failed',exit_code=client.returncode,serving_success=serving_success,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());update()
            if not serving_success:raise RuntimeError('Replay failed qualification; inspect preserved evidence')
    except BaseException as exc:result.update(status='failed',error=str(exc).replace(str(ROOT),'<repo>').replace(str(folder),'<model>'));update();raise
    finally:stop(client);stop(server)

if __name__=='__main__':main()
