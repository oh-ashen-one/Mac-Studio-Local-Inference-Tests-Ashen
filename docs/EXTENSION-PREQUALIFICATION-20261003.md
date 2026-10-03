# Four-release extension prequalification

Metadata-only inspection found that every manifest-listed file in the four selected owner downloads exists and matches its declared byte size. Expected per-file hashes, snapshot identifiers, manifest/config hashes and limits are preserved in `hardware/extension-prequalification-20261003.json`. Tensor hashes remain unverified: the running MiMo measurement is preserved, and bulk reads must wait for an idle boundary. No new model has been loaded.

| Selected package | Config model type | Declared position limit | Next qualification issue |
|---|---|---:|---|
| Qwen 3.5 35B A3B | qwen3_5_moe | 262144 | Verify exact artifact encoding/tensor mapping and independent runtime |
| GPT-OSS20B | gpt_oss | 131072 | The declared 200K tasks exceed this limit; record unsupported context cells, never truncate or change RoPE to claim coverage. Check total input plus output allowance for the 131072-input speed condition too. |
| Bonsai2 27B | prism_hadamard_qwen35 | 262144 | Custom Hadamard architecture requires compatible independent support; no matching single-file module found in the existing MLX-LM environments. This is not yet proof no compatible runtime exists. |
| Nemotron3.5 Lightning | nemotron_h | 262144 | Verify exact artifact encoding/tensor mapping and independent runtime |

Single-file MLX-LM source modules for Qwen3.5, GPT-OSS and Nemotron exist in the pinned environments; their hashes are recorded. Presence is not qualification. The MLX-VLM single-file probe does not inventory package-directory implementations and must not be interpreted as absence of VLM support. No runtime import, provider activation, runtime update, weight conversion or inference occurred during this inspection.

Before admission: verify tensor hashes on the M5 while no timed group is running, preserve independent artifact/runtime locks, test compatible runtime setup with separately labeled qualification evidence, and declare any unsupported workload with concrete evidence. Keep the original full suite for supported cells. Do not substitute another quantization or silently relax output/context budgets.

## Independent Bonsai source candidate found

PrismML publishes a dedicated [`prism-hadamard-qwen35` MLX-LM branch](https://github.com/PrismML-Eng/mlx-lm/tree/38f27dc24b535928246b64b211b66d38b7a3e17f), pinned for evaluation at `38f27dc24b535928246b64b211b66d38b7a3e17f`. Its [model implementation](https://github.com/PrismML-Eng/mlx-lm/blob/38f27dc24b535928246b64b211b66d38b7a3e17f/mlx_lm/models/prism_hadamard_qwen35.py) explicitly checks pack schema/namespace, grouped activations and 2-bit affine/group128 encoding. This is a concrete independent runtime candidate, not a compatibility pass. Source hash and remaining gates are in `config/extension-runtime-candidates.json`.

The candidate has not been installed, imported or used for inference. Use a separate environment and pin its full resolved dependency set before qualification; preserve baseline environments unchanged. Do not replace the downloaded artifact with the vendor's GGUF alternative.

A metadata-only check of the verified downloaded Bonsai config found schema2, namespace `mlx-vlm-qwen3_5`, grouped GDN activations, 2-bit affine/group128 encoding and402 packed module records. These match the candidate loader's initial declared schema conditions. Tensor-name/shape validation and numerical/runtime qualification are still pending; no model/runtime import was performed for this check.
