#!/usr/bin/env python3
"""Summarize saved repository attempts; never runs inference or tests."""
import argparse,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prefix',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=[]
    for path in sorted((ROOT/'results').glob(a.prefix+'-*/result.json')):
        r=json.loads(path.read_text());rows.append({'attempt':r['attempt'],'status':r['status'],'passed':r['passed'],'human_rescues':r['human_rescues'],'turns':len(r['turns']),'initial_chat_tokens':r['initial_chat_tokens'],'task_wall_s':r.get('wall_s'),'first_turn_ttft_s':r['turns'][0]['first_visible_output_s'] if r['turns'] else None,'total_output_tokens':sum(x.get('usage',{}).get('completion_tokens',0) for x in r['turns']),'error':r.get('error')})
    complete=[r for r in rows if r['status']=='complete'];times=[r['task_wall_s'] for r in complete]
    report={'kind':'repo_diagnostic_summary','task':'django__django-14500','planned_attempts':5,'completed_attempts':len(complete),'successful_attempts':sum(r['passed'] for r in complete),'infrastructure_failures':sum(r['status']=='failed' for r in rows),'human_rescues':sum(r['human_rescues'] for r in rows),'median_task_wall_s':statistics.median(times) if times else None,'attempts':rows,'clock_definition':'Server ready to final test result; includes input fill, generation and tool/test time; excludes package setup, file hashing, tokenizer preparation and model-server startup.','limitation':'Same historical public bug across seeds, not five independent tasks. Training contamination possible. No general intelligence or long-horizon reliability score.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='attempts'},indent=2))
if __name__=='__main__':main()
