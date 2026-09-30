#!/usr/bin/env python3
"""Run a small transparent correctness diagnostic against an already-running local server."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.request
ROOT=Path(__file__).resolve().parents[1]


def final_json(text):
    text=text.split('</think>')[-1].strip()
    text=re.sub(r'^```(?:json)?\s*|\s*```$','',text).strip()
    return json.loads(text)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True);p.add_argument('--port',type=int,default=18181)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    specs=json.loads((ROOT/'config/models.lock.json').read_text())['models']
    spec=next((m for m in specs if m['id']==a.model),None)
    if not spec:p.error('Unknown model')
    path=ROOT/'config/quality-smoke.json';pack=json.loads(path.read_text())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    for case in pack['cases']:
        payload={'model':spec['repo'],'messages':[{'role':'user','content':case['prompt']}],
                 'temperature':0,'max_tokens':2048,'stream':False}
        if a.model=='qwen-27b':payload['chat_template_kwargs']={'enable_thinking':False}
        if spec['backend']=='dwarfstar':payload['thinking']={'type':'disabled'}
        row={'kind':'quality_diagnostic','model_id':a.model,'task_id':case['id'],
             'suite_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'request':payload,
             'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        start=time.perf_counter()
        try:
            request=urllib.request.Request(f'http://127.0.0.1:{a.port}/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=600) as response:body=json.load(response)
            text=body['choices'][0]['message']['content']
            row.update({'response':body,'status':'ok','passed':final_json(text)==case['expected']})
        except Exception as e:row.update({'status':'error','passed':False,'error':str(e)})
        row['wall_s']=time.perf_counter()-start
        with a.output.open('a') as stream:stream.write(json.dumps(row)+'\n')
        print(case['id'],row['passed'],flush=True)


if __name__=='__main__':main()
