#!/usr/bin/env python3
"""Summarize only saved additional-cohort evidence; never imports a model runtime."""
import datetime,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    lock=json.loads((ROOT/'config/additional-models.lock.json').read_text());records=[]
    for path in (ROOT/'results').glob('*/result.json'):
        r=json.loads(path.read_text())
        if r.get('campaign_id') or path.parent.name.startswith('u20261002-'):continue
        r['evidence']=str(path.relative_to(ROOT));records.append(r)
    replays=[]
    for path in (ROOT/'results').glob('*aa*/run.json'):
        r=json.loads(path.read_text())
        if r.get('campaign_id') or path.parent.name.startswith('u20261002-'):continue
        if not r.get('model_id'):continue
        summary=path.parent/'raw/summary.json'
        if summary.exists():
            saved=json.loads(summary.read_text())
            r['serving_summary']={k:saved.get(k) for k in ['success','totals','measured_duration_ms','end_to_end_output_tokens_per_second']}
            r['context_evidence']=saved.get('config',{}).get('context')
        r['evidence']=str(path.relative_to(ROOT));replays.append(r)
    report={'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'models':[],'hardware_comparison':'No original M3 inference; no matched chip-only percentage.','speed_definition':'Median of complete 200K-input, 256-output, empty-KV-cache text runs; model load/tokenization excluded. Swap column covers timed prefill/decode only; whole-job loading observations are reported separately when available.','original_cohort':'Unchanged; original three speed cells remain n=1.'}
    report['retrospective_profile_note']='Historical direct MLX speed profile omitted normal process memory wiring. MiMo 0.30-0.41 tok/s describes that unwired harness, not normal resident inference. A separate recommended-residency setup probe reached 37.5743 tok/s with identical input/output token IDs; the unified repeated study is separate. Original repository/replay outcomes are unchanged.'
    matrix=ROOT/'results/m5-additional-summary-20261001/campaign.json'
    if matrix.exists():report['campaign']=json.loads(matrix.read_text())
    lines=['# Additional M5 model results','',report['speed_definition'],'',report['hardware_comparison'],'','| Configuration | 200K samples | Fill median | Prefill median | Decode median (range) | Peak MLX | Swap growth |','|---|---:|---:|---:|---:|---:|---:|']
    if report.get('campaign',{}).get('status')=='complete':lines[2:2]=['**Identified additional cohort complete.** All 22 tracked cells are handled, including the preserved failed MiMo qualification and its unrun unsupported original full profile. Complete means accounted for, not every task passed. The final completion check found no task-owned inference processes; see the saved completion receipt.','']
    lines[2:2]=['**Archived phase; the six-configuration unified campaign is still active.** '+report['retrospective_profile_note']+' [Current protocol](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md) · [Current coverage](../unified-overnight-20261002/README.md).','']
    detail=[]
    for m in lock['models']:
        own=[r for r in records if r.get('model_id')==m['id']]
        runs=[r for r in own if r.get('kind')=='long_context' and r.get('status')=='complete' and r.get('input_tokens')==200000 and r.get('output_tokens')==256]
        identities={(r['model_lock_sha256'],r['runtime_lock_sha256'],r['input_token_ids_sha256']) for r in runs}
        if len(identities)>1:raise ValueError('Different configurations must not be aggregated: '+m['id'])
        trials=[r for r in own if r.get('kind')=='repo_task' and r.get('status') in ('complete','failed')]
        measured=[r for r in trials if r.get('status')=='complete']
        summary={'model_id':m['id'],'revision':m['revision'],'quantization':m['quantization'],'sample_count':len(runs),'planned_speed_samples':3,'planned_repo_attempts':5,'completed_repo_attempts':len(measured),'repo_passed':sum(r.get('passed',False) for r in measured),'repo_infrastructure_failures':sum(r.get('status')=='failed' for r in trials),'human_rescues':sum(r.get('human_rescues',0) for r in trials),'evidence':[r['evidence'] for r in own]}
        summary['repo_median_wall_s']=statistics.median(r['wall_s'] for r in measured) if measured else None
        summary['replays']=[r for r in replays if r['model_id']==m['id']]
        summary['whole_job_swap_observations']=[]
        for r in runs:
            path=(ROOT/r['evidence']).parent/'campaign-telemetry.json'
            if path.exists():
                telemetry=json.loads(path.read_text())
                if telemetry:summary['whole_job_swap_observations'].append({'run':Path(r['evidence']).parent.name,'system_swap_growth_bytes':max(x['swap_bytes'] for x in telemetry)-telemetry[0]['swap_bytes'],'scope':'Whole job including loading; system-wide, not process attribution'})
        if runs:
            for k in ['context_fill_s','prefill_tok_s','decode_tok_s']:summary[k+'_median']=statistics.median(r[k] for r in runs)
            summary['decode_range']=[min(r['decode_tok_s'] for r in runs),max(r['decode_tok_s'] for r in runs)]
            summary['peak_metal_gib']=max(r['peak_metal_bytes'] for r in runs)/2**30;summary['max_swap_growth_bytes']=max(r['swap_increase_bytes'] for r in runs)
            lo,hi=summary['decode_range'];lines.append(f"| {m['display_name']} · {m['quantization']} | {len(runs)}/3 | {summary['context_fill_s_median']:.2f} s | {summary['prefill_tok_s_median']:.2f} tok/s | **{summary['decode_tok_s_median']:.2f}** ({lo:.2f}–{hi:.2f}) | {summary['peak_metal_gib']:.2f} GiB | {summary['max_swap_growth_bytes']} bytes |")
        else:lines.append(f"| {m['display_name']} · {m['quantization']} | 0/3 | Pending | Pending | Pending | Pending | Pending |")
        report['models'].append(summary)
        detail+=['',f"## {m['display_name']}",'',f"Repository diagnostic: **{summary['repo_passed']}/{len(measured)} completed attempts passed**, of five planned. Infrastructure failures: {summary['repo_infrastructure_failures']}; human rescues: {summary['human_rescues']}. Same historical Django bug, 19 immutable tests, 200K starting context, eight turns, 2048 output tokens per turn, temperature 0.2, seeds 1001–1005. This is a narrow diagnostic, not a general intelligence score.",'','Saved evidence:','']
        for r in sorted(own,key=lambda r:r['evidence']):
            outcome='passed' if r.get('passed') else ('did not pass' if 'passed' in r else r.get('status'))
            detail.append(f"- [{r['evidence'].split('/')[1]}](../../{r['evidence']}) — {r.get('kind')}, {r.get('status')}, {outcome}.")
        if summary['whole_job_swap_observations']:
            detail+=['','Whole-job system swap observations (including loading; distinct from timed-phase swap above):','']
            for row in summary['whole_job_swap_observations']:
                detail.append(f"- {row['run']}: {row['system_swap_growth_bytes']:,} bytes increase. System-wide observation, not process attribution.")
        if summary['replays']:
            detail+=['','Replay cells (serving only, not tasks solved):','']
            for r in summary['replays']:
                totals=r.get('serving_summary',{}).get('totals',{})
                context=r.get('context_evidence') or {}
                detail.append(f"- [{r['replay']}](../../{r['evidence']}) — {r['status']}; {totals.get('successful_turns',0)}/{totals.get('turns',0)} turns served; {totals.get('short_output_warnings',0)} short-output warnings; output policy {r.get('output_token_policy')}. Context evidence: {context.get('observed_reason','not recorded')}, observed limit {context.get('observed_tokens')}. Not directly comparable to the original managed exact-output cohort.")
    lines+=detail+['','## Runtime and interpretation','', 'Qwen’s initial MLX-LM loader produced gibberish. The separately pinned MLX-VLM loader passed. MiMo initially rejected optional MTP tensors; the adapter excludes precisely 42 draft tensors while retaining strict checks for every base weight. Its base-model validation answered correctly but fenced its JSON, so strict formatting failed. Those original records remain intact. No model files were edited; MTP speculation is disabled.','', 'Official AA attached-server replays use recorded output caps because this MLX server does not implement ignore_eos. The exact-output cell is unsupported, and recorded-policy results are not directly comparable to the original Q4_K_M managed replay. Serving completed turns does not mean solving tasks.','', 'The original three model configurations and their results remain separate. Darkbloom’s provider is off. The original M3 remains occupied. Results are for local/GitHub review; no website deployment has occurred.','']
    out=ROOT/'results/m5-additional-summary-20261001';out.mkdir(exist_ok=True)
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');(out/'README.md').write_text('\n'.join(lines))

if __name__=='__main__':main()
