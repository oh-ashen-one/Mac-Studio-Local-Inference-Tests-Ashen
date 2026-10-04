#!/usr/bin/env python3
"""Read-only coverage/statistics for the frozen unified study; no model imports."""
import json,statistics,datetime,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from publication_labels import public_spec

def stats(values):
    values=[x for x in values if isinstance(x,(int,float))]
    return {'n':len(values),'median':statistics.median(values) if values else None,'mean':statistics.mean(values) if values else None,'stdev':statistics.stdev(values) if len(values)>1 else None,'min':min(values) if values else None,'max':max(values) if values else None}

def collect(plan_path='config/unified-campaign.json',state_path='work/unified-campaign.json'):
    plan=json.loads((ROOT/plan_path).read_text());specs=json.loads((ROOT/plan['model_lock']).read_text())['models']
    live_path=ROOT/state_path;live=json.loads(live_path.read_text()) if live_path.exists() else None
    jobs=live['jobs'] if live else [{**j,'status':'pending'} for j in plan['jobs']]
    records={}
    for j in jobs:
        folder=ROOT/'results'/j.get('result_run_id',j['id']);file=folder/('run.json' if j['kind']=='replay' else 'result.json')
        if file.exists():
            try:
                r=json.loads(file.read_text());records[j['id']]=r
                if not live:j['status']=r['status']
                summary=folder/'raw/summary.json'
                if summary.exists():r['replay_summary']=json.loads(summary.read_text())
            except (OSError,ValueError):pass
    declared={j["id"]:j for j in plan["jobs"]}
    for j in jobs:
        amendment=declared.get(j["id"],{})
        if j['status'] in ('pending','needs_review') and amendment.get('disposition') in ('omitted_by_owner_scope','unsupported_resource','deferred_resource_review','unsupported_request_budget','unsupported_request_budget_cases'):
            j.update(status=amendment['disposition'],reason=amendment['disposition_reason'])
    models=[]
    for spec in specs:
        spec=public_spec(spec)
        own=[j for j in jobs if j['model_id']==spec['id']];done=[j for j in own if j['status']=='complete'];m={'id':spec['id'],'name':spec['display_name'],'runtime':spec['runtime'],'quantization':spec['quantization'],'completed_jobs':len(done),'planned_jobs':len(own),'speed':{},'repo':{},'quality':{},'replay':{},'serving':{}}
        m['budget_limited_jobs']=sum(j['status'] in ('unsupported_request_budget','unsupported_request_budget_cases') for j in own)
        m['resource_limited_jobs']=sum(j['status']=='unsupported_resource' for j in own)
        m['deferred_jobs']=sum(j['status']=='deferred_resource_review' for j in own)
        m['omitted_jobs']=sum(j['status']=='omitted_by_owner_scope' for j in own)
        m['historical_comparison']=any(spec['id'] in a.get('historical_model_ids',[]) for a in plan.get('scope_amendments',[]))
        for length in plan['context_lengths']:
            rows=[records[j['id']] for j in done if j['kind']=='speed' and j['tokens']==length and j['output_tokens']==256 and j['id'] in records]
            m['speed'][str(length)]={'decode':stats([r.get('decode_tok_s') for r in rows]),'fill':stats([r.get('context_fill_s') for r in rows]),'prefill':stats([r.get('prefill_tok_s') for r in rows])}
        tails=[records[j['id']] for j in done if j['kind']=='speed' and j['output_tokens']==2048 and j['id'] in records]
        m['sustained']={'completed':len(tails),'planned':3,'decode':stats([r.get('decode_tok_s') for r in tails]),'fill':stats([r.get('context_fill_s') for r in tails]),'actual_input_tokens':[r.get('input_tokens') for r in tails],'actual_output_tokens':[r.get('output_tokens') for r in tails]}
        for turns in [8,20]:
            rows=[records[j['id']] for j in done if j['kind']=='repo' and j['max_turns']==turns and j['id'] in records]
            m['repo'][str(turns)]={'completed':len(rows),'passed':sum(bool(r.get('passed')) for r in rows),'wall_s':stats([r.get('wall_s') for r in rows])}
        for suite in ['structured','retrieval','humaneval']:
            j=next(x for x in own if x['kind']=='quality' and x['suite']==suite);r=records.get(j['id'],{})
            m['quality'][suite]={'status':j['status'],'completed':r.get('completed_cases',0),'passed':r.get('passed_cases',0),'planned':r.get('planned_cases',{'structured':24,'retrieval':9,'humaneval':164}[suite])}
            if j.get('case_continuation'):
                m['quality'][suite].update(planned=9,attempted_cases=r.get('attempted_cases',0)+1,unscored_request_budget_cases=r.get('unscored_request_budget_cases',0)+1,continuation_run_id=j['result_run_id'],requires_full_case_review=True)
        for mini in [True,False]:
            j=next(x for x in own if x['kind']=='replay' and x['mini']==mini);r=records.get(j['id'],{});s=r.get('replay_summary',{})
            m['replay']['mini' if mini else 'full']={'status':j['status'],'run_id':j['id'],'turns':s.get('totals',{}).get('turns'),'served':s.get('totals',{}).get('successful_turns'),'end_to_end_tok_s':s.get('end_to_end_output_tokens_per_second'),'context_evidence':s.get('config',{}).get('context'),'output_policy':s.get('config',{}).get('output_tokens',{}).get('policy'),'measured_duration_s':s.get('measured_duration_ms',0)/1000 if s else None,'short_output_warnings':s.get('totals',{}).get('short_output_warnings'),'server_output_tokens':s.get('totals',{}).get('total_server_output_tokens'),'server_prompt_tokens':s.get('totals',{}).get('total_server_prompt_tokens'),'server_cached_prompt_tokens':s.get('totals',{}).get('total_server_cached_prompt_tokens')}
        for c in [1,2,4]:
            j=next(x for x in own if x['kind']=='serving' and x['concurrency']==c);r=records.get(j['id'],{})
            m['serving'][str(c)]={k:r.get(k) for k in ['aggregate_output_tok_s','ttft_median_s','ttft_p95_s','latency_median_s','latency_p95_s','completed_requests','wall_s','total_output_tokens']};m['serving'][str(c)]['status']=j['status']
        models.append(m)
    active=next((j for j in jobs if j['id']==(live or {}).get('active')),None)
    return {'campaign_id':plan['id'],'status':(live or {}).get('status','saved_results'),'overall_deadline':None,'active':active,'error':(live or {}).get('error'),'amendments':plan.get('amendments',[]),'completed_jobs':sum(j['status']=='complete' for j in jobs),'planned_jobs':len(jobs),'omitted_jobs':sum(j['status']=='omitted_by_owner_scope' for j in jobs),'resource_limited_jobs':sum(j['status']=='unsupported_resource' for j in jobs),'deferred_jobs':sum(j['status']=='deferred_resource_review' for j in jobs),'budget_limited_jobs':sum(j['status'] in ('unsupported_request_budget','unsupported_request_budget_cases') for j in jobs),'remaining_jobs':sum(j['status'] not in ('complete','omitted_by_owner_scope','unsupported_resource','unsupported_request_budget','unsupported_request_budget_cases') for j in jobs),'scope_amendments':plan.get('scope_amendments',[]),'required_extension':plan.get('required_extension'),'extension_planned_jobs':len(json.loads((ROOT/plan['required_extension']).read_text())['jobs']) if plan.get('required_extension') else 0,'cancelled_extension':plan.get('cancelled_extension'),'models':models,'jobs':jobs,'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}

def write(plan_path='config/unified-campaign.json',state_path='work/unified-campaign.json',output='results/unified-overnight-20261002'):
    r=collect(plan_path,state_path);out=ROOT/output;out.mkdir(exist_ok=True);(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
    lines=['# Unified all-configuration benchmark — interim report','',f"Coverage: **{r['completed_jobs']}/{r['planned_jobs']} cells completed**. Status: {r['status']}. No overall deadline. A completed task attempt may still be unsuccessful.",'','[Frozen protocol and research sources](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md). Historical measurements and the initial residency investigation are separate; no unsupported cell may be silently treated as completed.','','| Configuration | Cells | 200K decode median | 200K repetitions | Eight-turn repair | Twenty-turn repair | HumanEval |','|---|---:|---:|---:|---:|---:|---:|']
    lines[3] += f" Owner scope omissions: {r['omitted_jobs']}; remaining baseline groups: {r['remaining_jobs']}. Omissions are not passes. Required extension: {r['extension_planned_jobs']} separately declared groups awaiting verification/qualification." if r.get('required_extension') else ''
    if r.get('resource_limited_jobs'):lines[3] += f" Resource-limited attempted groups: {r['resource_limited_jobs']}; deferred for resource review: {r['deferred_jobs']}. Neither is scored as a pass; deferred groups remain required."
    if r.get('budget_limited_jobs'):lines[3] += f" Audited request-budget-limited attempted groups: {r['budget_limited_jobs']}, unscored; original failed records preserved."
    if r.get('cancelled_extension'):lines[3] += ' The 156-group four-model extension was cancelled by owner scope; none is counted as passed.'
    for m in r['models']:
        speed=m['speed']['200000']['decode'];q=m['quality']['humaneval'];rate=f"{speed['median']:.3f} tok/s" if speed['n'] else 'Pending'
        lines.append(f"| {m['name']} | {m['completed_jobs']}/{m['planned_jobs']} | {rate} | {speed['n']}/5 | {m['repo']['8']['passed']}/{m['repo']['8']['completed']} completed | {m['repo']['20']['passed']}/{m['repo']['20']['completed']} completed | {q['passed']}/{q['completed']} scored of 164 |")
    lines += ['', '## Sustained 200K input / 2048 output', '']
    for m in r['models']:
        t=m['sustained'];rate=t['decode']['median']
        if t['completed']:lines.append(f"- {m['name']}: {t['completed']}/3 repeats; median decode {rate:.5f} tok/s; actual inputs {t['actual_input_tokens']}; actual outputs {t['actual_output_tokens']}.")
    lines += ['', '## Serving load — completed measured profiles', '', '| Configuration | Concurrency | Requests | Output tokens | Measured seconds | Aggregate output tok/s | Median latency s | P95 latency s |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    def display(value):return f'{value:.3f}' if isinstance(value,(int,float)) else '—'
    for m in r['models']:
        for c,t in m['serving'].items():
            if t['status']=='complete':lines.append(f"| {m['name']} | {c} | {t['completed_requests']} | {t['total_output_tokens']} | {display(t['wall_s'])} | {display(t['aggregate_output_tok_s'])} | {display(t['latency_median_s'])} | {display(t['latency_p95_s'])} |")
    lines += ['', 'Two warmups per profile are excluded from measured metrics. Concurrency changes both aggregate throughput and individual latency; results describe each pinned serving runtime. Exact request/output/cache counts are preserved in raw artifacts.', '']
    lines+=['','Different models/precisions/runtimes on one M5. No matched M3 hardware speedup is established. Scores are benchmark-specific; public tasks may be contaminated. Replays measure serving, not task solving. Full model/runtime/source hashes, prompts and raw outcomes remain in each run directory.','']
    for amendment in r['amendments']:
        lines += [f"{amendment.get('label','Preserved setup failure')}: `{amendment['preserved_failed_run']}`. Separately labeled replacement: `{amendment['replacement_run']}`. [Review and unchanged measurement limits](../../{amendment['review']}).",'']
    (out/'README.md').write_text('\n'.join(lines))

if __name__=='__main__':write()
