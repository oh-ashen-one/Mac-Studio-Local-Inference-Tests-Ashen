#!/usr/bin/env python3
"""Bind the image-generated infographics to frozen evidence and package the release.

This script copies no tensors, imports no inference libraries, and edits no pixels.
Images are generated with the built-in image tool; labels/scales were reviewed.
"""
import hashlib
import json
import struct
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'viewer/assets'
REPO='https://github.com/oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen'
BRANCH=REPO+'/blob/codex/long-context-dashboard-20261001/'
MODEL_IDS=['qwen-27b','gemma-31b','deepseek-v4-flash','mimo-v2.6-flash-mopd','mistral-medium35-q4']


def build_data():
    source=ROOT/'results/research-report-20261004/source-summaries.json'
    frozen=json.loads(source.read_text())
    models=[m for cohort in frozen.values() for m in cohort['models'] if m['id'] in MODEL_IDS]
    assert len(models)==5 and len({m['id'] for m in models})==5
    by_id={m['id']:m for m in models};q=by_id['qwen-27b']
    refs={r['id']:r for r in json.loads((ROOT/'research/external-benchmarks.json').read_text())['rows']}
    pairs=[]
    for context,ident,url in [(200000,'m3-256-60-200k',None),(131072,'m3-256-8bit-128k','https://omlx.ai/benchmarks/performance/ymgck04x')]:
        stat=q['speed'][str(context)]['decode'];ref=dict(refs[ident])
        if url:ref['url']=url
        assert stat['n']==5 and ref['context_tokens']==context and ref['concurrency']==1
        pairs.append({'context':context,'ours':stat,'reference':ref,'reported_rate_increase_percent':(stat['median']/ref['decode_tps']-1)*100})
    assert round(pairs[0]['reported_rate_increase_percent'],1)==55.3
    assert round(pairs[1]['reported_rate_increase_percent'],1)==42.1
    specs=[
        ('200k','M3 · 200K','M5 versus M3 at 200K','+55.3% reported generation rate. Qwen 3.8 27B, 8-bit, 200,000 input tokens. M5 median of five; published M3 60-GPU reference. Different runtime and corpus.',['https://omlx.ai/benchmarks/performance/h35d8wcq']),
        ('128k','M3 · 128K','80 GPU cores, two generations','+42.1% reported generation rate. Both configurations have 80 GPU cores. Qwen 3.8 27B, 8-bit, 131,072 input tokens; software and corpus differ.',['https://omlx.ai/benchmarks/performance/ymgck04x']),
        ('market','GPU field','How the M5 compares with other setups','M5, optimized M3, DGX Spark and RTX 5090 snapshots. Prompt lengths, precision, acceleration and timers differ; these are configuration reports.',['https://omlx.ai/benchmarks/performance/msy3uto1',refs['spark-fp8-code']['url'],refs['rtx5090-q4-short']['url']]),
        ('models','Our models','200K tokens, five models','Native generation after 200,000 input tokens. Five-run medians, 256 output tokens; different model sizes, precision and runtimes.',[]),
        ('wait','Input wait','Reading 200K tokens','M5 context-fill timer versus published M3 time to first token. Different timing boundaries; no faster percentage inferred.',['https://omlx.ai/benchmarks/performance/h35d8wcq']),
    ]
    cards=[]
    for name,label,title,alt,sources in specs:
        file=DEST/('infographic-'+name+'.png');raw=file.read_bytes()
        width,height=struct.unpack('>II',raw[16:24]);assert raw.startswith(b'\x89PNG') and width>=1500 and abs(width/height-16/9)<.025
        cards.append({'id':name,'label':label,'title':title,'alt':alt,'png':'/assets/infographic-'+name+'.png','width':width,'height':height,'sha256':hashlib.sha256(raw).hexdigest(),'brands':(['mimo','deepseek','qwen','gemma','mistral'] if name=='models' else ['apple','nvidia','qwen'] if name=='market' else ['apple','qwen']),'sources':sources,'evidence':BRANCH+'docs/M5-RESEARCH-REPORT-20261004.md'})
    return {'schema':2,'renderer':'Built-in image generation; exact visible values reviewed against source records','scope':{'completed':183,'unscored':11,'owner_omitted':1,'required_remaining':0},'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pairs':pairs,'models':models,'cards':cards,'market_values':{'m5_8k_native_decode':q['speed']['8192']['decode']['median'],'optimized_m3_200k_reported':refs['m3-512-optimized-200k']['decode_tps'],'dgx_spark_short_serving':refs['spark-fp8-code']['decode_tps'],'rtx5090_8k_mtp3_reported':98.2}}


def main():
    data=build_data();(DEST/'showcase-data.json').write_text(json.dumps(data,indent=2)+'\n')
    manifest={'source_summaries_sha256':data['source_sha256'],'renderer':data['renderer'],'prompt_set':'outputs/benchmark-infographic-prompts.md','source_review':'research/showcase-source-review-20261004.json','graphics':{c['id']:{'png':c['sha256'],'width':c['width'],'height':c['height'],'visible_labels_reviewed':True,'common_zero_origin_and_proportions_reviewed':c['id']!='wait'} for c in data['cards']}}
    (ROOT/'outputs/visual-showcase-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(DEST/'benchmark-image-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
        for c in data['cards']:z.write(DEST/Path(c['png']).name,Path(c['png']).name)
        z.writestr('README.txt','ASHEN / BENCHMARK LAB\nFive image-generated benchmark results infographics.\n'+BRANCH+'docs/M5-RESEARCH-REPORT-20261004.md\n'+BRANCH+'outputs/benchmark-infographic-prompts.md\nValues and chart proportions were reviewed against frozen measurements and primary references. External configurations differ; no isolated hardware-only speedup is claimed.\n')
    print(json.dumps({'infographics':len(data['cards']),'primary_rate_increase_percent':data['pairs'][0]['reported_rate_increase_percent']}))


if __name__=='__main__':main()
