# M5 Ultra local inference research report

Evidence snapshot: October 4, 2026. **The study is closed at the owner-approved reduced scope.** The final unrun MiMo trial was explicitly omitted by the owner; the two actual GPU memory failures remain preserved and unscored.

The delivered M5 has evidence for all 39 Mistral logical groups: 30 completed groups and 9 independently audited, unscored request-budget groups. Across the five retained configurations, the original 195 groups are accounted as **183 completed, 11 actually attempted but unscored, and 1 explicit owner omission**. The final required scope contains 194 groups, all accounted, with zero required/unrun groups remaining. A completed group can contain functional failures; these coverage counts are not success rates. Two independent MiMo Metal allocation failures reached the explicit safety limit. Automatic inference remains stopped, with owned processes and shared holders verified absent. [Owner scope decision and closeout](OWNER-FINAL-MIMO-OMISSION-20261004.md).

## Scope, provenance and measurement boundaries

The target was directly inventoried as Mac17,15 / Apple M5 Ultra,36 CPU cores,80 GPU cores,256GB-labeled memory(274877906944bytes), approximately2TB physical storage, macOS27.0.1/build26A434. See [actual inventory](../hardware/incoming-device.json). The M3 was a controller and was reserved for other owners; there is no matched M3 inference cohort. Paired preparation and identical model files do not establish a hardware speedup. No power, Neural Engine throughput, cluster scaling or absolute hardware-ceiling measurement is claimed.

The retained baseline contains four39-group configurations plus the separate39-group Mistral addition. The original234-group baseline also includes preserved historical results for QwenQ4 and Qwen3.6:60 completed groups and18 explicit owner omissions. Its final accounting is 213 complete + 19 owner omissions + 2 actual resource-limited attempts. The nineteenth omission is the final original MiMo trial, authorized at closeout. The156-group Qwen3.5/GPT-OSS/Bonsai/Nemotron extension was explicitly cancelled before admission; those groups are neither passes nor model failures. TensorFold remains backlog. Legacy Qwen3.6 FP4/MXFP8 IDs are provenance identifiers; public precision is4-bit MLX affine with8-bit gates, with the original bytes preserved.

| Retained configuration | Completed groups | Actually attempted/unscored | Owner omitted/unrun | Originally declared groups |
|---|---:|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|39|0|0|39|
|Qwen3.8 27B ·8-bit MLX|39|0|0|39|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|39|0|0|39|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|36|2|1|39|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|30|9|0|39|

All model/runtime revisions, artifact manifests, tokenizer/corpus fingerprints, prompts, exact reported usage, raw outputs and source commits remain in the per-run records. Model/runtime families, parameter counts and precisions differ, so this is a configuration comparison on one M5 rather than an isolated architecture, quantization or hardware experiment. [Baseline model lock](../config/unified-models.lock.json), [Mistral lock](../config/mistral-models.lock.json) and [frozen protocol](UNIFIED-OVERNIGHT-PROTOCOL.md) define the cohort. Mistral uses Unsloth revisionc8f5b1477e1b22cd2d819157d450f001f7047298, three Q4_K_M shards(74897139136bytes), native sourcef1cee9941b0e843ea260bf8dd9a090fbd9711b6a and a verified26-file launcher/library closure. MiMo uses its pinned53-file manifest(172863462401bytes); the actual model/config/runtime/source checks are [recorded](../hardware/mimo-original-continuation-validation-20261004.json).

Cold context means fresh KV/state, not cold SSD cache or a reboot. Weight hashing/load and tokenization are not native steady decode. Five original cold repetitions use8192/32768/131072/200000 actual input tokens and256 forced-work output tokens; three sustained repetitions use200000 input/2048 output. The common corpus hash does not make tokenized text identical across different tokenizers. Chat-task packets use native reported counts and the declared tolerance; calibrated estimates are never substituted for missing final usage.

Useful work preserves900-second request deadlines and original output/turn/job budgets. The repeated Django diagnostic uses5 fresh8-turn seeds and3 fresh20-turn seeds, full200K starting packets,2048 output caps and no human rescues. Serving uses60 measured requests plus2 excluded warmups at each concurrency1/2/4,8192 input target and256 output cap. Native decode, HTTP fill, first visible output, complete request wall, aggregate serving throughput and official replay throughput have different denominators; they must not be pooled.

## Cold context speed

Medians below retain all five declared repetitions. The first table is backend-reported steady decode, while the second is measured context fill. They are not task-success or semantic-context scores.

| Configuration |8K decode tok/s|32K decode tok/s|128K decode tok/s|200K decode tok/s|
|---|---:|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|25.848|24.165|19.147|15.255|
|Qwen3.8 27B ·8-bit MLX|30.581|28.928|24.448|21.426|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|55.350|51.820|41.570|37.610|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|65.703|59.425|44.486|37.676|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|12.557|9.983|5.353|4.041|

