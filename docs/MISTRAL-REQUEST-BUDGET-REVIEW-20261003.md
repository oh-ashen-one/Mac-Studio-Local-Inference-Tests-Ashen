# Mistral first repository request-budget limitation

`u20261003-mistral35-repo8-r1` actually attempted the unchanged200K starting packet and900-second request budget. The initial native template/tokenizer calibration was200025 tokens. The first request exceeded its deadline before returning any complete response or final native usage. Last logged prefill progress was79872 tokens at878.86 seconds. The server cancelled the request and exited gracefully; driver59984/wrapper70154/server70223 all exited, shared slots empty. There was no new GPU safety event.

The original result remains failed, with zero completed responses, empty patch, no final evaluator result and no task-success score. Its exact SHA256 is bound by `completion-audit.json`. The complete initial packet, clearly reconstructed request (not a captured successful request), original wrapper/server logs, stopped ledger and telemetry are preserved. The attempt wall962.396s includes cleanup and streaming deadline-check granularity; it is not a successful request latency or a claim that enforcement occurred at exactly900.000s. Final actual server token usage is unknown, not zero or equal to calibration.

Whole-child minimum72.129GiB available, zero swap growth; server minimum72.143GiB. No memory or time budget was relaxed. The separate direct first200K speed repetition completed under its original longer measurement budget, with4919.995s fill, but this trial's disposition uses its own actual timeout evidence. Speed completion does not establish useful-task completion within the shorter request deadline.

## Explicit disposition and continuation

Only this actually attempted cell is `unsupported_request_budget`, unscored and not a pass. The driver verifies its original failed-result hash, precise deadline error, completed-response count, fixed900s audit and null task score before skipping the preserved attempt. It never retries this ID. The other36 unrun groups remain required; no seed, retrieval case, task suite or context is classified unsupported by analogy. Any later timeout requires its own preserved attempt and explicit review.

The prior plan bytes/hash are archived. Every job ID, order, context, output, temperature, seed, turn count, individual budget, cache policy, weight/quantization/native runtime and memory guard stays unchanged. Adopt this accounting amendment only at the verified stopped/empty boundary, then start exactly one qualified Mistral continuation, which skips2 completed cells and the one audited failed attempt. It must pass the normal60-second download-quiescence gate before the next predeclared mini replay. No inference configuration fix or accelerated profile is inferred. MiMo's two deferred cells remain required; the global second-GPU-failure stop still applies.

The current audited request-budget disposition covers the individual repository attempt only. If a future retrieval/coding/structured group aborts partway, its completed/failed/unrun case counts must stay explicit. A single timed-out request cannot account for the remaining cases by analogy; preserve each actual attempt and declare any changed continuation separately before resuming.

## Independent original fresh seed1002 attempt

`u20261003-mistral35-repo8-r2` actually attempted the same declared200K packet under seed1002. It hit the same fixed900s request deadline on its first response; zero complete responses/final native usage/task-success score, empty patch. Calibration200025 tokens is not final observed usage. Last logged prefill79872 at879.36s; wrapper wall962.750s includes cleanup/streaming check granularity. Whole-child minimum67.868GiB available and swap growth0. No new GPU safety event (global total1). Driver72523/wrapper40458/server40562 exited, holders empty.

Its own original result hash, full initial packet, reconstructed request, wrapper/server logs, stopped ledger and telemetry are independently preserved; all11 publication hashes verified. Only this attempted seed is newly `unsupported_request_budget`; unscored and never retried. Seeds1003/1004/1005 remain required. Current plan bytes/hash are archived before amendment.

At this clean stopped boundary the budget audit admission check is explicitly restricted to job kind repo/result kind repo_task. A single failed request cannot account for a multi-case retrieval/coding/structured suite; a regression test enforces that refusal.52 unit checks pass under pinned Python3.12. No measurement-entry/model/runtime/weight/cache/seed/token/turn/time/memory setting changes. After publication/sync and idle verified qualification/admission, start exactly one continuation toward the next original fresh seed1003.

## Independent original fresh seed1003 attempt

`u20261003-mistral35-repo8-r3` actually hit the unchanged900s first-request deadline before any complete response/final usage/functional score. It is unscored and independently hash-bound, never retried. Initial native calibration200025, not final usage; last logged prefill79872 at879.38s; wall962.816s includes cleanup/check granularity. Whole-child min68.349GiB available, swap growth0. No GPU event added, global count1. Old driver42884/wrapper42892/server42985 exited, holders empty. Own11 artifact publication hashes checked; originals retained before sync.

Prior plan bytes/hash archived before this single-attempt amendment. Only actually attempted seeds1001/1002/1003 are audited budget limits;1004/1005 and all other cases remain required. All job IDs/order/measurement parameters unchanged. Existing repository-only admission verifies each own failure, not analogies. Continue toward original fresh seed1004 after verified idle qualification/admission; no source/harness/runtime/profile change in this review.
