# Mistral Medium3.5 128B Q4_K_M — completed32K speed stage

Completed declared32768/256-output stage only; remaining Mistral8K/full suites and MiMo deferred cells are unfinished. Setup excluded.

All5 declared repeats used exactly32768 native input token IDs and256 generated tokens, fresh server/slot and cache_prompt false. No setup/outlier pooled or removed.

| Repeat | Decode tok/s | HTTP fill s | Request s | Swap growth MiB |
|---|---:|---:|---:|---:|
| [1](../u20261003-mistral35-core-32768-r1/result.json) | 9.982586 | 209.671 | 235.217 | 0.000 |
| [2](../u20261003-mistral35-core-32768-r2/result.json) | 9.971332 | 209.734 | 235.309 | 0.000 |
| [3](../u20261003-mistral35-core-32768-r3/result.json) | 9.987549 | 209.735 | 235.268 | 0.000 |
| [4](../u20261003-mistral35-core-32768-r4/result.json) | 9.978291 | 209.642 | 235.199 | 0.000 |
| [5](../u20261003-mistral35-core-32768-r5/result.json) | 9.986554 | 209.705 | 235.241 | 0.000 |

Native decode tok/s: n=5; median9.982586, mean9.981262, sample SD0.006647, range9.971332–9.987549.

HTTP fill seconds: n=5; median209.705213, mean209.697470, sample SD0.040565, range209.641994–209.734764.

Whole-child minimum available146.574GiB, maximum positive swap growth0.000MiB. Observed intervals, not promised spare capacity.

Source commits differ for publication/accounting; all6 measurement-entry/runtime-adapter/guard/model-registry blobs are identical across5 repeats.
Model/runtime/native binary/corpus/token-ID fingerprints match. All30 artifacts SHA-checked; originals retained on M5. JSON contains raw result/telemetry/receipt hashes and full pins.

Cold context is no reused KV/state, not cold SSD/reboot. Native decode and HTTP fill have distinct boundaries. This is one model/precision/runtime on M5; no intelligence/hardware-ceiling or matched M3 claim.

Full study remains active:8K/sustained/task/replay/coding/retrieval/serving and MiMo deferred cells remain required.