| Configuration |8K fill s|32K fill s|128K fill s|200K fill s|
|---|---:|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|6.359|28.510|165.833|311.842|
|Qwen3.8 27B ·8-bit MLX|4.961|21.437|115.589|212.930|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|8.342|35.631|175.570|303.859|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|8.418|27.930|178.426|392.706|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|32.586|209.705|2239.119|4923.512|

MiMo and DeepSeek have the highest observed200K steady decode in their respective retained configurations. Qwen8-bit fills200K faster in this corpus test, while Gemma is slower but has stronger results on several bounded task diagnostics. Mistral’s200K median fill is4923.512seconds, about82.06minutes; that is far beyond a900-second first useful-work request budget. Its exact-token speed completion therefore cannot be used to claim that its200K task requests completed. See [all20 Mistral cold repeats](../results/mistral-speed-summary-20261003/README.md) and the raw baseline groups.

## Sustained200K input /2048 output

| Configuration |n|Median decode tok/s|Observed decode range|Sample SD|Median fill s|
|---|---:|---:|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|3|15.37908|15.37529–15.37996|0.00248|311.760|
|Qwen3.8 27B ·8-bit MLX|3|21.41945|21.36740–21.42903|0.03317|209.941|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|3|38.14000|20.43000–38.15000|10.22776|301.200|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|3|37.60352|37.56640–37.64233|0.03797|383.392|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|3|3.95959|3.94819–3.96882|0.01034|5011.771|

All15 original sustained runs completed exact200000 input/2048 output. DeepSeek’s three decode values20.43/38.14/38.15tok/s have a wide range; the slow first repeat is retained and the cause is unproven. A median38.14 does not imply three stable38tok/s runs. MiMo’s narrow sustained range also does not establish safe growing-history behavior: its sustained flat-prompt workload completed while extended repository history later caused two actual device-memory failures. MiMo sustained r1 has1MiB positive whole-child swap growth even though its narrower server-only summary reported0; later sustained repeats reported0. Preserve both scopes. Mistral’s [full three-repeat audit](../results/mistral-sustained-summary-20261004/README.md) checks18 original/publication artifact pairs, matching source/runtime/model/corpus/token-ID fingerprints and zero reported cache reuse/positive whole-child swap growth.

## Bounded quality and repository diagnostics

| Configuration |Structured cases|Synthetic200K retrieval|Restricted HumanEval|8-turn Django repair|20-turn Django repair|
|---|---:|---|---:|---|---|
|Gemma4 31B ·8-bit MLX|24/24|9/9|159/164|5/5 completed trials|3/3 completed trials|
|Qwen3.8 27B ·8-bit MLX|21/24|9/9|158/164|4/5 completed trials|3/3 completed trials|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|24/24|9/9|148/164|5/5 completed trials|3/3 completed trials|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|24/24|9/9|154/164|1/5 completed trials|2 actual resource failures;1 owner-omitted/unrun|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|21/24|9 actual deadline attempts; unscored|151/164|5 actual deadline attempts; unscored|3 actual deadline attempts; unscored|

These are diagnostic-specific outcomes. HumanEval uses one greedy chat-adapted sample per canonical case, a restricted Python3.10-compatible evaluator, OS sandbox and CPU/wall/file/RSS guards. The actual canonical164-solution and negative-control qualification passed before generated-code scoring; its receiptSHA is2fcafe57da88796cb288e797d6e0ebccecdf4a80e2e1d688ab5627eb3ea62486. Public tasks may be present in training data. These are not official leaderboard scores, general-intelligence rankings or pass@k>1. Mistral’s151/164 includes13 retained functional assertion failures, with no repair/retry/rescore. MiMo’s154/164 includes policy/output-format exclusions as well as functional failures; an unsupported sympy import and a cap-limited unclosed code fence are not silently repaired.

Qwen8-bit and Mistral each score21/24 structured cases, with all three state-tracking seeds failing. The retrieval probe is a controlled exact-answer task at three positions and three seeds, not proof that all content or a nominal maximum context is useful. MiMo’s fresh9-case replacement is kept separate from the owner-interrupted original8/9 run; no case stitching. The replacement’s download-overlap comparability flag remains visible. DeepSeek’s initial zero-turn swap-guard failure is preserved separately from its qualified before-server tokenization replacement, with the changed setup boundary declared.

Gemma and DeepSeek passed all five8-turn repair trials; Qwen passed four and MiMo one. Gemma/Qwen/DeepSeek passed all three20-turn diagnostics. These are repeated seeds on one public Django issue, not a diverse SWE-bench leaderboard. Negative functional results are retained; completed-group coverage is not a pass count. Mistral’s eight original repository attempts all actually exceeded their first900s deadlines with no completed response/final usage/task score; it is not scored0/8. All nine original Mistral retrieval cases were individually attempted and independently audited before their logical group was accounted; it is not scored0/9 or deemed semantically unable by analogy. [Repository budget series](../results/mistral-repo20-budget-series-20261004/README.md) and [retrieval audit](../results/mistral-retrieval-all-cases-audit-20261004/README.md) bind the actual attempts.

