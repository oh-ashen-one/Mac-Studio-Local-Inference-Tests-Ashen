# MiMo extended-history GPU resource failure — October3

`u20261002-mimo-repo20-r1` stopped after11 complete responses, with request12 failing in the pinned MLX runtime. The server log records `kIOGPUCommandBufferCallbackErrorOutOfMemory` at `mx.eval([c.state for c in prompt_cache])` while preparing generation. The client surfaced missing token-usage data because the stream aborted before final usage. This is a GPU allocation failure, not a task-success score or a demonstrated incorrect code patch. All completed responses, cache counts, feedback, logs, telemetry and empty candidate patch remain unchanged.

The reconstructed request12, built from the preserved initial packet and exactly11 saved response/feedback pairs, has233765 tokenizer-preflight tokens. This is an estimate, not a server-observed count: the failed stream emitted no final usage. The model config declares1048576 positions. Last successfully served prompt227274 tokens,18 generated tokens,226627 reported cached tokens. The failure is not evidence of hitting the nominal positional limit.

Whole-child available-memory minimum16.578GiB; server interval16.354GiB. Swap growth3,604,480 bytes (3.4375MiB). The12GiB available/2GiB growth guards did not trip; GPU allocation can fail above those OS thresholds. The process-local82% memory limit and official recommended wired limit are unchanged. No weights, quantization, prefix/KV cache policy, input, output, seed, concurrency or task budget is altered. All owned inference processes exited; shared GPU holders are empty. This is conservatively recorded as GPU safety event1; a second event prevents automatic inference relaunch.

## Explicit disposition and continuing work

Only the actually failed first20-turn-budget trial is `unsupported_resource`, supported by its completion audit and server log. It has no final task-success score and is not counted as passed or as a completed repair trial. It is not retried or stitched. The original result remains failed.

The two unrun extended trials are `deferred_resource_review`: they remain required, are not scored, and are not declared unsupported by analogy. The remaining predeclared sustained repetitions and short8K serving profiles may continue after verified cleanup under identical guards. This postpones the riskier history-growth condition while gathering the safer planned evidence. The original job IDs, order, inputs and budgets remain preserved; deferred entries are revisited only after review and fresh plan recording.

Mistral remains required. Once the safe baseline driver exits, the M5 can perform separately labeled Mistral qualification/full suite while the two MiMo deferred cells remain visibly incomplete. Full-study completion is forbidden until those cells are completed or have their own concrete evidenced dispositions. No profile change or broad model-unsupported claim is inferred from this one failure.

The preserved audit is `results/u20261002-mimo-repo20-r1/completion-audit.json`, with a clearly labeled reconstructed request. Prior plan bytes/hashes are archived. The driver now validates audited resource dispositions, distinguishes deferral from completion, and refuses automatic relaunch after two recorded GPU safety failures.
