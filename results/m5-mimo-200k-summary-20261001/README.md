# MiMo V2.6 Flash — three 200K speed runs on M5

**Retrospective correction, October 2:** this archived direct-generation profile omitted normal MLX process memory wiring. Its slow numbers remain valid records of that unwired harness, but do not represent normal resident inference. A separately labeled setup probe reached 37.5743 tok/s with identical input/output token IDs. [The new repeated study](../unified-overnight-20261002/README.md) remains separate; original raw measurements and task outcomes are unchanged. The observations below describe the original run at the time.

All three fresh-process runs completed 200,000 actual input tokens and 256 output tokens using the same pinned MXFP4 artifact, independent text runtime and input token-ID hash. Empty KV/state cache was used; this does not imply a cold filesystem or reboot. Model loading and tokenization are outside the timed fill/decode interval.

| Repeat | Context fill | Input tok/s | Output tok/s | Peak MLX | Timed system swap change |
|---|---:|---:|---:|---:|---:|
| [1](../m5-mimo-200k-20261001-1/result.json) | 638.938 s | 316.124 | 0.30331 | 210.36 GiB | 0 bytes |
| [2](../m5-mimo-200k-20261001-2/result.json) | 543.158 s | 371.427 | 0.39819 | 210.36 GiB | 0 bytes |
| [3](../m5-mimo-200k-20261001-3/result.json) | 523.893 s | 385.187 | 0.41286 | 210.36 GiB | -8,388,608 bytes |

Median: **0.39819 output tok/s**, **543.158s fill**, **371.427 input tok/s**. The observed output-rate range is 0.30331–0.41286 tok/s. Output token-ID sequences were identical across the three runs.

The slowdown is reproducible in this exact configuration. Its cause is not established, and no profiler or optimization changed these baseline runs. These results do not establish a model-quality score or the maximum performance possible with another runtime. The same bounded repository and official replay stages follow.

No timed phase showed swap growth; repeat 3 ended with 8 MiB less system swap. Whole-job telemetry includes loading: the first run observed 127.69 MiB maximum system swap growth, the second 1.75 MiB; see [summary.json](summary.json) for all boundaries. These are system-wide measurements, not model-attributed swap. Peak MLX allocation is distinct from process RSS.

[First-sample interpretation](../m5-mimo-200k-20261001-1/README.md) retains the original n=1 assessment. All raw outputs, prefill timelines, model/runtime/source hashes and telemetry are preserved in the per-run directories.
