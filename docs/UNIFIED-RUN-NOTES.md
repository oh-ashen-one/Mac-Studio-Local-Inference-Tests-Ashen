# Unified M5 study — observations in progress

These notes accompany the frozen protocol and raw records. They describe incomplete samples, not final rankings or hardware-only effects. The active cohort contains six configurations; the prior study remains separate.

## October 2, 05:35 UTC — first useful-work outcomes

| Configuration | Eight-turn repository attempts completed | Passed | First attempt time | Initial actual input | Observed cache behavior |
|---|---:|---:|---:|---:|---|
| Gemma 4 31B 8-bit MLX | 1 of 5 | 1 | 1002.606 s | 200009 tokens | All three responses reported zero cached input |
| DeepSeek V4 Flash mixed Q4 / DwarfStar | 1 of 5 | 1 | 334.153 s | 200001 tokens | Later turns reused 200019 and 204367 input tokens |

Both models solved the same pinned Django regression within three of the eight allowed turns, passed all 19 evaluator tests and received zero human rescues. These are different model/runtime configurations on the same M5. The cache difference helps interpret elapsed time; the observations do not isolate chip performance and are not a general coding ranking. All five attempts per configuration are still required.

DeepSeek's original zero-turn setup hit the swap guard. The separately labeled pretoken-v2 continuation passed with zero sampled swap growth and at least 82.17 GiB available across the whole-child interval. [The failure, scheduling amendment and limits of the diagnosis](DEEPSEEK-SETUP-REVIEW-20261002.md) remain part of the record.

DeepSeek's official mini recorded-policy replay served **6/6 turns**, zero failures, with **six short-output warnings**. This is qualification data; it is not a full replay result or six solved tasks. Full replay remains planned.

The Qwen 3.8 Q4_K_M variant scored **21/24** on the small structured suite. It returned 13 instead of the expected 23 on the state-tracking task in all three seeds. Those are retained task failures; no parser relaxation or replacement sample was used. This eight-case suite is a format/correctness diagnostic, not an intelligence score or a substitute for the planned HumanEval/repository/retrieval trials.

[Current coverage and measurements](../results/unified-overnight-20261002/README.md) are updated as each finished group is published. Raw folders retain requests, outputs, usage counters, patches, tests, telemetry, hashes and any failures.

## October 2, 05:50 UTC — first Qwen Q4 long-context sample

The downloaded Qwen 3.8 27B Q4_K_M configuration completed a fresh llama.cpp native-endpoint run with **200000 input / 256 generated tokens**, no prefix reuse, ignored EOS for fixed output work, f16 KV and no speculation. HTTP input-to-first-output time was **528.876s**; native prompt processing was **378.171 input tok/s** and native decode **24.5473 output tok/s**. Native counters independently reported prompt_n=200000 and predicted_n=256. Both whole-child and server-only telemetry observed zero swap growth; whole-child minimum available memory was **206.64 GiB**.

This is the first of five planned 200K samples. It is a separate precision/runtime configuration from Qwen 8-bit MLX. We will compare the complete repeated profiles rather than treat this single sample as an established maximum or hardware-only speedup. Its first actual 200008-token repository attempt is currently running. Raw input-token hash, runtime/model revisions, server binary hash, settings, timings and stream evidence are retained in `results/u20261002-qwen38q4-core-200000-r1/`.

## October 2, 06:05 UTC — generation rate versus task completion

| Qwen 3.8 configuration | Post-200K decode | Context fill | First repository trial | Task result |
|---|---:|---:|---:|---|
| 8-bit MLX | 21.4446 tok/s | 212.930 s | 230.510 s | 19/19 tests passed, three turns, zero rescues |
| Q4_K_M llama.cpp | 24.5473 tok/s | 528.876 s | 559.862 s | 19/19 tests passed, three turns, zero rescues |

