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


## October 2, 15:18 UTC — Gemma long-context retrieval complete

Gemma correctly returned the exact key in **9/9 retrieval cases**: three deterministic keys at each of approximately 10%, 50% and 90% of the included document. Actual positions were **10.0074%, 50.0054% and 90.0035% of document characters**, not exact token depths. Server input counts were **200022–200026 actual tokens** with **zero cached tokens in every case**. Each request and its preflight count are retained; no context was silently shortened.

Median time to first output was **315.889s**; median full response time was **317.449s**, range **313.310–321.925s**. Responses contained **22–27 generated tokens**, so these times are not interchangeable with the fixed 256-output speed condition. Full stage elapsed time including preparation was **3085.991s (51m26s)**. This small exact-key diagnostic demonstrates retrieval in the specified source corpus; it does not establish broad 200K reasoning or multi-hop reliability.

Whole-child telemetry observed zero swap growth and **161.19 GiB** minimum system available memory (server interval: **161.54 GiB**). [Nine case outcomes](../results/u20261002-gemma-retrieval/result.json) and each exact request/response are published. Gemma now has **30/39 groups complete**, with sustained generation, twenty-turn repair and serving-load tests still queued in the later phase.

DeepSeek's second eight-turn-budget repository attempt also passed **19/19 tests** in **327.726s**, three turns and zero rescues. Its initial input was **200001 tokens**; later requests reported **200019** and **204128** cached tokens. Native tokenization was completed before server loading, as required by the disclosed setup amendment. The unchanged patch and all evaluations remain in [attempt two](../results/u20261002-deepseek-repo8-r2/result.json). Whole-child swap growth was zero and minimum available memory **68.90 GiB**. This is **2/5 planned attempts complete**, both passing, not a final five-trial rate. Attempt three is active.

The full campaign is **146/234 groups complete** at this checkpoint. All configurations continue sequentially; no model is declared finished merely because its speed or initial quality stages are complete.


## October 2, 15:33 UTC — fourth DeepSeek repository attempt complete

DeepSeek attempts three and four passed all **19/19 tests** in **327.558s** and **326.777s**, respectively. Both took three turns with zero human rescue and began with **200001 actual input tokens**. Both second turns reused 200019 cached tokens; their third turns reused 204151 and 204128 tokens. Each preserved patch adds the missing unapply record for the replacement migration. Passing this fixed historical test suite is not a general patch-correctness guarantee.

Whole-child system swap growth was zero for both. Minimum available memory was **69.09 GiB** (r3) and **69.43 GiB** (r4); independently sampled server-interval minima were **69.09 GiB** and **69.54 GiB**. Original raw evidence and hashes are published. The series is **4/5 complete**, all four observed attempts passing, with attempt five active. The full study is **148/234 groups complete** at this checkpoint.


## October 2, 15:40 UTC — DeepSeek five-trial repository series complete

All five DeepSeek attempts passed **19/19 tests**, three turns per attempt and **zero human rescues**. Median task time was **327.558s (5m28s)**, range **325.762–334.153s**. The fifth took **325.762s**, began with **200001 actual input tokens**, and reused 200019 then 204151 cached tokens on subsequent requests. Whole-child system swap growth was zero in all five; the fifth observed **70.21 GiB** minimum available memory. All exact patches, evaluations and hashes are retained.

This is five samples of the same pinned historical issue, not five different problems or a general correctness score. The first successful attempt is explicitly named `pretoken-v2`; the original zero-turn setup failure remains excluded from these five measured attempts and preserved as a separate failure. No successful sample replaced an unsuccessful measured solution.

The driver has advanced to DeepSeek's full recorded-policy agent replay. The campaign is **149/234 groups complete**. Other suites and configurations remain queued.


## October 2, 16:04 UTC — preserve native log bytes during publication

A read-only monitor encountered invalid UTF-8 bytes in the active DeepSeek native log. The benchmark and replay client remained healthy and continued advancing. Monitoring can decode a display-only tail with replacement characters; original files remain unchanged.

The publication helper previously returned undecodable files unchanged, which could also skip private-path redaction. It now replaces only the known private path/host byte sequences directly, preserving every other byte, including incomplete UTF-8 and NULs. Original and published SHA256s remain recorded separately. Regression checks cover invalid UTF-8 surrounding private values and byte-identical preservation of unrelated text/binary fragments. This is an evidence-publication correction, with no model, inference runtime, request policy or measurement change.


## October 2, 16:33 UTC — DeepSeek replay and HumanEval complete

The official full recorded-policy replay served **168/168 requests**, zero failed turns, measured **3033.066s (50m33s)**. End-to-end output rate was **5.0519 tok/s**; the separate generation-only rate was **55.7115 tok/s**. Median first-token wait was **13.295s**, p95 **45.698s**; median request latency **14.781s**, p95 **47.264s**. Those latency distributions comprise 168 turns from one replay, not repeated independent runs.

Exact server totals: **2,468,626 input tokens**, **46,747 cached tokens**, **15,322 output tokens**. Only **two requests** reported cached input. Maximum single-request input was **52,192 tokens**, separate from the 200K speed tests. Local-counted output was 11,914 tokens, while recorded target output was 30,883. Natural stopping and tokenizer differences remain explicit. **11 short-output warnings** and **131 length-finished turns** are preserved. The attached endpoint's context limit was not discoverable (`model-not-listed`, observed null, `reduced: true`), so the official non-comparable flag remains. No retries or exact-output substitution were used.

The large gap between generation-only and end-to-end rates shows why input wait and caching must be reported alongside generation. DeepSeek and Gemma produced different actual output lengths, so their replay rates do not establish a hardware-only speedup. Their observed cache counts describe these precise recorded trajectories, not every possible application. Serving completion does not establish tool correctness or task solving.

