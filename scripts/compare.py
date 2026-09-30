#!/usr/bin/env python3
"""Compare matched fixed-token records; reject incompatible or duplicate runs."""
import argparse
import csv
import json
import random
import statistics
import sys
from pathlib import Path


def records(path):
    result={}
    for line in path.read_text().splitlines():
        row=json.loads(line)
        if row.get('kind')!='hardware_microbenchmark' or row.get('cell',{}).get('warmup'):
            continue
        key=(row['model_id'],row['cell']['id'],row['session'],row['cell']['repeat'])
        if key in result:raise ValueError('Duplicate measured record: '+str(key))
        result[key]=row
    return result


def compatible(a,b):
    for field in ['model_revision','model_lock_sha256','runtime_lock_sha256','campaign_sha256','runtime_versions','runtime_commit','compiler','os_build','settings','input_token_ids_sha256','source_prompt_sha256','input_tokens','output_tokens']:
        if a.get(field)!=b.get(field):raise ValueError('Cannot compare mismatched '+field)
    if a.get('harness_source_sha256')!=b.get('harness_source_sha256') or a.get('harness_sha256')!=b.get('harness_sha256'):
        raise ValueError('Cannot compare different harness source')


def interval(ratios):
    rng=random.Random(1729)
    samples=sorted(statistics.median(rng.choices(ratios,k=len(ratios))) for _ in range(10000))
    return samples[249],samples[9749]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old',type=Path);parser.add_argument('new',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    old,new=records(args.old),records(args.new)
    groups={};excluded=[]
    for key in sorted(old.keys()|new.keys()):
        a,b=old.get(key),new.get(key)
        if not a or not b or a.get('status')!='ok' or b.get('status')!='ok':
            excluded.append({'key':key,'reason':'missing or failed pair'});continue
        compatible(a,b)
        if a['machine_id']!='studio-old' or b['machine_id']!='studio-new':raise ValueError('Wrong machine labels')
        for metric,invert in [('decode_tok_s',False),('prefill_tok_s',False),('ttft_s',True)]:
            x,y=a.get(metric),b.get(metric)
            if x and y:
                groups.setdefault((key[0],key[1],metric),[]).append((x,y,x/y if invert else y/x))
    rows=[]
    for (model,cell,metric),values in sorted(groups.items()):
        ratios=[v[2] for v in values];lo,hi=interval(ratios)
        rows.append({'model':model,'cell':cell,'metric':metric,'matched_pairs':len(values),
                     'old_median':statistics.median(v[0] for v in values),'new_median':statistics.median(v[1] for v in values),
                     'median_paired_speedup':statistics.median(ratios),'bootstrap_95_low':lo,'bootstrap_95_high':hi})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    report={'method':'Paired median ratios; deterministic 10000-resample bootstrap. One pair per prompt, grouped by model/cell. Not a quality score.',
            'rows':rows,'excluded_pairs':excluded}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    if rows:
        with args.output.with_suffix('.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    elif args.output.with_suffix('.csv').exists():
        args.output.with_suffix('.csv').unlink()
    print('Matched comparison groups:',len(rows),'Excluded pairs:',len(excluded))
    if not rows:raise SystemExit('No comparable measured rows; smoke checks are intentionally excluded.')


if __name__=='__main__':main()
