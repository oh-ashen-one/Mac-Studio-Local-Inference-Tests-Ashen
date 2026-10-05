# Full visual research landing page

The page represents the complete retained study as a visual research story, with speed comparisons leading the page. Fixed navigation jumps to the major sections. Sourced company and model logos remain beside the relevant configurations. No download, save or image-pack promotion is shown.

The landing page includes:

- M5 versus published M3 configurations at200K/128K, with rate differences and reported input wait.
- DGX Spark, RTX5090 and optimized M3 snapshots, keeping different prompt/precision/acceleration settings visible.
- All five retained model rates, an interactive8K-to200K curve plot and preserved earlier Qwen profiles.
- Sustained2048-output medians and observed ranges, including the slow DeepSeek repeat.
- HumanEval pass-rate rings, repository8-/20-turn conditions,200K retrieval and structured JSON outcomes.
- Serving concurrency1/2/4 with throughput/latency switching, plus the full168-request replay per configuration.
- Study extent, explicit unscored/omitted outcomes, and GitHub links to the full report, methods and raw records.

The five image-generated result figures are retained as comparison anchors. The remaining charts are native SVG/HTML graphics drawn from frozen numeric records, so axes, ring fractions, ranges and unscored statuses remain exact. Detailed source records stay in GitHub. The read-only controller preview imports no inference runtime; the closed study and PAUSED follow-up are unchanged.

## Viewing from the laptop

The benchmark preview runs on the Studios. `localhost` in a laptop browser refers to the laptop itself, so the Studio loopback URL does not provide cross-machine access.

The controller now exposes the existing read-only preview on TCP port18765 through **Tailscale Serve, privately within the existing tailnet**. Connect Tailscale on the laptop, then open `http://<Studio-Tailscale-IP>:18765/`; discover the current Studio address with `tailscale status`. No public Funnel or website deployment is enabled. Existing Tailscale Serve ports are preserved. The private address and exact previous Serve configuration are retained only in ignored task-local `work/` receipts.

The Studio-side endpoint and closed-study API were verified. The laptop showed offline at setup, so end-to-end laptop access requires its Tailscale connection and has not yet been observed from the laptop. The route now forwards to the controller’s own read-only showcase service on loopback18765; `work/visual-showcase-preview.pid` identifies it. The previous owned SSH forward was retired; the M5 service is preserved. This access change does not restart the M5 preview, run inference or resume the paused benchmark follow-up.

To remove only this task's private preview route when requested: `tailscale serve --tcp=18765 off`. Do not use a global Serve reset, which would remove other owners' routes.