The original native server log contains invalid UTF-8 token fragments. Its published copy preserves those bytes, with only private path/host bytes redacted and original/published hashes recorded. All 12 replay artifact hashes were checked. [Official summary](../results/u20261002-deepseek-aa-full/raw/summary.json) and [per-turn counters](../results/u20261002-deepseek-aa-full/raw/turns.jsonl) retain the evidence.

DeepSeek's separate HumanEval diagnostic passed **148/164 cases (90.24%)** under the same declared chat adaptation and restricted evaluator. All 16 non-passes were functional test failures: HumanEval **32, 54, 97, 101, 106, 115, 126, 127, 129, 130, 132, 140, 145, 146, 160 and 163**. Fourteen failed assertions; /32 raised `ValueError`, and /130 raised `IndexError`. No case was rejected for an unsupported import, and every response ended naturally. No sample was retried.

HumanEval stage elapsed time was **335.671s (5m36s)** including setup/evaluation; request sum **271.122s**, median request **1.482s**. Actual inputs were **95–449 tokens** per problem, 31,338 in total, with zero cached tokens; total generated output was **11,367 tokens**. These are short coding diagnostics, not 200K speed conditions. The shorter responses and different runtime/precision prevent interpreting elapsed-time differences as an isolated hardware effect. This is not an official leaderboard score; the public tasks may be training-contaminated. [All 164 results](../results/u20261002-deepseek-humaneval/result.json) and 825 published artifact hashes were verified.

Whole-child swap growth was zero for both groups. Minimum system available memory was **67.33 GiB** during replay and **68.65 GiB** during HumanEval; corresponding independently sampled server minima were **67.33 GiB** and **68.64 GiB**. The campaign is **151/234 groups complete**, with DeepSeek's nine actual 200K retrieval cases now running.


## October 2, 17:33 UTC — DeepSeek retrieval and second Qwen Q4 repair complete

DeepSeek passed **9/9 exact-key retrieval cases**, three deterministic keys at approximately 10%, 50% and 90% document-character positions. Actual input counts were **200004–200032 tokens**, with **zero cached tokens in every request**. Exact preflight counts and per-case character fractions are saved; these fractions are not token-depth claims. Every prompt was counted before loading the native server under the disclosed metadata-scheduling fix.

Median first output was **306.673s**; median response time **307.039s**, range **304.266–309.348s**. Responses contained **14–16 output tokens** and stopped naturally. Full stage time, including preparation, was **2911.025s (48m31s)**. This diagnostic establishes retrieval of the specified keys in this corpus, not general long-context reasoning. Whole-child system swap growth was zero, with **67.18 GiB** minimum available memory; independently sampled server minimum was **67.05 GiB**. [Exact cases and outcomes](../results/u20261002-deepseek-retrieval/result.json) are published. DeepSeek has **30/39 groups complete**, with sustained generation, twenty-turn repair and load tests still pending.

Qwen 3.8 27B Q4_K_M's second repository attempt passed **19/19 tests** in **587.698s (9m48s)**, four turns and zero rescues. It began at **200008 tokens**; later requests reused **200023, 203683 and 207432** cached tokens. The patch and immutable test outputs are preserved in [attempt two](../results/u20261002-qwen38q4-repo8-r2/result.json). Whole-child swap growth was zero and minimum available memory **178.90 GiB** (server interval **178.86 GiB**). Its series is **2/5 complete**, both observed attempts passing; the third is active.

Overall coverage is **153/234 groups complete**. Completed speed/initial quality coverage does not finish either model's full matrix.


## October 2, 17:48 UTC — third Qwen Q4 repository attempt complete

Qwen 3.8 Q4_K_M attempt three passed **19/19 tests** in **617.157s**, using seven of the eight allowed turns and zero human rescues. Starting input was **200008 tokens**; the final request contained 211743 tokens with 211717 cached. Intermediate actions/evaluations and the final patch remain preserved. Whole-child swap growth was zero, minimum available system memory **177.47 GiB** (server interval **177.39 GiB**).

The series is **3/5 complete**, with three observed passes and attempt four active; no final five-trial rate is inferred yet. Full campaign coverage is **154/234 groups**.


## October 2, 18:03 UTC — Qwen Q4 five-trial repository series complete

Qwen 3.8 27B Q4_K_M passed all **five fresh attempts**, each passing **19/19 immutable tests** within the original eight-turn budget, with **zero human rescues**. Starting input was **200008 tokens** for every attempt; packet hashes and server configurations match across the series.

| Attempt | Task time | Turns | Final tests | Whole-child swap growth | Minimum available memory |
|---:|---:|---:|---:|---:|---:|
| 1 | 559.862s | 3 | 19/19 | 0 MiB | 200.28 GiB |
| 2 | 587.698s | 4 | 19/19 | 0 MiB | 178.90 GiB |
| 3 | 617.157s | 7 | 19/19 | 0 MiB | 177.47 GiB |
| 4 | 620.150s | 7 | 19/19 | 0 MiB | 176.51 GiB |
| 5 | 564.575s | 3 | 19/19 | 0 MiB | 177.95 GiB |

Median task time is **587.698s (9m48s)**, mean **589.889s**, sample standard deviation **28.313s**, range **559.862–620.150s**. Server-reported prefix caching was reused after the first turn. Intermediate actions and evaluations remain preserved, including the longer seven-turn trials. System available memory is not a per-process allocation measurement.

This is five attempts at one historical issue, not five independent tasks or a general coding-success score. The separate Qwen 8-bit series still needs its remaining trials. [Fourth trial](../results/u20261002-qwen38q4-repo8-r4/result.json) and [fifth trial](../results/u20261002-qwen38q4-repo8-r5/result.json) complete the raw series.

