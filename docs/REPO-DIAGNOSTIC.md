# Large-context repository repair diagnostic

This is an intentionally narrow, transparent check using the public historical bug `django__django-14500`, not an intelligence leaderboard or proof of arbitrary long-horizon coding ability. Model training may contain this issue. The separately reported AA benchmark replays recorded trajectories and cannot answer whether a model can repair this bug.

## Reproduce

Preparation, no model load:

```sh
.venv/bin/python scripts/repo_task.py --prepare
```

After the owner reserves the M5 GPU, inspect the active task processes and use a fresh run ID:

```sh
.venv/bin/python scripts/run_repo_task.py --allow-inference --run-id m5-repo-qwen-YYYYMMDD --attempts 5
```

Do not run this on the original M3 while other sessions use its GPU. The runner uses the standard Qwen 8-bit MLX model and defaults to the new Studio. After the owner explicitly releases the original GPU, pass `--machine studio-old`; hardware checks and the shared slot guard still apply. Other-model extensions must preserve the task/scaffold and record their configurations.

The initial request contains 200,000–200,032 chat tokens from the pinned repository source plus the bug statement. Actual tokenizer count, packet hash, server usage, output and tool feedback are retained. Each attempt gets a new process/cache and repository; later turns may use the server's normal prompt cache. Report initial cold fill separately from warm turns. Eight model turns, 2,048 output tokens per turn, temperature 0.2 and recorded seeds bound the attempt. JSON format errors receive mechanical feedback and consume a turn. The controller supplies no suggested fix. Human rescues are counted separately from ordinary test feedback.

Only read/replace/test/finish actions exist. Model edits are limited to `django/db/migrations/*.py`. There is no generated shell-command execution. Evaluation copies trusted source and tests afresh, applies candidate implementation changes, adds the published regression test, and runs 19 tests in a macOS sandbox with no network or access to private user files. CPU and wall-clock limits bound execution. The baseline fails the expected regression; the published reference patch passes all 19. A private sentinel read and socket connection were explicitly denied. macOS's dyld boot cache requires read access to its system cache locations; the profile grants those without granting user-home access.

Task wall time starts after server readiness and ends after final testing; it includes input fill, generation and tools/tests but excludes preparation, hash verification, tokenization and server startup. `scripts/report_repo_task.py` summarizes the actual saved attempts without running anything.

`result.json` records each attempt, successful/failed checks, response caps, latency, actual token usage and zero-rescue count; `candidate.patch`, test logs and resource telemetry provide the evidence. Preserve every unsuccessful attempt. Do not infer success from valid JSON, a patch, or model claims. The final test result is the acceptance criterion. Report successes as N/5 only once five attempts actually ran; fewer attempts remain a diagnostic sample. This small historical task does not establish a general finish-without-rescue rate.

Django source/test material is BSD-3-Clause. The task metadata and regression patch come from the pinned Artificial Analysis repository, derived from SWE-bench. See `config/repo-task.json` for provenance and `config/repo-eval/validation.json` for evaluator checks. Runtime downloads and fresh candidate workspaces are ignored by Git; intentional result releases are versioned.
