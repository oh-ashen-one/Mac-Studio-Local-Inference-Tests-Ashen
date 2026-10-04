# Mistral serving — two audited original profiles

Only concurrency1/2 of three original serving profiles complete/audited. Concurrency4, two MiMo trials, final report and owned inference-exit verification remain required; not whole-study completion.

| Concurrency | Measured requests | HTTP aggregate output tok/s | Median latency s | p95 latency s | Median TTFT s | Measured wall s |
|---|---:|---:|---:|---:|---:|---:|
| [1](../u20261003-mistral35-serving-c1/result.json) |60/60|4.75647209|53.513639|54.773583|33.168544|3229.284162|
| [2](../u20261003-mistral35-serving-c2/result.json) |60/60|4.92781870|103.794911|104.031787|42.448653|3116.997790|

Each profile has2 separate warmups excluded from metrics, byte-identical62 request payloads, measured nativeinput8215(8)/8216(52) kept distinct from8192target, all60outputs256/total15360/alllengthendings, reported cached input0. Actual response/usage/chunks retained; no tasks-solved or cold-native-decode claim. All16 original M5+16 publication hashes/six measurement-sourceblobs/corpus/model/native/runtime pins checked. Profile slots/globalcontext vary only as declared, same16384context per slot/temperature0/noexplicitseed/cache_promptfalse/900s requests/7200s job. Zero reported reused input does not mean zero physical native cache memory; allocator unchanged.

Display-idle prevention policy changed under owner request DURING c2 at16:35:44.864UTC, after measurement began16:31:10UTC. The task-owned display-awake service wasdisabled throughout c1; actual physical pixels unobserved. Raw timings remain unadjusted, no causal timing-effect or clean concurrency-only attribution. Metrics are descriptive observations for this pinned model/runtime. C4/MiMo/report/exits remain required; not an official AIPerf submission or whole-study conclusion.
