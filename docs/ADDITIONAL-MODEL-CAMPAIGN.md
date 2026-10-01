# Additional M5 models — owner-authorized conditional campaign

The owner explicitly requested the same rigorous tests on the local files downloaded for Darkbloom, after the downloads finish, with results in this localhost dashboard and the public GitHub repository. Darkbloom itself must not be turned on or operated. The original M3 remains busy and must not run inference.

## Readiness and identity

Use `scripts/inventory_downloads.py --machine studio-new --include-darkbloom-model-files`. This reads filenames, model JSON and file sizes without loading weights or invoking an app. Do not change or interrupt the owner's download process. The observed storage is the M5 user's Hugging Face cache; snapshots can use Darkbloom staging/finalization identifiers rather than Hugging Face Git commits.

Wait for the identified download batch to complete, not just one finished shard. Require all index-referenced or numbered shards, no `.part`/`.incomplete` files, no staging snapshot, and stable completed files. Treat audio tokenizers, vision encoders and draft components as parts of their model unless provenance establishes an independent checkpoint. File presence does not establish integrity. Pin source/checkpoint, native artifact revision, exact bytes, SHA256, tokenizer/template, actual tensor precision and compatible runtime in a separate additional-cohort manifest. Never silently replace the original three-model lock, change quantization, or take a file name as proof of its precision.

The observed Qwen package name says MXFP8 but its staging config currently reports a 4-bit default. Resolve final metadata and tensor layout before choosing a loader or making quality/precision claims. Do not run custom remote code just because a config requests it. Confirm supported independent MLX/llama.cpp/DwarfStar or another reviewed runtime; do not use the Darkbloom app executable as the benchmark engine or enable serving to obtain access.

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