Each is **n=1 of five planned repetitions/attempts**. Q4's observed generation rate was 14.5% higher, while the 8-bit MLX configuration's first task took 58.8% less time. These are preliminary configuration gaps on the same M5, not isolated quantization or hardware effects. The synthetic speed inputs have identical token-ID hashes (`6bda6365581cb867a636893aa7b20ad182aedb2e951e4d2661c2b71bda094502`), exact 200000 input / 256 output work and no prefix reuse. Native/server measurement boundaries remain disclosed. Task chat templates and actual initial counts differ slightly: 200020 for 8-bit MLX, 200008 for Q4 llama.cpp.

Both repository runs reused large prefixes after the initial turn: MLX reported 200036 and 203845 cached input tokens; llama.cpp reported 200023 and 203867. Their server and whole-child intervals showed zero swap growth. The result illustrates why raw decode speed and cold-fill/task latency are reported separately; remaining repetitions are required before a final claim.

Both Qwen 3.8 mini recorded-policy replays served **6/6 turns** with four short-output warnings each. Full replays remain planned. The 8-bit configuration's structured score was **21/24**, returning 13 instead of 23 on the state question at all three seeds, matching the Q4 error pattern.

Qwen 3.6 35B A3B FP4 completed its first 200K/256 speed sample at **80.3715 tok/s**, with **66.236s** fill and zero sampled swap growth. Its structured score was **21/24**: it returned 19 instead of 23 on that same state-tracking question at all seeds. Its first repository attempt is running. The small structured suite remains a limited diagnostic, not an intelligence ranking.

## October 2, 06:20 UTC — retained task failure and MiMo entry

Qwen 3.6's first eight-turn repository attempt did **not** pass. It finished the full budget in **592.190s**, made one ineffective edit (`remove` to `discard` in the unapply loop), and produced three responses rejected by the fixed JSON-action parser. No rescue, additional turn or replacement trial was given. All eight responses reported zero cached input; the initial count was 200020 and the final request reached 214300 tokens. Both telemetry intervals observed zero swap growth, with 195.60 GiB minimum available memory across the child interval. Its 80.37 tok/s synthetic result therefore must not be treated as proof that it finishes this task fastest. This is one of five planned attempts.

Its mini recorded-policy replay qualified **6/6** serving turns with three short-output warnings. MiMo then passed **24/24** structured checks. MiMo's complete structured-check server/child interval recorded **8.12 MiB system-swap growth** (not attributable solely to the model) and 83.02 GiB minimum available memory. Its first measured resident 200K speed sample is now running.

README and historical MiMo report wording has been corrected to identify the old unwired speed profile. Historical raw measurements, sample counts, medians and task outcomes are unchanged. The historical report generator now excludes unified campaign records so future regeneration cannot combine the two profiles.

## October 2, 06:35 UTC — first measured resident MiMo result

MiMo's first **measured** resident-profile run completed exact **200000 input / 256 output tokens** at **37.7477 output tok/s**, with **392.977s context fill**, **509.123 prefill tok/s** and **210.36 GiB peak MLX allocation**. Both timed generation and whole-child sampling observed zero swap growth. Whole-child minimum available memory was **25.56 GiB**. The input token hash and all 256 output token IDs match both the excluded resident setup probe and the archived first unwired result. The speed difference therefore accompanies the explicitly recorded memory-residency change without different generated work. This is still **n=1/5**; it is not pooled with the historical unwired samples or the setup probe.

MiMo's first repository attempt **did not solve the bug**: it used all eight turns to read files, made no edit, and failed the target regression (18/19 tests passed). Elapsed task time was **549.753s**, zero rescues. Initial input was **200008 tokens** and the final request reached **221781**, with later requests reporting substantial prefix reuse. Both server and whole-child intervals had zero observed swap growth; the minimum available memory across those samples was **17.59 GiB**. The empty patch and all requests/outputs are retained. This is one of five planned attempts, not a final 0/5 outcome.

