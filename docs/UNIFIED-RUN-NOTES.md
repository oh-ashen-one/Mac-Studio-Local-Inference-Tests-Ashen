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

## October 2, 09:50 UTC — repeated Qwen 200K configuration comparison

Qwen 3.8 8-bit MLX completed all five **200000 input / 256 output** repetitions. Decode median is **21.4262 tok/s**, mean **21.2872**, sample standard deviation **0.2123**, range **21.0291–21.4536**. Context-fill median is **212.930s**, mean **213.487s**, sample standard deviation **3.437s**, range **209.874–217.512s**. All five share the same input/output token sequences and model/runtime/residency identities, with zero observed timed and whole-child swap growth.

| Configuration, 200K input / 256 output | Decode median | Context-fill median | Samples |
|---|---:|---:|---:|
| Qwen 3.8 8-bit MLX | 21.4262 tok/s | 212.930s | 5 |
| Qwen 3.8 Q4_K_M llama.cpp | 24.5246 tok/s | 531.977s | 5 |

The two five-sample groups confirm **14.5% higher generation rate for Q4**, but **60.0% less context-fill time for 8-bit MLX**. Inputs have identical token-ID hashes and both use fixed 256-token output work without prefix reuse. This compares coupled precision/runtime configurations on the same M5; it does not isolate quantization or hardware. MLX measures its direct input-to-first-token interval; llama.cpp retains native timings and HTTP first-output latency separately. Repository timing remains a separate metric, and its five-attempt outcome comparison is not yet complete.

The 8-bit grid's other input lengths remain in progress. Earlier one-sample observations stay preserved as dated observations rather than being treated as extra repetitions in this group.

## October 2, 10:05 UTC — both Qwen 3.8 context-speed grids complete

Qwen 3.8 8-bit MLX completed all **20** runs, five repetitions at every length with 256 generated tokens:

| Actual input tokens | 8-bit MLX decode | Q4 llama.cpp decode | 8-bit MLX fill | Q4 llama.cpp fill |
|---:|---:|---:|---:|---:|
| 8192 | 30.5813 tok/s | 44.7961 tok/s | 4.961s | 6.738s |
| 32768 | 28.9279 tok/s | 41.0698 tok/s | 21.437s | 34.279s |
| 131072 | 24.4479 tok/s | 29.4163 tok/s | 115.589s | 265.209s |
| 200000 | 21.4262 tok/s | 24.5246 tok/s | 212.930s | 531.977s |

Every table entry is a **five-sample median**. All 20 8-bit runs have exact counters, unchanged model/runtime/residency identities, identical input/output sequences within each length and zero observed whole-child swap growth. The Q4 and 8-bit input-token hashes match at each input length. Q4 generates faster at every measured length; 8-bit MLX fills context faster at every length. Both precision and runtime differ, so the table cannot isolate either factor. Native timing fields, HTTP first-output timing and direct MLX timing retain their documented boundaries.

Within the 8-bit MLX configuration, generation at 200K is **29.9% slower** than at 8192 tokens, and context fill takes **42.9 times as long**. This does not establish an intelligence ranking or the completed repository success rates; those repeated useful-work suites remain outstanding.

Four configurations now have complete repeated speed grids. The runner is continuing with Qwen 3.6, followed by the remaining MiMo measurements and all unfinished work/quality/load suites. Its newly published second 200K sample is **78.7654 tok/s** with **66.737s** fill.

## October 2, 10:20 UTC — Qwen 3.6's complete context-speed grid

Qwen 3.6 35B A3B FP4 completed all **20** fresh-process speed runs, five repetitions per input length and 256 generated tokens each:

| Actual input tokens | Decode median | Context-fill median | Repetitions |
|---:|---:|---:|---:|
| 8192 | 145.8938 tok/s | 0.928s | 5 |
| 32768 | 131.9741 tok/s | 4.526s | 5 |
| 131072 | 96.8335 tok/s | 33.092s | 5 |
| 200000 | 78.7654 tok/s | 66.722s | 5 |

