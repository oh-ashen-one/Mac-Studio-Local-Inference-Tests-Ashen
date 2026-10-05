# DeepSeek repository setup review — October 2, 2026

At 05:18:43 UTC the unified driver stopped `u20261002-deepseek-repo8-r1` during initial prompt calibration, before any inference request or repository action. The original failed result, server log, server telemetry, empty candidate patch and driver stop record are preserved. This was a guarded setup failure, not an unsuccessful model solution and not an OS/GPU crash.

The server planned 156.52 GiB for the model, KV and buffers. The available-memory sample fell to 13.81 GiB and system swap grew by 8.33 GiB in the server interval. The guard triggered and the driver/server/tokenizer exited; there were no remaining owned workers or GPU holders when inspected. The original driver lost its own telemetry write when raising the guard; those samples cannot be reconstructed. Server telemetry remains intact. Future driver failures now write their telemetry in a `finally` block and save the guard-triggering sample.

The native tokenizer maps the same GGUF metadata while the Metal server has its model mapping resident. Source inspection confirms `--dump-tokens` returns before engine initialization and does not prefetch the tensor payload. A separate, guarded, tokenizer-only audit of the same 902,359-byte input completed in 0.331 seconds, emitted 221,413 tokens and peaked at 18,022,400 bytes RSS. Its binary SHA256 is recorded in `hardware/deepseek-tokenizer-standalone-audit.json`. No inference occurred in that audit.

The exact OS mapping/residency interaction is not established by this evidence. Concurrent native metadata mapping is a concrete setup difference to remove and investigate; this review does not claim that DeepSeek cannot fit, or that the model itself needs the observed excess memory. Its earlier structured checks and actual 200K/256 speed run both completed with zero swap growth in their sampled intervals.

## Explicit protocol amendment

The replacement setup/run ID is `u20261002-deepseek-repo8-r1-pretoken-v2`. The frozen plan records the previous plan hash and this amendment. There are still 234 required measurement groups, plus the preserved original setup failure. The failed zero-turn original is not counted as one of the five completed task trials.

All native metadata-only calibration for DeepSeek repository, retrieval and serving packets now finishes **before** loading the server. The wrapper refuses to invoke that tokenizer while its DwarfStar server is active. Model bytes, native runtime binary, quantization, tokenizer, packet-building algorithm, 200K input target, seed, task, evaluator and request/turn budgets remain unchanged. Packet calibration was already outside the measured repository interval; its scheduling change is recorded explicitly. No successful or unsuccessful measured trial is retried or extended.

The revised setup must pass actual server-token-count checks and the same memory guards. If it fails, preserve the new evidence and investigate; do not relax the guards or rerun automatically.

At 05:29 UTC the reviewed continuation reached native server prefill at 200,001 actual prompt tokens with approximately 85.6 GiB available. This verifies the revised setup reached inference; it is not yet a passed repository trial or proof of the exact underlying OS cause.

At 05:35 UTC the revised trial completed successfully: all 19 regression tests passed in **334.153 seconds**, using three of eight allowed turns and zero rescues. Actual initial input was **200001 tokens**. Later turns reported 200019 and 204367 cached input tokens. Both server-only and whole-child telemetry observed **zero swap growth**; whole-child minimum available memory was **82.17 GiB**. The model read the executor file, added the missing unapplied-record branch, and requested evaluation. The patch and every turn are saved under the revised run ID.

This is **n=1 of five** planned eight-turn trials, not the model's final success rate. Gemma's first trial also passed but took 1002.606 seconds; its three reported cached-input counts were zero. Cache behavior is one observed runtime difference, so these task times must not be presented as isolated GPU hardware speedups. The successful revised setup supports keeping metadata calibration outside the resident server interval; it does not alone establish the precise OS-level mechanism behind the earlier spike.
