# Mistral full recorded replay

Original `u20261003-mistral35-aa-full` completed **168/168 recorded requests served**, zero failed turns and official client exit0. This is serving recorded trajectories, not autonomous tasks solved or an intelligence score. **53 short-output warnings and40 length-finished turns** remain in the original per-turn data; natural output caps/policy were not forced or retuned.

Official measured/wall duration **2719.371805s** (about45m19s). Reported end-to-end output throughput **5.25593776tok/s** and output throughput **11.22343072tok/s** use the official tool's definitions; they are not the native cold-context decode metric. Median request e2e **7.925742s**, p95 **41.714172s**; median TTFT **2.555966s**. Raw normalized and observed metrics remain separate.

Native/server totals:2,596,099 prompt tokens,2,416,273 cached and179,826 uncached;14,292 server output tokens. Local tokenizer output total13,030 and recorded target30,883 are separately retained, not equated. Recorded histories are shorter than the200K speed/repository cells. Endpoint reported262144 context versus the replay's65536 request, reduced=false; this is endpoint metadata, not a semantic long-context pass.

Original900s request,14,400s inner/15,000s driver budgets, recorded caps, standard sampling and direct SSE no-retry transport stayed unchanged. Model/native/runtime/AA revision pins and five measurement-source blobs match mini qualification. All168 per-turn success/abort/error fields, **all12 original M5 artifact hashes and12 publication hashes** were checked. Old replay wrapper/server/client exited; the same parent driver continued into HumanEval without restart.

Whole-child minimum available **64.016174GiB**; server sample minimum **63.995010GiB**. Whole-child swap growth0, no new GPU safety event. The owner requested display sleep at04:36:41UTC during this replay; its display-only assertion was disabled while system-awake/inference stayed active. This condition transition is explicitly recorded; raw timings were not adjusted and no causal performance effect is claimed.

HumanEval, retrieval, sustained/extended repair/load groups and two deferred MiMo trials remain required. Whole study is not complete.