Generation at 200K is **46.0% slower** than at 8192 tokens; context fill takes **71.9 times as long**. Exact counters, unchanged model/runtime/residency/corpus identities, identical input/output token sequences within every length, and zero observed timed/whole-child swap growth were verified across all 20 runs. The 200K generation range is **78.4142–80.3715 tok/s**, with all observations retained.

This is throughput performance for the disclosed FP4/MLX-VLM profile, not an intelligence or task-success conclusion. Its first bounded repository attempt failed within eight turns; that evidence remains unchanged, with four further attempts plus the separate twenty-turn condition still required. The runner has advanced to MiMo's repeated speed measurements. Five configurations have complete speed grids, but the full 234-group study remains unfinished.

## October 2, 10:50 UTC — all six five-repeat 200K groups complete

MiMo's five measured resident-profile runs completed exact **200000 input / 256 output** work. Decode median is **37.6764 tok/s**, mean **37.5792**, sample standard deviation **0.2115**, range **37.2172–37.7477**. Context-fill median is **392.706s**, mean **392.215s**, sample standard deviation **2.046s**, range **388.804–394.284s**. Prefill median is **509.465 tok/s**. Peak MLX allocation was **210.36 GiB** in each run.

All five share model/runtime/residency identities and identical input/output token sequences. Timed inference showed **zero swap growth**; the fifth timed interval ended with 8 MiB less swap. Broader whole-child intervals including loading observed system-wide growth of **0, 3.0625, 1.25, 1.4375 and 1.8125 MiB**. These boundaries are not interchangeable and do not attribute system swapping to the model. No sample was replaced or omitted. The old unwired samples and the separate resident setup probe remain excluded.

Every configuration now has five measured 200K repetitions:

| Configuration | Decode median | Context-fill median | Samples |
|---|---:|---:|---:|
| Qwen 3.8 27B · 8-bit | 21.4262 tok/s | 212.930s | 5 |
| Gemma 4 31B · 8-bit | 15.2549 tok/s | 311.842s | 5 |
| DeepSeek V4 Flash · mixed Q4 | 37.6100 tok/s | 303.859s | 5 |
| MiMo V2.6 Flash · MXFP4 | 37.6764 tok/s | 392.706s | 5 |
| Qwen 3.6 35B A3B · FP4 | 78.7654 tok/s | 66.722s | 5 |
| Qwen 3.8 27B · Q4_K_M | 24.5246 tok/s | 531.977s | 5 |

Timing boundaries and tokenizers differ across model families/runtimes, as declared in the protocol. This table describes configurations on the same M5, not hardware-only effects or general intelligence. MiMo's shorter-context grid remains in progress, followed by all unfinished useful-work, sustained-output and serving suites. Completing this common 200K group does not complete the 234-group study.

## October 2, 11:35 UTC — standard speed phase complete

All **120 predeclared standard speed runs** are complete: six configurations, four input lengths, five repetitions, 256 outputs each. A strict export audit checked every result's completion status, actual input/output count, model/campaign identity and published-result SHA256 receipt. The consolidated statistics independently match the readonly dashboard for all configurations and contexts. Historical runs, the excluded resident setup probe and unrun 2048-output conditions are not included.

[Consolidated report and 120-run manifest](../results/unified-speed-summary-20261002/README.md) · [PNG figure](../outputs/unified-speed-phase.png) · [Editable SVG](../outputs/unified-speed-phase.svg).

MiMo's completed grid:

| Actual input tokens | Decode median | Context-fill median | Repetitions |
|---:|---:|---:|---:|
| 8192 | 65.7032 tok/s | 8.418s | 5 |
| 32768 | 59.4253 tok/s | 27.930s | 5 |
| 131072 | 44.4855 tok/s | 178.426s | 5 |
| 200000 | 37.6764 tok/s | 392.706s | 5 |

The report retains per-group variability, distinct timing definitions, whole-job system-memory/swap observations, MLX-only allocation metrics, source links and hashes. The figure uses standard Matplotlib with the CPU-only Agg backend in a separate plotting environment; inference environments and model files were not changed. The exported layout was visually inspected.

