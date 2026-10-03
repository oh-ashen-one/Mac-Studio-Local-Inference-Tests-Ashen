# MiMo XML-parser-v2 qualification

The separately labeled parser-corrected profile completed **6/6 replay turns with zero transport failures**. Six short-output warnings are retained under the recorded-cap policy. This is setup/serving qualification, not a performance headline or a task-solving score.

The only configuration change from the preserved failed profile is explicit selection of the pinned runtime's existing `qwen3_coder` XML tool parser. Model files, template, sampling, recorded output policy and request budgets are unchanged. The CPU-only fixture verified that identical messages render to identical token IDs under both parser selections; normal AA per-run cache-isolation namespaces still differ between replay runs.

The original auto-parser qualification remains [failed and preserved](../m5-aa-mimo-mini-recorded-20261001/README.md). The original full profile was never launched and is recorded unsupported. This XML-v2 profile now qualifies for its separately recorded full replay. It retains AA's non-comparable context-discovery flag and does not replace the original Qwen exact-output cohort.
