# Measurement protocol v0.1

Status: preregistered plan; no inference runs have been collected. Freeze this protocol's commit before pilot data are promoted to the main results. Changes require a changelog entry and a new result cohort.

## 1. Experimental controls

- Compare the same model artifact hashes, tokenizer/chat template, runtime commit, build flags, Metal backend, context allocation, batch sizes, GPU offload, KV type, thread count, seed and sampling parameters.
- Use the same macOS version/build where both machines support it. If they cannot match, title the result a hardware-plus-OS comparison and report the confound. Keep an additional best-supported-stack track separate.
- Record power mode, plugged-in state, display setup, ambient temperature, fan policy, background CPU/GPU activity, free storage, memory pressure and swap before/after every run. Never change global GPU-memory limits silently.
- Reserve quiet time; do not kill or pause another collaborator's processes. Postpone a contaminated run, retain its exclusion reason, and rerun it.
- Run the driver on the inference machine for direct-engine tests. Measure local HTTP overhead separately. For network service tests use the same controller and path; do not let the controller become a hidden bottleneck.
- Store UTC wall timestamps for provenance and monotonic clocks for durations. Record the orchestrator identity/settings as actually exposed; do not infer a model or effort from a filename.
- Pre-download models. Hash files outside measured intervals. Separate loading, first compilation, fresh-process generation and warmed generation. A fresh process is not a cold filesystem cache. Use “post-reboot cold” only when that was actually done on a reserved machine.

## 2. Fixed core matrix, then targeted expansion

Start with three compatible models (small dense, 27–32B dense, ~30B MoE), one quality-acceptable 4-bit artifact per backend, both machines, both engines, concurrency 1. Use five input/output cells:

| Input tokens | Output tokens | Purpose |
|---:|---:|---|
| 512 | 128 | Short interactive reply |
| 2,048 | 512 | Typical assistant/code request |
| 8,192 | 512 | Repository/document request |
| 32,768 | 512 | Long prefill |
| 2,048 | 2,048 | Sustained decode |

This is 60 cells (3 models × 2 machines × 2 engines × 5 workloads). Use two unscored warmups per cell and at least 10 measured repetitions across three fresh process sessions. Use a bank of at least 10 frozen prompts, pairing prompt IDs and seeds across machines. Randomize cell order with a recorded seed and balance old/new order across blocks. Separate synthetic fixed-token microbenchmarks from natural tasks that stop at EOS. Never force token output during quality scoring.

If one anchor lacks support on a backend, mark the cell unsupported; do not swap a different model into only one machine's comparison. Pilot trials used for tuning are labeled pilot and excluded from headline statistics.

Expansion sweeps:

- 4-/6-/8-bit and BF16 on fitting representative models; exact quantization and group size always recorded.
- Context ladder: 512, 2K, 8K, 32K, 64K, 128K; optional 256K only within declared model/runtime support. Record actual tokenized length including template/BOS and preserve room for output. No silent truncation or RoPE scaling.
- Concurrency: 1, 2, 4, 8; optional 16 if memory and latency remain useful. One model-serving process can batch many requests; this is not permission to spawn many renderers.
- KV cache precision, prefix reuse, speculative decoding/MTP and optimized attention each tested separately against a fixed baseline. Record draft model, acceptance rate and its memory/power for speculation.
- Vision extension: fixed image hashes, sizes and image-token counts; separately time preprocessing, image encoding and text decoding. Text-only results remain comparable on their own.

Estimate total work after the pilot using measured seconds/cell, quality-task counts, download sizes and disk headroom. Publish planned, completed, failed and skipped cell counts. Do not silently drop slow cells to make the project finish.

## 3. Timing definitions

Use direct-engine synchronized measurements for kernels and client-observed measurements for serving. Synchronize lazy/asynchronous GPU work before stopping engine timers.

- **Load time:** before model load to model ready; report compilation separately when observable.
- **Time to first token (TTFT):** request sent to receipt of first generated token; state whether queueing, tokenization and network are included. Also record time to first visible answer token for thinking models.
- **Prompt throughput:** actual input tokens divided by backend-measured prefill seconds. Do not call input tokens/TTFT pure prefill throughput.
- **Decode throughput:** `(generated_tokens - 1) / (last_token_time - first_token_time)` for token-level timestamps and at least two tokens. Use null for fewer tokens. Record engine-native throughput separately if its timing convention differs.
- **Streaming chunks are not tokens.** If only chunk timestamps exist, label inter-chunk latency and use a validated backend counter for token throughput. Preserve tokenizer version and finish reason.
- **End-to-end latency:** request start to completed response, including queueing and failures up to timeout.
- **Aggregate throughput:** completed output tokens during the declared measurement window divided by its wall duration; disclose treatment of boundary requests. Do not sum unrelated peak tok/s numbers.
- **Quality-adjusted throughput:** passed tasks per wall hour, with a fixed task set and timeouts. Report accuracy alongside it.
- Count reasoning and visible tokens separately where available; otherwise explicitly mark the split unavailable. Show both total decode and visible-answer rate. Cross-tokenizer tok/s is not a direct measure of equivalent work; also publish task latency and output characters/bytes.

## 4. Service load and reliability

First run a closed-loop concurrency sweep. Then use a fixed seeded arrival schedule at 25%, 50%, 75%, 100% and 125% of pilot capacity, with identical offered load when directly comparing machines. Run at least 10 minutes and aim for at least 200 requests per cell; disclose lower counts. Capture p50/p95/p99 latency only with sample counts and an explicit quantile estimator; do not present ten observations as a reliable tail estimate.