Coverage is **156/234 groups complete**. Qwen Q4's full recorded-policy replay is running; its broader coding/retrieval diagnostics and later sustained, extended-repair and serving-load groups remain required.


## October 2, 18:18 UTC — Qwen Q4 full recorded replay complete

The official replay served **168/168 requests**, zero failed turns, in **627.299s (10m27s)** measured time. End-to-end output rate was **27.9161 tok/s**; the separate generation-only metric was **44.2474 tok/s**. Median first-token wait was **0.743s**, p95 **4.401s**; median request latency **2.829s**, p95 **9.532s**. These are 168 turns within one replay, not independent repeated replay runs.

The server counted **2,577,822 input tokens**, of which **2,399,938 (~93.1%) were cached**, with **166 requests** reporting cached input. Uncached input totaled 177,884 tokens. Maximum request input was **56,114 tokens**, separate from the 200K speed condition. It produced **17,506 server output tokens**, versus 15,136 local-counted tokens and 30,883 recorded targets. The **five short-output warnings** and **144 length-finished turns** remain in the official summary. Output lengths were not forced to match the historical exact-output cohort.

Unlike the MLX and DwarfStar attached endpoints in this campaign, this llama.cpp endpoint reported its configured **262144-token context**; AA recorded `observed_reason: reported` and `reduced: false` for its requested 65536-token replay condition. That context-discovery result does not make natural recorded-cap output identical to managed exact-length output, prove effective retrieval at the advertised limit, or establish task solving.

The high observed prefix reuse and low first-token waits are a useful property of this specific model/runtime/recorded-trajectory combination. Other configurations have different input tokenization, returned output lengths and cache behavior; no hardware-only percentage is inferred from the replay durations.

Whole-child system swap growth was zero and minimum available memory **165.15 GiB**; the server interval minimum was **165.11 GiB**. All 12 published artifact hashes were verified. [Official summary](../results/u20261002-qwen38q4-aa-full/raw/summary.json), [per-turn counters](../results/u20261002-qwen38q4-aa-full/raw/turns.jsonl), settings and logs are retained.

The campaign is **157/234 groups complete**. Qwen Q4's HumanEval diagnostic is active; its score remains partial until all 164 cases finish.


## October 2, 18:33 UTC — Qwen Q4 HumanEval complete

Qwen 3.8 27B Q4_K_M passed **158/164 cases (96.34%)** under the same declared single greedy chat sample and restricted Python evaluator. Six non-passes were functional failures: **HumanEval/62, /83, /127, /130, /140 and /145**. Five failed assertions; /130 raised an `IndexError`. No case was rejected for an unsupported import. All original requests, responses, code and evaluator traces are retained, with no sample retry or scoring-policy change.

Full stage elapsed time was **938.101s (15m38s)** including preparation/evaluation. Summed request time was **916.554s**, median request **4.303s**. Actual input ranged from **109–473 tokens** per case, totaling **34,112 tokens**; reported cached input was zero. Generated output totaled **40,231 tokens**. These are short coding diagnostics, separate from 200K performance measurements. Different output lengths, tokenization and runtimes limit direct latency comparisons; this is not an official HumanEval leaderboard score or general intelligence ranking.

Whole-child system swap growth was zero and minimum available memory **168.71 GiB**; independently sampled server minimum was **168.68 GiB**. All **825 published artifact hashes** were checked. [All 164 case outcomes](../results/u20261002-qwen38q4-humaneval/result.json) retain the evidence and failure categories.

Campaign coverage is **158/234 groups complete**. Qwen Q4's nine 200K retrieval cases are active, with all remaining configurations and later stress/load conditions still required.


## October 2, 20:04 UTC — Qwen Q4 retrieval complete; Qwen 8-bit trials continue

Qwen 3.8 Q4_K_M passed **9/9 exact-key retrieval cases** with **200001–200005 actual input tokens** per request. The first case reported zero cached tokens; each later case reported **28 cached prefix tokens**, which remain disclosed rather than calling the whole series zero-cache. Responses contained **17–32 tokens**. The three deterministic keys at each approximate 10%/50%/90% document-character position were recovered; exact request metadata records each actual position and count.

Median first output was **536.025s**; median response **536.738s (8m57s)**, range **530.202–552.059s**. Full stage time was **4893.615s (81m34s)** including preparation. Whole-child system swap growth was zero; minimum available memory **176.96 GiB** (server interval **176.92 GiB**). [All nine outcomes](../results/u20261002-qwen38q4-retrieval/result.json) are published. This is exact-key retrieval in the specified corpus, not general long-context reasoning. Qwen Q4 now has **30/39 groups complete**.

Qwen 3.8 8-bit MLX attempts two and three passed **19/19 tests** in **237.594s / four turns** and **243.138s / three turns**. Both began at **200020 tokens**, reused prefix cache in later turns, and had zero human rescues or whole-child swap growth. Whole-child minimum available memory was **144.37 GiB** and **145.60 GiB**, respectively; server interval minima were **144.37 GiB** and **144.59 GiB**.

**Attempt four failed the bounded task**, completing in **257.260s** after all eight allowed turns. It made seven read requests (including one nonexistent file) and one test request, never edited code, and left an empty patch. Final evaluation was **18/19 passed**, with the intended replacement-migration regression still failing. Starting input was **200020 tokens**; the final request had 216427 input and 216160 cached tokens. Zero rescue, zero whole-child swap growth, minimum available memory **139.45 GiB** (server interval **137.11 GiB**). [The failure and all actions](../results/u20261002-qwen38q8-repo8-r4/result.json) remain immutable. It was not retried or given extra turns.

