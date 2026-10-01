# Mac Studio benchmark handoff

## Default action: prepare only

The owner wants to open this chat later and say “start.” Other sessions use the GPU. **Do not load any model, run inference, start a model server, or run smoke/pilot/quality/benchmark commands just because you read this repository.** Do not launch renderer-bearing apps or change memory limits. Do not touch another session's processes.

When asked to prepare a new Mac from this README, run `bash scripts/prepare.sh`. It installs pinned dependencies, builds the native command-line runtime if necessary, downloads the three locked artifacts, verifies SHA256 and writes `work/READY.json`. It never loads a model. If Apple's developer-tool installation needs a macOS dialog, explain that one prerequisite and finish all independent preparation first. Do not ask for passwords, tokens or private SSH keys in chat.

If `work/READY.json` already exists, inspect it, the lock hashes and local file state before repeating downloads. Reading metadata and hashing files is allowed in preparation mode. Continue incomplete downloads with the same pinned revisions. Keep the required models and this active installation ready for the owner; remove only task-owned canceled/duplicate downloads and disposable staging files.

## Start only on the owner's explicit request

When the owner explicitly says to start the tests in the current chat, recheck host identity, free memory, swap, other GPU/engine activity and the owner's reserved window. Start one model at a time. Commands that generate tokens require `--allow-inference`; this flag is a guard, not permission to ignore the owner's current instruction. The owner explicitly halted model loading during preparation on September 29, 2026.

First inspect both device inventories and confirm identical files/runtime revisions. Run the small validation stage before the full campaign. Preserve every failure and do not label setup/pilot data as benchmark results. Render the actual comparison locally with `scripts/preview.py` for owner review **before** publishing results to the personal website. Do not merge the website PR or deploy by inference from benchmark authorization.

## Repository and model scope

The GitHub remote is authoritative. Work on your own branch, push all project changes in the session, and do not merge into `main` without explicit owner permission. The paired preparation branch is `codex/m5-model-setup-20261001`. Both devices are inventoried and staged; read HANDOFF.md and docs/M5-READY.md for the current state. Do not reset/rebase/overwrite collaborators' work.

Exactly three standard model configurations are selected in `config/models.lock.json`: Qwen 3.8 27B 8-bit MLX, Gemma 4 31B 8-bit MLX, and DeepSeek V4 Flash 0731 mixed Q4 through DwarfStar/Metal. No Mistral, no abliterated models, no automatic model upgrades. Any variant/version change creates a new cohort on **both** machines.

Weights, caches and virtual environments stay out of Git. Model and runtime revisions, file hashes, preparation tools, sanitized inventories and intentional result releases are versioned. The incoming order is owner-confirmed: M5 Ultra, 36 CPU cores, 80 GPU cores, 32 Neural Engine cores, 256 GB, 2 TB. The delivered hardware was directly inventoried on October 1, 2026.