## Serving throughput and response latency

Every profile completed60 measured requests; two warmups are excluded. Each entry below is aggregate HTTP outputtok/s / median response latencyseconds, not steady native decode.

| Configuration |Concurrency1|Concurrency2|Concurrency4|
|---|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|15.337 / 16.689|21.601 / 23.700|26.587 / 38.522|
|Qwen3.8 27B ·8-bit MLX|18.472 / 13.854|26.393 / 19.380|34.017 / 30.076|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|19.505 / 13.124|8.159 / 63.264|12.257 / 59.722|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|28.011 / 9.138|35.028 / 14.606|40.257 / 25.432|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|4.756 / 53.514|4.928 / 103.795|5.768 / 177.539|

The MLX Qwen/Gemma/MiMo profiles show higher aggregate throughput at greater concurrency with higher individual latency. The DwarfStar DeepSeek profile shows negative scaling relative to c1:19.505tok/s at c1 versus8.159 at c2 and12.257 at c4, with a c4 latencyp95 of167.887seconds. This runtime-specific result is retained rather than tuned away; no causal implementation defect is asserted from the timings alone. MiMo’s strong serving result does not negate its growing-history resource failures.

Mistral’s c1/c2/c4 outputs are4.756/4.928/5.768tok/s, while median latency grows53.514/103.795/177.539seconds. All180 measured Mistral responses reached256 outputtokens, with measured inputs8215(8requests)/8216(52) per profile, distinct from8192target, and zero reported reused inputtokens. The native allocator can retain physical prompt snapshots despite cache_prompt=false; zero reused input is not zero physical cache memory. [Serving audit](../results/mistral-serving-summary-20261004/README.md) retains24 original/publication artifact pairs and byte-identical requests.

The owner changed the M5 task-owned display-idle policy during Mistralc2 at16:35:44.864UTC, after timed measurement began16:31:10UTC. That service was disabled through c1 and enabled through c4. Physical pixels were not inspected. Raw timings are unadjusted, and this condition change prevents clean causal attribution to concurrency alone. An earlier display-sleep request occurred during Mistral full replay at04:36:41UTC and is likewise retained without a timing-effect claim. These are real requested operating conditions, not corrections to data.

## Full recorded-request replay

| Configuration |Requests served|Measured duration s|Official end-to-end outputtok/s|Short-output warnings|
|---|---:|---:|---:|---:|
|Gemma4 31B ·8-bit MLX|168/168|2987.624|8.223|4|
|Qwen3.8 27B ·8-bit MLX|168/168|2024.850|8.347|7|
|DeepSeek V4 Flash0731 ·mixedQ4/DwarfStar|168/168|3033.066|5.052|11|
|MiMo V2.6 Flash ·MXFP4/MLX-VLM|168/168|1747.914|8.828|10|
|Mistral Medium3.5 128B ·Q4_K_M/llama.cpp|168/168|2719.372|5.256|53|

All five retained configurations served all168 recorded requests. This proves serving completion, not task solving or matching the recorded target output. The recorded workload has shorter varying histories and substantial cache reuse; it is distinct from a cold200K task request. Baseline endpoint context was not listed/reported to the replay client(reduced flagtrue/observed contextnull); that metadata limitation is retained. Mistral reported262144/requested65536/reducedfalse, which is endpoint metadata rather than semantic context proof.

Mistral’s replay retained53 short-output warnings and40 length-finished turns. Server prompt2596099/cached2416273/uncached179826 and server output14292 are distinct from local output13030 and recorded target30883. Its official5.25594 end-to-end rate and11.22343 output-time rate have different timing boundaries; neither is cold native decode. See [168-turn audit](../results/mistral-full-replay-audit-20261004/README.md).

## Two MiMo resource failures and the final owner omission

Original seed1001 failed request12 after11 complete responses with kIOGPUCommandBufferCallbackErrorOutOfMemory. Last successful native prompt227274/output18/cached226627 was observed; reconstructed233765 tokenizer-estimated input for the failed request was not final native usage. Whole-child minimum16.578GiB/swap growth3.4375MiB were within the declared host guards. That original attempt was preserved, unscored and never retried.

Original fresh seed1002 was admitted only after Mistral39 was fully accounted and all old inference controls/workers/holders exited. All53 MiMo artifacts were hash-verified, model/config/runtime/source fingerprints checked, the original baseline branches/default payloads compared and70 CPU checks passed on both hosts. Only r2/r3 deferrals were removed after exact-plan archive; IDs/seeds/full200K packet/20turns/2048cap/900s requests/7800s job/82% process/recommended wired/cache policy were unchanged. No runtime fix or history truncation was adopted.

