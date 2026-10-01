# HANDOFF — Mac Studio long-context campaign

Date: 2026-10-01 · Branch: `codex/long-context-dashboard-20261001` · Host: original M3 Studio · Status: **M5 200K campaign in progress; M3 blocked by other sessions**


## Current owner instruction and active work

The owner authorized the long-context/agent/multitasking campaign and confirmed the M3 GPU is occupied. Do not run inference on the original M3 or stop its other sessions. Continue sequential tests on the verified M5. Darkbloom installation is last. The previous initial M5 results below remain valid history, but statements that every model is unloaded no longer describe the active run.

- Qwen 200K completed: 214.47 seconds to fill, 933.63 input tok/s, 21.44 post-fill output tok/s, zero swap growth.
- Gemma 200K completed: 314.93 seconds to fill, 635.74 input tok/s, 15.41 post-fill output tok/s, zero swap growth.
- DeepSeek 200K is running on the M5, owned driver `scripts/long_context.py`, run ID `m5-deepseek-200k-20261001`. Check the live JSON/process before doing anything; do not restart blindly.
- The M5 hostname changed. Read ignored `config/machines.local.json` on the controller for verified routing, preserving the existing SSH host identity.
- `docs/LONG-CONTEXT-CAMPAIGN.md` records exact methodology, outstanding agent/Blender/repo tasks and interpretation limits.
- Visual dashboard source now prioritizes 200K metrics, waiting-time bars, source-linked external references and collapsed transcripts. The readonly localhost server must be restarted after updating its Python source.
- External peer reports are reference configurations, not a matched hardware leaderboard. No measured M3/M5 percentage exists yet.

## Previous setup and first-look history

## What this is

Prepare the owner's original M3 Ultra and new M5 Ultra for reproducible local-model comparisons and later content creation. The owner explicitly authorized sequential M5 tests on October 1. Those three model tests are now complete. Do not start further inference merely by reading this handoff. Review future results on localhost before any website publication.

## Repo / branch map

- Remote: `oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen`.
- Active checkout: `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github` on the original Studio.
- Current published task branch: `codex/long-context-dashboard-20261001`.
- Previous benchmark preparation/default branch: `codex/setup-20260930`.
- No sibling checkout or stash was found by the handoff collector. Other active engine and infrastructure processes belong to other sessions; leave them untouched.

## Where things stand

Both machines now have the three locked model artifacts. All 34 files were SHA256 verified on the M5. The original files remain present and their earlier hash-verification receipt matches the same model lock; the benchmark runner rechecks integrity before loading. Python/package versions, native source revision, build flags, compiler version, and OS build match. The M5 subsequently ran Qwen, Gemma and DeepSeek sequentially; the M3 was not benchmarked. Models are unloaded again.

The new machine is directly verified as Mac17,15 / M5 Ultra / 36 CPU cores / 80 GPU cores / 256 GB memory / 2 TB SSD, running macOS 27.0.1 build 26A434. SSH login from the original Studio works after the owner added the original machine's public key. The connection identity/address stays in the local SSH configuration/chat, not this public handoff.

All nine requested desktop apps are installed in `/Applications` on the new Studio: Wispr Flow, Notion, Screen Studio, Todoist, Ghostty, Notion Calendar, Grok Bot, ChatGPT (the current Codex desktop bundle), and Claude. Their versions match the signed bundles in daily use on the original Studio. All nine passed deep/strict code-signature verification and Gatekeeper assessment on the new machine.

## What happened this session

The owner requested a live localhost dashboard on the M5 and one-by-one tests. The run used a shared GPU slot on the M5 only, one model at a time. Each model performed a 512-input / 256-output speed probe (one warmup plus three measured repeats), followed by one real Python coding request through a temporary local server. Execution source was `a69a3a9`. Results and logs are versioned under `results/m5-firstlook-20261001`.

Peak / median decode rates: Qwen **32.05 / 32.02 tok/s**, Gemma **27.63 / 27.59**, DeepSeek **63.83 / 63.71**. Real first-output latency: **1.62 / 1.55 / 0.67 seconds**. Qwen hit its 512-token response cap; the other two responses stopped normally. This is an initial interactive run with Photos/iCloud activity and Safari present, not an absolute maximum, intelligence ranking or M3 comparison.

The localhost dashboard was opened in Safari on the **new M5** and its HTTP request was confirmed in the remote viewer log. Published records redact local runtime paths. RSS undercounts DwarfStar’s mapped model, so the dashboard shows observed system-memory change instead, with the limitation stated.

The M5 received the repository at `/Users/midirstudio2/mac-studio-inference-tests`, pinned Python environment, Apple Command Line Tools, a native DwarfStar build, and the full 228 GB model cohort. Direct pinned downloads replaced a slower wireless peer copy; the canceled partial was removed. Commits `86e79bb`, `743cf3f`, and `07c68b6` record the readiness guard, matched inventories and completed M5 preparation. [docs/M5-READY.md](docs/M5-READY.md) and the hardware receipts contain the detailed evidence.