All six configurations now have an initial measured 200K speed sample and an initial bounded repository outcome. Repetition, long generation, longer-horizon repair, full replay, retrieval, HumanEval and load-test coverage remain outstanding. No final model ranking is established by this milestone.

At the end of this checkpoint, MiMo mini replay qualified **6/6** serving turns with **6 short-output warnings**. The initial structured / 200K speed / repository / mini-replay pass is complete for all six configurations (**24/234 required groups**). The runner has advanced to Gemma’s second fresh 200K speed repetition. This is a progress milestone, not study completion.

## October 2, 07:05 UTC — Gemma's full five-sample 200K group

Gemma completed all five fresh-process **200000 input / 256 output** repetitions. Decode median is **15.2549 tok/s**, mean **15.2779**, sample standard deviation **0.1505**, observed range **15.1111–15.4434**. Context-fill median is **311.842s**, mean **314.023s**, sample standard deviation **5.479s**, observed range **310.775–323.786s**. Prefill median is **641.684 tok/s** under the declared separate prefix-timing boundary.

The fifth fill was slower at 323.786s; it remains included without a retry or outlier exclusion. All five input hashes and 256-token output sequences match, as do model/runtime locks and the process residency setting. All five observed zero swap growth over their whole-child interval. Timed swap sometimes decreased; this does not mean the host's total existing swap was zero. These statistics describe five observations under this configuration, not a universal hardware maximum or confidence interval for all workloads.

The runner has proceeded to the 131072-token group. Its first sample measured **19.2105 tok/s** and **169.046s fill**; remaining repetitions and smaller-context groups remain in progress. The 200K group is complete, not the full Gemma or six-configuration study.

## October 2, 07:27 UTC — Gemma's complete context-speed grid

All **20** Gemma speed runs are complete, five fresh processes per length, 256 generated tokens each:

| Actual input tokens | Decode median | Context-fill median | Repetitions |
|---:|---:|---:|---:|
| 8192 | 25.8484 tok/s | 6.359 s | 5 |
| 32768 | 24.1650 tok/s | 28.510 s | 5 |
| 131072 | 19.1474 tok/s | 165.833 s | 5 |
| 200000 | 15.2549 tok/s | 311.842 s | 5 |

Within this pinned model/runtime configuration, generation at 200K was **41.0% slower** than at 8192 tokens; the median context fill took **49.0 times as long**. The input length itself is about 24.4 times larger. This is a context-scaling observation, not a cross-hardware claim. Each length keeps its own token hashes and fixed output work; generated continuations are not required to match across different input lengths. All raw repetitions, ranges, means and standard deviations remain available.

The localhost viewer now plots generation and fill time against actual context length, with a configuration selector. Lines connect adjacent measured lengths only; whiskers represent observed ranges, not confidence intervals, and missing lengths stay visibly queued. The 8K-to-200K headline is shown only after both groups reach five samples. The repeated speed phase has moved on to DeepSeek; Gemma's other required suites remain outstanding.

## October 2, 07:50 UTC — DeepSeek's full five-sample 200K group

DeepSeek completed all five fresh-process **200000 input / 256 output** repetitions through the pinned native runtime. Decode median is **37.61 tok/s**, mean **37.804**, sample standard deviation **0.359**, observed range **37.50–38.20**. Native context-fill median is **303.859s**, mean **303.997s**, sample standard deviation **2.177s**, observed range **301.019–306.387s**. Prefill median is **658.20 tok/s**. Context-fill values follow the declared native-counter timing boundary; they are not HTTP first-token latency.

All five retain the same model lock, runtime revision, executable SHA256 and corpus hash. Native counters confirm exact input/output work; no repetition was discarded or retried. Every whole-child interval observed zero system-swap growth. The prior historical first result of 38.20 tok/s lies within this new five-sample range; it remains a separate historical sample rather than a sixth observation. The published 36.01 tok/s reference still has different quantization and unstated input length, so these repetitions do not establish a matched hardware percentage against it.