The Qwen 8-bit series has **three passes among four completed trials, of five planned**. Its separately predeclared fifth seed is running. Overall coverage is **162/234 groups complete**, including the unsuccessful completed attempt.


## October 2, 20:09 UTC — Qwen 8-bit repository series complete

The fifth predeclared Qwen 3.8 8-bit trial passed all **19/19 tests** in **229.898s**, three turns and zero human rescue. It reused 200036 then 203845 cached tokens after its first request. Whole-child swap growth was zero and minimum available memory **148.12 GiB**. This completes the current five-trial series at **4/5 passed**, preserving the fourth trial's empty patch and failed target regression.

| Attempt | Outcome | Attempt duration | Turns |
|---:|---|---:|---:|
| 1 | Passed 19/19 | 230.510s | 3 |
| 2 | Passed 19/19 | 237.594s | 4 |
| 3 | Passed 19/19 | 243.138s | 3 |
| 4 | Failed target regression; 18/19 | 257.260s | 8 |
| 5 | Passed 19/19 | 229.898s | 3 |

Median **attempt duration across all five, including the failure**, is **237.594s (3m58s)**, mean **239.680s**, sample standard deviation **11.237s**, range **229.898–257.260s**. The five initial packet hashes match and all start at **200020 actual tokens**. These are repeated attempts at one historical issue, not broad task coverage. No failed attempt was replaced or extended. [Fifth raw trial](../results/u20261002-qwen38q8-repo8-r5/result.json) is published alongside the failed fourth.

The controller briefly received an SSH reachability error during publication. The existing sync completed, and a bounded read-only recheck reached the same verified M5 and original driver PID with no campaign error. The benchmark had advanced to the full Qwen 8-bit replay. No test was restarted or endpoint rerouted. This was a monitoring interruption, not recorded as a model failure.

Coverage is **163/234 groups complete**, and the full recorded-policy Qwen 8-bit replay is active.


## October 2, 20:51 UTC — owner-requested display wake

The owner requested through manager Midir that the verified M5 display stay on. Stored AC display idle timeout was **10 minutes**. The attempt to set it permanently to zero was blocked by `sudo: a password is required`; the stored value remains unchanged. A task-owned `caffeinate -d` process now holds `PreventUserIdleDisplaySleep = 1`, and a five-second user-activity wake assertion was issued. Existing system/idle `caffeinate -is` remains active. The new display assertion does **not persist across reboot**; administrator authentication is still required for the durable setting. Lock/password/security settings were preserved. Physical pixels were not visually verified.

Driver 55667, HumanEval wrapper 66001 and model server 66017 remained alive before and after. The owner-requested display condition change is timestamped here; no model, budget, concurrency, runtime or inference worker was changed or restarted.


## October 2, 20:54 UTC — Qwen 8-bit full replay complete

The official recorded-policy replay served **168/168 requests**, zero failed turns, in **2024.850s (33m45s)**. End-to-end output rate was **8.3474 tok/s**, while the separate generation-only metric was **31.2591 tok/s**. Median first-token wait was **7.127s**, p95 **25.592s**; median request latency **10.577s**, p95 **29.063s**. These distributions contain 168 turns from one replay, not independent repeated replay runs.

Server totals were **2,577,822 input tokens**, **404,728 cached tokens**, and **16,901 output tokens**. 163 requests reported some cached input; maximum single-request input was **56,114 tokens**. Local-counted output was 14,037 tokens, recorded targets 30,883. Retain **seven short-output warnings**, **141 length-finished turns**, and 44 runtime tool-parser warnings. The attached MLX endpoint did not prove its context window (`model-not-listed`, observed null, `reduced: true`), and remains non-comparable to the managed standard. Serving success does not imply solved tasks or valid generated tool actions.

Whole-child and server telemetry both observed zero swap growth and **168.69 GiB** minimum available system memory. All 12 published artifact hashes were checked. [Official summary](../results/u20261002-qwen38q8-aa-full/raw/summary.json) and [per-turn counters](../results/u20261002-qwen38q8-aa-full/raw/turns.jsonl) preserve settings, actual token counts, cache behavior and warnings. The campaign was **164/234 groups complete** at collection, with Qwen 8-bit HumanEval active.

## October 2, 20:58 UTC — display assertion resumes at user login

Following Midir's owner-authorized request, a standard per-user LaunchAgent was installed with a unique task label, `com.ashen.benchmark.display-awake`, executing Apple's `/usr/bin/caffeinate -d`. Plist validation and GUI-domain bootstrap succeeded. Initial raw process-argument inspection was denied; it was stopped without retry or elevation. Supported `launchctl print` independently confirmed the service's program/running PID, and `pmset -g assertions` confirmed that PID's display assertion. Only after this verification was the old manual display PID 67253 retired. One task-owned display assertion remains, PID 68047, alongside system-awake PID 50803.

The LaunchAgent loads **at this user's GUI login after reboot**, not before login. Reboot persistence was not tested by rebooting the benchmark machine. Stored AC display timeout remains 10 minutes; no root power setting, autologin, lock/password or security setting changed. Benchmark driver and current workers remained active during replacement. [Exact reversible configuration and verification/removal instructions](M5-DISPLAY-AWAKE.md) are published. The benchmark heartbeat keeps its existing cadence and ACTIVE state.


## October 2, 21:09 UTC — Qwen 8-bit HumanEval complete

Qwen 3.8 27B 8-bit MLX passed **158/164 cases (96.34%)** under the same declared one-sample greedy chat adaptation and restricted evaluator. The six functional failures were **HumanEval/83, /115, /127, /130, /140 and /145**. Five failed assertions; /130 raised `IndexError`. There were no restricted-import rejections or retries. All original code, requests/responses and evaluator traces are preserved.

