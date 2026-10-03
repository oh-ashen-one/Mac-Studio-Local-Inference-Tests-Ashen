# Additional M5 model results

**Archived phase; the six-configuration unified campaign is still active.** Historical direct MLX speed profile omitted normal process memory wiring. MiMo 0.30-0.41 tok/s describes that unwired harness, not normal resident inference. A separate recommended-residency setup probe reached 37.5743 tok/s with identical input/output token IDs; the unified repeated study is separate. Original repository/replay outcomes are unchanged. [Current protocol](../../docs/UNIFIED-OVERNIGHT-PROTOCOL.md) · [Current coverage](../unified-overnight-20261002/README.md).

**Identified additional cohort complete.** All 22 tracked cells are handled, including the preserved failed MiMo qualification and its unrun unsupported original full profile. Complete means accounted for, not every task passed. The final completion check found no task-owned inference processes; see the saved completion receipt.

Median of complete 200K-input, 256-output, empty-KV-cache text runs; model load/tokenization excluded. Swap column covers timed prefill/decode only; whole-job loading observations are reported separately when available.

No original M3 inference; no matched chip-only percentage.

| Configuration | 200K samples | Fill median | Prefill median | Decode median (range) | Peak MLX | Swap growth |
|---|---:|---:|---:|---:|---:|---:|
| Xiaomi: MiMo-V2.6-Flash · mxfp4 catalog; 4-bit config default | 3/3 | 543.16 s | 371.43 tok/s | **0.40** (0.30–0.41) | 210.36 GiB | 0 bytes |
| Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates) · 4-bit affine MLX, group size 64; gate/shared-expert-gate overrides use 8 bits | 3/3 | 66.69 s | 3001.24 tok/s | **79.78** (79.64–79.96) | 23.98 GiB | 0 bytes |

## Xiaomi: MiMo-V2.6-Flash

Repository diagnostic: **0/5 completed attempts passed**, of five planned. Infrastructure failures: 0; human rescues: 0. Same historical Django bug, 19 immutable tests, 200K starting context, eight turns, 2048 output tokens per turn, temperature 0.2, seeds 1001–1005. This is a narrow diagnostic, not a general intelligence score.

Saved evidence:

- [m5-mimo-200k-20261001-1](../../results/m5-mimo-200k-20261001-1/result.json) — long_context, complete, complete.
- [m5-mimo-200k-20261001-2](../../results/m5-mimo-200k-20261001-2/result.json) — long_context, complete, complete.
- [m5-mimo-200k-20261001-3](../../results/m5-mimo-200k-20261001-3/result.json) — long_context, complete, complete.
- [m5-mimo-pilot-vlm-20261001](../../results/m5-mimo-pilot-vlm-20261001/result.json) — runtime_validation, failed, failed.
- [m5-mimo-pilot-vlm-base-20261001](../../results/m5-mimo-pilot-vlm-base-20261001/result.json) — runtime_validation, complete, did not pass.
- [m5-repo-mimo-20261001-1](../../results/m5-repo-mimo-20261001-1/result.json) — repo_task, complete, did not pass.
- [m5-repo-mimo-20261001-2](../../results/m5-repo-mimo-20261001-2/result.json) — repo_task, complete, did not pass.
- [m5-repo-mimo-20261001-3](../../results/m5-repo-mimo-20261001-3/result.json) — repo_task, complete, did not pass.
- [m5-repo-mimo-20261001-4](../../results/m5-repo-mimo-20261001-4/result.json) — repo_task, complete, did not pass.
- [m5-repo-mimo-20261001-5](../../results/m5-repo-mimo-20261001-5/result.json) — repo_task, complete, did not pass.

Whole-job system swap observations (including loading; distinct from timed-phase swap above):

- m5-mimo-200k-20261001-2: 1,835,008 bytes increase. System-wide observation, not process attribution.
- m5-mimo-200k-20261001-3: 1,835,008 bytes increase. System-wide observation, not process attribution.
- m5-mimo-200k-20261001-1: 133,890,048 bytes increase. System-wide observation, not process attribution.

Replay cells (serving only, not tasks solved):

