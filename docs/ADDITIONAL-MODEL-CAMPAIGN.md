# Additional M5 models — owner-authorized conditional campaign

The owner explicitly requested the same rigorous tests on the local files downloaded for Darkbloom, after the downloads finish, with results in this localhost dashboard and the public GitHub repository. Darkbloom serving must remain off. The owner explicitly authorized retrying the failed Qwen download; the official download-only command completed on October 1. No other app/provider operation is authorized. The original M3 remains busy and must not run inference.

## Readiness and identity

Use `scripts/inventory_downloads.py --machine studio-new --include-darkbloom-model-files`. This reads filenames, model JSON and file sizes without loading weights or invoking an app. Do not change or interrupt the owner's download process. The observed storage is the M5 user's Hugging Face cache; snapshots can use Darkbloom staging/finalization identifiers rather than Hugging Face Git commits.

Wait for the identified download batch to complete, not just one finished shard. Require all index-referenced or numbered shards, no `.part`/`.incomplete` files, no staging snapshot, and stable completed files. Treat audio tokenizers, vision encoders and draft components as parts of their model unless provenance establishes an independent checkpoint. File presence does not establish integrity. Pin source/checkpoint, native artifact revision, exact bytes, SHA256, tokenizer/template, actual tensor precision and compatible runtime in a separate additional-cohort manifest. Never silently replace the original three-model lock, change quantization, or take a file name as proof of its precision.

The verified Qwen package has catalog FP4 and affine 4-bit/group-64 configuration; its legacy identifier says MXFP8. Label the actual precision, not the identifier. All 66 files across Qwen and MiMo passed SHA256; see `hardware/additional-model-verification.json` and the separate additional-model lock. Do not run custom remote code just because a config requests it. Confirm supported independent MLX/llama.cpp/DwarfStar or another reviewed runtime; do not use the Darkbloom app executable as the benchmark engine or enable serving to obtain access.

## Measurement matrix

1. Verify M5 identity, runtime, free memory, swap and other GPU work; hold the shared slot and start one model at a time. Preserve the owner's apps/processes and downloaded files.
2. Run the small compatibility/format validation stage; keep it labeled setup rather than a benchmark.
3. Reproduce the 200,000-actual-input / 256-output cold-context workload from the pinned corpus. Record actual token IDs/counts, fresh KV/state, prefill chunk size, precision, model-load/tokenization boundaries, fill latency, post-fill generation, memory and swap. Repeat valid speed cells for a median/range, and show sample count rather than comparing a peak with a median. The existing M5 long-context baseline is n=1 and must remain labeled so until repeated.
4. If 200K is unsupported or does not fit within the guard, preserve that outcome. A shorter supported-context run is a separate labeled cell, never silently substituted or described as 200K.
5. Run the official agent replay only where its context, tool-format and exact-output requirements are supported. Preserve qualification/comparability flags. It measures serving speed, not solved tasks. Do not swap to another model/quantization to hide an unsupported cell.
6. Run the same bounded Django diagnostic where compatible: pinned issue/snapshot/tests, five fresh attempts with recorded seeds, 200K starting context, eight turns, 2048 output tokens per turn, fixed reasoning/sampling policy and immutable sandboxed evaluation. Preserve every failure and any human rescue. Unsupported controls/scaffolds require an explicit separate cell, not a claimed equivalent score.
7. Unload each task-owned model before the next. Preserve all raw successful/failed records and exact runtime/model settings. No automatic retries of crashes or unbounded loops.

## Reporting and follow-up

The existing 15-minute heartbeat continues this work, remains quiet when unchanged and reports meaningful readiness, results, failures or a concrete new blocker. It must not repeatedly ask the owner for an unknown path. Stop/pause it after the identified cohort is handled or the owner cancels.

Update the visual dashboard and push task-branch changes throughout. New model results must carry actual model/quantization/context/runtime identities and sample counts. Reference comparisons do not isolate hardware when those differ. No website deployment, main-branch merge, social publication or external benchmark submission is authorized by this request.

DeepSeek's existing valid measurement needs no repeat merely because its reference lacks context metadata: 38.20 versus 36.01 tok/s is a 2.19 tok/s reported gap across unmatched runs. A controlled hardware percentage needs a matched M3 run or a sufficiently specified comparable reference.

## Independent runtime qualification

Qwen failed with baseline MLX-LM 0.31.3 due to an MTP/RMSNorm conversion mismatch, before any performance score was accepted. The failed raw replies are retained. Official MLX-VLM at `d73f4b1ad90194d53e37beac6e9eef76976aadc5` drops MTP weights before detecting norm-shift convention and passes the same qualification. Its independent MiMo implementation supports the V2.6 fused QKV and MXFP4 expert tensors. This environment is separately pinned and never changes the original cohort runtime. Text-only tests do not establish vision/audio performance.

The MLX-LM HTTP server does not implement the AA exact-output `ignore_eos` policy. An attached independent-server replay may use the official **recorded** cap policy as a separate exploratory cell, with this difference disclosed; it is not a comparable replacement for the original exact-length Q4_K_M managed run. No result is submitted to AA.

## Reproduce the additional runtime and resume

The exact extra environment is independent of the original `.venv`:

```sh
.tools/uv venv --python 3.12.13 vendor/vlm-runtime/.venv
.tools/uv pip install --python vendor/vlm-runtime/.venv/bin/python -r config/requirements-mlx-vlm.lock
```

This only prepares packages. Inference still requires owner authorization and a verified M5 window. With that authorization, `scripts/additional_campaign.py --allow-inference` runs the finite sequential matrix. Inspect `work/additional-campaign.json` and its live PID before invoking it: never start a second driver. It resumes only completed cells, refuses existing failed/incomplete cells pending review, and has per-job deadlines and memory/download/GPU-holder guards.

[Current saved results and all failure links](../results/m5-additional-summary-20261001/README.md). Summaries are regenerated from raw saved artifacts with `python3 scripts/report_additional.py`.

The initial attached-server qualification also retains AA's official context-discovery flag: `model-not-listed`, `observed_tokens: null`, and non-comparable status. The independently verified model context limit and successful 200K tests do not overwrite AA's endpoint qualification metadata. The six-turn Qwen mini run served all six requests, with three short-output warnings; it is a setup cell, not a substitute for the full replay or a task-solving score.