The total matches the Qwen Q4 run, but the outcomes are not identical: five failures overlap; the 8-bit configuration passed /62 and failed /115, while Q4 had the opposite outcomes on those two cases. Equal aggregate scores on this public, potentially contaminated suite do not establish broad equivalence or isolate quantization effects from the different runtimes.

Full stage time was **1267.688s (21m08s)**; summed request time **1246.605s**, median request **5.902s**. Actual inputs ranged **109–473 tokens**, totaling **34,112 input tokens**, with zero reported cached input. Generated output totaled **38,302 tokens**. These are short coding tasks, separate from long-context throughput tests; actual output lengths differ between configurations.

Whole-child swap growth was zero and minimum system available memory **181.08 GiB**; independently sampled server minimum was **181.17 GiB**. All **825 published artifact hashes** were verified. [All case outcomes](../results/u20261002-qwen38q8-humaneval/result.json) remain a reproducible restricted-evaluator diagnostic, not an official leaderboard submission.

The full campaign is **165/234 groups complete**, and Qwen 8-bit's nine 200K retrieval cases are active. The verified login LaunchAgent continues to hold the owner-requested display-awake assertion.


## October 2, 21:39 UTC — Qwen 8-bit retrieval complete

Qwen 3.8 27B 8-bit MLX passed **9/9 exact-key retrieval cases**, with **200001–200005 actual input tokens** and **zero reported cached input** for every request. Responses contained **27–32 tokens**. Median first output was **210.457s**; median full response **211.817s (3m32s)**, range **211.615–211.867s**. Total suite time including preparation was **2051.951s (34m12s)**. Positions cover three keys each near 10%/50%/90% of document characters; exact positions and prompts remain in the raw records.

The nine request message payloads were verified identical to their Qwen Q4 counterparts, and actual input counts match case by case. Both configurations passed all nine. Q4's total was 81m34s and median response 536.738s, compared with 34m12s and 211.817s here. The configurations differ in precision and runtime, and returned output lengths/cache behavior also differ (Q4 reused 28 prefix tokens after the first case). These are observed end-to-end configuration results on one M5, not an isolated quantization effect or a cross-hardware speedup.

Whole-child swap growth was zero and minimum system available memory **156.03 GiB**; independently sampled server minimum was **156.34 GiB**. All published artifact hashes were verified. [Exact cases and outcomes](../results/u20261002-qwen38q8-retrieval/result.json) remain a narrow exact-key diagnostic, not proof of broad long-context reasoning.

Coverage is **166/234 groups complete**. Qwen 8-bit, Qwen Q4, Gemma and DeepSeek each have 30/39 groups complete. The driver is executing Qwen 3.6's remaining eight-turn repository trials; all later sustained-output, extended-task and load conditions remain required.


### Subsequent checkpoint — Qwen 3.6 attempt two

Qwen 3.6 35B A3B FP4's second repository attempt passed **19/19 tests** in **214.739s**, three turns and zero human rescues, starting at **200020 actual input tokens**. Whole-child swap growth was zero, with **174.78 GiB** minimum available memory. The unsuccessful first attempt remains intact; this is **one pass among two completed of five planned attempts**, not a final success rate. [Second raw trial](../results/u20261002-qwen36-repo8-r2/result.json) is published. Coverage reached **167/234 groups**, with attempt three active.


## October 2, 21:54 UTC — Qwen 3.6 repository series complete

Qwen 3.6 35B A3B FP4 completed all five fresh repository trials at the frozen eight-turn budget: **4/5 passed**, zero human rescues. The first unsuccessful attempt remains immutable; attempts two through five each passed all **19/19 tests** in three turns. All initial packet hashes match, with **200020 actual starting tokens**. The runtime reported zero cached tokens throughout the series.

| Attempt | Outcome | Duration | Turns | Minimum available memory, whole child |
|---:|---|---:|---:|---:|
| 1 | Target regression failed, 18/19 | 592.190s | 8 | 195.60 GiB |
| 2 | Passed 19/19 | 214.739s | 3 | 174.78 GiB |
| 3 | Passed 19/19 | 215.214s | 3 | 175.02 GiB |
| 4 | Passed 19/19 | 214.640s | 3 | 171.37 GiB |
| 5 | Passed 19/19 | 214.567s | 3 | 174.86 GiB |

Median **attempt duration including the unsuccessful attempt** was **214.739s (3m35s)**, mean **290.270s**, sample standard deviation **168.779s**, range **214.567–592.190s**. Whole-child system swap growth was zero for all five. Successful final patches reconcile the replacement migration's recorded state; passing this fixed historical regression suite is not a general correctness guarantee. No failed attempt was replaced, retried or extended.

[Third trial](../results/u20261002-qwen36-repo8-r3/result.json), [fourth trial](../results/u20261002-qwen36-repo8-r4/result.json), and [fifth trial](../results/u20261002-qwen36-repo8-r5/result.json) complete the published raw series. The campaign is **170/234 groups complete**. Qwen 3.6's full recorded-policy replay is active; its coding/retrieval diagnostics and the later sustained/extended/load suites remain required.


## October 2, 22:10 UTC — Qwen 3.6 full replay and HumanEval complete

The official recorded-policy replay served **168/168 requests**, zero failed turns, in **696.940s (11m37s)** measured time. End-to-end output rate was **40.1741 tok/s**; the separate generation-only metric was **150.8118 tok/s**. Median first-token wait **1.477s**, p95 **5.574s**; median request latency **2.542s**, p95 **7.072s**. These are request distributions within one replay, not repeated replay samples.

