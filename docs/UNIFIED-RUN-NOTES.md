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
