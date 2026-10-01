#!/usr/bin/env python3
"""Render the actual single-run 200K measurements as a shareable static figure."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
ids=['qwen','gemma','deepseek'];names=['Qwen 3.8 27B','Gemma 4 31B','DeepSeek V4 Flash'];colors=['#84e4c6','#86abfa','#f0c781']
rows=[json.loads((ROOT/f'results/m5-{x}-200k-20261001/result.json').read_text()) for x in ids]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'text.color':'#e9f0f7','axes.labelcolor':'#a4b5c8','xtick.color':'#a4b5c8','ytick.color':'#e9f0f7','axes.edgecolor':'#2b3b4d','axes.facecolor':'#101923','figure.facecolor':'#0c1118'})
fig,axes=plt.subplots(1,2,figsize=(15,7.8),gridspec_kw={'width_ratios':[1.15,1]});fig.subplots_adjust(left=.19,right=.95,top=.69,bottom=.24,wspace=.35)
fig.text(.045,.93,'ASHEN BENCHMARK  /  M5 ULTRA · 256 GB · 80 GPU CORES',color='#84e4c6',fontsize=12,weight='bold')
fig.text(.045,.845,'200,000 tokens in. What happens next?',fontsize=29,weight='bold')
fig.text(.045,.78,'Actual input tokens · Empty context cache · 256 generated tokens · One run per model',fontsize=13,color='#a4b5c8')
for ax,values,title,unit,maxx in [(axes[0],[r['context_fill_s'] for r in rows],'Time to fill the context','seconds · shorter is better',370),(axes[1],[r['decode_tok_s'] for r in rows],'Generation after the fill','tokens / second · higher is better',46)]:
 ax.barh(range(3),values,color=colors,height=.5);ax.invert_yaxis();ax.set_xlim(0,maxx);ax.set_yticks(range(3),names if ax is axes[0] else ['']*3);ax.set_title(title,loc='left',pad=22,fontsize=17,color='#e9f0f7');ax.set_xlabel(unit,labelpad=13,fontsize=12);ax.grid(axis='x',alpha=.12);ax.set_axisbelow(True)
 for i,v in enumerate(values):ax.text(v+maxx*.02,i,f'{v:.1f}',va='center',weight='bold',fontsize=17)
 for spine in ax.spines.values():spine.set_visible(False)
 ax.tick_params(length=0)
fig.text(.045,.135,'All three completed with zero swap growth.',fontsize=16,weight='bold')
fig.text(.045,.084,'Pinned 8-bit MLX (Qwen/Gemma); mixed Q4 DwarfStar (DeepSeek). Input tokenizers and timing counters differ.\nCold = empty KV/state cache; model load and tokenization excluded. Throughput stress test, not a quality score.\nThe original M3 is busy with other sessions. No matched hardware speedup is claimed.',fontsize=10.3,color='#a4b5c8',va='top',linespacing=1.6)
(ROOT/'outputs').mkdir(exist_ok=True);fig.savefig(ROOT/'outputs/200k-context-results.png',dpi=150);fig.savefig(ROOT/'outputs/200k-context-results.svg');plt.close(fig)