Earlier commit `729c9bb` adds the explicit app provisioning helper, sanitized new-device inventory, app installation evidence and app setup notes. The helper transfers application bundles only, preserves existing target apps, validates their signatures/identities and never launches them. No Library profiles, credentials, browser sessions or agent configurations were copied.

## Verification done

- Live SSH login and hardware/OS/disk inventory succeeded on the new M5.
- Code-signature verification succeeded before transfer and after installation for all nine apps.
- Gatekeeper accepted all nine installed bundles.
- A separate final remote check found all nine app directories.
- The initial M5 campaign completed all three models successfully; nine measured speed repeats and three real transactions are retained. Safari loaded the results on the new Mac.
- 18 harness tests passed on the controller after adding the first-look reporting checks; the prior 17 preparation tests had passed on both Macs. The native build completed on the M5. All 38 package versions match. Both Macs run macOS 27.0.1 build 26A434 and use Apple Clang 21.0.0 (clang-2100.3.34.2).
- The M5 readiness receipt is `prepared_not_loaded`; all 34 selected files passed SHA256 verification.
- Source/install evidence was committed and pushed. No local-only commits or stashes remain after this handoff is pushed.

## Not done / explicitly out of scope

- App sign-ins, license activations, microphone/accessibility/screen-recording approvals, and GUI launch testing are left to the owner.
- M3 inference in a controlled matched campaign remains pending. M5 DeepSeek generation now has direct successful-run evidence.
- No cross-machine speedup measurement, cluster configuration, standardized quality evaluation, website merge or deployment has happened.

## Next steps

1. Review the completed results on the M5 localhost dashboard and `results/m5-firstlook-20261001/README.md`.
2. Inspect both `work/READY.json` receipts and the current private `config/machines.local.json` routing adapter on the original Studio. The new M5 checkout is `/Users/midirstudio2/mac-studio-inference-tests`; its branch is `codex/long-context-dashboard-20261001`. No further downloads are needed unless integrity checks identify a missing/corrupt file.
3. Inspect both live OS builds before measuring; do not silently upgrade/reboot a shared machine.
4. For another campaign, obtain the owner's current run instruction, inspect other sessions, and follow current shared-brain slot rules. Do not benchmark the M3 while another session owns its GPU.
5. Review saved results through `scripts/preview.py` on localhost before publishing to the personal site.

## Key files

- `results/m5-firstlook-20261001/README.md` and `summary.json` — actual M5 results, responses and limitations.
- `scripts/first_test.py` — sequential fixed-probe + real-transaction runner; requires `--allow-inference` and a fresh campaign ID.
- `docs/M5-READY.md` and `hardware/pair-readiness.json` — completed paired preparation and remaining validation boundary.
- `docs/NEW-STUDIO-APPS.md` — installed versions and owner first-launch steps.
- `hardware/new-studio-apps.json` — signed-bundle installation and Gatekeeper evidence.
- `hardware/incoming-device.json` — sanitized live M5 inventory.
- `docs/ARRIVAL.md` and `AGENTS.md` — preparation-only protocol and owner-start gate.
- `config/models.lock.json` — exact three standard model artifacts; no substitutions.

## Running processes / infra

The M5 viewer is intentionally running at `http://127.0.0.1:18765` (PID 5621 when last verified), serving saved results only. Its Safari window is open on that machine. All task-owned inference/model-server processes exited and the shared GPU holder was released. No automation was created. Other sessions' processes and ports were preserved.

## Picking this up on the other machine

All project code, locks, docs and intentional evidence are on the task branch. App binaries are installed on the new Mac; account/session data was not migrated. Both Studios' `models/`, `.venv/`, native binaries and readiness receipts remain intentionally staged for the next test session. The new machine already has its own complete copies. These runtime inputs are ignored by Git; all manifests and intentional evidence are pushed. Do not delete this active preparation installation as abandoned work.

## Secrets

No credential values are recorded here. The owner authorized SSH with a public key; the original private key stayed on the original Studio. Use the existing SSH identity normally, never copy it to the new machine or publish it.

## Gotchas

The current Codex app appears as **ChatGPT.app**, bundle ID `com.openai.codex`. Grok Bot is the exact existing signed app, not an inferred replacement from an unrelated download. “Installed” here means bundle present and statically verified, not authenticated or launched. The completed campaign does not authorize automatic repeats. The viewer is read-only. MLX health probing initially logged a missing empty HF cache directory; the successful transactions and diagnostic logs are retained, and future runs create a task-local empty cache first.

## Resume command

Read HANDOFF.md in `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github` on branch `codex/long-context-dashboard-20261001`; review the completed M5 results, preserve the running localhost viewer and other sessions, and wait for the owner before another inference run.