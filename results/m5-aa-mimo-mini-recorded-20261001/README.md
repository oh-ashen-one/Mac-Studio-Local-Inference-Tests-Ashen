# MiMo recorded-policy replay — original qualification failed

Five of six requests failed AA F0 transport validity. The HTTP server returned 200 but discarded XML tool-call output using a JSON parser. One request served successfully; no replay speed score is accepted from this failed qualification. The original full-profile replay was not launched.

The pinned tokenizer's template contains compact `<tool_call><function=...>` markup. MLX-LM 0.31.3's XML detector requires a newline between those markers; it falls back to `json_tools` for this template. Server logs show five JSON parsing failures. CPU-only [validation](../../hardware/mimo-xml-parser-validation.json) reproduces the mismatch and verifies the upstream `qwen3_coder` XML parser handles the declared format while rendered prompt token IDs stay identical.

The original failure, raw reports and logs remain unchanged. A separately named XML-parser-v2 qualification uses the same model, template, sampling and output budgets. Repository trials use a separate plain JSON-action protocol, so their five recorded task failures are not relabeled or retried by this repair.
