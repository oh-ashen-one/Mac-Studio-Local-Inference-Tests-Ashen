# Mistral serving — all three original profiles complete

All three original Mistral serving profiles complete/audited:180 measured requests+6 separate warmups. Two MiMo trials, final report and owned inference-exit verification remain required; not whole-study completion.

| Concurrency | Measured requests | HTTP aggregate output tok/s | Median latency s | p95 latency s | Median TTFT s | Measured wall s |
|---|---:|---:|---:|---:|---:|---:|
| [1](../u20261003-mistral35-serving-c1/result.json) |60/60|4.75647209|53.513639|54.773583|33.168544|3229.284162|
| [2](../u20261003-mistral35-serving-c2/result.json) |60/60|4.92781870|103.794911|104.031787|42.448653|3116.997790|
| [4](../u20261003-mistral35-serving-c4/result.json) |60/60|5.76806153|177.539497|179.002800|51.583368|2662.939694|

Each profile has2 separate warmups excluded from metrics and byte-identical62 request payloads. Native measured inputs8215(8)/8216(52) perprofile, distinct from8192target; all180measured outputs256(total46080), allfinishlength/reportedcachedinput0. Rawresponses/usage/chunks retained. All24 original M5+24 publication hashes, six measurement-sourceblobs/corpus/model/native/runtime fingerprints checked. Only declared slots/globalcontext change(16384context per slot); temperature0/noexplicitseed/cache_promptfalse/900s requests/7200s jobs unchanged. Zero reported reused input does not mean zero physical native cache memory; allocator snapshots are not retuned.

Display-idle prevention policy changed under directownerrequest duringc2 at16:35:44.864UTC after measurement began16:31:10UTC. Task-owned service disabled throughoutc1/enabled throughoutc4; physical pixels unobserved. Rawtimings unadjusted/no causal timing-effect or clean concurrency-only attribution. Profiles are descriptive for this pinned model/runtime, not cold-native-decode, tasks-solved, an official AIPerf submission or hardware ceiling. Two MiMo trials/finalreport/owned inference-exit verification remain required.