Seed1002 failed request13 after12 complete responses at18:58:52.404UTC. The client’s missing-final-usage error is explained by the actual server Metal out-of-memory traceback at mx.eval(cache state). Last completed native prompt227541/cached226894/output18 is known; the failing request’s final usage and total input are UNKNOWN, with no estimate claimed. Server-logged incremental prefill6473/progress2048 is not a final total. Whole-child minimum15.152GiB/server16.034GiB/swap growth25.3125MiB remained within12GiB/2GiB host guards. The empty patch and missing final evaluator do not turn into a scorezero. [Independent second-failure audit](MIMO-SECOND-METAL-FAILURE-20261004.md) preserves11 artifact hash pairs and exact failure bindings.

These two actual device-memory events reached the explicit safety limit. The driver and owned workers stopped and no seed1003 inference was launched. After being told that this was the final remaining trial, the owner explicitly instructed that it be left out and the study finished. Original seed1003 is therefore owner-omitted, unrun and unscored. It supplies no observed failure, token usage or task score. The source review identifies full/rotating cache behavior and cache-state evaluation but proves neither physical array duplication nor a deterministic capacity bound or an invariant-preserving fix. Host free-memory counters do not guarantee device allocation capacity. Automatic further inference remains prohibited. The original 195-group declaration and previous report are archived, and the approved 194-group required scope is fully accounted.

## Interpretation and practical limits

Within these pinned observations, Qwen8-bit combines relatively short200K fill time, fast repository diagnostics and158/164 restricted coding outcomes; Gemma has the highest restricted coding count159/164 and5/5 short repair success with slower long-context/request latency. DeepSeek has high native steady decode and strong repository outcomes but a wide sustained spread and negative serving-concurrency scaling. MiMo has high speed/serving rates and154/164 restricted coding outcomes but only1/5 short repair success and two independently observed long-history GPU-memory failures. Mistral can complete exact200K performance workloads and151/164 restricted coding cases, yet its long fill time prevents the tested900s full-packet useful-work requests from finishing. These are workload/configuration tradeoffs, not universal model rankings or hardware conclusions.

The report retains all repetitions, functional failures, short-output warnings, unknown counts, setup exclusions and owner omissions. It does not repair/rescore generated answers, pool warmups or continuation boundaries, silently extend budgets, tune caches/weights for a failing ID, claim every group passed, or convert a required unrun cell into a failure. The M3 controller’s owner-reported crash/reboot interrupted supervision; M5 did not reboot. The earlier supervision gap is documented rather than claimed as healthy15-minute checks. Latest owner preference keeps displays awake on both Macs; no stored power/lock/security setting was changed.

## Evidence map and current disposition

- [Actual hardware inventory](../hardware/incoming-device.json), [model locks](../config/unified-models.lock.json), [Mistral model/runtime closure](../config/mistral-models.lock.json), [frozen protocol](UNIFIED-OVERNIGHT-PROTOCOL.md).
- [Reconciled baseline aggregate](../results/unified-overnight-20261002/README.md) and [Mistral aggregate](../results/mistral-extension-20261003/README.md), with raw per-run request/response/usage/evaluation/log/telemetry links.
- [Mistral39 completion audit](../results/mistral-campaign-completion-20261004/README.md):30 completed +9 independently audited unscored groups,1202 retained original/publication artifact pairs checked.
- [MiMo source/runtime validation](../hardware/mimo-original-continuation-validation-20261004.json), [model weights verification](../hardware/mimo-original-weights-verification-20261004.json), [actual start](../hardware/mimo-original-continuation-start-20261004.json), [two-event ledger](../hardware/compute-safety-two-events-20261004.json).
- [Final owned inference exit verification](../hardware/owned-inference-exit-closeout-20261004.json):both campaign controls/latest workers absent, no unexpected task-owned inference processes or shared holders. Preview/SSH forward/caffeinate/unrelated owners are preserved.
- [This report’s frozen source summaries](../results/research-report-20261004/source-summaries.json), exact parsed model metrics and coverage accounting. Earlier snapshots remain in Git history; the read-only report now reconciles already-exited saved results that a resumed driver had not yet revisited.

**Final disposition:** the study is closed at the owner-approved reduced scope: 183 completed groups, 11 actual unscored groups, 1 explicit owner omission, and zero remaining required groups. The report, scope archive, raw evidence and final owned-exit proof are retained. The existing 15-minute follow-up is PAUSED after final publication and live verification. The two-event inference stop remains in force. The report preview and display-awake assertions are retained; no main merge, personal-site/social deployment or benchmark submission is included in closeout.
