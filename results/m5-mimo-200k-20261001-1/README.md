# MiMo V2.6 Flash — first full 200K run on M5

The pinned MXFP4 artifact completed **200,000 actual input tokens and 256 output tokens** through the independent MLX-VLM text runtime. This first sample is valid throughput evidence for this configuration, but it is very slow after context fill. It is not a claim about every MiMo runtime or the M5's maximum performance. Two repetitions remain in the declared campaign.

| Measurement | Result |
|---|---:|
| Empty-cache context fill / first token | 638.938 s (10m 39s) |
| Prefill rate | 316.124 input tok/s |
| Post-fill generation | **0.30331 tok/s** |
| Generation phase after first token | 840.730 s (about 14m 01s) |
| Peak MLX allocation | 210.36 GiB |
| Swap growth during timed prefill/decode | 0 bytes |
| System swap growth over whole job, including load | 133,890,048 bytes (127.69 MiB) |

Whole-job and timed-phase memory observations have different boundaries. The system-wide swap increase during the broader job must not be reported as zero; it does not by itself establish model-attributed swapping or explain the slow decode. Peak MLX allocation is not the same measurement as process RSS. The minimum sampled available memory during the job was 80.18 GiB.

No context shortening, quantization substitution, MTP speculation or retry was applied. The generated fixed-token continuation, exact token hashes, model/runtime/source revisions, timings and settings are in [result.json](result.json). The [prefill timeline](prefill-timeline.json), [whole-job telemetry](campaign-telemetry.json) and [assessment](assessment.json) remain available.

Read-only runtime inspection confirms stock MLX attention calls and unquantized KV caches; that is not a profiler diagnosis. The specific bottleneck is unproven. The current second repetition is left intact, and any later optimized lane must be separately pinned and checked for correctness.
