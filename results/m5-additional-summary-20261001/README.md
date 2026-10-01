# Additional M5 model results

Median of complete 200K-input, 256-output, empty-KV-cache text runs; model load/tokenization excluded.

No original M3 inference; no matched chip-only percentage.

| Configuration | 200K samples | Fill median | Prefill median | Decode median (range) | Peak MLX | Swap growth |
|---|---:|---:|---:|---:|---:|---:|
| Xiaomi: MiMo-V2.6-Flash · mxfp4 catalog; 4-bit config default | 0/3 | Pending | Pending | Pending | Pending | Pending |
| Qwen 3.6 35B A3B · fp4 catalog; 4-bit config default | 3/3 | 66.69 s | 3001.24 tok/s | **79.78** (79.64–79.96) | 23.98 GiB | 0 bytes |

## Xiaomi: MiMo-V2.6-Flash

Repository diagnostic: **0/0 completed attempts passed**, of five planned. Infrastructure failures: 0; human rescues: 0. Same historical Django bug, 19 immutable tests, 200K starting context, eight turns, 2048 output tokens per turn, temperature 0.2, seeds 1001–1005. This is a narrow diagnostic, not a general intelligence score.

Saved evidence:

- [m5-mimo-pilot-vlm-20261001](../../results/m5-mimo-pilot-vlm-20261001/result.json) — runtime_validation, failed, failed.
- [m5-mimo-pilot-vlm-base-20261001](../../results/m5-mimo-pilot-vlm-base-20261001/result.json) — runtime_validation, complete, did not pass.

## Qwen 3.6 35B A3B

Repository diagnostic: **0/0 completed attempts passed**, of five planned. Infrastructure failures: 0; human rescues: 0. Same historical Django bug, 19 immutable tests, 200K starting context, eight turns, 2048 output tokens per turn, temperature 0.2, seeds 1001–1005. This is a narrow diagnostic, not a general intelligence score.

Saved evidence:

- [m5-qwen36-200k-20261001-1](../../results/m5-qwen36-200k-20261001-1/result.json) — long_context, complete, complete.
- [m5-qwen36-200k-20261001-2](../../results/m5-qwen36-200k-20261001-2/result.json) — long_context, complete, complete.
- [m5-qwen36-200k-20261001-3](../../results/m5-qwen36-200k-20261001-3/result.json) — long_context, complete, complete.
- [m5-qwen36-pilot-20261001](../../results/m5-qwen36-pilot-20261001/result.json) — runtime_validation, complete, did not pass.
- [m5-qwen36-pilot-vlm-20261001](../../results/m5-qwen36-pilot-vlm-20261001/result.json) — runtime_validation, complete, passed.

## Runtime and interpretation

Qwen’s initial MLX-LM loader produced gibberish. The separately pinned MLX-VLM loader passed. MiMo initially rejected optional MTP tensors; the adapter excludes precisely 42 draft tensors while retaining strict checks for every base weight. Its base-model validation answered correctly but fenced its JSON, so strict formatting failed. Those original records remain intact. No model files were edited; MTP speculation is disabled.

Official AA attached-server replays use recorded output caps because this MLX server does not implement ignore_eos. The exact-output cell is unsupported, and recorded-policy results are not directly comparable to the original Q4_K_M managed replay. Serving completed turns does not mean solving tasks.

The original three model configurations and their results remain separate. Darkbloom’s provider is off. The original M3 remains occupied. Results are for local/GitHub review; no website deployment has occurred.