The runner has advanced to DeepSeek's 131072-token group. Its full context-speed grid and remaining useful-work suites are not yet complete.

## October 2, 08:25 UTC — DeepSeek's complete context-speed grid

All **20** DeepSeek native speed runs are complete, five fresh processes per input length and 256 generated tokens each:

| Actual input tokens | Decode median | Native context-fill median | Repetitions |
|---:|---:|---:|---:|
| 8192 | 55.35 tok/s | 8.342 s | 5 |
| 32768 | 51.82 tok/s | 35.631 s | 5 |
| 131072 | 41.57 tok/s | 175.570 s | 5 |
| 200000 | 37.61 tok/s | 303.859 s | 5 |

Within this configuration, median generation at 200K is **32.1% slower** than at 8192 tokens, and native context fill takes **36.4 times as long**. The input count is about 24.4 times larger. These are native-counter timings under the documented boundary, not HTTP TTFT. Every run has verified exact input/output counters, the same model/runtime/executable/corpus identities and zero observed whole-child swap growth. All repetitions, including the slower 8K observation at 54.19 tok/s, remain included.

Gemma and DeepSeek now both have complete repeated context-speed grids. The runner has moved to Qwen 3.8 Q4_K_M repetitions; other model profiles and all unfinished task, replay, retrieval, HumanEval and serving-load groups remain required. The dashboard's model selector exposes the completed DeepSeek curve with sample counts and observed ranges.

## October 2, 09:05 UTC — Qwen Q4's full five-sample 200K group

Qwen 3.8 Q4_K_M completed all five fresh-server **200000 input / 256 output** repetitions through the pinned llama.cpp native endpoint. Decode median is **24.5246 tok/s**, mean **24.4321**, sample standard deviation **0.1820**, observed range **24.1187–24.5473**. HTTP context-fill median is **531.977s**, mean **532.759s**, sample standard deviation **4.235s**, observed range **528.876–539.975s**. Native prefill median is **375.967 input tok/s**; native timing fields and HTTP latency remain separately recorded.

All five confirm the exact workload, identical input token hashes, model lock, runtime commit and executable hash, with no observed swap growth in either server-only or whole-child telemetry. The slower fifth repetition is retained without replacement. Fixed output work ignores EOS; ordinary chat/agent workloads remain separate diagnostics.

The first 131072-token sample measured **29.4906 tok/s** with **265.160s** HTTP fill. Remaining repetitions at that length and the shorter contexts are in progress. The complete Q4 context-speed grid and its remaining task/quality/load suites are not yet finished; the earlier one-run Q4-versus-8-bit comparison is not promoted into a final cross-configuration result before both repeated profiles are complete.

## October 2, 09:35 UTC — Qwen Q4's complete context-speed grid

All **20** Qwen 3.8 Q4_K_M / llama.cpp speed runs are complete, five fresh servers per input length and 256 generated tokens each:

| Actual input tokens | Decode median | HTTP context-fill median | Repetitions |
|---:|---:|---:|---:|
| 8192 | 44.7961 tok/s | 6.738 s | 5 |
| 32768 | 41.0698 tok/s | 34.279 s | 5 |
| 131072 | 29.4163 tok/s | 265.209 s | 5 |
| 200000 | 24.5246 tok/s | 531.977 s | 5 |

Within this configuration, median generation at 200K is **45.3% slower** than at 8192 tokens, while context fill takes **79.0 times as long**. Exact input/output counters, input-token hashes within each length, model/runtime/executable identities and zero observed swap growth were verified across all 20 runs. Native timing fields and HTTP first-output latency remain separately recorded. No repetition was replaced or omitted.

The runtime is now measuring the repeated 8-bit MLX profile. Its second 200K sample completed at **21.0825 tok/s** with **217.512s** fill. The final repeated Q4-versus-8-bit comparison remains pending the rest of the 8-bit grid. Q4's task, quality and load suites are not implied complete by finishing its speed grid.
