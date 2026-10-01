#!/usr/bin/env python3
"""Render an initial-test Markdown report from recorded summary data."""
import argparse,json
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);a=p.parse_args()
    s=json.loads((a.directory/'summary.json').read_text())
    names={'qwen-27b':'Qwen 3.8 27B · MLX 8-bit','gemma-31b':'Gemma 4 31B · MLX 8-bit','deepseek-v4-flash':'DeepSeek V4 Flash 0731 · DwarfStar mixed Q4'}
    lines=['# Initial M5 Ultra local inference test — October 1, 2026','',
           '**Completed on the M5 Ultra only. No M3 speedup or intelligence ranking is claimed.**','',
           '| Model | Fastest decode tok/s | Median decode tok/s | First streamed output | Real response time | Input / generated tokens | End-to-end output tok/s | Observed RAM increase |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for key,row in s['models'].items():
        t=row['transaction'];lines.append(f"| {names[key]} | {row['fastest_decode_tok_s']:.2f} | {row['median_decode_tok_s']:.2f} | {t['ttft_stream_s']:.2f} s | {t['response_wall_s']:.2f} s | {t['prompt_tokens']} / {t['completion_tokens']} | {t['end_to_end_output_tok_s']:.2f} | {row['observed_system_memory_delta_bytes']/1024**3:.1f} GiB |")
    lines+=['','## Method','',
        '- Machine: M5 Ultra, 36 CPU cores / 80 GPU cores / 256 GB, macOS 27.0.1 build 26A434.',
        '- Run order: Qwen, Gemma, DeepSeek. Each model completed its speed probes and real request before the next loaded. Models and temporary inference servers were stopped afterward.',
        '- Speed probes: synthetic 512-token input, exactly 256 generated tokens; one excluded warmup, then three measured repeats. Peak and median use only those three measured repeats. Greedy decoding, no speculation or model quantization changes.',
        '- MLX rates use token-level timestamps, excluding the first token from the steady-decode numerator/interval. DwarfStar rates use its native gen_steady_tps counter. Tokenization and engine implementations differ across models; this is throughput, not equivalent semantic work or an intelligence score.',
        '- MLX keeps its model loaded between speed repeats. DwarfStar starts a fresh process for each native probe. Model loading is excluded from both decode-rate figures; weights and shader/filesystem caches are warm after preceding work. These are not cold-boot measurements.',
        '- Real transaction: identical user prompt, greedy decoding, requested thinking disabled, maximum 512 generated tokens, local HTTP streaming on the M5. A new model server was started after each model’s speed probes. No WAN/SSH latency is included in transaction timings.',
        '- TTFT here means client-observed time to the first streamed content/reasoning fragment. Output token counts come from backend usage; chunks are never treated as tokens. End-to-end output rate is generated tokens divided by complete request wall time, including prompt processing.',
        '- The Qwen transaction reached the 512-token cap (finish_reason=length), truncating the end of its explanation. Gemma and DeepSeek stopped normally. All actual outputs are preserved; completion of a request is not a correctness grade.',
        '- Memory is the drop from initial system-available RAM to its lowest sampled value during speed probes. It includes background changes and is not an exact per-model allocation. Samples were taken about once per second. Process RSS is retained separately.',
        '- DwarfStar reported a planned 153.41 GiB allocation for the short probe, including its mapped 153.32 GiB model. Its ordinary process RSS is small because it does not represent these mapped GPU weights; do not report DeepSeek as a sub-GB model.',
        '- Initial MLX /v1/models readiness probes logged a missing empty Hugging Face cache directory before later readiness succeeded. The actual POST transactions completed successfully; the diagnostics are preserved. Future runs create an empty task-local cache before launching the server.',
        '- server_ready_s is HTTP readiness, not a validated cold model-load measurement.',
        '- No swap increase was observed in the probe telemetry. Power/energy were not measured.',
        '- Photos/iCloud work and the live Safari dashboard were present. This is an initial interactive test, not a quiet-system absolute maximum. The task used a shared GPU capture slot and ran one model at a time.',
        '', '## Provenance','',
        f"Driver/worker source at execution: `{s['harness_commit']}`. Exact model revisions and hashes are in `config/models.lock.json`; environment and engine details appear in each speed record. The summary’s memory calculation was derived after the run from the unchanged telemetry records.",
        '', 'Raw records: each model has `*-speed.jsonl`, `*-speed-telemetry.json`, `*-transaction.json`, and execution/server logs. Local checkout paths in published records are replaced with `<repo>`; metrics and model outputs are unchanged. `summary.json` drives the localhost dashboard.',
        '', 'Rebuild this report with:', '', '```sh', f'python3 scripts/report_firstlook.py results/{a.directory.name}', '```','']
    (a.directory/'README.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
