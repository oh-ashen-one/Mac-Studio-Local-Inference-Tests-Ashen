# Remaining-work estimate — October 2, 2026, 23:09 UTC / 7:09 PM EDT

**Planning estimate, not a measured result or deadline.** The verified M5 driver remained healthy at 177/234 completed groups, with MiMo's full replay active. No benchmark, profiling, stress or retry job was added to produce this estimate. The frozen model locks, schedule, budgets and concurrency remain unchanged.

## Remaining execution

| Work | Remaining workload | Planning range |
|---|---|---:|
| MiMo initial quality block | Remainder of 168-turn replay, 164 coding problems, nine 200K retrieval cases | 1.5–2.5 hours |
| Sustained output | 18 fresh runs, each 200K input / 2048 output | 2–2.5 hours |
| Extended repository tasks | 18 fresh attempts, each with up to twenty turns | 2.5–8 hours |
| Serving load | 18 groups × 60 measured requests, plus 36 total warmups; declared concurrency 1/2/4 | 2–4.5 hours |

Reserve approximately **8–18 more hours of execution**, followed by final evidence audit/report packaging, assuming no runtime or resource-guard stop and no major throughput degradation. This is a deliberately broad planning range, not a confidence interval or guaranteed upper bound. The extended tasks and unmeasured concurrent serving behavior dominate uncertainty. Group completion percentage is not elapsed-time completion percentage.

## Evidence and assumptions

For sustained output, summing `3 × (median 200K fill seconds + 2048 / median 200K decode rate)` across the six configurations gives **1.890 hours of timed inference**. Medians come from the five-repeat completed speed phase. Applying the observed per-model setup overhead from those 200K runs adds approximately **0.146 hours**, giving a **2.036-hour proxy** before allowing for longer-output throughput changes. Hence the 2–2.5-hour planning range. This extrapolates 256-output measurements; actual 2048-output runs have not yet been measured.

For extended repository tasks, three times each model's observed median eight-turn stage duration totals **2.619 hours**. This is only a reference scenario if task behavior remains similar and successful attempts stop early. Twenty-turn budgets can permit substantially more work. Gemma alone could consume several additional hours if its attempts repeatedly use all twenty long-context turns. The high end of the range allows for that behavior; it is not an experimentally established cap.

For serving, a deliberately serial proxy using the completed 8192-input/256-output medians for **62 requests × three concurrency levels × six configurations** gives **3.617 hours of timed work**. The real stage uses HTTP, natural output lengths, two warmups per group and concurrent requests. Batching, queuing, shorter outputs, preparation and runtime-specific behavior can change this substantially; no linear concurrency speedup is assumed.

MiMo's retrieval component alone has roughly an hour of input processing if its nine cases resemble its observed 200K fills. Its remaining replay and coding timings are still uncertain. These estimates do not pool historical unwired measurements into the active resident cohort.

Individual-job safety deadlines remain stop-for-review limits. They are **not predictions**, and summing those timeouts would not yield a useful ETA. A stopped group can require review and extend calendar time beyond this planning range.

## Where the elapsed time went

Across the completed records as of this snapshot, recorded stage durations total approximately:

| Completed work | Stage time, including each recorded stage's preparation |
|---|---:|
| 120 standard speed runs | 5.313 hours |
| 30 eight-turn repository trials | 4.941 hours |
| Five nine-case retrieval suites | 3.802 hours |
| Replay runs and qualifications | 2.711 hours |
| Five HumanEval suites | 1.159 hours |
| Structured checks | 0.069 hours |

The median gap between completed jobs was **2.057 seconds**. Since the reviewed driver resume at 05:28 UTC, these gaps sum to **5.642 minutes**. The largest earlier between-record gap was **651.257 seconds** and includes the preserved DeepSeek zero-turn setup failure and review; it should not all be called idle time. All between-completed-record gaps sum to **16.582 minutes**. There is no evidence of repeated fifteen-minute waits between benchmark jobs.

Most elapsed time is inside declared stages: repeated input processing, generation, evaluations and setup such as file verification/model loading. This does not prove every runtime/kernel is optimal. Earlier preparation and historical campaigns precede the current matrix and are separate from these totals.

Sources: frozen plan, completed result start/end timestamps, the current M5 ledger and [five-repeat speed statistics](../results/unified-speed-summary-20261002/summary.json). Refresh this estimate after the first extended-task and concurrent-serving measurements complete, without adding probes or changing conditions.
