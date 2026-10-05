# Mistral setup qualification review — October3

Original `q20261003-mistral-qualification-r1` is preserved as failed setup, not one of39 measured groups. All model hashes verified, native load passed, direct8192-input/32-output token counts matched, and explicit none/high reasoning settings rendered correctly. The no-reasoning chat returned exactly `{"ready": true}` with empty reasoning and six generated tokens. It did not crash or trigger a GPU/memory safety event.

The gate failed because the chat-count estimator omitted a model-required BOS token, while native chat usage correctly included it (33 prompt tokens). The previous helper called native /tokenize with add_special false for all GGUFs. Mistral's embedded template does not contain a BOS marker; its native vocabulary behavior prepends the token. The corrected Mistral-only lock field native_add_special_tokens true makes template counting include it. Other model defaults are unchanged; direct token-ID speed probes remain exact8192/32 and future declared lengths, with no extra token silently added to those explicit arrays.

The native runtime's default-verbosity log does not print n_ctx_train. Its actual /v1/models endpoint exposes that field from loaded native model metadata. The gate now preserves that response and requires n_ctx_train262144, rather than assuming a log line exists. Stored corrected YaRN metadata remains independently verified. This is an evidence-transport fix, not a context-limit or budget change.

Model files, source/binary/dylib pins, memory/swap guards, no-reasoning policy and task budgets are unchanged. A separately labeled `q20261003-mistral-qualification-r2` will requalify the corrected harness. The first attempt remains failed, with full requests/replies/logs/telemetry and original/published hash receipt. No qualification or measurement pass is inferred before actual complete child/supervisor receipts.

## Revised setup r2 completed

`q20261003-mistral-qualification-r2` passed all gates and both child/supervisor completed with workers exited. All model hashes matched, native load passed, exact8192-input/32-output direct probe matched, native none/high rendering matched, BOS-aware chat count33 matched actual usage, response had no reasoning, and loaded native metadata declared262144 training positions. Native source, launcher and all task-owned dylib hashes are pinned in the immutable setup receipt. Setup remains excluded from all39 measured groups; first failed r1 remains unchanged. Model/runtime admission is now ready for the separately declared campaign.
