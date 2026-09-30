# Ready for the second Studio

The owner confirmed the purchased machine: **M5 Ultra, 36-core CPU, 80-core GPU, 32-core Neural Engine, 256 GB unified memory, 2 TB storage**. The old machine was inspected as **M3 Ultra, 32-core CPU, 80-core GPU, 256 GB, 2 TB**. Device/OS inspection on the new machine remains an arrival-day step.

## Final three-model cohort

| Model | Exact artifact | Size (decimal GB) | Engine | Why selected |
|---|---|---:|---|---|
| Qwen 3.8 27B | `mlx-community/Qwen3.8-27B-8bit` | 29.53 | MLX-LM/Metal | Requested anchor; widely adopted, modest resident size, high-precision quantized baseline |
| Gemma 4 31B IT | `lmstudio-community/gemma-4-31B-it-MLX-8bit` | 33.80 | MLX-LM/Metal | Strong independent family, high adoption, similar dense-model size to Qwen |
| DeepSeek V4 Flash 0731 | `antirez/deepseek-v4-gguf`, Q4KExperts / F16HC / F16Compressor / F16Indexer / Q8Attn / Q8Shared / Q8Out, calibrated 0731 file | 164.63 | DwarfStar/Metal | Full Flash checkpoint with a quantization/runtime combination explicitly recommended by its maintainer for 256 GB Macs |

**Exactly three standard models. No Mistral or abliterated variants.** The canceled R1 distill is not part of the cohort. Total selected artifact storage is about 228 GB (212 GiB). Load one model at a time; the disk total is not the simultaneous RAM requirement. Vision towers may be included in MLX files, but this initial campaign tests text only.

Full immutable revisions, file sizes and SHA256 hashes are in `config/models.lock.json`. The Qwen and Gemma 8-bit choices favor quality retention while leaving plentiful room for context. DeepSeek uses the maintainer's calibrated mixed Q4 recipe to fit comfortably enough for useful contexts; it is not the much larger BF16 checkpoint. These choices are strong starting points, not a measured claim that 8-bit beats 4-bit on speed or that any model is universally “smartest.” A later paired 4-/8-bit sweep can quantify that trade-off.

The Hugging Face API snapshot in `config/selection-evidence.json` recorded approximately 7.0M downloads / 16.6K likes for Qwen, 4.5M / 4.0K for DeepSeek Flash 0731, and 9.7M / 4.0K for Gemma. Counts describe the official base-model repositories at the observation time, not the downloaded conversion repos. Likes are not star ratings and downloads do not establish intelligence. GPT-OSS-120B was also considered; Gemma offered more base-model downloads in this comparison and a recent, supported independent dense-model control. This is a bounded selection, not an exhaustive global leaderboard.

DeepSeek V4.1 is newer, but its available DwarfStar formats add large SSD-resident Engram tables. The Q4 main weights exceed 256 GB; the Q2 format still uses roughly 341 GiB of disk and includes SSD-dependent access. V4 Flash 0731 Q4 is the cleaner resident-model starting point for this hardware comparison. The full 671B V3.2 / V4 Pro and two-machine experiments remain later capacity tracks.

