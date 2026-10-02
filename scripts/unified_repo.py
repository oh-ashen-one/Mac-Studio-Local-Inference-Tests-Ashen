#!/usr/bin/env python3
"""Same bounded repository diagnostic for every pinned serving backend."""
import argparse,datetime,difflib,json,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import shared_gpu_slot,safety,write_json
from model_registry import resolve_model
from models import digest,verify
from repo_task import BASE,TASK,fresh,act,evaluate
from run_repo_task import SYSTEM
from unified_server import server,chat,chat_payload,fill_to_tokens

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True);p.add_argument('--run-id',required=True);p.add_argument('--attempt',type=int,required=True);p.add_argument('--max-turns',type=int,default=8);p.add_argument('--context',type=int,default=200000);a=p.parse_args()
    if not a.allow_inference:p.error('Owner inference authorization required')
    if a.max_turns not in [8,20] or not 1<=a.attempt<=5:p.error('Use the declared task budgets and seeds')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec,folder,lock=resolve_model(a.model,'config/unified-models.lock.json');out=ROOT/'results'/a.run_id;out.mkdir(exist_ok=False)
    candidate=ROOT/'work'/f'{a.run_id}-candidate';result={'kind':'repo_task','campaign_id':'unified-overnight-20261002','model_id':a.model,'machine_id':'studio-new','attempt':a.attempt,'status':'starting','passed':False,'human_rescues':0,'protocol':'django-charprefix-v2-'+str(a.max_turns)+'turns','task_id':TASK['instance_id'],'base_commit':TASK['base_commit'],'model_revision':spec['revision'],'model_lock_sha256':digest(lock),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'max_turns':a.max_turns,'max_output_tokens_per_turn':2048,'temperature':.2,'seed':1000+a.attempt,'thinking_requested':False,'turns':[],'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    def update():write_json(out/'result.json',result);write_json(ROOT/'work/unified-job-live.json',result)
    update();started=None
    try:
        with shared_gpu_slot():
            result['preflight']=safety('studio-new');verify(spec,folder);fresh(candidate)
            corpus=''
            for file in sorted(BASE.rglob('*.py')):
                corpus+='\nFILE '+str(file.relative_to(BASE))+'\n'+file.read_text(errors='replace')
                if len(corpus)>1800000:break
            system=SYSTEM.replace('You have eight turns',f'You have {a.max_turns} turns')
            with server(spec,folder,out) as (port,telemetry):
                messages,count=fill_to_tokens(spec,folder,system,'Repository snapshot (partial; use read for other files):\n',corpus,'\n\nTASK:\n'+TASK['problem_statement'],a.context,port)
                result.update(status='working',initial_chat_tokens=count,initial_packet_sha256=__import__('hashlib').sha256(json.dumps(messages,sort_keys=True).encode()).hexdigest());write_json(out/'initial-packet.json',messages);update();started=time.perf_counter()
                for turn in range(a.max_turns):
                    if telemetry.rows and (telemetry.rows[-1]['available_bytes']<12*2**30 or telemetry.rows[-1]['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*2**30):raise RuntimeError('Memory guard reached')
                    payload=chat_payload(spec,messages,2048,.2,1000+a.attempt)
                    row=chat(port,payload,900);row['turn']=turn+1;row['first_visible_output_s']=row['first_output_s']
                    if turn==0 and not a.context<=row['usage'].get('prompt_tokens',0)<=a.context+64:raise RuntimeError('Actual server input count outside declared range; preserve mismatch')
                    text=row['output'];messages.append({'role':'assistant','content':text})
                    try:
                        request=json.loads(text.strip().removeprefix('```json').removesuffix('```').strip());feedback=act(request,candidate,out/f'eval-{turn+1}')
                    except (ValueError,KeyError,TypeError) as exc:feedback={'error':str(exc)}
                    row['feedback']=feedback;result['turns'].append(row);update()
                    if feedback.get('passed') or feedback.get('finished'):break
                    messages.append({'role':'user','content':json.dumps(feedback)})
                    if time.perf_counter()-started>3600*(2 if a.max_turns==20 else 1):raise TimeoutError('Declared attempt wall-time budget exhausted')
                final=evaluate(candidate,out/'final-evaluation');result.update(status='complete',passed=final['passed'],final_evaluation=final,wall_s=time.perf_counter()-started)
    except BaseException as exc:
        result.update(status='failed',error=str(exc).replace(str(ROOT),'<repo>').replace(str(folder),'<model>'),wall_s=time.perf_counter()-started if started else None)
        raise
    finally:
        if candidate.exists():
            diff=''
            for file in candidate.glob('django/db/migrations/*.py'):
                relative=file.relative_to(candidate);diff+=''.join(difflib.unified_diff((BASE/relative).read_text().splitlines(True),file.read_text().splitlines(True),fromfile='a/'+str(relative),tofile='b/'+str(relative)))
            (out/'candidate.patch').write_text(diff)
        result['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()

if __name__=='__main__':main()
