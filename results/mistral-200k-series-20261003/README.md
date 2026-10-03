# Mistral Medium3.5 128B Q4_K_M — completed200K speed stage

Completed declared200K/256-output stage only; remaining Mistral contexts/suites and MiMo deferred cells are unfinished. Setup probes excluded.

All5 declared repeats used exactly200000 native input token IDs and256 generated tokens, fresh native server/slot and cache_prompt false. No setup sample or outlier was included/removed.

| Repeat | Decode tok/s | HTTP fill s | Complete request s | Whole-child swap growth MiB |
|---|---:|---:|---:|---:|
| [1](../u20261003-mistral35-core-200000-r1/result.json) | 4.041410 | 4919.995 | 4983.100 | 0.000 |
| [2](../u20261003-mistral35-core-200000-r2/result.json) | 4.041009 | 4921.053 | 4984.164 | 0.000 |
| [3](../u20261003-mistral35-core-200000-r3/result.json) | 4.044121 | 4923.512 | 4986.574 | 0.000 |
| [4](../u20261003-mistral35-core-200000-r4/result.json) | 4.041480 | 4924.726 | 4987.830 | 0.000 |
| [5](../u20261003-mistral35-core-200000-r5/result.json) | 4.041644 | 4925.004 | 4988.106 | 0.000 |

Native steady decode tok/s: n=5; median4.041480, mean4.041933, sample SD0.001245, range4.041009–4.044121.

HTTP context fill seconds: n=5; median4923.511796, mean4922.857965, sample SD2.234847, range4919.995139–4925.004038.

Whole-child minimum available memory88.921GiB; maximum positive swap growth0.000MiB. This is an observed interval, not spare capacity promised to another app.

Source commits differ for publication/accounting; measurement-entry/runtime adapter/guard/model-registry blobs are identical across all5 repeats.
Model/runtime/native binary/corpus/token-ID fingerprints and all measurement-entry blobs match. Every published per-run artifact SHA was checked; originals remain preserved on the M5. JSON includes result/telemetry/receipt hashes and full pins.

Cold context means no reused KV/state, not cold SSD cache or a reboot. Native decode and HTTP fill have different timing boundaries. This describes this pinned model/precision/runtime on one M5; speed is not intelligence or an absolute hardware ceiling. No matched M3 hardware inference exists.

The full study remains active: other contexts, sustained output, repository trials, full replay, coding, retrieval, serving and MiMo deferred cells are still required. No final report/completion claim.
