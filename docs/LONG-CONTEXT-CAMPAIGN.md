# Long-context and real-work campaign

Owner request, 2026-10-01: start with 200,000 actual input tokens, record prefill and post-fill decode, add agent replay and repository completion tests, then repeat with Blender open. The original M3 is busy with other sessions: **all M3 GPU runs are blocked until its owner reserves it**. Never interrupt those sessions.

## First measurements

| M5, 256 GB / 80 GPU cores | Cold context fill | Prefill input tok/s | Post-fill output tok/s | Peak MLX allocation | Swap increase |
|---|---:|---:|---:|---:|---:|
| Qwen 3.8 27B, 8-bit MLX | 214.47 s | 933.63 | 21.44 | 42.02 GiB | 0 |
| Gemma 4 31B, 8-bit MLX | 314.93 s | 635.74 | 15.41 | 49.95 GiB | 0 |
| DeepSeek V4 Flash 0731, mixed Q4 | 301.75 s | 662.81 | 38.20 | 155.81 GiB planned total, not measured peak | 0 |

These are single runs, not a statistically established maximum or intelligence ranking. The source corpus is pinned CPython 3.12.13; the script takes exactly 200,000 tokens according to each model's own tokenizer. Source-file ordering and hashes are in `config/context-corpus.lock.json`; actual token hashes and output are in each result record. Different tokenizers consume different source prefixes. Generation continues through EOS to perform the fixed 256-token workload, so the continuation is not a quality evaluation.

“Cold” means a fresh process and empty context/KV state; it does not mean cold filesystem caches, a reboot, or model-loading time. MLX's full-fill latency includes the first generated token step; its prefill rate covers the first 199,999 tokens. DwarfStar uses its native full-prefill counters. Do not silently equate the timing definitions. MLX peak allocation includes model allocations. Its sampled system-memory delta is measured after load and is additional context-phase memory, not total model residency.

No speculation, no quantized KV cache for the MLX runs, prefill chunks 2048. Background macOS services remain present. Context limits were read from local model configs: Qwen and Gemma both declare 262,144 total tokens. Fail rather than silently truncate an oversized request. Stop on low memory, growing swap, or the two-hour per-run budget. Run one model at a time under the shared GPU slot protocol.

## Work still required

1. **Same model on both Macs:** match locks, source, model-token hashes, OS/runtime, sampling, input/output counts and condition. Reserve the M3 first. Repeat each completed cell at least three times; publish medians, ranges and sample counts. No hardware-only percentage before matched data exists.
2. **AA-AgentPerf-Local:** use the official pinned replay and preserve its comparability flags. The standard replay has 168 turns, eight tasks and requires a 65,536-token server context. It measures serving speed; it does not solve the tasks. Stock MLX server lacks the official `ignore_eos`/context-reporting contract. Do not report an unofficial recorded-output run as the standard exact-output benchmark. An official GGUF recipe is a separate cohort from our 8-bit MLX cohort, with identical recipe/artifact on both Macs.
3. **Blender open:** use one task-owned signed Blender instance and a fixed scene, idle viewport, fixed window size, no render. Record the actual version/scene hash/process and reserve its second GPU slot. Repeat the exact baseline protocol. Active rendering is a separate condition, never silently substituted for “open.” Close only the task-owned app after measuring.
4. **Long repository task:** use a pinned public repository snapshot and predeclared task/tests. Every attempt starts from the same snapshot and uses the same agent scaffold, context policy, tool/time/token budget and sampling. Preserve failed attempts, final diffs, test reports, elapsed time, model/tool time and human-rescue count. At least five independent attempts per condition are needed before interpreting completion frequency; report the count and uncertainty. A source-continuation speed test or recorded AA trajectory is not a successful autonomous code change.
5. **Largest comfortable model:** the staged DeepSeek artifact is ~153 GiB of weights. Report the actual context completed, memory headroom and swap; do not claim it is the largest possible model or force an advertised maximum context without budgeting. Bigger/lower-bit variants get separately named pinned cohorts on both devices.
6. **Darkbloom last:** inspect official installation, install without starting provider work while benchmarks run, then owner account linking. A credible daily rate requires a measured 24-hour window, completed paid jobs, actual earnings, utilization and energy cost. Model throughput times a published token price is only a theoretical ceiling, not daily income.

## External evidence

`research/external-benchmarks.json` contains source-linked reports from M3 Ultra 256/512 GB, DGX Spark, RTX 5090 and AMD R9700 users. Each row records quantization, actual input length, runtime, acceleration, concurrency and limitations. This is a curated reference collection, not a statistical consensus or an exhaustive fastest-result search. Community submissions have not been independently reproduced here.

The visual dashboard defaults to 200K reports. Tuned speculative runs and aggregate multi-user throughput are labeled and filterable. No hardware-only percent is computed across those heterogeneous sources. Raw prompts/responses are collapsed.

Sources: [official AA repository](https://github.com/ArtificialAnalysis/aa-agentperf-local), [Darkbloom installation](https://docs.darkbloom.dev/provider/install), [Darkbloom earnings](https://docs.darkbloom.dev/provider/earnings). Exact peer URLs are attached to every JSON row and dashboard row.

## Repository diagnostic implementation

The first task is historical SWE-bench `django__django-14500` at commit `8c3bd0b708b488a1f6e8bd8cc6b96569904605be`. The scaffold supports bounded read/replace/test/finish actions, with no model shell access. Initial input is 200,000–200,032 actual chat tokens, followed by up to eight turns of 2,048 output tokens. Only migration implementation modules can be edited. Each evaluation restores immutable tests into a fresh copy and runs 19 regression tests in a filesystem/network sandbox with CPU/time limits. Baseline fails the expected new test; the published reference fix passes all 19. Sentinel-read and network denial were verified.

This is a large-context repository diagnostic, not yet a broad long-horizon benchmark. It uses a known public bug and may be contaminated by training data. Five attempts at temperature 0.2 with recorded seeds are planned; report raw successes/attempts and zero-rescue behavior, not a general intelligence score. Each attempt gets a fresh model server/cache and repository. Failures are retained.
