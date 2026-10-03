# Qwen 3.6 attached-server replay — M5

The official 168-turn replay served **168/168 turns**, with zero request failures, in **604.56 seconds**. Server-reported output was **22,866 tokens**, yielding **37.83 end-to-end output tokens/sec**. This measures serving, not task solving. Ten turns received short-output warnings.

This cell uses recorded output caps and normal EOS stopping. The original managed Qwen 3.8 Q4_K_M cell forced exact output lengths (30,883 tokens). Different weights, precision, runtime and output lengths prevent a direct performance percentage between those cells. The exact-output policy is unsupported by this MLX HTTP runtime.

AA also records `model-not-listed`, a null observed context limit, and non-comparable context status. Requested replay context is 65,536 tokens; the largest actual server-reported input was **56,076 tokens**. This is not the separate 200K cold-context test. Of 2,563,686 aggregate server input tokens, 398,534 were reported cached and 2,165,152 uncached. Median first-token latency was 1.477s; p95 was 5.672s. No measured swap growth.

Exact model/runtime/source hashes and sampling settings are in [run.json](run.json), [measurement binding](raw/measurement.json) and [raw summary](raw/summary.json). All [turn measurements](raw/turns.jsonl), [server logs](server.log), and [telemetry](telemetry.json) are retained. The bundled recorded replay is pinned to AA source commit `0e1c95ab295ed5f783898129ef63a9f207924a30`; it replays recorded histories without executing generated tool calls. No result was submitted to an external service.
