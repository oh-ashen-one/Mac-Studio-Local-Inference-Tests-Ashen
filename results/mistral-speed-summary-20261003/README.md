# Mistral Medium3.5 128B Q4_K_M — complete cold-context speed matrix

All20 predeclared Mistral cold-context speed runs complete; full study/useful-work/sustained/load and MiMo deferred cells are unfinished. Setup excluded.

20/20 declared runs:5 at8192/32768/131072/200000 actual input tokens,256 generated tokens each. No setup/outlier pooled or removed.

| Input tokens | n | Decode median tok/s | Decode observed range | Fill median s | Fill observed range s |
|---:|---:|---:|---:|---:|---:|
| 8192 | 5 | 12.557384 | 12.523009–12.560075 | 32.586 | 32.558–32.622 |
| 32768 | 5 | 9.982586 | 9.971332–9.987549 | 209.705 | 209.642–209.735 |
| 131072 | 5 | 5.353021 | 5.352817–5.355117 | 2239.119 | 2238.855–2239.188 |
| 200000 | 5 | 4.041480 | 4.041009–4.044121 | 4923.512 | 4919.995–4925.004 |

Publication/accounting commits differ; all6 measurement-entry/adapter/guard/model-registry blobs and common native/model/corpus fingerprints match across20 runs. Native context allocation follows each declared length.
Each context has identical native input token IDs/command across its5 repeats. All120 per-run artifact SHA values were checked; originals remain preserved on M5. JSON retains means/sampleSD/ranges plus all20 result/telemetry/receipt hashes.

No reused KV/state; fresh native server/slot and cache_prompt false. Cold context does not mean cold SSD or reboot. Native decode and HTTP fill have distinct boundaries. All20 runs report zero native cache reuse and zero positive whole-child swap growth. These are observed intervals, not promised spare capacity.

This is one pinned model/precision/runtime on M5. Speed is not intelligence or a hardware ceiling; no matched M3 hardware inference exists. The full quality/task/sustained/load matrix remains required.
