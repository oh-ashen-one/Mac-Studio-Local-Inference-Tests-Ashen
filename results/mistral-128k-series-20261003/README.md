# Mistral Medium3.5 128B Q4_K_M — completed128K speed stage

Completed declared131072/256-output stage only; remaining Mistral contexts/suites and MiMo deferred cells are unfinished. Setup probes excluded.

All5 declared repeats used exactly131072 native input token IDs and256 generated tokens, fresh native server/slot and cache_prompt false. No setup sample or outlier was included/removed.

| Repeat | Decode tok/s | HTTP fill s | Complete request s | Swap growth MiB |
|---|---:|---:|---:|---:|
| [1](../u20261003-mistral35-core-131072-r1/result.json) | 5.355117 | 2238.855 | 2286.479 | 0.000 |
| [2](../u20261003-mistral35-core-131072-r2/result.json) | 5.353021 | 2239.142 | 2286.784 | 0.000 |
| [3](../u20261003-mistral35-core-131072-r3/result.json) | 5.355101 | 2238.918 | 2286.542 | 0.000 |
| [4](../u20261003-mistral35-core-131072-r4/result.json) | 5.352817 | 2239.119 | 2286.763 | 0.000 |
| [5](../u20261003-mistral35-core-131072-r5/result.json) | 5.352861 | 2239.188 | 2286.831 | 0.000 |

Native decode tok/s: n=5; median5.353021, mean5.353784, sample SD0.001213, range5.352817–5.355117.

HTTP fill seconds: n=5; median2239.118882, mean2239.044331, sample SD0.147707, range2238.855146–2239.187660.

Minimum whole-child available memory112.043GiB; maximum positive swap growth0.000MiB. Observed intervals do not promise capacity to another app.

Source commits differ for publication/accounting; all6 measurement-entry/runtime-adapter/guard/model-registry blobs are identical across5 repeats.
Model/runtime/native binary/corpus/token-ID fingerprints match. All30 per-run publication artifacts were SHA-checked; originals remain preserved on M5. JSON retains result/telemetry/receipt hashes and full pins.

Cold context means no reused KV/state, not cold SSD or reboot. Native decode and HTTP fill have different timing boundaries. This is one pinned model/precision/runtime on one M5, not intelligence, a hardware ceiling or a matched M3 comparison.

Full study remains active:32K/8K/sustained/task/replay/coding/retrieval/serving and MiMo deferred cells remain required.