References: [Qwen artifact](https://huggingface.co/mlx-community/Qwen3.8-27B-8bit), [Gemma artifact](https://huggingface.co/lmstudio-community/gemma-4-31B-it-MLX-8bit), [DeepSeek artifact](https://huggingface.co/antirez/deepseek-v4-gguf), [DwarfStar Mac memory recommendations](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/docs/METAL.md), [DwarfStar model definitions](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/docs/MODELS.md).

## What is implemented

- A Python 3.12.13 environment with exact package versions, including MLX 0.32.3 / MLX-LM 0.31.3.
- Native DwarfStar source pinned to a full Git commit; a fixed portable CPU compilation target on both machines and automatic Metal hardware paths.
- Immutable downloads and full-file SHA256 verification.
- A sequential runner with one model per worker, per-checkout exclusion lock, machine identity checks, free-memory checks, setup smoke mode, core fixed-token mode, append-only records and failure retention.
- A matched-results comparer that rejects incompatible configurations and excludes smoke/warmup rows.
- Loopback-only model-server launch commands and eight original correctness diagnostics. Those eight tasks are setup checks, not an intelligence leaderboard.
- A read-only setup doctor and sanitized hardware inventory collector.

The full published quality suites, HTTP concurrency/load tests, power-meter integration, two-hour soaks and distributed cluster adapter are still later campaign stages. The preparation does not claim these are implemented or already measured.

## First setup on the new Mac

1. Complete macOS first-run setup and connect Ethernet. Confirm the delivered specifications. Match the old Mac's macOS build if supported; otherwise keep results in a hardware-plus-OS cohort until matched. Do not upgrade or reboot a shared machine without scheduling it.
2. Enable **System Settings → General → Sharing → Remote Login** for the intended user, and note the new Mac's address. Pair its SSH host key through the normal verified first-connection flow. Keep credentials and IP addresses out of the public repo. No public port forwarding is needed.
3. From the old Mac, verify `ssh USER@NEW_MAC`. Use an existing authorized public key or add a dedicated public key through the owner-controlled setup. Never copy private keys to the new Mac. No SSH alias or network configuration has been changed by this preparation.
4. On the new Mac, clone this repo and explicitly select the preparation branch:

```sh
git clone --branch codex/setup-20260930 https://github.com/oh-ashen-one/Mac-Studio-Local-Inference-Tests-Ashen.git
cd Mac-Studio-Local-Inference-Tests-Ashen
bash scripts/bootstrap.sh
.venv/bin/python scripts/build_native.py
```

The bootstrap needs `uv` and Apple's command-line developer tools (`xcode-select --install` if missing). It installs a pinned Python environment inside the repo and builds the exact native dependency; it does not change system Python or another local-model app.

5. Either download directly using pinned revisions:

```sh
.venv/bin/python scripts/models.py download
```

or copy the existing `models/` directory from the old Mac over the local network into the new checkout. For a normal username/host and a no-space destination path:

```sh
rsync -avP models/ USER@NEW_MAC:/ABSOLUTE/PATH/TO/REPO/models/
```

Use a resumable LAN/Thunderbolt transfer, not a new model search. The expected payload is about 228 GB. Both transfer methods end with:

```sh
.venv/bin/python scripts/models.py verify
.venv/bin/python scripts/doctor.py
.venv/bin/python scripts/collect_inventory.py --machine-id studio-new > hardware/incoming-device.json
.venv/bin/python -m pytest -q
.venv/bin/python scripts/bench.py --machine studio-new --suite smoke --output work/new-smoke.jsonl
```

For a short timing-path check before the full campaign, add `--suite pilot` with the same runner; pilot rows are excluded from the comparer.

An “ok” download is insufficient: every artifact must pass hash verification, and each model must generate a valid reply on the new device. The live device inventory is separate from the owner-confirmed order.

## Launch the first measured comparison

Reserve an idle window on both machines. Close other GPU/model workloads with their owners; never terminate another session to clear the bench. The core runner rejects detected EXO/LM Studio/Ollama services and known serving processes. This is a conservative check, not a complete guarantee that no background work exists. Record background state and displays. Use the same configuration on each machine.

Old Mac:

```sh
.venv/bin/python scripts/bench.py --machine studio-old --suite core --output work/old-core.jsonl
```

New Mac:

```sh
.venv/bin/python scripts/bench.py --machine studio-new --suite core --output work/new-core.jsonl
```

The arrival subset contains **15 cells per machine** (three models × five input/output cells), ten measured repeats each plus warmups, spread across three sessions. Both machines together give 300 measured runs. This is a practical first slice of the broader README plan, not the original two-backend Cartesian matrix. Expect a multi-hour job; use pilot runtimes to schedule it. Failures are retained, and no failed model is automatically retried.

After copying both result files to one checkout:

```sh
.venv/bin/python scripts/compare.py work/old-core.jsonl work/new-core.jsonl --output work/comparison.json
```

It writes JSON plus CSV with matched sample counts, median ratios and a deterministic paired bootstrap interval. It refuses different OS builds, model revisions, prompt hashes, settings or runtime locks. Keep unmatched/different-OS runs as a separately labeled cohort rather than weakening this gate. Raw outputs stay in `work/` until reviewed and intentionally promoted to a versioned result release.

MLX mode records token-level TTFT and steady decode rate. It does not pretend input-tokens/TTFT is pure prefill throughput. DwarfStar mode preserves the native prefill/steady-decode CSV and does not call its post-prefill first-generation time TTFT. DwarfStar core cells start fresh processes; MLX cells reuse a loaded model within each session. Compare each engine/model setup across machines, not engine internals as if they had identical cache/load semantics. Native first-run compilation/caching effects must be examined in pilot data before headline reporting.

## Chat and diagnostic commands

Start one server (in a headless task-owned process if running unattended), for example:

```sh
.venv/bin/python scripts/serve.py qwen-27b --port 18181
```

Valid IDs: `qwen-27b`, `gemma-31b`, `deepseek-v4-flash`. The endpoint binds to `127.0.0.1`; use an SSH tunnel for remote testing. Run the diagnostic from another process:

```sh
.venv/bin/python scripts/quality_smoke.py --model qwen-27b --port 18181 --output work/qwen-quality-smoke.jsonl
```

Repeat for the other models one at a time. The test records the expected pinned model revision, chip, complete request, response, actual token usage if returned, wall time and failures. MLX requests select the already-loaded `default_model` with Hub access disabled, preventing implicit downloads or a switch to an unpinned model. Thinking is disabled explicitly where the backend supports the selected request control; verify the returned behavior before drawing quality conclusions. Reasoning-on quality trials need a separate documented budget.

## Retention and cleanup

The owner explicitly requested this machine remain ready for tomorrow. Keep this one active installation, its virtual environment, pinned native binaries and the three model downloads. These are required staged inputs, not abandoned QA worktrees. Their manifests and setup source are pushed; third-party weights stay out of Git. Do not delete shared caches or other sessions. Remove canceled downloads and temporary build/object files where they are not needed for the staged setup. After the comparison is published, retire the task-owned checkout and disposable evidence under the owner's normal cleanup policy.
