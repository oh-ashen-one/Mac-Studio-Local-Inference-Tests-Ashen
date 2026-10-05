# Visual benchmark showcase

The landing page presents five image-generated benchmark infographics, with sourced company/model logos beside the relevant labels. A compact selector changes the main image; each figure can be expanded and downloaded, and the full image pack is available as a ZIP. Detailed methodology and raw results are linked on GitHub.

The image set contains:

- M5 versus published M3 at200K: +55.3% reported Qwen generation rate.
- Both80-GPU configurations at128K: +42.1% reported Qwen generation rate.
- M5, optimized M3, DGX Spark and RTX5090 configuration snapshots, with context/precision/acceleration labels.
- Five-model200K generation medians on the M5.
- Reported200K input-processing wait, retaining the different timer definitions.

These are reported configuration comparisons. The owner's own M3 has not supplied a matched measured cohort. External optimized results are retained and may exceed the M5 baseline. The source-bound values, image hashes, full generation prompts and logo sources are recorded in [visual release notes](VISUAL-SHOWCASE-20261004.md).

The page serves local fonts and assets, respects reduced-motion preferences, and keeps the private laptop preview route. The read-only server has no inference-start endpoint. The completed study and paused follow-up are unchanged.

## Viewing from the laptop

The benchmark preview runs on the Studios. `localhost` in a laptop browser refers to the laptop itself, so the Studio loopback URL does not provide cross-machine access.

The controller now exposes the existing read-only preview on TCP port18765 through **Tailscale Serve, privately within the existing tailnet**. Connect Tailscale on the laptop, then open `http://<Studio-Tailscale-IP>:18765/`; discover the current Studio address with `tailscale status`. No public Funnel or website deployment is enabled. Existing Tailscale Serve ports are preserved. The private address and exact previous Serve configuration are retained only in ignored task-local `work/` receipts.

The Studio-side endpoint and closed-study API were verified. The laptop showed offline at setup, so end-to-end laptop access requires its Tailscale connection and has not yet been observed from the laptop. The route now forwards to the controller’s own read-only showcase service on loopback18765; `work/visual-showcase-preview.pid` identifies it. The previous owned SSH forward was retired; the M5 service is preserved. This access change does not restart the M5 preview, run inference or resume the paused benchmark follow-up.

To remove only this task's private preview route when requested: `tailscale serve --tcp=18765 off`. Do not use a global Serve reset, which would remove other owners' routes.
