# Unified M5 benchmark protocol — 2026-10-02

The owner explicitly authorized an autonomous sequential campaign for **every downloaded configuration**, then removed the initial nine-hour cutoff. There is no overall deadline. Individual request and evaluation budgets remain fixed so a hung request cannot stop all work indefinitely. The display may sleep; `caffeinate -is` keeps the M5 accessible. The original M3 is reserved for other sessions.

## Frozen scope

`config/unified-models.lock.json` pins six configurations: Qwen 3.8 27B 8-bit MLX, Gemma 4 31B 8-bit MLX, DeepSeek V4 Flash mixed Q4/DwarfStar, Qwen 3.6 35B A3B FP4/MLX-VLM, MiMo V2.6 Flash MXFP4/MLX-VLM, and the downloaded Qwen 3.8 Q4_K_M GGUF/llama.cpp variant. Model bytes, revisions and hashes are unchanged. The original locks and historical measurements remain separate.

`config/unified-campaign.json` is the predeclared **234-cell** plan. Each configuration receives the same applicable suite:

| Suite | Per configuration | Purpose |
|---|---|---|
| Cold-context throughput | 8,192 / 32,768 / 131,072 / 200,000 actual input tokens, 256 generated tokens, five fresh-process repetitions at each length | Context scaling, prefill, first-token wait, decode, memory/swap and variability |
| Sustained generation | 200,000 input / 2,048 output, three repetitions | Speed and latency after context fill over a longer generation |
| Bounded repository repair | Five fresh 200K Django attempts, eight turns, 2,048 output tokens per turn | Comparable useful-task success and elapsed time |
| Extended repair | Three fresh attempts, twenty turns, same issue and output budget | Separate longer-horizon condition, not rescue of failed eight-turn trials |
| Official agent replay | Mini qualification then full AA-AgentPerf-Local recorded-policy replay | Serving realistic recorded histories; not tasks solved |
| Structured output | Eight original deterministic tasks, three sampling seeds | Small correctness/format checks, not the speed headline |
| Long retrieval | Nine 200K cases: three document positions × three deterministic keys | Useful retrieval after a large context; actual location/count recorded |
| HumanEval | All 164 original problems, one greedy chat-adapted completion each | Broader functional coding diagnostic, with sandboxed execution |
| Serving load | Request concurrency 1 / 2 / 4, 60 measured requests per level plus two warmups, approximately 8K actual input and 256 output cap | Per-request latency distributions, aggregate throughput and queueing |

Coverage is completed across configurations before drawing cross-model conclusions. Unsupported interfaces or resource limits require concrete evidence and an explicit record; they are never hidden by shortening input, swapping quantizations or changing budgets. No GPU job is run concurrently with another model. Multiple requests inside the single serving process are explicitly labeled load-test conditions.

## Primary methods researched

- [llama.cpp llama-bench](https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md): prompt processing, generation and combined tests; five repetitions; means/standard deviations and raw repetition data. We adopt repeated exact-length work and retain medians/ranges as well. Native internal timing boundaries are not equated with HTTP latency.
- [MLX-LM large-model guidance](https://github.com/ml-explore/mlx-lm#large-models) and the pinned installed `wired_limit` implementation: MLX's normal generation/server paths wire model/cache memory. Our former low-level generator path omitted this. New MLX speed cells explicitly request the device's recommended per-process wired limit, record both prior/new limits and restore it at exit. No global `sysctl` is changed.
- [AA-AgentPerf-Local](https://github.com/ArtificialAnalysis/aa-agentperf-local), pinned at `0e1c95ab295ed5f783898129ef63a9f207924a30`: the actual official tool is run. The common recorded-cap policy accommodates MLX HTTP's lack of `ignore_eos`; warnings and endpoint qualification flags remain visible. The managed exact-output historical cohort is not pooled with it.
- [NVIDIA GenAI-Perf metrics](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/README.html) and its successor [AIPerf](https://github.com/ai-dynamo/aiperf): TTFT, request latency, per-request and aggregate output throughput, actual token counts, warmups and concurrency. Our portable load harness implements these measurement concepts; it does not claim to be an official AIPerf run.
- [HumanEval](https://github.com/openai/human-eval), pinned at `6d43fb980f9fee3c892a914eda09951f772ad10d`: original 164 problems/tests under MIT. This study uses a disclosed chat adaptation and restricted Python 3.10 evaluator, not an official leaderboard submission. Only one sample per problem is generated, so no pass@k above k=1 is claimed.

## Timing, residency and cache definitions

Cold context means no reused KV/state, not a cold SSD cache or reboot. Model-file verification, load and tokenization are separately recorded and excluded from the direct fill/decode interval. MLX reports input-to-first-token time, then `(N-1)/(last-first)` decode rate. DwarfStar reports native prefill and steady-generation counters. llama.cpp uses the exact corpus token IDs through its native completion endpoint and retains native timings plus HTTP first-output latency. SSE chunks are never treated as tokens.

The first MiMo recommended-residency run, `u20261002-mimo-200000-r1`, is an **investigation/setup probe**, not one of the five predeclared core repetitions. Its historical unwired comparisons remain preserved. It must not be pooled into the old baseline or presented as a hardware improvement.

The load test records actual returned token lengths and any reported cached tokens; it does not force identical natural output lengths. Replays, repository tasks and warm serving are distinct from the empty-cache synthetic throughput cells. The source corpus is fixed and model-specific token IDs/counts are retained. Native tokenizers and server-reported usage must confirm requested lengths; no silent truncation is accepted.

## Useful-work controls

Repository source, issue and immutable evaluation tests remain pinned. The new common packet builder cuts the same public source text at a model-specific character boundary to reach the declared actual token count; the packet/hash is saved. Eight-turn and twenty-turn conditions have separate IDs and results. Failed trials are never extended or retried under the original ID. Public historical tasks may be training-contaminated and are not general intelligence scores.

HumanEval responses retain raw code, prompt and evaluator outcome. Complete-function answers are inserted into the provided problem context; body-only completions are appended with documented indentation normalization. Required imports from the original problem remain available. Code runs under macOS deny-default sandboxing with private-home/network/fork denial, CPU/wall/file-size/data limits and a 512 MiB RSS watchdog. An AST gate excludes file access, reflection and non-approved modules. Numeric `eval` is implemented by an arithmetic-only AST evaluator, permitting the legitimate algebra problem without arbitrary evaluation. All 164 canonical solutions and explicit sandbox negative controls must pass before model scoring.

Retrieval positions are defined as fractions of included document characters, with the actual fraction saved; they are not claimed to be exact token-depth positions. Context is recalibrated after insertion and the answer's presence is verified. Hidden expected values are not passed as model instructions.

## Evidence and operational rules

Save every outcome, including invalid controls, errors, timeouts, format failures and negative results. Record runtime/package/source hashes, model identity, actual input/output counts, settings, timestamps, telemetry and sampling counts. Use medians, ranges, means/standard deviations and per-request percentile distributions with explicit sample sizes. Do not call a fastest observed sample an absolute hardware limit.

One model at a time through the shared GPU slot. Available-memory and swap-growth guards remain active; stop driver then owned workers gracefully if necessary. Do not relaunch a crash repeatedly. The existing heartbeat monitors, fixes concrete harness compatibility issues transparently, publishes completed sanitized artifacts and updates coverage. It must not declare completion while any configuration lacks a required cell without an evidenced disposition. No provider activation, main merge, social post, external submission or personal-site deployment is included.
