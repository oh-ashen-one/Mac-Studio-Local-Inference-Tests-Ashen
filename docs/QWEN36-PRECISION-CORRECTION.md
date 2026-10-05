# Qwen 3.6 publication-label correction

October 2, 2026 owner timezone. Correct publication label: **Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates)**.

The downloaded config explicitly records `bits: 4`, `mode: affine`, `group_size: 64`, with layer gate/shared-expert-gate overrides at eight bits. The saved vendor catalog calls manifest `d932e96b00404b0575fff47e2dac8ed113056b3f22d0040c3c8d3f9ef25b09ed` `fp4`, while its legacy package ID contains `mxfp8`. Neither name establishes floating FP4 or MXFP8 tensor encoding. No tensor bytes were read for this correction.

Current presentation labels/descriptive metadata are corrected. Original model locks, package IDs, catalog fields, raw results, runtime settings and measurements remain unchanged. Historical prose that used FP4 must be read with this dated correction. The correction is a factual label change, not a new benchmark configuration.

Darkbloom v0.9.14's [ModelsCommand.swift](https://github.com/Layr-Labs/d-inference/blob/v0.9.14/provider-swift/Sources/darkbloom/ModelsCommand.swift#L129-L164) derives its checkmark from the unfiltered on-disk scanner's model IDs. It means locally downloaded/discovered, not memory eligibility, provider activity or successful model testing. Source was read without invoking the app/CLI; the default catalog command can run a GPU capability diagnostic, so it was deliberately not executed for this inspection.
