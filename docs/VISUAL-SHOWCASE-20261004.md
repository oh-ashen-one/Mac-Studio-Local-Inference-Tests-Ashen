# Image-generated benchmark result infographics

The owner requested a visual website showcase emphasizing speed comparisons, with detailed evidence on GitHub. The final five infographics were made with the built-in image-generation tool from exact benchmark numbers and edited with a reference sheet of sourced brand marks. Hardware-product artwork and rejected plotting-library exports are excluded from the published assets.

## Evidence and labels

The200K Qwen rate difference uses the full-precision M5 five-run median21.42618768956603 divided by the published M3 60-GPU result13.8, minus1:55.2622296%, displayed55.3%. The128K comparison uses the M5 five-run median24.44787 and published M3 80-GPU result17.2, displayed42.1%. Displayed rate labels are rounded to two decimals. Both are configuration reports with different software/corpus, not isolated chip-only effects.

The market infographic preserves M5 native decode30.6 at8192 input tokens; optimized M3 report45.8 at200K with MTP/selective prefill; DGX Spark serving output throughput37.3 at approximately204 input tokens with FP8/DFlash2; RTX5090 fixed-output decode98.2 at8192 with NVFP4/MTP3. These differing workloads/timers are labeled and no matched winner or cross-row speedup percentage is assigned. The reviewed DGX report does not supply a matched200K run.

The M5 lineup is the five retained configurations'200K/256-output five-run medians: MiMo37.68, DeepSeek37.61, Qwen21.43, Gemma15.25 and Mistral4.04. Model sizes, precisions and runtimes differ. The wait graphic retains212.930s context fill versus1184.985s reference TTFT and does not turn the different timing boundaries into a faster percentage.

All five final images were inspected after generation and logo edits. The visible values, axis origins and approximate bar proportions were checked against the source values. Brand shapes come from Lobe Icons; exact SVG assets are also used beside labels in the page. [Source review](../research/showcase-source-review-20261004.json), [logo sources and hashes](../research/showcase-brand-assets.json), [full prompt set](../outputs/benchmark-infographic-prompts.md), and [image manifest](../outputs/visual-showcase-manifest.json) preserve provenance. Logos identify the configurations; no endorsement is claimed.

## Release and verification

The images are in viewer/assets/infographic-*.png. Run `.venv/bin/python scripts/build_visual_showcase.py` to bind them to frozen source summaries, record hashes/dimensions and rebuild the five-PNG ZIP. The script performs no pixel edits and imports no inference library. Assets are served only from viewer/assets; traversal and escaping symlinks are rejected.

77 CPU checks pass on the controller, including source-bound rate arithmetic, final image hashes/dimensions, sourced logo availability and private-file rejection. The candidate page loaded all images and logos, selector/expand controls worked, and the narrow389px layout had no horizontal overflow. Page height was approximately one screen in the tested narrow layout and about one screen in the desktop layout. Browser screenshot capture was unavailable; exported images were inspected directly and UI verification used rendered accessibility state and DOM layout bounds. This does not substitute for the owner's subjective design acceptance.

Publish and sync this task branch, run the same CPU checks on actualM5, then restart only the verified owned read-only preview because its asset-serving module changed. Preserve existing forwarding/Tailscale routes, displays awake, raw measurements, the two-event inference stop and the PAUSED follow-up. No personal-site deployment or main merge is part of this preview update.