Server totals: **2,563,686 input tokens**, including **398,534 cached**, and **27,994 output tokens**. 163 requests reported some cache reuse; maximum single-request input was **56,076 tokens**. Local output count was 14,424, recorded target output 30,883. Preserve **nine short-output warnings**, **138 length-finished turns**, and **64 runtime parser warnings**. The attached MLX-VLM endpoint's context limit was unverified (`model-not-listed`, observed null, `reduced: true`), so the official non-comparable flag remains. Natural recorded-cap output is distinct from managed exact-length output; served requests are not solved tasks. [Official summary](../results/u20261002-qwen36-aa-full/raw/summary.json) and complete raw turn/log evidence are published with all 12 artifact hashes checked.

HumanEval passed **158/164 (96.34%)** under the unchanged one-sample greedy chat adaptation and restricted evaluator. Six assertion failures were **HumanEval/62, /99, /113, /116, /134 and /145**, with no import-policy rejection or sample retry. Stage time was **355.766s (5m56s)**, summed requests **336.658s**, median request **1.629s**. Actual input was **109–473 tokens** per problem, 34,112 total; output totaled **46,850 tokens**, reported cached input zero. Different actual output lengths/runtime/tokenization must remain visible in comparisons. This public coding suite may be training-contaminated and is not an official leaderboard submission. [All 164 coding outcomes](../results/u20261002-qwen36-humaneval/result.json) and all 825 published artifact hashes were verified.

Whole-child swap growth was zero for both stages. Minimum system available memory was **147.97 GiB** for replay and **188.24 GiB** for coding; independent server interval minima **148.30 GiB** and **188.28 GiB**. Coverage is **172/234 groups complete**, with Qwen 3.6's nine 200K retrieval cases active.


## October 2, 22:24 UTC — Qwen 3.6 retrieval complete

Qwen 3.6 35B A3B FP4 passed **9/9 exact-key retrieval cases** with **200001–200005 actual input tokens** and **zero reported cached input** in every request. Each of three deterministic keys was recovered near the 10%/50%/90% document-character positions. Responses contained **22–26 output tokens**.

Median first output was **66.796s**; median response **67.130s (1m07s)**, range **67.054–67.228s**. The entire suite, including preparation, took **746.394s (12m26s)**. This measures exact-key retrieval in the declared corpus, not broad long-context reasoning or an isolated hardware effect.

Whole-child system swap growth was zero and minimum available memory **180.15 GiB**; independent server interval minimum **180.29 GiB**. All **23 published artifact hashes** were verified. [All nine outcomes](../results/u20261002-qwen36-retrieval/result.json) and exact requests/responses retain the evidence.

Coverage is **173/234 groups complete**. Five configurations have completed their first 30 groups; all still require their nine sustained-output, twenty-turn and serving-load groups. MiMo's remaining eight-turn repository trials are now active, followed by its full replay, coding and retrieval diagnostics. Existing memory guards and one-model-at-a-time rules remain in force.


## October 2, 22:39 UTC — MiMo second repository attempt complete

MiMo's second attempt passed **19/19 tests** in **575.874s (9m36s)**, using all eight allowed turns and zero human rescues. It read six files, edited the replacement-migration state handling on turn seven, and requested successful evaluation on turn eight. Starting context was **200008 actual tokens**; final request **218495 input tokens**, including **218474 cached**. The patch and every action/evaluation are retained in [the raw trial](../results/u20261002-mimo-repo8-r2/result.json).

Whole-child and server intervals both observed **319.625 MiB of system-wide swap growth**. Minimum available system memory was **16.55 GiB** across the whole child and **16.17 GiB** in the independently sampled server interval. These remain above the 12 GiB available-memory guard and below the 2 GiB swap-growth limit, which were unchanged. The swap observation includes setup/loading and is not attributed solely to timed inference or to this process. Do not describe this trial as zero-swap.

This current series has **one pass among two completed attempts, of five planned**. The first unsuccessful attempt is preserved, and no trial was retried or given extra turns. Attempt three is active; full campaign coverage is **174/234 groups complete**.


## October 2, 22:54 UTC — MiMo third and fourth attempts preserved

MiMo attempt three completed unsuccessfully in **505.360s**, using the original eight-turn budget and zero rescues. It read two files, made four edits and requested two evaluations; the target regression still failed, with final **18/19 tests passed**. Its changed patch and intermediate failures are preserved. Last request: **209935 input / 209914 cached tokens**. Whole-child swap growth was zero, minimum available memory **19.09 GiB**; server interval minimum **19.08 GiB**.

Attempt four completed unsuccessfully in **536.083s**, with eight reads, no edits and an empty patch. Final evaluation remained **18/19**, target regression failed. Zero rescue. Last request: **221781 input / 214941 cached tokens**. Whole-child and server intervals observed **24 MiB system swap growth**; minimum available memory **16.17 GiB** and **15.87 GiB**, respectively. Neither trial hit the unchanged memory/swap guards. Both began at **200008 tokens**.

[Third trial](../results/u20261002-mimo-repo8-r3/result.json) and [fourth trial](../results/u20261002-mimo-repo8-r4/result.json) are published without retry, replacement or budget extension. This series currently has **one pass among four completed of five planned attempts**. The fifth is active, and campaign coverage is **176/234 groups complete**.


## October 2, 23:09 UTC — MiMo repository series complete; remaining-time assessment

MiMo attempt five completed unsuccessfully in **496.500s**, eight turns, zero human rescues and **200008 starting tokens**. It made five edits, with final evaluation reporting **five failures and two errors across 19 tests**. Its patch and full evaluator output are preserved. Whole-child swap growth was zero and minimum available system memory **20.06 GiB**. The current five-trial series therefore finishes **1/5 passed**, median attempt duration **536.083s**, with all four unsuccessful attempts retained.

