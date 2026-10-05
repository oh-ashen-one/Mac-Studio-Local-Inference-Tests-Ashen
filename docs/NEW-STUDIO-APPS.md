# New Studio desktop apps — October 1, 2026

Installed on the directly verified M5 Ultra (36-core CPU, 80-core GPU, 256 GB, 2 TB, macOS 27.0.1 build 26A434). The nine signed app bundles were transferred from the owner's original Studio to `/Applications` over authenticated, host-key-verified SSH. This matches the versions already in daily use instead of silently substituting unrelated apps or major upgrades.

| App | Version | Verification |
|---|---|---|
| Wispr Flow | 1.6.1021 | Signature valid; Gatekeeper accepted |
| Notion | 7.36.0 | Signature valid; Gatekeeper accepted |
| Screen Studio | 3.7.5-4595 | Signature valid; Gatekeeper accepted |
| Todoist | 9.30.0 | Signature valid; Gatekeeper accepted |
| Ghostty | 1.3.1 | Signature valid; Gatekeeper accepted |
| Notion Calendar | 1.139.0 | Signature valid; Gatekeeper accepted |
| Grok Bot | 0.61.0 | Signature valid; Gatekeeper accepted |
| ChatGPT | 26.928.31416 | Signature valid; Gatekeeper accepted |
| Claude | 2.16120.0 | Signature valid; Gatekeeper accepted |

“Wispr” is Wispr Flow, “Ghosty” is Ghostty, and “Grokbot” is the exact signed Grok Bot application found on the original machine. The current Codex desktop installation is named **ChatGPT.app**, with bundle ID `com.openai.codex`; no old standalone Codex build was substituted.

Only application bundles were copied. No user Library profiles, login sessions, API credentials, SSH private keys, browser data, model weights or background agent configurations were copied. Existing target applications would have been preserved. No app was launched, and no OS privacy permission was pre-approved or bypassed.

The apps are installed and statically verified, not signed in or GUI-tested. Wispr Flow may request microphone/accessibility permissions; Screen Studio requires its usual recording permissions and account/license setup. Those remain owner-controlled first-launch steps. SSH control works from the original Studio. No local model was loaded or benchmark run.

The new Mac currently lacks an active Apple command-line developer-tool installation. Benchmark runtime setup/model transfer to the new machine has **not** been performed as part of this app-install request. Existing benchmark model files remain staged on the original Studio. Use the preparation-only runbook when continuing, and preserve the explicit owner-start requirement for all inference.

Evidence: [app installation report](../hardware/new-studio-apps.json), [new-device inventory](../hardware/incoming-device.json). The install helper is `scripts/install_daily_apps.py`; it is an explicit one-time desktop provisioning command, not part of automatic benchmark preparation.
