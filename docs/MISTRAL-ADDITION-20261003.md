# Owner-requested Mistral addition — October 3

The owner explicitly requested one current, highly regarded Mistral model, overriding the older preparation-era no-Mistral scope. Selected **Mistral Medium3.5 128B**, the newer general-purpose flagship combining coding, reasoning and instruction following. It has256K declared context. Mistral's May22 announcement reports77.6% SWE-Bench Verified and replacement of Devstral2 in Vibe. These are vendor-reported results, not results from our campaign.

Sources: [official announcement](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/), [official model card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B), [official organization](https://huggingface.co/mistralai). This selection is not a claim that one model leads every popularity/quality ranking. HF download counts differ by task and older models have more downloads; audio/moderation/formal-proof releases are not replacements for this general-purpose suite.

## One pinned local configuration

The official card links [Unsloth's GGUF conversion](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF). Selected Q4_K_M, revision `c8f5b1477e1b22cd2d819157d450f001f7047298`, three shards totaling74,897,139,136 bytes. Expected per-file SHA256 values are in `config/mistral-models.lock.json`. It is pinned for preparation, **not downloaded, verified or runtime-qualified yet**. Use a compatible independently pinned llama.cpp runtime; no provider/API inference. Do not replace another model's runtime or precision.

The official model card warns that earlier Transformers configurations degraded long-context performance and affected derived GGUFs. Verify the [upstream fix](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/commit/c4be198050fb5789774a55b92ed697becfbf20ae) against selected GGUF metadata before admission. Shard size alone does not establish that fix or runtime compatibility. Preserve all qualification evidence and resource limits.

`config/mistral-campaign-20261003.json` declares the full39-group suite using the original contexts, repetitions, turn/output budgets, quality cases and load requests. The four-model extension and remaining Qwen3.6 groups remain cancelled. Mistral is a separate required extension; finishing the retained baseline alone is not whole-study completion.

Current Gemma concurrency4 remains uninterrupted. Existing owner-skip boundary guard21919 will stop the old driver after that test; adopt both latest scope changes at the same reviewed boundary. At an idle verified M5 boundary, check storage and duplicate/partial downloads, then download and verify only the pinned Mistral configuration. Do not overlap heavy download/verification with timed inference. No new Mistral inference is admitted until weights, runtime and long-context configuration are qualified. The existing heartbeat remains ACTIVE.
