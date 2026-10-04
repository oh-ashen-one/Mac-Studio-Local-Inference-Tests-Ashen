# Mistral sustained generation — two completed repeats

Two of three original sustained200K/2048 repeats complete. Third and remaining required Mistral/MiMo groups/report/exits unfinished. No full-series statistics or whole-study completion.

| Repeat | Exact input/output | Native decode tok/s | HTTP fill s | Generation request wall s | Whole-child min available GiB | Positive swap growth MiB |
|---|---|---:|---:|---:|---:|---:|
| [1](../u20261003-mistral35-tail-200000-2048-r1/result.json) |200000/2048|3.95959289|5011.770631|5528.753184|83.844162|0.000000|
| [2](../u20261003-mistral35-tail-200000-2048-r2/result.json) |200000/2048|3.96881933|4992.601014|5508.380064|82.932892|0.000000|

Both final native receipts confirm zero cache reuse/exact token work. All12 original M5 and12 publication artifact hashes were checked; both exited worker pairs are absent. Model/native/runtime/corpus/token-ID pins, native commands/generation settings and6 measurement-source blobs match across repeats. Raw responses/chunks/telemetry remain linked. No repetition substitution or outlier removal.

Pinned Q4_K_M GGUF/f16 KV, fresh native server/slot, cache_prompt=false, temperature0/seed1729, EOS ignored, Metal/flash attention/no context shift. Native decode, HTTP fill and request wall have distinct timing boundaries.2048-output runs are kept separate from cold256-output measurements. No speed-as-intelligence, semantic context, absolute hardware ceiling or matched-M3 causal claim. Display wake disabled throughout/system awake preserved. Third repeat and remaining trials/report/exits remain required.