The driver has advanced to the remaining repository trials. Speed-phase completion is not completion of the overall 234-group study, a general intelligence ranking, a paired M3 hardware result or permission to deploy the personal site. All remaining task, quality, sustained-output and serving-load groups still require completion or an evidenced unsupported disposition.


## October 2, 12:17 UTC — three of five Gemma repository attempts complete

Gemma's second and third fresh eight-turn-budget attempts both passed the immutable **19/19** Django tests, with zero human rescue. Attempt two took **1762.435s** and five turns; attempt three took **1013.277s** and three turns. Alongside the first successful attempt, this is **3/3 observed passes with only 3/5 planned attempts complete**, not a final success rate. Attempt four is running.

Attempt three began with **200009 actual input tokens**; subsequent requests contained 204305 and 204854 tokens. All three requests reported zero cached tokens. The sequence read the executor, edited the squash-migration unapply handling and requested evaluation. The accepted patch, raw outputs and immutable final test log are preserved. Whole-child telemetry observed no swap growth and a minimum **148.09 GiB** available system memory; the narrower server interval minimum was **150.11 GiB**. System-wide memory observations are not per-process attribution.

The full campaign is **140/234 groups complete** at this checkpoint. The standard speed phase remains complete; other useful-work, quality, sustained-output and load cells remain pending.


## October 2, 12:33 UTC — fourth Gemma repository attempt complete

Attempt four passed **19/19 tests** in **1042.159s**, three turns and zero human rescues. It began at **200009 input tokens** and reported zero cached tokens across all turns. Its read/edit/evaluate sequence and exact patch remain in the raw record; passing this fixed regression suite is not a claim of general patch correctness. Whole-child telemetry recorded zero swap growth and **149.92 GiB** minimum available system memory (server interval: **149.86 GiB**, independently sampled).

The series now has four observed passes with **4/5 required attempts complete**; attempt five is active. The campaign is **141/234 groups complete**, with all non-speed groups still required under their original budgets.


## October 2, 13:18 UTC — Gemma five-trial repository series complete

All five fresh attempts passed **19/19 immutable tests** within the original eight-turn limit, with **zero human rescues**. Each used the same 200009-token initial packet, model lock and runtime configuration; all **20 total turns reported zero cached tokens**.

| Attempt | Elapsed time | Turns | Final tests | Whole-child swap growth | Minimum available memory |
|---:|---:|---:|---:|---:|---:|
| 1 | 1002.606s | 3 | 19/19 | 0 MiB | 144.70 GiB |
| 2 | 1762.435s | 5 | 19/19 | 0 MiB | 146.91 GiB |
| 3 | 1013.277s | 3 | 19/19 | 0 MiB | 148.09 GiB |
| 4 | 1042.159s | 3 | 19/19 | 0 MiB | 149.92 GiB |
| 5 | 2082.353s | 6 | 19/19 | 0 MiB | 147.32 GiB |

Median completion time is **1042.159s (17m22s)**, mean **1380.566s**, sample standard deviation **507.593s**, range **1002.606–2082.353s**. These are end-to-end task times under the declared harness, not token-generation rates. Zero reported cache reuse means every request processed the long history again. Memory/swap values are system-wide observations sampled across each whole child, not process-attributed allocations.

The fifth attempt's first evaluated edit failed on turn three. The model then made two more edits and passed evaluation on turn six, inside its original budget. Both intermediate evaluations and the final patch remain preserved in [attempt five](../results/u20261002-gemma-repo8-r5/result.json). This is autonomous correction within a trial, not a rescued or rerun failed trial.

**5/5 is the observed outcome on one pinned historical Django issue**, not five different tasks, a general intelligence score or proof that every patch is correct outside the fixed suite. Other configurations' five-trial series are not complete yet, so no comparative success ranking is inferred. The current aggregate and visual dashboard show full sample counts. The driver advanced to Gemma's official full recorded-policy replay; **142/234 campaign groups** are complete. Replay serving success will remain separate from solving tasks.


## October 2, 14:03 UTC — Gemma full recorded replay complete

