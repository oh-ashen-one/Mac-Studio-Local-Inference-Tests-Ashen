# Setup status — existing M3 Ultra

**October 1 update:** the M5 has also been fully prepared; see [the paired setup receipt](M5-READY.md). Both computers remain unloaded by this task. The earlier checks below are historical preparation evidence.

**Current mode: preparation only. Downloads and file hashing are allowed; all inference is deferred.**

**All three models are now downloaded and fully SHA256 verified. The installation is in `prepared_not_loaded` state.**

This is preparation evidence, not the M3-versus-M5 benchmark report. The M5 order is owner-confirmed; that computer has not been inventoried or measured yet.

| Component | State |
|---|---|
| Python / MLX environment | Installed; exact dependency versions locked |
| DwarfStar Metal runtime | Built from pinned commit with fixed CPU target |
| Qwen 3.8 27B 8-bit | Downloaded and SHA256 verified; local generation, serving and token-timing pilot passed |
| Gemma 4 31B 8-bit | Downloaded and SHA256 verified; local generation, serving and token-timing pilot passed |
| DeepSeek V4 Flash 0731 Q4 | Downloaded and SHA256 verified; not loaded, per owner instruction |
| Harness unit/integration tests | 15 passed, including preparation-only guards and read-only preview HTTP checks |
| Comparison and report tool | Exercised with test fixtures; rejects mismatches, excludes smoke/warmup data |
| Standardized intelligence suites | Planned; not run |
| Controlled hardware performance comparison | Pending new Mac and quiet windows |
| SSH to new Mac | Pending physical setup / Remote Login on the new machine |

The eight original diagnostic tasks are deliberately small smoke checks, not a validated intelligence benchmark. Qwen passed 7/8; its incorrect state/arithmetic answer was retained. Gemma passed 8/8. These trials used greedy decoding and the requested no-thinking controls where supported. They do not establish a model ranking or a quantization quality guarantee.

Both MLX token-timing pilots produced exactly 512 input tokens and 32 output tokens. Pilot runs took place on a shared active machine, so their speeds are excluded from the comparison tool. The owner subsequently instructed that no models be loaded because other sessions are using the GPU. The queued native generation/timing checks were canceled before they started. DeepSeek runtime validation is deferred until the owner explicitly starts the tests. No local-model servers from this task remain running.

See [ARRIVAL.md](ARRIVAL.md) for the exact models, methods, commands and remaining campaign stages. The setup branch is `codex/setup-20260930`; [preparation PR #1](https://github.com/oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen/pull/1) is unmerged.

Preparation receipts: [machine readiness](../hardware/preparation-old.json), [file verification](../hardware/model-verification-old.json). Earlier diagnostic records are retained in [results/setup](../results/setup) so failures are not lost. They predate the owner's stop-inference instruction; no further model loads were performed after it.

The task-owned inference controllers and model servers are stopped. The three artifacts occupy 227,960,569,245 bytes (about 228 GB / 212.3 GiB). The local installation and files remain staged intentionally for tomorrow. The model files, virtual environment and native binaries are ignored by Git; their manifests and reconstruction commands are published.