- [aa-mini-v1](../../results/m5-aa-mimo-mini-recorded-20261001/run.json) — failed; 1/6 turns served; 6 short-output warnings; output policy recorded. Context evidence: model-not-listed, observed limit None. Not directly comparable to the original managed exact-output cohort.
- [agentperf-default-v1](../../results/m5-aa-mimo-full-xml-v2-recorded-20261001/run.json) — complete; 168/168 turns served; 11 short-output warnings; output policy recorded. Context evidence: model-not-listed, observed limit None. Not directly comparable to the original managed exact-output cohort.
- [agentperf-default-v1](../../results/m5-aa-mimo-full-recorded-20261001/run.json) — unsupported; 0/0 turns served; 0 short-output warnings; output policy recorded. Context evidence: not recorded, observed limit None. Not directly comparable to the original managed exact-output cohort.
- [aa-mini-v1](../../results/m5-aa-mimo-mini-xml-v2-recorded-20261001/run.json) — complete; 6/6 turns served; 6 short-output warnings; output policy recorded. Context evidence: model-not-listed, observed limit None. Not directly comparable to the original managed exact-output cohort.

## Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates)

Repository diagnostic: **4/5 completed attempts passed**, of five planned. Infrastructure failures: 0; human rescues: 0. Same historical Django bug, 19 immutable tests, 200K starting context, eight turns, 2048 output tokens per turn, temperature 0.2, seeds 1001–1005. This is a narrow diagnostic, not a general intelligence score.

Saved evidence:

- [m5-qwen36-200k-20261001-1](../../results/m5-qwen36-200k-20261001-1/result.json) — long_context, complete, complete.
- [m5-qwen36-200k-20261001-2](../../results/m5-qwen36-200k-20261001-2/result.json) — long_context, complete, complete.
- [m5-qwen36-200k-20261001-3](../../results/m5-qwen36-200k-20261001-3/result.json) — long_context, complete, complete.
- [m5-qwen36-pilot-20261001](../../results/m5-qwen36-pilot-20261001/result.json) — runtime_validation, complete, did not pass.
- [m5-qwen36-pilot-vlm-20261001](../../results/m5-qwen36-pilot-vlm-20261001/result.json) — runtime_validation, complete, passed.
- [m5-repo-qwen36-20261001-1](../../results/m5-repo-qwen36-20261001-1/result.json) — repo_task, complete, passed.
- [m5-repo-qwen36-20261001-2](../../results/m5-repo-qwen36-20261001-2/result.json) — repo_task, complete, passed.
- [m5-repo-qwen36-20261001-3](../../results/m5-repo-qwen36-20261001-3/result.json) — repo_task, complete, passed.
- [m5-repo-qwen36-20261001-4](../../results/m5-repo-qwen36-20261001-4/result.json) — repo_task, complete, did not pass.
- [m5-repo-qwen36-20261001-5](../../results/m5-repo-qwen36-20261001-5/result.json) — repo_task, complete, passed.

Whole-job system swap observations (including loading; distinct from timed-phase swap above):

- m5-qwen36-200k-20261001-3: 0 bytes increase. System-wide observation, not process attribution.
- m5-qwen36-200k-20261001-2: 0 bytes increase. System-wide observation, not process attribution.

Replay cells (serving only, not tasks solved):

- [agentperf-default-v1](../../results/m5-aa-qwen36-full-recorded-20261001/run.json) — complete; 168/168 turns served; 10 short-output warnings; output policy recorded. Context evidence: model-not-listed, observed limit None. Not directly comparable to the original managed exact-output cohort.
- [aa-mini-v1](../../results/m5-aa-qwen36-mini-recorded-20261001/run.json) — complete; 6/6 turns served; 3 short-output warnings; output policy recorded. Context evidence: model-not-listed, observed limit None. Not directly comparable to the original managed exact-output cohort.

## Runtime and interpretation

Qwen’s initial MLX-LM loader produced gibberish. The separately pinned MLX-VLM loader passed. MiMo initially rejected optional MTP tensors; the adapter excludes precisely 42 draft tensors while retaining strict checks for every base weight. Its base-model validation answered correctly but fenced its JSON, so strict formatting failed. Those original records remain intact. No model files were edited; MTP speculation is disabled.

Official AA attached-server replays use recorded output caps because this MLX server does not implement ignore_eos. The exact-output cell is unsupported, and recorded-policy results are not directly comparable to the original Q4_K_M managed replay. Serving completed turns does not mean solving tasks.

The original three model configurations and their results remain separate. Darkbloom’s provider is off. The original M3 remains occupied. Results are for local/GitHub review; no website deployment has occurred.