The actual pinned AA-AgentPerf-Local client served **168/168 recorded turns** with zero failed turns. Measured duration was **2987.624s (49m48s)** and official end-to-end output rate was **8.2231 tok/s**. The separate generation-only metric was **24.9034 tok/s**; it excludes input waits and must not replace the end-to-end number. Median first-token wait was **9.357s**, p95 **32.499s**; median request latency **13.655s**, p95 **38.588s**. These distributions contain 168 requests from a single replay, not repeated independent benchmark runs.

The server counted **2,539,617 input tokens**, including **366,565 cached tokens**; 163 requests reported some cached input. Maximum actual single-request input was **53,483 tokens**, so this is not the separate 200K-context speed condition. Outputs were **24,566 server tokens**, versus 20,872 local-counted tokens and 30,883 recorded target tokens; tokenizer/output-policy differences remain visible. The profile uses recorded output caps and natural stopping, not forced exact-length output.

Preserved limitations: **four short-output warnings**, **155 length-finished turns**, and **16 runtime tool-call parser warnings**. The parser log attributes these warnings to potentially truncated tool text; the benchmark's transport success does not establish valid tool use or solved tasks. AA reports `model-not-listed`, no observed context limit and `reduced: true`; the endpoint remains non-comparable to the standard managed result despite successfully serving this replay. No warning was suppressed, and no request was retried.

Whole-child telemetry observed zero system swap growth and **178.19 GiB** minimum available memory; the independently sampled server interval minimum was **178.11 GiB**. [Official raw summary](../results/u20261002-gemma-aa-full/raw/summary.json), [all turn counters](../results/u20261002-gemma-aa-full/raw/turns.jsonl), and [runtime log](../results/u20261002-gemma-aa-full/server.log) preserve the evidence.

The visual dashboard now places the full replay's elapsed time, end-to-end rate, output policy and context/short-output warnings together. Exact token totals and raw evidence are expandable. The driver has started Gemma's 164-problem HumanEval diagnostic under the already qualified sandbox; **143/234 groups** are complete.


## October 2, 14:19 UTC — Gemma HumanEval-164 complete

Gemma passed **159/164 cases (96.95%)** under the predeclared **single greedy sample, chat-adapted, restricted Python evaluator**. All 164 cases are accounted for, with no retry or changed output budget. The stage took **1275.696s (21m16s)** including setup/evaluation; summed request time was **1252.357s**, with **6.826s** median request latency. These short coding prompts contained **110–490 actual input tokens** per case, separate from the long-context speed and retrieval conditions. Total input was 35,475 tokens, total generated output 33,127 tokens, and reported cached tokens zero.

The five non-passing outcomes have different causes:

| Case | Recorded outcome | Interpretation |
|---|---|---|
| HumanEval/32 · find_zero | Failed assertion | Functional test failure in polynomial root finding |
| HumanEval/103 · rounded_avg | Failed assertion | Functional test failure in rounded average output |
| HumanEval/132 · is_nested | Failed assertion | Functional test failure in bracket nesting |
| HumanEval/145 · order_by_points | Failed assertion | Functional test failure in digit-sum ordering |
| HumanEval/124 · valid_date | Rejected before execution | Generated `import datetime`, outside the evaluator's frozen import subset; not a demonstrated functional failure |

The import rejection remains a non-pass under this declared protocol. Its unchanged code is preserved without executing it under a relaxed policy or substituting another sample. The evaluator had already passed **164/164 canonical solutions** and private-file/network/fork negative controls. Thus this is a reproducible restricted-evaluator result, **not an official HumanEval leaderboard score**. Public task contamination and the chat adaptation limit broader conclusions. No cross-model ranking is inferred before matched coverage.

Whole-child telemetry observed zero system swap growth and **192.29 GiB** minimum available memory; the independently sampled server interval minimum was **195.42 GiB**. [All case outcomes](../results/u20261002-gemma-humaneval/result.json), exact requests/responses, code and evaluator traces are preserved by the publication hash manifest.

The campaign is **144/234 groups complete**. The next active group is Gemma's nine actual 200K-token retrieval cases. All remaining configurations and suites continue under their original budgets.
