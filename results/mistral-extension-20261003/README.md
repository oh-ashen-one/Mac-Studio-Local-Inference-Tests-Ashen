# Unified all-configuration benchmark — interim report

Coverage: **29/39 cells completed**. Status: running. No overall deadline. A completed task attempt may still be unsuccessful.
 Audited request-budget-limited attempted groups: 9, unscored; original failed records preserved.
[Frozen protocol and research sources](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md). Historical measurements and the initial residency investigation are separate; no unsupported cell may be silently treated as completed.

| Configuration | Cells | 200K decode median | 200K repetitions | Eight-turn repair | Twenty-turn repair | HumanEval |
|---|---:|---:|---:|---:|---:|---:|
| Mistral Medium 3.5 128B · Q4_K_M GGUF | 29/39 | 4.041 tok/s | 5/5 | 0/0 completed | 0/0 completed | 151/164 scored of 164 |

## Sustained 200K input / 2048 output

- Mistral Medium 3.5 128B · Q4_K_M GGUF: 3/3 repeats; median decode 3.95959 tok/s; actual inputs [200000, 200000, 200000]; actual outputs [2048, 2048, 2048].

## Serving load — completed measured profiles

| Configuration | Concurrency | Requests | Output tokens | Measured seconds | Aggregate output tok/s | Median latency s | P95 latency s |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mistral Medium 3.5 128B · Q4_K_M GGUF | 1 | 60 | 15360 | 3229.284 | 4.756 | 53.514 | 54.774 |
| Mistral Medium 3.5 128B · Q4_K_M GGUF | 2 | 60 | 15360 | 3116.998 | 4.928 | 103.795 | 104.032 |

Two warmups per profile are excluded from measured metrics. Concurrency changes both aggregate throughput and individual latency; results describe each pinned serving runtime. Exact request/output/cache counts are preserved in raw artifacts.


Different models/precisions/runtimes on one M5. No matched M3 hardware speedup is established. Scores are benchmark-specific; public tasks may be contaminated. Replays measure serving, not task solving. Full model/runtime/source hashes, prompts and raw outcomes remain in each run directory.