The driver advanced to MiMo's full replay, with **177/234 groups complete**. In response to the owner's timing question, a read-only assessment confirmed **1.890 hours** of sustained timed-inference extrapolation, approximately **2.036 hours** after observed setup overhead. The remaining long-task and serving phases are much more uncertain. [Remaining-work estimate and elapsed-time accounting](REMAINING-TIME-ESTIMATE-20261002.md) documents a rough **8–18-hour execution planning range**, separate from safety deadlines and final report packaging. No additional benchmark/profiling job, runtime change or acceleration was introduced.


## October 2, 23:46 UTC — MiMo full replay and coding complete

MiMo's official recorded-policy replay served **168/168 requests**, zero failed turns, in **1747.914s (29m08s)** measured time. End-to-end rate was **8.8282 tok/s**; separate generation-only metric **72.0169 tok/s**. Median first-token wait **6.632s**, p95 **28.720s**; median request latency **8.412s**, p95 **29.916s**. These distributions contain 168 turns from one replay, not repeated independent runs.

Server totals were **2,458,654 input tokens**, **360,272 cached tokens**, and **15,430 output tokens**. 163 requests reported cached input; maximum request input **55,628 tokens**. Local output count was 12,531, recorded target 30,883. Preserve **ten short-output warnings**, **119 length-finished turns**, **59 runtime tool-parser warnings**, and the unverified-context flag (`model-not-listed`, observed null, `reduced: true`). Serving success does not establish task solving or tool correctness. [Official summary](../results/u20261002-mimo-aa-full/raw/summary.json) and all 12 artifact hashes were verified.

HumanEval passed **154/164 cases (93.90%)** under the frozen one-sample greedy chat adaptation and restricted evaluator:

- Eight functional assertion failures: **/10, /101, /120, /127, /129, /132, /145, /163**.
- **/39** was rejected for importing `sympy`, outside the declared allowed subset; its functional correctness was not established.
- **/130** hit the fixed output cap (`finish_reason: length`), leaving an unclosed code fence and incomplete output that the frozen extractor/evaluator rejected as invalid syntax. No extra output tokens, parser relaxation or retry were provided.

Stage duration was **592.946s (9m53s)**, summed request time **523.037s**, median request **2.556s**. Actual inputs **101–454 tokens** per problem, 32,345 total; generated output **32,062 tokens**, reported cached input zero. All 821 published coding artifact hashes were verified. [All outcomes](../results/u20261002-mimo-humaneval/result.json) retain the distinct failure categories. This remains a public, potentially contaminated, chat-adapted diagnostic rather than an official leaderboard score.

Whole-child swap growth was zero in both stages. Minimum available memory was **60.52 GiB** for replay and **77.15 GiB** for coding; independently sampled server minima **60.56 GiB** and **78.29 GiB**. All six full replay suites and six 164-case coding suites are now complete. Coverage is **179/234 groups**, with MiMo's nine 200K retrieval cases active before the 54 declared sustained-output, extended-repair and serving-load groups.


## October 2, 8:38 PM EDT / October 3, 00:38 UTC — explicit owner pause

The owner requested a pause through Midir while considering TensorFold. The existing heartbeat was changed to **PAUSED** before stopping the verified M5 driver, preventing scheduled continuation. SIGTERM was sent to driver 55667 first; its wrapper 91210 and model server 91271 exited through the established graceful cleanup. Verification found no surviving owned inference processes and no shared GPU holder. System/display-awake assertions remained active.

Completed coverage remains **179/234 groups**. MiMo retrieval completed **8/9 cases, all eight passing**; case `needle-0.9-303` was interrupted. The original result, requests, logs and telemetry are preserved, with a separate `completion-audit.json` identifying **owner-requested interruption rather than a model/runtime failure**. This group is not marked complete or silently retried. The live ledger records the pause and the original pre-pause ledger/process identities are retained privately.

No TensorFold installation/execution, method change or new benchmark was performed. Resume requires explicit owner authorization, safety/ownership rechecks and a documented disposition/new run ID or reviewed continuation for the interrupted group; the existing runner deliberately rejects the unmodified incomplete result. All other completed groups remain skippable from saved evidence.


## October 2, 9:18 PM EDT / October 3, 01:18 UTC — authorized resume

The owner explicitly resumed the unchanged baseline through Midir. Original interrupted MiMo retrieval evidence remains unchanged and separately labeled. A fresh nine-case replacement, `u20261002-mimo-retrieval-resume-v2`, is declared in the plan with prior-plan, preserved-result/audit/manifest and model-lock hashes. Required group count remains 234; all 179 completed groups were checked and skipped. [Amendment and evidence](MIMO-OWNER-RESUME-20261002.md).

M5 preflight passed with no prior owned workers or GPU holders and approximately 237 GiB available. New driver 98036 launched exactly once; wrapper 98040/server 98118 began the first 200027-token input, with prefill visibly advancing. Only then was the existing 15-minute heartbeat restored to ACTIVE. Guards, budgets, concurrency, model/runtime files and measured request policy remain unchanged. The archive is not counted as a model failure or pooled into the replacement.

An authorized metadata-only inventory then reconfirmed two additional independent checkpoints, no partial markers in documented cache roots, and expected file presence/sizes for all six locked configurations. The original estimated ten remains an unresolved itemization/location gap; no cohort expansion or new download was performed. The M3 remains occupied with Unreal Engine and receives no heavy compute or inference. TensorFold stays in the future backlog.

### October 3, first Gemma sustained-output repeat

