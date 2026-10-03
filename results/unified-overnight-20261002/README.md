# Unified all-configuration benchmark — interim report

Coverage: **212/234 cells completed**. Status: running. No overall deadline. A completed task attempt may still be unsuccessful.
 Owner scope omissions: 18; remaining baseline groups: 3. Omissions are not passes. Required extension: 39 separately declared groups awaiting verification/qualification. Resource-limited attempted groups: 1; deferred for resource review: 2. Neither is scored as a pass; deferred groups remain required. The 156-group four-model extension was cancelled by owner scope; none is counted as passed.
[Frozen protocol and research sources](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md). Historical measurements and the initial residency investigation are separate; no unsupported cell may be silently treated as completed.

| Configuration | Cells | 200K decode median | 200K repetitions | Eight-turn repair | Twenty-turn repair | HumanEval |
|---|---:|---:|---:|---:|---:|---:|
| Qwen 3.8 27B · 8-bit | 39/39 | 21.426 tok/s | 5/5 | 4/5 completed | 3/3 completed | 158/164 scored of 164 |
| Gemma 4 31B · 8-bit | 39/39 | 15.255 tok/s | 5/5 | 5/5 completed | 3/3 completed | 159/164 scored of 164 |
| DeepSeek V4 Flash · mixed Q4 | 39/39 | 37.610 tok/s | 5/5 | 5/5 completed | 3/3 completed | 148/164 scored of 164 |
| MiMo V2.6 Flash · MXFP4 | 35/39 | 37.676 tok/s | 5/5 | 1/5 completed | 0/0 completed | 154/164 scored of 164 |
| Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates) | 30/39 | 78.765 tok/s | 5/5 | 4/5 completed | 0/0 completed | 158/164 scored of 164 |
| Qwen 3.8 27B · Q4_K_M | 30/39 | 24.525 tok/s | 5/5 | 5/5 completed | 0/0 completed | 158/164 scored of 164 |

## Sustained 200K input / 2048 output

- Qwen 3.8 27B · 8-bit: 3/3 repeats; median decode 21.41945 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].
- Gemma 4 31B · 8-bit: 3/3 repeats; median decode 15.37908 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].
- DeepSeek V4 Flash · mixed Q4: 3/3 repeats; median decode 38.14000 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].
- MiMo V2.6 Flash · MXFP4: 3/3 repeats; median decode 37.60352 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].

## Serving load — completed measured profiles

| Configuration | Concurrency | Requests | Output tokens | Measured seconds | Aggregate output tok/s | Median latency s | P95 latency s |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen 3.8 27B · 8-bit | 1 | 60 | 15360 | 831.543 | 18.472 | 13.854 | 13.891 |
| Qwen 3.8 27B · 8-bit | 2 | 60 | 15360 | 581.980 | 26.393 | 19.380 | 19.603 |
| Qwen 3.8 27B · 8-bit | 4 | 60 | 15360 | 451.545 | 34.017 | 30.076 | 30.289 |
| Gemma 4 31B · 8-bit | 1 | 60 | 15360 | 1001.471 | 15.337 | 16.689 | 16.712 |
| Gemma 4 31B · 8-bit | 2 | 60 | 15360 | 711.094 | 21.601 | 23.700 | 23.745 |
| Gemma 4 31B · 8-bit | 4 | 60 | 15360 | 577.719 | 26.587 | 38.522 | 38.559 |
| DeepSeek V4 Flash · mixed Q4 | 1 | 60 | 15360 | 787.475 | 19.505 | 13.124 | 13.130 |
| DeepSeek V4 Flash · mixed Q4 | 2 | 60 | 15360 | 1882.486 | 8.159 | 63.264 | 63.757 |
| DeepSeek V4 Flash · mixed Q4 | 4 | 60 | 15360 | 1253.112 | 12.257 | 59.722 | 167.887 |
| MiMo V2.6 Flash · MXFP4 | 1 | 60 | 15360 | 548.358 | 28.011 | 9.138 | 9.159 |
| MiMo V2.6 Flash · MXFP4 | 2 | 60 | 15360 | 438.510 | 35.028 | 14.606 | 14.699 |

Two warmups per profile are excluded from measured metrics. Concurrency changes both aggregate throughput and individual latency; results describe each pinned serving runtime. Exact request/output/cache counts are preserved in raw artifacts.


Different models/precisions/runtimes on one M5. No matched M3 hardware speedup is established. Scores are benchmark-specific; public tasks may be contaminated. Replays measure serving, not task solving. Full model/runtime/source hashes, prompts and raw outcomes remain in each run directory.

Preserved setup failure: `u20261002-deepseek-repo8-r1`. Separately labeled replacement: `u20261002-deepseek-repo8-r1-pretoken-v2`. [Review and unchanged measurement limits](../../docs/DEEPSEEK-SETUP-REVIEW-20261002.md).

Preserved owner-requested interruption: `u20261002-mimo-retrieval`. Separately labeled replacement: `u20261002-mimo-retrieval-resume-v2`. [Review and unchanged measurement limits](../../docs/MIMO-OWNER-RESUME-20261002.md).
