# Qwen large-context repository diagnostic — five fresh attempts

**4/5 attempts passed all 19 restored Django regression tests, with zero human rescues.** Median task wall time was **238.37 seconds (3m 58s)**. There were no infrastructure failures in the measured attempts.

| Attempt / seed | Input chat tokens | Model turns | Task time | Final result |
|---|---:|---:|---:|---|
| 1 / 1001 | 200,001 | 3 | 234.04 s | 19/19 tests pass |
| 2 / 1002 | 200,001 | 4 | 238.37 s | 19/19 tests pass |
| 3 / 1003 | 200,001 | 3 | 243.75 s | 19/19 tests pass |
| 4 / 1004 | 200,001 | 8 | 261.05 s | Regression still fails; eight reads, no edit |
| 5 / 1005 | 200,001 | 3 | 231.63 s | 19/19 tests pass |

All five initial request packets had the same SHA256: `7ab1bc9a6676fd0eafa33d492c09cc4b9770f2223ba545e41e02fb06d25b87d6`. Each attempt used a fresh model server/cache and repository. Normal cached follow-up turns were allowed. Temperature 0.2, explicit seeds, eight-turn limit, 2,048 output tokens per turn. Execution checkout `642eae96f79d499eb092e16d2410b77a392df036`. Standard Qwen 8-bit artifact/runtime locks were unchanged.

The first attempt spent 213.66 seconds waiting for its first visible output. The remaining read/edit/test turns were much shorter. Task wall time includes input processing, generation and tools/tests after server readiness, but excludes setup, file hashing, tokenization and server startup.

This tests one historical public Django bug (`django__django-14500`), not five independent tasks. It may have appeared in training data. **4/5 is the observed count for this scaffold and budget, not a general 80% reliability or intelligence score.** A larger task set, longer horizons, other models, matched M3 runs and repeated conditions are still needed. No human fixed the failed attempt or extended its turn limit.

Each sibling attempt folder retains its actual outputs/tool feedback, candidate patch, final test report and resource telemetry. The immutable test harness failed on the untouched baseline and passed with the published reference fix before these model runs began. See [the protocol](../../docs/REPO-DIAGNOSTIC.md).