`u20261002-gemma-tail-200000-2048-r1` completed exactly 200000 input tokens and 2048 generated tokens. Context fill 311.429s, decode 15.37996 tok/s. This is one of three sustained repetitions, not a completed sustained series. Driver continued to the independently declared first twenty-turn repository attempt; no failed eight-turn attempt was rescued or extended.

### October 3, Gemma extended repair and second sustained repeat

`u20261002-gemma-repo20-r1` completed successfully in three turns, 997.837s, zero human rescues. This is a fresh predeclared twenty-turn-budget attempt, not a continuation of an eight-turn trial. Whole-child telemetry shows no swap growth. `u20261002-gemma-tail-200000-2048-r2` completed exactly200000 input/2048 output, fill311.771s, decode15.37908 tok/s, zero observed swap growth. Sustained coverage is now two of three repeats; extended repair one of three. Driver6759 continued to `u20261002-gemma-repo20-r2`.

### October 3, Gemma sustained series complete

All three sustained repetitions finished with exactly200000 input and2048 generated tokens. Decode median15.3790769 tok/s, range15.3752937–15.3799593. Third fill311.760s, zero whole-child swap growth. Second fresh twenty-turn-budget repair passed in three turns/998.060s, zero human rescues and swap growth. Extended repair remains2/3; third trial is active. This is one configuration's completed sustained series, not full-model or full-campaign completion.

### October 3, Gemma extended repair series complete

All three fresh twenty-turn-budget attempts passed, each using three turns and zero human rescues. Durations997.837/998.060/997.614s, median997.837s. Third attempt whole-child swap growth was zero, matching the earlier two. These are independent declared trials, not extensions of prior attempts. Gemma now has36/39 groups complete; its concurrency1/2/4 serving tests remain. Driver advanced to the60-request concurrency1 group.

### October 3, Gemma concurrency-one serving completed

`u20261002-gemma-serving-c1` completed60/60 measured requests after two separately recorded warmups: actual inputs8207–8208 tokens,256 output tokens each (15360 total), zero reported cached input, zero whole-child swap growth. Measured wall1001.471s (16m41.5s), aggregate15.33744 output tok/s; median/p95 first output6.545/6.554s and response latency16.689/16.712s. Setup/tokenization precedes that measured interval; group elapsed is not the same metric. Driver advanced to concurrency2 with the same60-request count. No concurrency scaling conclusion until remaining load profiles finish.

### October 3, Gemma concurrency-two serving completed

60/60 measured requests completed in711.094s, aggregate21.60051 output tok/s; median/p95 latency23.700/23.745s. Compared with concurrency1, aggregate throughput increased about40.8%, while per-request latency increased. This is the expected throughput/latency tradeoff, not a universal speedup. Concurrency4 remains active; no final scaling conclusion yet. Raw request/output/cache and whole-child telemetry are preserved.

### October3: Gemma coverage complete

Gemma finished all39 declared groups. Concurrency4 serving completed60/60 measured requests in577.719s, aggregate26.58730 output tok/s, median/p95 response latency38.522/38.559s. Its concurrency1/2/4 aggregate rates were15.337/21.601/26.587 tok/s, while median latency rose16.689/23.700/38.522s. This is throughput scaling with higher individual latency, not reduced response time. Two warmups per group remain excluded from measured rates. Full-study work continues with27 retained baseline groups plus39 Mistral groups.

### October3, first DeepSeek sustained generation

`u20261002-deepseek-tail-200000-2048-r1` completed exact200000 input/2048 output tokens. Native steady decode20.43 tok/s (2047 steady tokens), native overall generation20.42 tok/s, context fill309.641s derived from native prefill645.91 tok/s. Whole-child swap growth zero; minimum available45.68GiB. This is1/3 sustained repeats; the lower longer-generation rate than the short256-token series requires the remaining repetitions before interpretation. Native timing/counter definitions and raw rows are preserved. Driver continued to the first fresh twenty-turn repair trial.

### October3, first DeepSeek twenty-turn-budget trial

The fresh declared attempt completed with passed=True, 3 turns, 331.324s task wall, 0 human rescues. Whole-child swap growth was 0 bytes. This is1/3 extended attempts, not an extension of a prior failed trial. Exact requests/cache/token counts and evaluator outcomes remain preserved.

### October3, DeepSeek sustained repetition spread

Second sustained200K/2048 repeat completed at38.14 native steady decode tok/s,301.164s fill, no whole-child swap growth. Repeat1 was20.43 tok/s,309.641s fill; native binary/source, model/runtime lock and corpus hashes match. Source-commit fields differ because read-only reporting/evidence was published between runs; inference code was not replaced. The last recorded native-process available-memory sample differed (46.91GiB versus75.49GiB), while both stayed above guards and had no swap growth. This is observable variation, not an established causal explanation. Retain both samples and wait for declared repeat3 before summarizing sustained performance; no extra retry or condition change. The fresh second extended repair remains active.

### October3, DeepSeek sustained series complete

All three200K/2048-output runs are complete, exact counts in each. Native steady decode20.43/38.14/38.15 tok/s, median38.14 and full range20.43–38.15. Context fill309.641/301.164/301.200s, median301.200s. All native binary/source, model/runtime lock and corpus hashes match; no whole-child swap growth. Preserve the slow first repeat in all summaries. Its cause remains unproven. Fresh extended repair trial2 passed in three turns/324.951s with no human rescues or whole-child swap growth; trial3 is active.

### October3, DeepSeek extended repair series complete

Trial3 passed=True in3 turns/325.462s, zero human rescues, whole-child swap growth0 bytes. All three predeclared twenty-turn-budget trials are now complete; each passed in three turns. Serving concurrency1/2/4 remains, with concurrency1 now active. This is36/39 completed groups for DeepSeek, not full configuration completion.
