# Isolated Mistral execution preparation

Prepared on task branch `codex/mistral-harness-20261003`, based on the published baseline. The active M5 baseline has not adopted these source changes. Do not synchronize them while any baseline driver/worker is alive.

The common wrappers accept explicit model-lock and campaign-ID options while retaining original defaults. The campaign runner accepts an explicit plan and separate ledger, takes the same global campaign mutex, and preserves memory/swap/deadline/shared-slot guards and every per-job budget. Mistral is still marked execution_ready false. No preparation code is a runtime qualification pass.

The extension admission gate requires an artifact-list-matched receipt, model revision, passed load/token/interface/metadata gates, runtime-lock hash and native-server hash. The native server path and runtime-lock path can identify an independently pinned Mistral runtime. Common task payloads explicitly request reasoning_effort none, consistent with the existing no-thinking task condition; template token counting uses the same request. Official replay retains its recorded policy and must be independently qualified.

Next authorized steps at an idle M5 boundary:

1. Inspect the qualified baseline llama.cpp source revision and metadata support. If incompatible, build a separately pinned task-owned native runtime without modifying baseline runtime/environment. Preserve setup failures and don't auto-relaunch after two crashes.
2. Run separately labeled Mistral qualification under the shared GPU protocol and resource guards; no measured cell counts as setup. Verify exact native token counts, task template/tool behavior, context settings and interpreter support. Preserve original model files/quantization.
3. Produce a qualification receipt with all admission fields, pin native binary/source/runtime hashes, then set execution_ready true only after the gates pass. Unsupported cells require concrete evidence and dispositions.
4. Integrate this reviewed task-branch change into the executor task branch after baseline processes exit, without main merge, then execute the separately declared 39-group Mistral plan using `--plan config/mistral-campaign-20261003.json --state work/mistral-campaign.json`.
5. Use the prepared `scripts/harvest_unified.py --campaign mistral` to harvest the separate ledger and u20261003 result IDs. Its own aggregate is results/mistral-extension-20261003; baseline defaults and aggregate remain separate. Deploy together with reporting changes only after the active baseline has exited. The sync verifies both ledgers before touching executing source and preserves both original result families.

Tests cover separate lock/ledger admission, exact preservation of all per-job budgets, refusal of unqualified artifacts, and explicit task reasoning policy. No GPU operation, model loading or M5 runtime mutation was performed while preparing this branch.

The baseline native launcher is dynamically linked, so launcher SHA256 alone is insufficient provenance. Admission now verifies the pinned complete native runtime file list (launcher plus task-owned dylibs), its source commit and qualification receipt. A regression test verifies that changing a linked library blocks an otherwise qualified runtime. Baseline source includes Mistral3 and the corrected YaRN log-multiplier reader; no actual Mistral load has been qualified yet.

Publication checks confirm separate-ledger selection, unchanged baseline aggregate bytes, per-file original/published hashes and rejection of wrong-campaign result IDs. The separate report currently shows39 declared/0 completed Mistral groups. This is prepared reporting, not measured evidence.

## Prepared qualification supervisor

At an idle verified M5 boundary, use `scripts/mistral_qualification_driver.py --allow-inference --run-id q20261003-mistral-qualification-r1`. It refuses live campaign drivers/GPU holders, takes the global mutex, supervises child/server memory and swap with the same12GiB/2GiB limits, preserves failed attempts, and performs graceful cleanup. Setup budget1800s is separate from all measured task budgets. It has not been executed or qualified yet.

The child verifies all model hashes, pins the reviewed native source and launcher/dylib closure, starts one loopback server, checks exactly8192 input/32 generated tokens, checks common no-reasoning chat/template usage, and confirms stored corrected context metadata plus the native loader's262144 declaration. It preserves requests/replies/logs/telemetry in a setup-only result directory. This does not claim full200K qualification; the39 declared measured groups retain their actual lengths and guards. Review the real receipt before setting execution_ready true. If a gate fails, preserve the attempt and diagnose it with a separately labeled follow-up; never silently retry or treat prepared code as passed evidence.

The prepared readonly dashboard exposes Mistral's separate ledger, qualification status and four-context sample counts in its own card. It starts at0/39 and explicitly awaiting runtime qualification; baseline/historical statistics stay separate. This change remains on the isolated preparation branch until idle adoption.

Publication synchronization now also protects a live qualification supervisor and download/verification control, including their interval before a model worker exists. Any live shared GPU holder protects inference source too. A stopped baseline ledger cannot make an active setup phase appear safe for code replacement. Tests exercise these transitions with the baseline exited.

The actual pinned GGUF chat template embeds reasoning effort in explicit MODEL_SETTINGS markers and accepts none/high. Qualification now requires the native /apply-template endpoint to render each requested mode correctly, and the no-reasoning inference response to omit reasoning fields/tags. The admission receipt must include reasoning_control_passed. A unit test covers missing/unsupported rendered settings. This adds evidence for the declared policy without running a high-reasoning inference workload.
