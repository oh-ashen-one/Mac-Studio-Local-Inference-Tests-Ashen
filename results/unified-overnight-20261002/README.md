# Unified all-configuration benchmark — interim report

Coverage: **195/234 cells completed**. Status: running. No overall deadline. A completed task attempt may still be unsuccessful.
 Owner scope omissions: 18; remaining baseline groups: 21. Omissions are not passes. Required extension: 39 separately declared groups awaiting verification/qualification. The 156-group four-model extension was cancelled by owner scope; none is counted as passed.
[Frozen protocol and research sources](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md). Historical measurements and the initial residency investigation are separate; no unsupported cell may be silently treated as completed.

| Configuration | Cells | 200K decode median | 200K repetitions | Eight-turn repair | Twenty-turn repair | HumanEval |
|---|---:|---:|---:|---:|---:|---:|
| Qwen 3.8 27B · 8-bit | 30/39 | 21.426 tok/s | 5/5 | 4/5 completed | 0/0 completed | 158/164 scored of 164 |
| Gemma 4 31B · 8-bit | 39/39 | 15.255 tok/s | 5/5 | 5/5 completed | 3/3 completed | 159/164 scored of 164 |
| DeepSeek V4 Flash · mixed Q4 | 36/39 | 37.610 tok/s | 5/5 | 5/5 completed | 3/3 completed | 148/164 scored of 164 |
| MiMo V2.6 Flash · MXFP4 | 30/39 | 37.676 tok/s | 5/5 | 1/5 completed | 0/0 completed | 154/164 scored of 164 |
| Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates) | 30/39 | 78.765 tok/s | 5/5 | 4/5 completed | 0/0 completed | 158/164 scored of 164 |
| Qwen 3.8 27B · Q4_K_M | 30/39 | 24.525 tok/s | 5/5 | 5/5 completed | 0/0 completed | 158/164 scored of 164 |

## Sustained 200K input / 2048 output

- Gemma 4 31B · 8-bit: 3/3 repeats; median decode 15.37908 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].
- DeepSeek V4 Flash · mixed Q4: 3/3 repeats; median decode 38.14000 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].

Different models/precisions/runtimes on one M5. No matched M3 hardware speedup is established. Scores are benchmark-specific; public tasks may be contaminated. Replays measure serving, not task solving. Full model/runtime/source hashes, prompts and raw outcomes remain in each run directory.

Preserved setup failure: `u20261002-deepseek-repo8-r1`. Separately labeled replacement: `u20261002-deepseek-repo8-r1-pretoken-v2`. [Review and unchanged measurement limits](../../docs/DEEPSEEK-SETUP-REVIEW-20261002.md).

Preserved owner-requested interruption: `u20261002-mimo-retrieval`. Separately labeled replacement: `u20261002-mimo-retrieval-resume-v2`. [Review and unchanged measurement limits](../../docs/MIMO-OWNER-RESUME-20261002.md).
