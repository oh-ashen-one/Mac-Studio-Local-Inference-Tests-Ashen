#!/usr/bin/env python3
"""Audit/export the complete 120-run speed phase without importing an inference runtime.

JSON/Markdown: python3 scripts/report_unified_speed.py
Figures: use an isolated environment with config/requirements-plotting.lock and --figures.
"""
from publication_labels import public_spec
import argparse
import datetime
import hashlib
import json
import os
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'results/unified-speed-summary-20261002'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stats(values):
    return dict(n=len(values), median=statistics.median(values),
                mean=statistics.mean(values), stdev=statistics.stdev(values),
                min=min(values), max=max(values))


def collect():
    plan_path = ROOT / 'config/unified-campaign.json'
    plan = json.loads(plan_path.read_text())
    lock_path = ROOT / plan['model_lock']
    specs = json.loads(lock_path.read_text())['models']
    jobs = [j for j in plan['jobs'] if j['kind'] == 'speed' and j['output_tokens'] == 256]
    if len(jobs) != 120 or len({j['id'] for j in jobs}) != 120:
        raise ValueError('The complete predeclared speed phase must contain 120 unique runs')
    records, manifest, runtime_identities = {}, [], {}
    for job in jobs:
        folder = ROOT / 'results' / job['id']
        path = folder / 'result.json'
        result = json.loads(path.read_text())
        if (result.get('status'), result.get('campaign_id'), result.get('model_id'),
            result.get('input_tokens'), result.get('output_tokens'), result.get('condition')) != (
                'complete', plan['id'], job['model_id'], job['tokens'], 256, 'alone'):
            raise ValueError('Missing, failed or mismatched speed cell: ' + job['id'])
        if result['model_lock_sha256'] != digest(lock_path):
            raise ValueError('Model lock mismatch: ' + job['id'])
        publication = json.loads((folder / 'publication.json').read_text())
        if publication['files']['result.json']['published_sha256'] != digest(path):
            raise ValueError('Published result changed after its receipt: ' + job['id'])
        server_config = json.loads((folder/'server-config.json').read_text()) if (folder/'server-config.json').exists() else {}
        fingerprint = (result.get('runtime_lock_sha256') or server_config.get('runtime_lock_sha256'),
                       result.get('native_binary_sha256') or server_config.get('native_binary_sha256'),
                       result.get('native_commit') or result.get('runtime_commit'),
                       result.get('wired_limit_bytes'), result.get('corpus_sha256'))
        runtime_identities.setdefault(job['model_id'], set()).add(fingerprint)
        telemetry = json.loads((folder / 'campaign-telemetry.json').read_text())
        records[job['id']] = (result, telemetry)
        manifest.append(dict(run_id=job['id'], model_id=job['model_id'], input_tokens=job['tokens'],
                             output_tokens=256, repeat=job['repeat'],
                             result_file=str(path.relative_to(ROOT)), result_sha256=digest(path),
                             telemetry_sha256=digest(folder / 'campaign-telemetry.json'),
                             publication_receipt_sha256=digest(folder / 'publication.json')))
    configurations = []
    for spec in specs:
        spec = public_spec(spec)
        if len(runtime_identities[spec['id']]) != 1:
            raise ValueError('Mixed runtime/binary/residency/corpus identities: ' + spec['id'])
        model = dict(id=spec['id'], name=spec['display_name'], runtime=spec['runtime'],
                     quantization=spec['quantization'], contexts={},
                     runtime_identity=dict(zip(['runtime_lock_sha256', 'native_binary_sha256',
                                               'native_source_commit', 'wired_limit_bytes', 'corpus_sha256'],
                                              next(iter(runtime_identities[spec['id']])))))
        for length in plan['context_lengths']:
            own = [j for j in jobs if j['model_id'] == spec['id'] and j['tokens'] == length]
            if sorted(j['repeat'] for j in own) != [1, 2, 3, 4, 5]:
                raise ValueError('Each configuration/length requires exactly five repetitions')
            runs = [records[j['id']][0] for j in own]
            traces = [records[j['id']][1] for j in own]
            ids = {x.get('input_token_ids_sha256') for x in runs} - {None}
            if len(ids) > 1:
                raise ValueError('Input token identities differ within a repeated group')
            context = dict(run_ids=[j['id'] for j in own],
                           decode_tok_s=stats([x['decode_tok_s'] for x in runs]),
                           context_fill_s=stats([x['context_fill_s'] for x in runs]),
                           prefill_tok_s=stats([x['prefill_tok_s'] for x in runs]),
                           whole_job_min_available_bytes=min(x['available_bytes'] for t in traces for x in t),
                           whole_job_max_swap_growth_bytes=max(max(x['swap_bytes'] for x in t)-t[0]['swap_bytes'] for t in traces),
                           input_token_ids_sha256=next(iter(ids), None))
            if all('peak_metal_bytes' in x for x in runs):
                context['peak_mlx_allocation_bytes'] = max(x['peak_metal_bytes'] for x in runs)
            if all('swap_increase_bytes' in x for x in runs):
                context['max_positive_timed_swap_change_bytes'] = max(0, max(x['swap_increase_bytes'] for x in runs))
            model['contexts'][str(length)] = context
        configurations.append(model)
    return dict(campaign_id=plan['id'], phase='standard-context-speed', status='complete',
                overall_study_status='in_progress', measured_runs=120, output_tokens_per_run=256,
                context_lengths=plan['context_lengths'], model_lock_sha256=digest(lock_path),
                plan_sha256=digest(plan_path), configurations=configurations, run_manifest=manifest,
                exclusions='Historical profiles, the residency setup probe, and sustained 2048-output cells are not included.',
                memory_scope='Available memory and swap are system-wide samples over the whole child including verification/load; not process attribution. MLX allocation is a separate metric and is not substituted for native process RSS.',
                timing_scope='Model load/tokenization excluded. MLX: direct uncached input to first token. DwarfStar: native prefill counters. llama.cpp: HTTP first output with native counters retained.',
                generated_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())


