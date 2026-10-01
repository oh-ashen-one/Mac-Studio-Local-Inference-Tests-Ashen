# HANDOFF — M5 long-context and real-work campaign

Updated 2026-10-01. Controller: verified original M3 Studio. Branch: `codex/long-context-dashboard-20261001`. Public repository: `oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen`. Review: [draft PR #3](https://github.com/oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen/pull/3), based on the initial M5-test branch. No merge or personal-site deployment authorized/performed.

## Owner instruction and boundaries

The owner explicitly authorized M5 inference and requested 200K input, prefill/decode metrics, agent replay, Blender multitasking, real repository completion and external hardware comparisons. They explicitly confirmed other sessions still use the original M3 GPU. **Do not run M3 inference or touch those sessions.** Its CPU-only preparation is complete.

**Latest owner steering:** roughly ten additional models are downloading somewhere on the M5, and the owner wants them tested after completion. Their app/path is unknown. Read-only metadata checks found two MiMo file groups in the HF cache, not the complete set. Do not interrupt downloads, load partial artifacts, or mistake file presence for verification. Use `scripts/inventory_downloads.py` and `research/additional-models.json`; preserve the existing three-model cohort and pin additions separately before testing one at a time.

The owner reports downloading Darkbloom themselves and explicitly said **do nothing with it yet**. This supersedes the old installation queue. Public documentation was reviewed only; no Darkbloom app, CLI, account, configuration or provider activity was touched. Do not run the prepared installer without a new owner request.

The owner rejected the previous localhost presentation as insufficiently visual. The viewer has been redesigned around ranked hardware bars, a selected-reference percentage gap, context-fill timing, completed-task graphics, and the download queue. Reference percentages describe reported configurations, not a controlled M3/M5 chip comparison. Context-mismatched percentages are withheld. Matched M3 runs and the Blender condition remain pending their previous GPU/GUI boundaries.

Reading this handoff does not itself authorize a new model run. Continue only the owner's current request and respect the occupied M3 / unresolved M5 GUI boundaries.

## Completed actual results

| M5 200K input / 256 output | Context fill | Prefill tok/s | Post-fill decode tok/s |
|---|---:|---:|---:|
| Qwen 3.8 27B, 8-bit MLX | 214.47 s | 933.63 | 21.44 |
| Gemma 4 31B, 8-bit MLX | 314.93 s | 635.74 | 15.41 |
| DeepSeek V4 Flash 0731, mixed Q4 | 301.75 s | 662.81 | 38.20 |

One measured long-context run per model. No swap growth. Cold means empty KV/state cache, not reboot/cold filesystem. Load/tokenization excluded. MLX first-token and native prefill counters have slightly different boundaries. Qwen/Gemma peak MLX allocation 42.02/49.95 GiB; DeepSeek planned total 155.81 GiB, minimum observed available system memory 64.53 GiB. Native planned allocation is not a measured peak. Full evidence is under `results/m5-*-200k-20261001` and [campaign methodology](docs/LONG-CONTEXT-CAMPAIGN.md).

**Official AA-AgentPerf-Local:** separate official Qwen Q4_K_M / llama.cpp cohort, exact output policy, standard 168-turn/eight-task replay. 168/168 turns completed, zero failures, measured 989.16s, end-to-end rate 31.23 tok/s. Median first-token latency 0.747s, p95 5.241s. Largest actual prompt 56,114 tokens with 65,536 server context. Most recurring input was cached. This is serving/transport success, not tasks solved. [Report](results/m5-aa-full-alone-20261001/README.md). The mini qualification is retained as setup only.

**Actual repository repair:** standard Qwen 8-bit, five fresh 200,001-token attempts on pinned historical Django bug `django__django-14500`. **4/5 passed all 19 tests, zero rescue**, median 238.37s. Attempt 4 used eight reads, never edited, and failed the regression; preserved without extra turns. Same packet hash across all seeds. Fresh process/repository per attempt, normal cache reuse within each attempt. [Report](results/m5-repo-qwen-summary-20261001/README.md). This small historical task may be training-contaminated and does not establish broad long-horizon intelligence.

Prior first-look 512/256 peaks remain 32.05 / 27.63 / 63.83 tok/s, explicitly setup/context-specific evidence; they are not the long-context headline.

## Machines and preparation

Original M3: Mac15,14, 32 CPU/80 GPU cores, 256 GB, 2 TB. New M5: Mac17,15, 36 CPU/80 GPU cores, 256 GB, 2 TB. Both directly inventoried, macOS 27.0.1 build 26A434, same Apple Clang 21.0.0. Public inventories are sanitized; private SSH routing remains in ignored `config/machines.local.json` on the controller. The new host's name changed; use that verified routing and existing trusted host identity, not a guessed hostname.

M5 installation root: `/Users/midirstudio2/mac-studio-inference-tests`. Controller root: `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github`. Both retain the 228 GB pinned three-model cohort and native/MLX runtimes. Model revisions and SHA256 are in `config/models.lock.json`. No automatic model upgrades.

Both additionally have the checksum-verified official AA Qwen Q4_K_M artifact, pinned AA source/environment and pinned llama.cpp binary. Receipts: `hardware/agentperf-old-ready.json`, `hardware/agentperf-new-ready.json`. Original preparation compiled on CPU only; no model was loaded there. Both have the same deterministic source corpus SHA256 `c35b8d1518b766d20272cb2de094051f5ee382f785bea88eeaa0363c47e63480`.

Both have the repository task source/evaluator prepared. Its sandbox was verified to deny a private sentinel read and network access. The immutable baseline fails the expected regression; the reference patch passes 19 tests. Python 3.10.19 and three evaluation dependencies are isolated from inference environments.

M5 has all nine previously requested daily apps installed and verified, plus a clean official Blender 5.2.0 bundle. The original Blender bundle failed a signature check and was not copied/modified. A future matched original-host Blender run needs the same clean task-owned version without overwriting the owner's existing app. User sign-ins and OS permissions are not migrated.

## Runtime state and review

All five repository attempts have ended and their task-owned MLX server processes exited. All earlier Qwen/Gemma/DeepSeek and AA servers also exited. No Blender instance was launched by the blocked condition. Verify process/slot state live before any future launch; do not infer safety from these historical lines.

The intentional M5 readonly viewer is `http://127.0.0.1:18765`. Safari was opened on the new Mac and its request verified. The controller also reviewed the page via an SSH tunnel at port 18766; that address is a forwarded view, not a second inference server. The UI prioritizes context-fill/decode bars, workflow status, actual repo outcomes, and 14 source-linked external M3/Spark/RTX/AMD configurations. Prompts/responses are collapsed. External configurations differ and no hardware-only percentage is inferred. [Shareable figure](outputs/200k-context-results.png).

18 harness tests pass. Live dashboard values/filtering/collapsed output were checked through the browser. Source, locks, intentional results, failures and reports are pushed on the task branch. Raw local paths are redacted in published evidence. Runtime caches/weights/environments remain ignored. Keep this active benchmark installation ready; remove only task-owned disposable duplicates/build objects.

## Remaining work and exact resume boundaries

1. Await the owner's M5 dialog clarification. Then inspect actual GUI/process state and run the identical full AA condition using `scripts/blender_condition.py --allow-inference --run-id <fresh-id>`. It owns the Blender fixture and closes only its own processes. Keep a second GPU slot reserved for the model. Do not substitute headless Blender for the requested open-app condition.
2. Darkbloom is **on owner hold**. The owner downloaded it; do not execute the prepared installer or operate the app. Only resume on a new explicit owner request. Actual daily earnings remain unmeasured.
3. When the owner explicitly frees the original GPU, re-inventory both hosts and run the same locked tests with `--machine studio-old` and fresh M3 IDs. The revised runners support explicit host selection; defaults remain the new Studio. Do not use this flag now while the M3 is occupied.
4. This is a first M5 phase, not the complete exhaustive study. Repeated matched M3/M5 cells, full advertised-window capacity sweeps, a broader/longer task set, other-model quality runs and the two-machine cluster remain pending. Follow `docs/PROTOCOL.md`, `docs/CLUSTER.md` and the current GPU slot rules. Max-context or new quant variants must not silently replace the pinned cohort.
5. Review actual paired visual results locally before any personal website publication. Do not merge the website PR or deploy by inference from benchmark authority. YouTube/content production is later.

## Provenance and safety

Long-context execution source: `26f2413`. Full AA-alone execution source: `97107b5`. Repository attempts executed from `642eae96f79d499eb092e16d2410b77a392df036`; later commits add reporting, host selection and cleanup without changing those historical runs. Preserve unsuccessful measured attempts. The active shared-brain revision was verified as `3be383eed8647847fe37fe066df7756ff6ec98f3`.

No secrets, SSH keys, browser profiles or authentication stores were synchronized or committed. No social posts were made. No remote publisher submission, website deployment, account creation, provider activation or financial transaction was performed.
