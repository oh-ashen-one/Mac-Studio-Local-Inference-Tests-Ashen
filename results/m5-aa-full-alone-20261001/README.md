# Official AA-AgentPerf-Local — M5 alone

Full `agentperf-default-v1` replay: **168/168 turns completed, zero failed turns**, across eight recorded tasks. Measured duration **989.16 seconds (16m 29s)**. Official end-to-end output rate **31.23 tok/s**. Median first-token latency **0.747 s**, p95 **5.241 s**.

This is the separately pinned **Qwen 3.8 27B Q4_K_M / llama.cpp** cohort, not the standard 8-bit MLX cohort. The official runtime qualification passed. Context was reported as 65,536; exact output policy, standard sampling, no speculation. No tool execution or external result submission was performed.

The replay processed **2,577,822 server-reported input tokens across all turns**: 2,385,367 cached and 192,455 uncached. Largest actual request: **56,114 input tokens**. Generated output: **30,883 server tokens**, matching target lengths. Local text-only token counts differ because the response also includes reasoning/tool-call channels; use the official server counters.

These are recorded agent trajectories, not 168 independently solved tasks. The software replays recorded messages/tool feedback; zero failed turns means serving/transport/length checks completed. It is not a code-correctness or intelligence score. This also differs from our 200K cold-context test: it intentionally measures normal growing conversations and cache reuse.

One run, with macOS background services present. The identical Blender condition is pending its GUI safety gate; no multitasking penalty is claimed yet. The original M3 is busy with other sessions and was not benchmarked. Raw summary, per-turn counters, runtime qualification, deployment logs and telemetry are retained in this folder.

Reproduction locks: `config/agentperf.lock.json`. Official tool revision: `0e1c95ab295ed5f783898129ef63a9f207924a30`; llama.cpp revision: `f1cee9941b0e843ea260bf8dd9a090fbd9711b6a`. Local paths are redacted in this public evidence release.
