# Initial M5 Ultra local inference test — October 1, 2026

**Completed on the M5 Ultra only. No M3 speedup or intelligence ranking is claimed.**

| Model | Fastest decode tok/s | Median decode tok/s | First streamed output | Real response time | Input / generated tokens | End-to-end output tok/s | Observed RAM increase |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen 3.8 27B · MLX 8-bit | 32.05 | 32.02 | 1.62 s | 18.73 s | 87 / 512 | 27.33 | 28.4 GiB |
| Gemma 4 31B · MLX 8-bit | 27.63 | 27.59 | 1.55 s | 16.97 s | 90 / 412 | 24.28 | 32.0 GiB |
| DeepSeek V4 Flash 0731 · DwarfStar mixed Q4 | 63.83 | 63.71 | 0.67 s | 5.09 s | 78 / 282 | 55.45 | 154.7 GiB |

## Method

- Machine: M5 Ultra, 36 CPU cores / 80 GPU cores / 256 GB, macOS 27.0.1 build 26A434.
- Run order: Qwen, Gemma, DeepSeek. Each model completed its speed probes and real request before the next loaded. Models and temporary inference servers were stopped afterward.
- Speed probes: synthetic 512-token input, exactly 256 generated tokens; one excluded warmup, then three measured repeats. Peak and median use only those three measured repeats. Greedy decoding, no speculation or model quantization changes.
- MLX rates use token-level timestamps, excluding the first token from the steady-decode numerator/interval. DwarfStar rates use its native gen_steady_tps counter. Tokenization and engine implementations differ across models; this is throughput, not equivalent semantic work or an intelligence score.
- MLX keeps its model loaded between speed repeats. DwarfStar starts a fresh process for each native probe. Model loading is excluded from both decode-rate figures; weights and shader/filesystem caches are warm after preceding work. These are not cold-boot measurements.
- Real transaction: identical user prompt, greedy decoding, requested thinking disabled, maximum 512 generated tokens, local HTTP streaming on the M5. A new model server was started after each model’s speed probes. No WAN/SSH latency is included in transaction timings.
- TTFT here means client-observed time to the first streamed content/reasoning fragment. Output token counts come from backend usage; chunks are never treated as tokens. End-to-end output rate is generated tokens divided by complete request wall time, including prompt processing.
- The Qwen transaction reached the 512-token cap (finish_reason=length), truncating the end of its explanation. Gemma and DeepSeek stopped normally. All actual outputs are preserved; completion of a request is not a correctness grade.
- Memory is the drop from initial system-available RAM to its lowest sampled value during speed probes. It includes background changes and is not an exact per-model allocation. Samples were taken about once per second. Process RSS is retained separately.
- DwarfStar reported a planned 153.41 GiB allocation for the short probe, including its mapped 153.32 GiB model. Its ordinary process RSS is small because it does not represent these mapped GPU weights; do not report DeepSeek as a sub-GB model.
- No swap increase was observed in the probe telemetry. Power/energy were not measured.
- Photos/iCloud work and the live Safari dashboard were present. This is an initial interactive test, not a quiet-system absolute maximum. The task used a shared GPU capture slot and ran one model at a time.

## Provenance

Driver/worker source at execution: `a69a3a9`. Exact model revisions and hashes are in `config/models.lock.json`; environment and engine details appear in each speed record. The summary’s memory calculation was derived after the run from the unchanged telemetry records.

Raw records: each model has `*-speed.jsonl`, `*-speed-telemetry.json`, `*-transaction.json`, and execution/server logs. Local checkout paths in published records are replaced with `<repo>`; metrics and model outputs are unchanged. `summary.json` drives the localhost dashboard.

Rebuild this report with:

```sh
python3 scripts/report_firstlook.py results/m5-firstlook-20261001
```
