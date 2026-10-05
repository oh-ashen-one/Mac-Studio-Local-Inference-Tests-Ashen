# Mistral sustained200K generation — all three original repeats complete

All three original Mistral sustained200K/2048 repeats complete. Remaining repository/serving, two MiMo trials, final report and owned inference-exit verification remain required; not whole-study completion.

| Repeat | Exact input/output | Native decode tok/s | HTTP fill s | Generation request wall s | Minimum whole-child available GiB | Positive swap growth MiB |
|---|---|---:|---:|---:|---:|---:|
| [1](../u20261003-mistral35-tail-200000-2048-r1/result.json) |200000/2048|3.95959289|5011.770631|5528.753184|83.844162|0.000000|
| [2](../u20261003-mistral35-tail-200000-2048-r2/result.json) |200000/2048|3.96881933|4992.601014|5508.380064|82.932892|0.000000|
| [3](../u20261003-mistral35-tail-200000-2048-r3/result.json) |200000/2048|3.94818518|5029.440074|5547.914215|82.869354|0.000000|

Native decode n=3: median **3.95959289tok/s**, mean3.95886580, sample SD0.01033628, observed range3.94818518–3.96881933. HTTP fill median5011.770631s. These are descriptive statistics for three declared repeats, not a hardware limit or confidence bound.

All final native receipts confirm exact200000 input/2048 output/zero reused cache tokens. All18 original M5 and18 publication artifact hashes, matching model/native/runtime/corpus/input-token-ID fingerprints, native commands/settings and6 measurement-source blobs checked. All prior owned sustained worker pairs exited. Raw responses, SSE chunks, native logs and both server/whole-child telemetry remain linked; no repeat substitution or outlier removal.

Pinned Q4_K_M GGUF/f16 KV, fresh server/slot/cache_prompt=false, temperature0/seed1729, ignore_eos=true, Metal/flash attention/no context shift. Native decode, HTTP fill and full request wall use distinct boundaries; weight verification/load/tokenization/setup are not native decode. Cold256-output runs are a separate condition. No speed-as-intelligence, semantic context, absolute hardware ceiling or matched-M3 causal claim. Display wake disabled throughout all3, system awake preserved. Required remaining repository/serving/MiMo/report/exits still unfinished.
