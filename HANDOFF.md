# HANDOFF — Mac Studio comparison — paired model setup

Date: 2026-10-01 · Branch: `codex/m5-model-setup-20261001` · Host: original M3 Studio · Status: **Both machines prepared; inference not started**

## What this is

Prepare the owner's original M3 Ultra and new M5 Ultra for reproducible local-model comparisons and later content creation. The owner explicitly requires preparation only until they say to start: no model loads, inference servers or benchmarks. Review future results on localhost before any website publication.

## Repo / branch map

- Remote: `oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen`.
- Active checkout: `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github` on the original Studio.
- Current published task branch: `codex/m5-model-setup-20261001`.
- Previous benchmark preparation/default branch: `codex/setup-20260930`.
- No sibling checkout or stash was found by the handoff collector. Other active engine and infrastructure processes belong to other sessions; leave them untouched.

## Where things stand

Both machines now have the three locked model artifacts. All 34 files were SHA256 verified on the M5. The original files remain present and their earlier hash-verification receipt matches the same model lock; the benchmark runner rechecks integrity before loading. Python/package versions, native source revision, build flags, compiler version, and OS build match. Neither machine loaded a model during this setup.

The new machine is directly verified as Mac17,15 / M5 Ultra / 36 CPU cores / 80 GPU cores / 256 GB memory / 2 TB SSD, running macOS 27.0.1 build 26A434. SSH login from the original Studio works after the owner added the original machine's public key. The connection identity/address stays in the local SSH configuration/chat, not this public handoff.

All nine requested desktop apps are installed in `/Applications` on the new Studio: Wispr Flow, Notion, Screen Studio, Todoist, Ghostty, Notion Calendar, Grok Bot, ChatGPT (the current Codex desktop bundle), and Claude. Their versions match the signed bundles in daily use on the original Studio. All nine passed deep/strict code-signature verification and Gatekeeper assessment on the new machine.

## What happened this session

The M5 received the repository at `/Users/midirstudio2/mac-studio-inference-tests`, pinned Python environment, Apple Command Line Tools, a native DwarfStar build, and the full 228 GB model cohort. Direct pinned downloads replaced a slower wireless peer copy; the canceled partial was removed. Commits `86e79bb`, `743cf3f`, and `07c68b6` record the readiness guard, matched inventories and completed M5 preparation. [docs/M5-READY.md](docs/M5-READY.md) and the hardware receipts contain the detailed evidence.

Earlier commit `729c9bb` adds the explicit app provisioning helper, sanitized new-device inventory, app installation evidence and app setup notes. The helper transfers application bundles only, preserves existing target apps, validates their signatures/identities and never launches them. No Library profiles, credentials, browser sessions or agent configurations were copied.

## Verification done

- Live SSH login and hardware/OS/disk inventory succeeded on the new M5.
- Code-signature verification succeeded before transfer and after installation for all nine apps.
- Gatekeeper accepted all nine installed bundles.
- A separate final remote check found all nine app directories.
- The task did not open any apps, load local models or run benchmarks.
- 17 non-inference harness tests passed on both Macs. The native build completed on the M5. All 38 package versions match. Both Macs run macOS 27.0.1 build 26A434 and use Apple Clang 21.0.0 (clang-2100.3.34.2).
- The M5 readiness receipt is `prepared_not_loaded`; all 34 selected files passed SHA256 verification.
- Source/install evidence was committed and pushed. No local-only commits or stashes remain after this handoff is pushed.

## Not done / explicitly out of scope

- App sign-ins, license activations, microphone/accessibility/screen-recording approvals, and GUI launch testing are left to the owner.
- DeepSeek generation on either machine is still deferred by the owner's no-inference instruction.
- No controlled cross-machine performance comparison, cluster configuration, website merge or deployment has happened.

## Next steps

1. Let the owner sign in and approve normal first-use permissions for the new desktop apps.
2. Inspect both `work/READY.json` receipts and the current private `config/machines.local.json` routing adapter on the original Studio. The new M5 checkout is `/Users/midirstudio2/mac-studio-inference-tests`; its branch is `codex/m5-model-setup-20261001`. No further downloads are needed unless integrity checks identify a missing/corrupt file.
3. Inspect both live OS builds before measuring; do not silently upgrade/reboot a shared machine.
4. Wait for the owner's explicit current start instruction, then reserve resources and follow the current shared-brain GPU/ownership rules. Run one model at a time.
5. Review saved results through `scripts/preview.py` on localhost before publishing to the personal site.

## Key files

- `docs/M5-READY.md` and `hardware/pair-readiness.json` — completed paired preparation and remaining validation boundary.
- `docs/NEW-STUDIO-APPS.md` — installed versions and owner first-launch steps.
- `hardware/new-studio-apps.json` — signed-bundle installation and Gatekeeper evidence.
- `hardware/incoming-device.json` — sanitized live M5 inventory.
- `docs/ARRIVAL.md` and `AGENTS.md` — preparation-only protocol and owner-start gate.
- `config/models.lock.json` — exact three standard model artifacts; no substitutions.

## Running processes / infra

No model server, inference controller, benchmark or automation was left running. The model download process completed. A short loopback-only viewer test ran and closed during the non-inference test suite; no persistent listener remains from this task. Other sessions' processes and ports were preserved.

## Picking this up on the other machine

All project code, locks, docs and intentional evidence are on the task branch. App binaries are installed on the new Mac; account/session data was not migrated. Both Studios' `models/`, `.venv/`, native binaries and readiness receipts remain intentionally staged for the next test session. The new machine already has its own complete copies. These runtime inputs are ignored by Git; all manifests and intentional evidence are pushed. Do not delete this active preparation installation as abandoned work.

## Secrets

No credential values are recorded here. The owner authorized SSH with a public key; the original private key stayed on the original Studio. Use the existing SSH identity normally, never copy it to the new machine or publish it.

## Gotchas

The current Codex app appears as **ChatGPT.app**, bundle ID `com.openai.codex`. Grok Bot is the exact existing signed app, not an inferred replacement from an unrelated download. “Installed” here means bundle present and statically verified, not authenticated or launched. The no-inference instruction remains active even after app installation and remote access succeed.

## Resume command

Read HANDOFF.md in `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github` on branch `codex/m5-model-setup-20261001`; continue preparation only, preserve other sessions, and do not load models until the owner explicitly starts the tests.
