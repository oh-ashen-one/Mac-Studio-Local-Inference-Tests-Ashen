# MiMo V2.6 Flash — five bounded repository trials

**0/5 attempts passed the target regression**, with zero human rescue and median task time **577.343s (9m 37s)**. All trials started with 200,001 input tokens, used the same pinned historical Django bug and immutable 19-test evaluator, and retained the eight-turn / 2048-output-token-per-turn limits. Seeds were 1001–1005; temperature was 0.2.

| Attempt | Seconds | Outcome |
|---|---:|---|
| [1](../m5-repo-mimo-20261001-1/result.json) | 587.866 | Eight reads, no edit |
| [2](../m5-repo-mimo-20261001-2/result.json) | 583.619 | Eight reads, no edit |
| [3](../m5-repo-mimo-20261001-3/result.json) | 541.170 | Ineffective edits; two rejected exact-span replacements |
| [4](../m5-repo-mimo-20261001-4/result.json) | 577.343 | Eight reads, no edit |
| [5](../m5-repo-mimo-20261001-5/result.json) | 559.614 | Seven reads and one ineffective edit |

All five completed normally at the declared turn limit. The target regression remained failing. These are outcomes of one historical public bug under a fixed scaffold, not a broad intelligence score. Conversation-prefix reuse was observed after initial requests, unlike Qwen 3.6's zero reported reuse.

These trials used plain JSON actions in response text, with no formal OpenAI tool-schema parser. The separately identified XML/JSON auto-parser mismatch in AA replay does not reclassify or invalidate these task outcomes. No trial was rescued, extended or retried. Full transcripts, patches, failures, hashes and telemetry remain in each linked run directory.
