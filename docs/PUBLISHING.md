# Ashen Benchmark publication and final video

## Website

Initial integration prepared in [Ashen-Port-Site PR #2](https://github.com/oh-ashen-one/Ashen-Port-Site/pull/2). The branch is pushed; the PR is open and has not been merged or deployed. TSX parsing/transpilation passed for all three edited files; full application build and browser visual review remain pending.

Destination: the existing Ashen Benchmark route at `/benchmark` in `oh-ashen-one/Ashen-Port-Site`. Preserve its existing design and model-grouped game results. Introduce a distinct hardware/local-inference study with status **Planned — results pending**, linked to this public repository. Do not label this a completed game build or invent a winner.

Initial copy: “Mac Studio Local Inference Tests Ashen — my existing M3 Ultra (32-core CPU, 80-core GPU, 256 GB) versus my incoming 256 GB / 2 TB Studio. Matched-model speed, answer quality, long context, power use and two-Mac clustering. Incoming hardware will be verified on arrival; results pending.”

After data collection, show filters for machine, model, engine, quantization, context and concurrency. Charts: TTFT versus context, decode throughput, throughput versus latency, quality versus latency, memory versus context, energy per solved task, and cluster versus single-node versus replicas. Tables must expose sample counts, uncertainty, failures, protocol/version and links to raw data. Generate site data from the same versioned result records used by the README; no manually maintained duplicate numbers.

Keep planned, measured and independently reproduced statuses distinct. Update through a branch/PR and obtain owner permission before merging into `main`. An open PR is not a live deployment. Preserve the owner's existing X link in the footer.

## GitHub release

Publish README summary, sanitized hardware manifests, locked runtime/model manifests, environment/build commands, protocol revision, prompt hashes, raw JSONL/CSV, evaluation outputs where licensed, reproducible chart scripts, uncertainty and all limitations. Store larger approved evidence as checksummed named release assets; never commit downloaded model weights, secrets or unbounded videos. Tag releases only after validation. Keep reruns/version updates distinct from the original cohort.

## YouTube/game loop — last phase, no build started here

Use the completed inference results to choose 2–3 configurations. Frame the episode around a concrete task: both machines receive the same original small-game brief, same starting repository and same frozen acceptance checks. A third lane can use the big clustered model. Select the game with the owner when this phase begins; do not assume an engine or story now.

Consult the `gaming-ralph-loops` engine recipes, operations checkpoints and failure catalog before implementing the harness. The current user-selected concept-to-engine art workflow overrides older asset-pack guidance. No concept generation or animation/video generation is commissioned by this plan.

Run two separate experiments: (1) same model and equal token/tool budget on each machine, (2) equal wall time (for example, a preregistered two-hour budget) with the chosen model per setup. Use at least three independent seeds/runs for any performance conclusion; a single filmed attempt is a demonstration. Keep tool permissions, context policy, retry limits, network access and manager interventions identical and recorded. If a cloud critic/director intervenes, label its model, tokens, time and changes; it is no longer an entirely local-model-only run.

Measure time to first playable version, behavioral test passes, regressions, accepted features, crashes, token/tool use, inference time versus build/test time, and time spent blocked. Capture rendered evidence at a fixed resolution and quality; reserve GPU capacity consistently so capture itself does not bias one machine. Test controls, full loop, ending and restart. Agent checks do not substitute for the owner's judgment of fun/responsiveness.

Use one task-owned renderer per agent with the shared slot lock and an initial global cap of four. No engine launch in this planning phase. Stop after two crashes, close idle engines, and clean task-owned caches/workspaces after the branch and required evidence are safely remote. Do not leave parallel builds or captures consuming hundreds of GB.

Preserve the complete run and failure ledger before editing highlights. The final video should explain the machines, measurement controls, side-by-side loop, actual playable results and honest failure cases; publish the raw benchmark separately from the entertainment edit. Video assembly/generation is deferred until explicitly begun and must follow the applicable video workflow then.
