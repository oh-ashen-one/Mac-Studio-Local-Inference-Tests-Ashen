# HANDOFF — M5 long-context and real-work campaign

Updated 2026-10-01. Controller: verified original M3 Studio. Branch: `codex/long-context-dashboard-20261001`. Public repository: `oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen`. Review: [draft PR #3](https://github.com/oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen/pull/3), based on the initial M5-test branch. No merge or personal-site deployment authorized/performed.

## Owner instruction and boundaries

The owner explicitly authorized M5 inference and requested 200K input, prefill/decode metrics, agent replay, Blender multitasking, real repository completion and external hardware comparisons. They explicitly confirmed other sessions still use the original M3 GPU. **Do not run M3 inference or touch those sessions.** Its CPU-only preparation is complete.

**Latest owner steering:** benchmark all completed downloaded language models on the M5 with the same long-context and bounded task diagnostics; retry failed Qwen 3.6 35B A3B. The explicit retry request authorized one download-only CLI invocation. `scripts/retry_qwen_download.py` ran the official `models download` command, which completed successfully. No Darkbloom serving, login, account/config change or inference through its executable is authorized or performed.

**Additional cohort now verified:** the entire identified batch in the M5 HF cache has no partial/staging files. Two language checkpoints were found: Qwen 3.6 35B A3B (21.309 GB, four main shards, catalog FP4 / affine-4 config despite legacy MXFP8 ID) and MiMo V2.6 Flash (172.863 GB including the audio-tokenizer component, 37 main shards, catalog MXFP4). All 66 files passed SHA256 against the manifests and public catalog. Separate `config/additional-models.lock.json` preserves exact files/provenance; the original three-model lock is unchanged. The owner estimated more models; do not confuse the public catalog or components with an actual selected download batch. Read-only monitoring can identify further arrivals.

**Runtime progress:** baseline MLX-LM 0.31.3 loaded Qwen but produced gibberish, preserved at `results/m5-qwen36-pilot-20261001`. Its Qwen sanitizer incorrectly adds one again to already-shifted norms when MTP weights are present. Official MLX-VLM commit `d73f4b1ad90194d53e37beac6e9eef76976aadc5` handles this and supports MiMo V2.6. It is pinned in `config/requirements-mlx-vlm.lock`, installed separately at `vendor/vlm-runtime/.venv`, and used through the text-only adapter in `scripts/text_runtime.py`. It does not execute model-repository Python. Corrected Qwen validation passes; three actual 200K/256 runs are complete: median 66.688s fill, 3001.24 prefill tok/s, 79.776 decode tok/s (79.635–79.959), 23.98 GiB peak MLX, zero swap in all three. This is a separate model configuration, not a comparison to the Qwen 3.8 model. Three speed repetitions and five bounded repository attempts are planned per compatible addition. Qwen repository attempt 1 has reached source editing; its first two HTTP turns report cached_tokens=0, so record actual reuse rather than assuming it from server cache settings. MiMo strict loading initially rejected 42 optional MTP draft tensors; the reviewed adapter excludes precisely those and retains strict base-weight validation. Its fresh pilot produces READY and correct arithmetic, but fences JSON: strict format fails and the assessment explicitly accepts runtime coherence only. Raw failures/results and the assessment are preserved. The finite headless driver `scripts/additional_campaign.py` is active on M5 (PID 17437 at launch); inspect `work/additional-campaign.json`, process identity and child logs before acting. It schedules 20 cells, with the first Qwen speed cell already complete: 3 speed repetitions, 5 fresh repo attempts, one AA mini qualification and one full recorded-policy replay for each addition. It halts on runtime errors, memory pressure, deadline, new partial downloads or another live GPU holder; it never retries failed cells. Resume only after inspecting the concrete stopped cell. Do not launch a duplicate driver.

The M5 has a task-owned `caffeinate -is` process (receipt `work/caffeinate.json`) requested by the owner. Display sleep remains allowed. It has negligible load and lasts until stopped or rebooted.

The existing **15-minute** thread follow-up `m5-model-download-follow-up` continues the campaign and publication to the task branch. Inspect active drivers, results and shared slots before doing anything; never duplicate or interrupt a running test. Original M3 inference, main merges and personal-site deployment remain prohibited. See `docs/ADDITIONAL-MODEL-CAMPAIGN.md`.

DeepSeek's saved 200K run is valid at 38.20 tok/s. The published M3 result is 36.01 tok/s with unstated input length and different MXFP4 quantization. The 2.19 tok/s arithmetic gap is not a matched hardware speedup. Do not rerun solely to make the percentage appear. The UI now explains the missing reference context and shows the raw gap.

The owner rejected the previous localhost presentation as insufficiently visual. The viewer has been redesigned around ranked hardware bars, a selected-reference percentage gap, context-fill timing, completed-task graphics, and the download queue. Reference percentages describe reported configurations, not a controlled M3/M5 chip comparison. Context-mismatched percentages are withheld. Matched M3 runs and the Blender condition remain pending their previous GPU/GUI boundaries.

The latest owner request explicitly authorizes sequential independent M5 tests after readiness; respect the occupied M3 and unresolved Blender GUI boundary.

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

All five ORIGINAL Qwen 3.8 repository attempts have ended and their task-owned MLX server processes exited. The additional campaign is now active; check its ledger before any new GPU work. All earlier Qwen/Gemma/DeepSeek and AA servers also exited. No Blender instance was launched by the blocked condition. Verify process/slot state live before any future launch; do not infer safety from these historical lines.

The intentional M5 readonly viewer is `http://127.0.0.1:18765`. Safari was opened on the new Mac and its request verified. The controller also reviewed the page via an SSH tunnel at port 18766; that address is a forwarded view, not a second inference server. The redesigned UI uses a light editorial layout with a dark sidebar, ranked SVG hardware charts, generation/wait/prefill modes, contextual percentage gaps, task-outcome graphics, and the download queue. It retains 14 source-linked M3/Spark/RTX/AMD reports. Prompts/responses are collapsed. External configurations differ and no hardware-only percentage is inferred. [Shareable figure](outputs/200k-context-results.png).

20 harness tests pass (including strict draft exclusion and the five-model readonly viewer). Live dashboard values/filtering/collapsed output were checked through the browser. Source, locks, intentional results, failures and reports are pushed on the task branch. Raw local paths are redacted in published evidence. Runtime caches/weights/environments remain ignored. Keep this active benchmark installation ready; remove only task-owned disposable duplicates/build objects.

## Remaining work and exact resume boundaries

1. Await the owner's M5 dialog clarification. Then inspect actual GUI/process state and run the identical full AA condition using `scripts/blender_condition.py --allow-inference --run-id <fresh-id>`. It owns the Blender fixture and closes only its own processes. Keep a second GPU slot reserved for the model. Do not substitute headless Blender for the requested open-app condition.
2. The Darkbloom **app/provider remains on owner hold**, while benchmarking its downloaded model files through independent runtimes is now authorized after the batch completes. Do not execute the prepared installer or enable serving. Actual daily earnings remain unmeasured.
3. When the owner explicitly frees the original GPU, re-inventory both hosts and run the same locked tests with `--machine studio-old` and fresh M3 IDs. The revised runners support explicit host selection; defaults remain the new Studio. Do not use this flag now while the M3 is occupied.
4. This is a first M5 phase, not the complete exhaustive study. Repeated matched M3/M5 cells, full advertised-window capacity sweeps, a broader/longer task set, other-model quality runs and the two-machine cluster remain pending. Follow `docs/PROTOCOL.md`, `docs/CLUSTER.md` and the current GPU slot rules. Max-context or new quant variants must not silently replace the pinned cohort.
5. Review actual paired visual results locally before any personal website publication. Do not merge the website PR or deploy by inference from benchmark authority. YouTube/content production is later.

## Provenance and safety

Long-context execution source: `26f2413`. Full AA-alone execution source: `97107b5`. Repository attempts executed from `642eae96f79d499eb092e16d2410b77a392df036`; later commits add reporting, host selection and cleanup without changing those historical runs. Preserve unsuccessful measured attempts. The active shared-brain revision was verified as `3be383eed8647847fe37fe066df7756ff6ec98f3`.

No secrets, SSH keys, browser profiles or authentication stores were synchronized or committed. No social posts were made. No remote publisher submission, website deployment, account creation, provider activation or financial transaction was performed.

## Evidence synchronization during the active driver

The controller publishes completed run directories; never overwrite a still-running result. Copy complete/failed records with logs, patches and evaluation outputs, redact private absolute paths/endpoints in a public copy, then run `python3 scripts/report_additional.py`. Push on this task branch. When a remote-generated untracked result conflicts with pulling its newly published tracked counterpart, compare exact bytes (or preserve the original sanitized-different version), move only that task-owned original to ignored `work/published-backup/`, then fast-forward. Never reset or discard another process's files. Original remote logs remain available. No pull should change currently executing runtime code; dashboard/report-only updates are safe.

The owned readonly preview was restarted as PID 17696 on port 18765; inspect identity before future restart. The controller forward at 18766 is verified. The 15-minute heartbeat remains active and must monitor rather than duplicate PID 17437's campaign. Use the progress ledger for current state; PID/time snapshots here are historical.
