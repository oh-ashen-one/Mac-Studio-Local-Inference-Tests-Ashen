# Isolated Mistral execution preparation

Prepared on task branch `codex/mistral-harness-20261003`, based on the published baseline. The active M5 baseline has not adopted these source changes. Do not synchronize them while any baseline driver/worker is alive.

The common wrappers accept explicit model-lock and campaign-ID options while retaining original defaults. The campaign runner accepts an explicit plan and separate ledger, takes the same global campaign mutex, and preserves memory/swap/deadline/shared-slot guards and every per-job budget. Mistral is still marked execution_ready false. No preparation code is a runtime qualification pass.

The extension admission gate requires an artifact-list-matched receipt, model revision, passed load/token/interface/metadata gates, runtime-lock hash and native-server hash. The native server path and runtime-lock path can identify an independently pinned Mistral runtime. Common task payloads explicitly request reasoning_effort none, consistent with the existing no-thinking task condition; template token counting uses the same request. Official replay retains its recorded policy and must be independently qualified.

Next authorized steps at an idle M5 boundary:

1. Inspect the qualified baseline llama.cpp source revision and metadata support. If incompatible, build a separately pinned task-owned native runtime without modifying baseline runtime/environment. Preserve setup failures and don't auto-relaunch after two crashes.
2. Run separately labeled Mistral qualification under the shared GPU protocol and resource guards; no measured cell counts as setup. Verify exact native token counts, task template/tool behavior, context settings and interpreter support. Preserve original model files/quantization.
3. Produce a qualification receipt with all admission fields, pin native binary/source/runtime hashes, then set execution_ready true only after the gates pass. Unsupported cells require concrete evidence and dispositions.
4. Integrate this reviewed task-branch change into the executor task branch after baseline processes exit, without main merge, then execute the separately declared 39-group Mistral plan using `--plan config/mistral-campaign-20261003.json --state work/mistral-campaign.json`.
5. Extend publication/coverage to the separate ledger and u20261003 result IDs before publishing measured cells. The existing harvester accepts only baseline u20261002 IDs and must not silently omit the extension.

Tests cover separate lock/ledger admission, exact preservation of all per-job budgets, refusal of unqualified artifacts, and explicit task reasoning policy. No GPU operation, model loading or M5 runtime mutation was performed while preparing this branch.
