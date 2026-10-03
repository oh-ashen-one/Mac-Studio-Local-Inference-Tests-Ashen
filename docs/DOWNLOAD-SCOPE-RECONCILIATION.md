# Recorded download-scope reconciliation

Prepared October 2, 2026 (owner timezone) from existing saved records only, at Midir's request. No fresh machine/model-storage scan, download, inference, runtime change or additional check job was performed for this clarification.

## Finding

**The original owner estimate of roughly ten additional downloaded models was not fully reconciled against an itemized owner-selected list.** The saved evidence positively identifies **two independent additional language checkpoints**, and verifies that the identified two-checkpoint batch completed. Those are different claims. The records do not establish that all of the owner's estimated ten were located, nor that exactly eight others exist or failed.

| Located independent checkpoint | Saved artifact revision and source | Verified package |
|---|---|---|
| MiMo V2.6 Flash | `XiaomiMiMo/MiMo-V2.6-Flash-RL`; artifact `2026-09-28-r1`; manifest SHA256 `2334547d8acc9898ad4a74570ce44d2b12390bbac8d4bc52c092eb5ad5cfe034` | MLX; catalog MXFP4 / 4-bit default; 172,863,462,401 bytes including components; 53 verified files |
| Qwen 3.6 35B A3B | `Qwen/Qwen3.6-35B-A3B`; artifact `2026-08-11-r1`; source revision `73a03825c2226177f3e679210965dba3508cdee8`; manifest SHA256 `d932e96b00404b0575fff47e2dac8ed113056b3f22d0040c3c8d3f9ef25b09ed` | MLX; catalog FP4 / affine 4-bit default despite legacy `mxfp8` package identifier; 21,308,856,601 bytes; 13 verified files |

MiMo's upstream Git source revision is not supplied in the lock (`source_revision: null`); its exact downloaded artifact is pinned by manifest and file hashes. Do not invent an upstream commit.

## What the records establish

- Saved inventory at **2026-10-01 21:03:27 UTC** showed MiMo, its `audio_tokenizer` component, and a partial/staging Qwen package with two of four main shards present. The component is part of MiMo, not a third independent language model. The snapshot remains local in `work/download-inventory-new.json`.
- The explicit owner-authorized **Qwen download-only retry completed successfully** at **21:21:30 UTC on October 1**, exit code zero: [retry receipt](../hardware/qwen-download-retry.json). Its earlier download failure was resolved; the failed runtime loader pilot is a separate preserved setup issue, not a failed download.
- [File verification](../hardware/additional-model-verification.json) records **53 MiMo + 13 Qwen files = 66 SHA256-verified files**. Its top-level active-file counter is the last model's counter; use the per-model records for the total. Files and numbered shards are not separate models.
- [Completion receipt at 2026-10-02 01:52:06 UTC](../hardware/additional-completion-receipt.json) lists only the two identified manifest directories and no incomplete markers. This is a dated observation of the identified batch, not proof that no model exists elsewhere or that no later download arrived.
- [Saved research inventory](../research/additional-models.json) retains `owner_reported_model_count: 10` alongside only two verified model entries.
- The manager-cited eleven-entry catalog describes available packages. Catalog membership alone does not establish selection, a download attempt, local file presence or completion.

## Residual scope

**Unresolved:** identities and locations of any other models intended by the owner's roughly-ten estimate. There is no saved itemized remainder that supports labeling particular additional checkpoints as downloaded, failed, incomplete, excluded or queued.

**Known named download still failed/incomplete:** none among the two verified additional checkpoints at the saved completion check.

**Known independent downloaded checkpoint excluded or queued outside the frozen six:** none established by these records. This is an evidence limit, not a global filesystem absence claim.

**Components/conditions excluded from separate model counting:** MiMo audio tokenizer, optional draft/MTP components, shards and catalog-only entries. The active text benchmark does not claim vision/audio testing or speculative decoding coverage.

## Why the active campaign has six configurations

The [unified lock](../config/unified-models.lock.json) contains the original three configurations (Qwen 3.8 27B 8-bit, Gemma 4 31B 8-bit, DeepSeek V4 Flash mixed Q4), the two verified additional checkpoints above, and the separately downloaded Qwen 3.8 Q4_K_M GGUF variant used with llama.cpp. That totals **six configurations spanning five base model identities**, not six additional Darkbloom models.

Keep the frozen campaign running under its existing methodology and cadence. Its completion will establish coverage of the six identified configurations; it will **not by itself close the unresolved original download-count question**. Any future reconciliation or expanded cohort must be recorded separately without rewriting the current cohort or pretending catalog entries were downloaded.


## Authorized current metadata update — October 3 01:20 UTC / October 2 9:20 PM EDT

Following the explicit owner resume through Midir, the existing inventory script was run on the verified M5 with `--include-darkbloom-model-files`. It inspected filenames, configs, sizes and completion markers only; no provider/app launch, new download, weight hash, model load or test was introduced for inventory. [Current receipt](../hardware/download-scope-current-20261003.json).

The documented cache roots again contain **two independent additional checkpoints**: MiMo V2.6 Flash and Qwen 3.6 35B A3B, plus the MiMo audio-tokenizer component. The Hugging Face root is readable with no incomplete markers; the six other documented LM Studio/Darkbloom model-root locations are absent. All six campaign configurations have their expected files and sizes; no unmatched GGUF was found in project model storage. This metadata update does not replace earlier SHA256 verification or claim that other unspecified locations were scanned.

Both additional checkpoints were tested in the earlier two-model campaign and are selected in the active six-configuration campaign. The original three configurations and the Qwen 3.8 Q4 variant also remain selected. No concrete downloaded independent checkpoint omitted from that matrix was identified in these locations. No known unresolved failed/incomplete download was identified; the earlier Qwen download failure remains resolved. The owner estimate of roughly ten still lacks an itemized selection or location record, so the original broader scope is not conclusively closed. No catalog entry or component was promoted to a downloaded model, and the frozen six were not expanded.
