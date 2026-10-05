# Both Studios prepared — October 1, 2026

The new M5 Studio is now fully staged at `/Users/midirstudio2/mac-studio-inference-tests`. The original M3 installation remains at `/Users/midir/Documents/Codex/2026-09-29/hey-buddy-make-a-new-github`. Both are on the published branch `codex/m5-model-setup-20261001`.

## Verified on the new M5

- Qwen 3.8 27B, 8-bit MLX: **29,531,519,752 bytes**, 18 files verified.
- Gemma 4 31B IT, 8-bit MLX: **33,795,546,901 bytes**, 15 files verified.
- DeepSeek V4 Flash 0731, calibrated mixed Q4: **164,633,502,592 bytes**, one file verified.
- All **34 selected files** passed SHA256 verification against the immutable model lock. Total: **227,960,569,245 bytes** (about 228 GB / 212.3 GiB).
- Python 3.12.13 and all 38 locked packages are installed; package versions match the original Studio.
- Apple Command Line Tools installed. DwarfStar was built on the M5 from pinned commit `0aaea5a238fb41a35106a551e73c8409dfb751ac`, with the same build flags and Apple Clang 21.0.0 (`clang-2100.3.34.2`) used on the M3.
- Both machines currently run macOS **27.0.1, build 26A434**.
- The **17 non-inference harness tests passed** on the M5 and the original Studio.
- The readiness receipt reports **prepared_not_loaded**. No inference or GPU model validation was performed in this setup.

A wireless Mac-to-Mac copy was initially slower, so it was canceled and its partial files removed. The new Mac downloaded the exact locked revisions directly from Hugging Face. The final hashes establish artifact identity independently of the transfer method.

## Receipts

- [New machine readiness](../hardware/preparation-new.json)
- [New machine file verification](../hardware/model-verification-new.json)
- [Paired readiness checks](../hardware/pair-readiness.json)
- [Current M5 inventory](../hardware/incoming-device.json)
- [Current M3 inventory](../hardware/existing-studio.json)

Native binaries are independently compiled and their hashes are recorded in the receipts. They need not have identical hashes because debug/build paths differ. The model bytes, runtime package versions, native source revision, build flags, compiler version and OS build were matched.

## Starting a test session

Return to this chat and explicitly start the tests when the GPUs are available. Recheck other sessions, memory and current shared-brain safety rules first. Do not kill or unload anyone else's workloads. One model at a time.

The first GPU phase is a short validation run on each computer. Download verification and a successful compile do not prove that generation works on the M5. DeepSeek generation is still unverified on both machines. Full performance/quality results follow successful validation and reserved quiet windows.

After explicit authorization, the runner accepts:

```sh
.venv/bin/python scripts/bench.py --allow-inference --machine studio-new --suite smoke --output work/new-smoke.jsonl
```

Use `studio-old` on the original machine. Continue with the pilot and full core suite only after inspecting the small validation results. Review actual comparison results through the read-only localhost viewer before publishing to the personal website.

The new Mac's models, virtual environment, compiled runtime and readiness receipts remain intentionally staged. Temporary download leftovers and compilation objects are disposable; preserve the required staged inputs. No apps, model servers, benchmarks or automations were left running by this preparation.