def markdown(report):
    lines = ['# M5 context-speed phase — 120 measured runs', '',
             '**Speed phase complete; the overall 234-group study remains in progress.** Six configurations, four input lengths, five fresh-process repetitions each, 256 output tokens per run. All 120 results passed exact-count, cohort and publication-receipt checks.', '',
             '[Frozen protocol](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md) · [Full-study progress](../unified-overnight-20261002/README.md) · [Research notes](../../docs/UNIFIED-RUN-NOTES.md) · [Statistics and 120-run manifest](summary.json)', '',
             '![Measured context scaling](../../outputs/unified-speed-phase.png)', '',
             '[Editable SVG figure](../../outputs/unified-speed-phase.svg) · [Figure provenance](figure-provenance.json)', '',
             '## Median generation rate (tokens/second)', '',
             '| Configuration | 8192 input | 32768 input | 131072 input | 200000 input |',
             '|---|---:|---:|---:|---:|']
    for m in report['configurations']:
        lines.append('| '+m['name']+' | '+' | '.join(f"{m['contexts'][str(n)]['decode_tok_s']['median']:.2f}" for n in report['context_lengths'])+' |')
    lines += ['', '## Median context-fill time (seconds)', '',
              '| Configuration | 8192 input | 32768 input | 131072 input | 200000 input |',
              '|---|---:|---:|---:|---:|']
    for m in report['configurations']:
        lines.append('| '+m['name']+' | '+' | '.join(f"{m['contexts'][str(n)]['context_fill_s']['median']:.3f}" for n in report['context_lengths'])+' |')
    lines += ['', 'Every table cell is n=5. JSON retains mean, sample standard deviation, minimum, maximum and each run reference; no outlier was dropped. The plotted whiskers are observed ranges, not confidence intervals.', '',
              '## Memory observations at 200000 input', '',
              '| Configuration | Minimum system memory available, GiB | Maximum whole-job swap growth, MiB | Peak MLX allocation, GiB |',
              '|---|---:|---:|---:|']
    for m in report['configurations']:
        c = m['contexts']['200000']
        peak = f"{c['peak_mlx_allocation_bytes']/2**30:.2f}" if 'peak_mlx_allocation_bytes' in c else 'Not an MLX metric'
        lines.append(f"| {m['name']} | {c['whole_job_min_available_bytes']/2**30:.2f} | {c['whole_job_max_swap_growth_bytes']/2**20:.4f} | {peak} |")
    lines += ['', report['memory_scope'], '',
              'MiMo has zero positive timed-inference swap change in these groups but small whole-job system-swap increases. Loading and timed inference must not be described interchangeably. Available memory is an observed minimum, not a promise that any second application will fit.', '',
              '## Interpretation and reproducibility', '', report['timing_scope'], '',
              'These are coupled model/precision/runtime configurations on one verified M5 Ultra. Tokenizers differ across model families; the two Qwen 3.8 configurations have identical input token IDs at each length. The original M3 remains unmeasured. Published external configurations are not substituted for a controlled paired test.', '',
              'Speed is not intelligence, task completion or an absolute hardware ceiling. Repository repetitions, longer repair budgets, full recorded replay, HumanEval, retrieval, sustained generation and serving-load coverage remain separate and unfinished. Replays measure serving, not tasks solved.', '',
              'Historical unwired MiMo measurements and the residency setup probe are excluded. Original failed setups and unsuccessful task attempts remain preserved in the full-study evidence. No model upgrade, quantization swap, silent context shortening, retry or outlier removal was used to complete this speed phase.', '',
              'Regenerate JSON/Markdown with `python3 scripts/report_unified_speed.py`. For PNG/SVG, install `config/requirements-plotting.lock` into an isolated plotting environment and add `--figures`; the script uses the CPU-only Agg backend and never imports or starts an inference runtime.', '']
    return '\n'.join(lines)


