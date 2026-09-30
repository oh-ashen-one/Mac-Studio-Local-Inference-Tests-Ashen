# Candidate selection and model provenance

Freeze the final manifest after arrival-day compatibility pilots. These are candidates checked against model/project sources on September 29, 2026, not an exhaustive ranking of the newest models.

| Candidate | Role | First experiment |
|---|---|---|
| [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Small dense control | Supported 4-/8-bit; BF16 quality reference |
| [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | Current everyday/game-loop anchor | 4-/8-bit, BF16 reference if supported |
| [Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | Coding MoE control | 4-/8-bit, tool-call correctness |
| [Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) | Non-Qwen larger dense control | 4-bit then higher precision; license/access check |
| [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | Recent sparse/hybrid candidate | Architecture, table residency and backend support check first |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | Large-capacity comparison | Supported 4-bit; short context first |
| [Qwen3-Coder-480B-A35B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct) | Large coding cluster candidate | Cluster allocation/correctness pilot |
| [DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2) | Third family, 671B cluster stretch | Confirm complete architecture support before download |

If the third family cannot run, select a smaller supported non-Qwen/non-Llama family before locking the quality cohort. Record the reason; do not imply the initial shortlist already covers three runnable families.

For each selected artifact, record repository ID, immutable commit, all weight-file SHA256 hashes, exact bytes, tokenizer/template hashes, base model revision, model license, quantizer/converter revision, calibration provenance, quantization method/group size, mixed-precision exceptions, KV precision, total and active parameter counts, supported context, thinking controls and backend compatibility.

Treat compressed/distilled/pruned/abliterated/retrained variants as different models, not merely quantization levels. Use documented original checkpoints as the primary baseline. Check converters against official architecture configs. Publish a manifest before measurement; moving `main` or a friendly LM Studio alias is not reproducible identity.

Aim for 6–8 final model/configuration representatives, with at least three cross-machine speed anchors. Do not run the full Cartesian product for all giant models. First select a quality/latency frontier from the pilot, then use targeted sweeps to explain trade-offs. Keep rejected candidates and compatibility failures in the report.

Model cards establish published architecture and intended use; they do not prove our machine's speed or quality. No vendor score is copied into our measured-results columns.
