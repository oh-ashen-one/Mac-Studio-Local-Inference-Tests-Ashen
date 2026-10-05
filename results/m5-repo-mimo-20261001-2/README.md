# MiMo repository trial 2 — unsuccessful within the declared budget

Seed 1002 completed eight valid read actions, made no edits and failed the target regression. Final result: 18/19 tests passed, empty candidate patch, **583.619 seconds**, zero human rescue. The original 200,001-token starting packet, eight-turn limit and 2048-token response limit were unchanged.

The server reused a large conversation prefix after the initial request. Server telemetry observed 5.25 MiB system-swap growth from its starting value; the broader campaign telemetry had an earlier, higher starting value and showed no increase above that value. These are different system-wide sampling intervals, not process attribution. Minimum sampled available memory was 14.55 GiB, above the existing 12 GiB guard.

All raw prompts, responses, feedback, immutable evaluation logs, hashes and telemetry remain in this directory. This is a failed bounded diagnostic, not a runtime crash or a general intelligence score. Attempt 3 is running; the declared five-trial cohort is incomplete.