def figures(report):
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'work/plot-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 2, figsize=(14, 7.6))
    fig.subplots_adjust(left=.07, right=.98, top=.80, bottom=.35, wspace=.22)
    colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#B17F00', '#56A8C4']
    markers = ['o', 's', '^', 'D', 'v', 'P']
    for m, color, marker in zip(report['configurations'], colors, markers):
        x = [n/1000 for n in report['context_lengths']]
        for ax, key in zip(axes, ['decode_tok_s', 'context_fill_s']):
            values = [m['contexts'][str(n)][key] for n in report['context_lengths']]
            med = [v['median'] for v in values]
            error = [[v['median']-v['min'] for v in values], [v['max']-v['median'] for v in values]]
            ax.errorbar(x, med, yerr=error, label=(m['name'].replace(' · 4-bit MLX (affine; 8-bit gates)', '\n4-bit affine MLX; 8-bit gates')+' ('+m['runtime']+')'),
                        color=color, marker=marker, linewidth=1.8, markersize=5,
                        capsize=3, elinewidth=1, alpha=.95)
    for ax, title, ylabel in zip(axes, ['Generation after context fill', 'Uncached context fill'],
                                 ['Output tokens / second — higher is faster', 'Seconds — lower is less waiting']):
        ax.set_title(title, loc='left', fontsize=13, fontweight='bold', pad=14)
        ax.set_ylabel(ylabel, labelpad=9)
        ax.set_xlabel('Input context', labelpad=9)
        ax.set_xticks([8.192, 32.768, 131.072, 200], ['8K', '32K', '128K', '200K'])
        ax.set_xlim(0, 205); ax.set_ylim(bottom=0)
        ax.grid(axis='y', alpha=.22); ax.set_axisbelow(True)
        for side in ['top', 'right']: ax.spines[side].set_visible(False)
    fig.suptitle('ASHEN  /  M5 Ultra context-speed study', x=.07, y=.96, ha='left', fontsize=20, fontweight='bold')
    fig.text(.07, .90, '120 measured runs · six configurations · five repetitions at each context · 256 generated tokens per run', fontsize=11)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.515, .26), ncol=3, fontsize=8.5, frameon=False, columnspacing=2.5)
    fig.text(.07, .145, 'Points/lines: medians. Whiskers: observed minimum–maximum, not confidence intervals.', fontsize=9)
    fig.text(.07, .11, 'Exact inputs: 8,192 / 32,768 / 131,072 / 200,000 tokens. Model load and tokenization excluded; timing boundaries differ by runtime.', fontsize=8.5)
    fig.text(.07, .075, 'Same M5; different models, precisions and runtimes. No matched M3 measurement or general quality ranking is implied.', fontsize=8.5)
    fig.text(.07, .035, 'SPEED PHASE COMPLETE · The remaining task, quality, sustained-output and serving-load study is still running.', fontsize=9, fontweight='bold', color='#9C3D22')
    for extension in ['png', 'svg']:
        fig.savefig(ROOT / 'outputs' / ('unified-speed-phase.'+extension), dpi=180, facecolor='white')
    svg_path = ROOT / 'outputs/unified-speed-phase.svg'
    svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
    plt.close(fig)
    provenance = dict(matplotlib_version=matplotlib.__version__, backend='Agg (CPU only)',
                      plotting_lock_sha256=digest(ROOT/'config/requirements-plotting.lock'),
                      statistics_sha256=digest(DEST/'summary.json'), script_sha256=digest(Path(__file__)),
                      phase='Only the complete 120-run standard speed matrix; all other study phases are excluded')
    (DEST/'figure-provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--figures', action='store_true')
    args = parser.parse_args()
    report = collect(); DEST.mkdir(exist_ok=True)
    (DEST/'summary.json').write_text(json.dumps(report, indent=2)+'\n')
    (DEST/'README.md').write_text(markdown(report))
    if args.figures: figures(report)
    print('Audited and exported 120/120 standard speed runs; full study remains in progress')


if __name__ == '__main__':
    main()