Predeclare request timeout (pilot-derived and frozen), queue depth, cancellation behavior and latency target. Publish goodput: successful requests meeting that target per minute. Retain failed requests in reliability denominators.

Run a 30-minute soak on all shortlisted configurations, two hours on finalists and an optional eight-hour mixed-workload test. Include successive long chats, cache reuse/eviction and repeated unload/reload. Sample process/Metal memory, system pressure, swap delta, thermals where exposed, CPU/GPU utilization and performance over time. Show first/middle/last segments, not just one average.

Stop a task-owned trial on sustained critical pressure, rapid swap growth, insufficient disk headroom, persistent thermal alarms or two crashes. Record exact thresholds in the frozen campaign config after pilot observation. Do not disable macOS protections or relaunch forever. Persist partial records before cleanup. A swap-heavy capacity demonstration gets its own label and does not count as a resident-memory speed win.

## 5. Quality (the practical meaning of “intelligence” here)

Use task-specific scores, not one invented IQ number. Separate equal-token tests from fixed-wall-time tests. Hardware should not change equal-budget quality materially; repeat outputs to detect kernel/numerical differences before assuming parity.

| Capability | Proposed suite | Scoring |
|---|---|---|
| Code generation | EvalPlus HumanEval+ and MBPP+ | Official pass@1, task IDs, full held-out tests |
| Reasoning/math | MATH-500 plus a frozen reasoning subset from a supported public harness | Exact answers and declared extraction rules; thinking budget included |
| General knowledge | MMLU-Pro, subject-level scores | Official protocol, full declared split or explicitly labeled fixed subset |
| Instructions | IFEval | Strict and loose official metrics |
| Tool use | Frozen local JSON-schema/tool simulator tasks | Valid schema, correct arguments, correct tool sequence, successful task |
| Long context | RULER plus realistic multi-document questions | Accuracy by length and answer position, cited answer evidence |
| Real code maintenance | 20–30 new small repository issues with hidden checks | Resolved issues, regressions, time, tool calls, attempts |

Pin evaluation code and dataset revisions; verify task support in the selected engine adapter. An OpenAI-compatible generation API does not automatically supply log probabilities required by some harness tasks. Pilot the adapter on known answers. Preserve prompt templates, few-shot examples, task IDs, seeds, decoding settings and grading code. Run generated code in isolated environments without credentials or unrestricted network access.

Use full selected standard splits for the main release; label any sample as a subset with its sampling seed. Do not pool different subsets as equivalent. Public sets may be contaminated by training: include new private-until-run tasks, commit their hashes before testing, and release them after scoring if licensing permits. Human judgment is blind to model/machine labels, uses a frozen rubric, and is supplementary to executable checks. Subjective game fun remains the owner's decision.

For deterministic temperature-zero tasks, use one official pass@1 completion per task and repeated hardware parity checks on a 50-task anchor set. For stochastic configurations, use at least three fixed seeds; report seed variation and the proper pass@k estimator only when sampling supports it. Never give one candidate free retries that another does not receive.

## 6. Statistics and power

- Publish every raw repeat with status and any exclusion reason. Predeclare exclusions: competing workload, harness failure or settings mismatch; slow valid runs stay included.
- Use per-cell median, interquartile range and paired bootstrap 95% confidence intervals over matched prompts/repeats (10,000 resamples, stored seed). Resample at the prompt/session block level to avoid treating correlated tokens as independent observations.
- For task accuracy, include a binomial confidence interval and paired task-level comparisons. Report cohort sizes and avoid overstating small differences.
- Speedup for throughput = new/old; latency speedup = old/new. Aggregate matched cell ratios with an explicitly weighted geometric mean, with per-cell results visible. Never average incompatible tasks or failed cells into a single hidden score.
- Use a wall power meter for whole-system watts and integrated Wh/task. `powermetrics`/software sensor readings are labeled chip/package estimates, not wall energy. Record sampling rate and instrumentation overhead with an on/off pilot.
- Report idle and loaded power; offer both gross energy and explicitly defined idle-subtracted energy. Cluster energy includes both computers and the network equipment. Price/value uses the owner's actual paid prices once supplied, not invented retail values.

## 7. Evidence and release gate

Every run needs: machine inventory ID, UTC time, protocol and harness commit, model repository/revision/SHA256, license reference, total/active parameters, weight bytes, quantization/KV settings, runtime/OS versions, exact command/config, prompt IDs/hashes, token counts, timings, memory/power telemetry, finish reason, status, failure detail and raw-record checksums.

Keep prompts/output artifacts where their licenses allow; otherwise publish retrieval instructions, hashes and scores. Create a machine-readable JSONL dataset, CSV summary and deterministic plotting command. The initial `run-template.json` is a field guide, not a validator or measured result. Implement schema validation before the first campaign.

Publish only after reproducing one anchor cell from a clean environment, reconciling planned versus observed runs, checking privacy/license rules and verifying every chart against raw data. Public conclusions must include uncertainty, exact configurations and the one-unit-per-configuration limitation.

## Primary tooling references

- [MLX-LM](https://github.com/ml-explore/mlx-lm)
- [llama-bench measurement implementation and flags](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [EvalPlus](https://github.com/evalplus/evalplus)
- [RULER](https://github.com/NVIDIA/RULER)

These identify tools to pin, not evidence that an unimplemented benchmark has passed.
