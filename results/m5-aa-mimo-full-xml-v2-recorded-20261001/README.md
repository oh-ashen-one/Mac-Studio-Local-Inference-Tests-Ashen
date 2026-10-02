# MiMo XML-parser-v2 — full recorded-policy replay

The official full replay served **168/168 turns**, with zero request failures, in **1,789.18 seconds (29m 49s)**. The server reported **14,817 output tokens**, yielding **8.282 end-to-end output tokens/sec**. Eleven short-output warnings remain recorded. This is serving success, not autonomous task solving.

The largest actual server-reported input was **55,628 tokens**, with 65,536 tokens requested as the replay context. This is not the separate 200K cold-context speed test. Total server input was 2,458,654 tokens, including 360,272 cached and 2,098,382 uncached. Median first-token latency was 6.753s; p95 was 30.298s. Server-telemetry system swap increased by at most 0.6875 MiB from its interval start; minimum sampled available memory was 53.72 GiB.

This profile explicitly uses the pinned runtime's upstream XML parser for MiMo's existing tool-call grammar. The unchanged original template/model, recorded output caps and sampling remain pinned. The original JSON-auto-parser qualification failure is preserved separately, with its full profile unrun and unsupported. The corrected qualification and full run have distinct IDs and source hashes.

AA records `model-not-listed`, null observed context limit and non-comparable context status. Normal EOS stopping produced fewer tokens than the original managed exact-output Qwen cohort, so direct speedup percentages are not justified. All [turn measurements](raw/turns.jsonl), [summary](raw/summary.json), [binding](raw/measurement.json), [run metadata](run.json), [logs](server.log) and [telemetry](telemetry.json) remain available. Generated tool calls were not executed and no result was submitted to another service.
