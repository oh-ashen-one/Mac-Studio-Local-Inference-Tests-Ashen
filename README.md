# Mac Studio Local Inference Tests Ashen

An open, reproducible record of my personal local-AI tests: my existing Mac Studio versus my incoming 256 GB / 2 TB Mac Studio, followed by experiments using both machines together.

**Status: benchmark protocol published; no inference results yet.** The existing machine was inspected directly on September 29, 2026. The incoming machine is expected September 30 and must be inspected before its identity is treated as confirmed. This is an independent personal experiment with one machine of each configuration, not a claim about every Mac or every model.

## What I want to find out

1. How much faster is the new Studio on exactly the same model and settings?
2. Which local models give the best useful answers per second, per watt, and per task?
3. How do context length, quantization, thinking, and concurrency change the answer?
4. Can both Studios run a model that is impractical on either alone? At what latency?
5. Is one distributed big model more useful than two independent local agents?
6. Finally: can these machines build a complete game in a controlled local-model loop, documented for YouTube?

The results will be linked from **[Ashen Benchmark](https://ashenoneport.com/benchmark)**. The website entry starts as “planned”; charts and conclusions follow verified runs. The game-building video comes last.

## The machines

| Field | Existing Studio: directly observed | Incoming Studio: provisional |
|---|---|---|
| Chip | Apple M3 Ultra | Expected Apple M5 Ultra; inspect on arrival |
| CPU | 32 cores: 24 performance + 8 efficiency | Expected top-chip 36-core configuration |
| GPU | 80 cores | Expected 80 cores |
| Unified memory | 256 GB; `hw.memsize` = 274,877,906,944 bytes | 256 GB, owner-reported |
| SSD | 2.0 TB; 2,001,111,162,880 bytes | 2 TB, owner-reported |
| Model identifier | Mac15,14 | Pending |
| OS at inventory | macOS 27.0, build 26A428 | Pending; match OS/build for controlled tests where supported |
| Memory bandwidth | 819 GB/s, Apple specification | 1.2 TB/s, current Apple top-chip specification; pending machine confirmation |
| Interconnect | Thunderbolt 5 and 10Gb Ethernet per Apple specification | Thunderbolt 5 and 10Gb Ethernet per current Apple specification; pending inspection |

**The 80-core number is the GPU, not the CPU. Both machines have 256 GB memory.** More RAM is therefore not the proposed upgrade's advantage; chip architecture, memory bandwidth, supported kernels and practical workload performance are what we need to measure. GPU core counts alone cannot predict speed.

The incoming chip is inferred from the owner's description and [Apple's current specifications](https://www.apple.com/mac-studio/specs/), checked September 29, 2026. This is not an inspected order confirmation. “Top-chip, 256 GB / 2 TB” is more precise than “fully maxed out”: Apple's current specifications also list larger memory and storage configurations. Historical M3 figures come from [Apple's 2025 specifications](https://support.apple.com/en-us/122211).

A theoretical bandwidth ratio is not a tokens-per-second prediction. We will publish measured ratios only after matched runs.

## Three comparisons, kept separate

| Track | What stays fixed | What it tells us |
|---|---|---|
| Hardware parity | Exact weights, tokenizer, quantization, runtime revision, prompts and sampling | Speed difference attributable to the machine under that software stack |
| Best practical setup | Published optimization budget and quality floor; each machine may use its best supported setup | What an owner can actually get from each computer |
| Quality frontier | Explicit model, quantization, thinking, time and context budgets | Which configuration solves the most tasks within a useful latency budget |

Faster hardware does not inherently make the same weights more intelligent. It may allow more attempts or more reasoning in a fixed time. Equal-token quality and equal-time usefulness are separate results.

## Benchmark coverage

| Suite | Workloads | Primary outputs |
|---|---|---|
| Single request | Short chat, code, long documents; fresh and reused prefixes | Time to first token, prompt tok/s, decode tok/s, total latency |
| Load and concurrency | 1, 2, 4, 8 requests; closed-loop and fixed arrival-rate runs | Per-user latency, aggregate tok/s, requests/minute, errors |
| Context and memory | 512, 2K, 8K, 32K, 64K, 128K input tokens where supported | Usable context, resident memory, swap delta, latency and retrieval accuracy |
| Quantization | 4-bit, supported 6-bit, 8-bit; BF16 reference for fitting smaller models | Speed/memory/quality trade-off, exact artifact sizes |
| Quality | Coding, reasoning, instruction following, tool calls, long-context retrieval | Exact task scores, success rate, confidence intervals, correct tasks/hour |
| Sustained work | 30-minute screening; two-hour finalist runs; optional eight-hour run | Drift, throttling, crashes, memory growth, energy/task |
| Two-machine cluster | Independent servers, pipeline sharding, supported tensor sharding | Latency, throughput, capacity, network cost, reliability |
| Final game loop | Same frozen brief and checks; equal-time and equal-token lanes | Time to playable build, accepted features, failures, owner review |

For every suite, failures, unsupported configurations, timeouts and out-of-memory outcomes are published. No cherry-picked best runs.

## Starting model roster

This is a **candidate roster, not a claim that every architecture already works on every backend**. Freeze compatible artifact revisions before execution. Refresh the roster once when the new machine arrives, then lock it for the release.

- Small dense anchor: Qwen3.5-9B or another verified 8–9B open-weight model.
- Everyday dense anchor: **Qwen3.8-27B**, including text/code tasks; add vision only as a separately timed extension.
- Coding MoE anchor: **Qwen3-Coder-30B-A3B-Instruct**.
- Larger dense control: one verified 70–72B model with a compatible license and supported kernels.
- Recent larger MoE: **Qwen3.8-Flash-Next**, if both runtimes support its complete architecture and offloaded tables; report all memory, not just active parameters.
- Large-model candidates: **Qwen3.5-397B-A17B** and **Qwen3-Coder-480B-A35B-Instruct**.
- Cluster stretch goal: **DeepSeek-V3.2 (671B)** at a supported quantization, only after a measured per-node memory fit and correctness check.

Keep at least three model families in the quality release if compatible artifacts are available. Qwen is the initial speed anchor because it also connects to the existing local-game workflow; it must not silently become the entire quality leaderboard. Candidate links and selection rules are in [the model plan](docs/MODELS.md).

## Runtime strategy

Use **MLX / MLX-LM** as the primary Apple-silicon path and **llama.cpp / Metal** as an independent baseline. Match model and settings *within* each backend first. MLX 4-bit and GGUF Q4 variants are not numerically identical formats; do not attribute their difference to hardware alone.

LM Studio and Ollama can be added as user-experience tracks after the underlying engines are measured; record the actual bundled backend and loaded model. Test speculative decoding, prompt caching, quantized KV cache, batching and new-chip-specific acceleration as separate ablations. Keep these off in the basic comparison where possible. New hardware features count only when the selected runtime actually uses them.

For clustering, start with **MLX distributed / JACCL over a direct Thunderbolt 5 link**, then evaluate **EXO** as an orchestration layer. Validate mixed M3/M5 support before downloading giant models. See [the cluster plan](docs/CLUSTER.md).

## Execution order

1. **Inventory and freeze:** inspect both machines, lock software/model revisions and prompt IDs, reserve quiet test windows and disk budgets.
2. **Pilot:** run one small and one 27–32B model on both machines; validate token counts, clocks, outputs and telemetry.
3. **Core speed:** complete the small fixed matrix, then expand only the dimensions needed to explain observed differences.
4. **Quality and capacity:** test the shortlist with full declared task sets, quantization comparisons and longer contexts.
5. **Sustained and concurrent work:** measure finalists under realistic service load and long runs.
6. **Cluster:** establish network baselines, prove a small distributed model, then attempt large models.
7. **Publish:** produce reproducible raw records, plots and an Ashen Benchmark summary.
8. **YouTube/game finale:** use the proven models and frozen loop protocol; preserve the full run before editing the story.

Planning allowance after both machines are ready: roughly 1 day of setup/pilots, 2–4 days of core and quality work, 1–3 days of cluster/reliability work, then reporting. This is an estimate, not a promised runtime: pilot measurements determine a logged run budget. A deliberately bounded release is more reproducible than an endlessly expanding matrix.

## Detailed plans and current artifacts

- [Measurement protocol and publication rules](docs/PROTOCOL.md)
- [Two-Mac clustering and memory fit](docs/CLUSTER.md)
- [Model selection and provenance](docs/MODELS.md)
- [Website and final YouTube/game phase](docs/PUBLISHING.md)
- [Sanitized existing-machine inventory](hardware/existing-studio.json)
- [Incoming-machine placeholder](hardware/incoming-studio.json)
- [Result record template](results/run-template.json)
- [Reproducible, allowlisted hardware collector](scripts/collect_inventory.py)

Only the inventory collector is implemented in this initial release. The inference harness, evaluation adapters, statistical reports and website charts remain planned. Nothing in `results/` is a measured inference result yet.

To collect a privacy-conscious inventory without running a benchmark:

```sh
python3 scripts/collect_inventory.py --machine-id studio-new > hardware/incoming-studio.json
```

Review the JSON before committing. The collector excludes serial numbers, UUIDs, hostnames, account names and network addresses. It does not install software, start engines or download models.

## Open-source and contribution policy

Project-owned code and documentation are **MIT licensed**. Model weights and benchmark datasets keep their original licenses; open weights do not automatically mean unrestricted open source. We distribute model references and hashes, not weights or private datasets.

Please include machine specs, exact revisions, full settings, raw measurements and all failure records when contributing. Community submissions are separate from the two-machine personal comparison. Work on a branch, push it, and open a PR. Merging into `main` requires the owner's approval. The initial repository uses `codex/benchmark-plan` as its default branch so the initial public plan does not require a merge into `main`.

Before publishing, remove credentials, personal filesystem paths, IP addresses, private prompts, serial numbers and UUIDs. Keep needed sanitized evidence in Git or a named release; discard task-owned temporary captures/builds after verification and publication. Never remove shared model caches or another session's work.

By [Ashen](https://x.com/ashen_one).
