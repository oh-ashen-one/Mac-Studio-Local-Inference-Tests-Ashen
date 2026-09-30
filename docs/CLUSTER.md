# Two-Mac cluster plan

## What we are testing

The observed old machine has 256 GB and the incoming machine is owner-reported as 256 GB. Together they provide 512 GB of marketed physical unified memory, distributed across two nodes. This is **not one 512 GB GPU**, and neither memory bandwidth nor GPU cores combine for free. Both operating systems, runtime buffers, KV caches and communications consume capacity. The usable per-node allocation must be measured.

Two useful outcomes are possible: fitting a larger model, and serving more independent work. A cluster that increases model capacity can still make one response slower.

## Recommended wiring and software

1. Keep management/SSH on Ethernet. Start with a direct certified Thunderbolt 5 cable between verified TB5 ports for inference traffic; do not confuse a USB-C charging cable with a TB5 cable. Record cable specification, port pair and negotiated link.
2. Match compatible macOS/MLX versions and verify RDMA availability on both machines. Current MLX documentation describes JACCL RDMA on TB5 Macs starting with macOS 26.2. OS-specific enablement can differ: the docs describe Recovery setup, while newer Apple material describes Settings. Follow the procedure for the actual OS; make reboot/network changes during an owner-reserved window.
3. Verify enumerated RDMA devices and an explicit JACCL two-rank smoke test. Record the actual selected transport; never let silent TCP fallback be labeled RDMA.
4. Keep a reproducible MLX distributed baseline. Test EXO separately for discovery, placement and serving; pin its commit and actual backend. Check mixed M3/M5 and each model architecture explicitly.
5. Use 10Gb Ethernet/TCP as a baseline/fallback and Thunderbolt TCP as another control. Tailscale/Wi-Fi are management conveniences, not primary performance links.

No software installation, network mutation, RDMA enablement or reboot is performed by this planning release.

## Stage gates

**A. Network:** test bidirectional sustained transfer, latency, jitter and CPU overhead with a fixed tool/version. Run all-reduce/all-gather microbenchmarks across message sizes representative of the model. `iperf3` measures TCP, not RDMA collectives. Do not use the advertised 120Gb/s display-boost figure as achieved symmetric tensor bandwidth. Watch whether both GPUs are being starved or mostly waiting on communications.

**B. Small model correctness:** first shard a known fitting anchor and compare its output/quality against the single-node version. Start with supported pipeline/layer splits; add tensor parallelism only when the model/runtime supports it. Verify model hashes on both machines, no accidental duplicate complete allocations, and no undisclosed offload.

**C. Controlled comparison:** for the exact same model/settings test:

| Setup | What it establishes |
|---|---|
| Old alone | Existing baseline |
| New alone | New baseline |
| Both as independent replicas | Practical aggregate service throughput |
| Both, pipeline/layer split | Capacity and communication trade-off |
| Both, tensor parallel if supported | Whether low-latency collectives improve the workload |
| Both, EXO-managed placement | Orchestration overhead and usability |

For pipeline partitioning try approximately 50/50, 60/40 and 70/30 layer allocation toward the faster node, subject to architecture and per-node memory. Tune on pilot prompts only, then freeze the split. Equal memory capacity does not imply equal optimal compute allocation. Vary batch/concurrency, reverse coordinator placement, and publish both per-user latency and aggregate throughput. A two-server arrangement does not share weights but may be the most useful way to run two agents.

**D. Large model:** move from a fitting 70–120B-class candidate to 397B/480B, then a 671B stretch candidate. Prove allocation at short context before extending it. Pin task timeout and resource limits; record “did not fit” as a valid outcome.

**E. Reliability:** run the successful configuration for at least two hours. Deliberately test only task-owned server restarts/cancellations in a reserved window, record recovery time and correctness after reconnect, and stop after two crashes. No reboot or interface reconfiguration while another task depends on it.

## Memory arithmetic: lower bounds, not fit promises

Nominal packed weights require `parameters × bits / 8` bytes. Decimal GB and binary GiB must be labeled. Quantization scales, higher-precision tensors, embeddings, runtime buffers, KV/state caches and alignment all add overhead. In a MoE, active parameters govern only part of compute; the full required expert weights still need residence or explicitly measured offload.

| Parameter scale | 4-bit packed weight lower bound (decimal GB) | Interpretation |
|---:|---:|---|
| 70B | 35 | Easy first capacity control, overhead still applies |
| 235B | 117.5 | Potential single-node large control |
| 397B | 198.5 | Single-node fit is context/format dependent |
| 480B | 240 | Very tight on 256 GB before overhead; strong cluster candidate |
| 671B | 335.5 | Plausible two-node experiment, architecture support and allocation must be proven |
| 1T | 500 | Leaves insufficient practical overhead for a dependable 512 GB cluster target |
| 2.4T | 1,200 | Outside this two-node resident-memory 4-bit plan |

Use actual downloaded artifact bytes and runtime allocation estimates, not just these arithmetic bounds. Begin with a planning ceiling around 80% of physical memory per node; reduce it if observed pressure requires more headroom. This ceiling is an experimental safety budget, not a claim about macOS's GPU allocation limit. Include replicated buffers and the coordinator's extra work. A theoretical summed fit is insufficient if either node exceeds its own budget.

Ordinary transformer KV memory can be estimated from layers, KV heads, head dimension, sequence length, element size and active requests, but hybrid/recurrent/latent-attention architectures have different state layouts. Derive allocation from the actual config and backend, then measure it. Reserve output tokens before accepting a context length.

Do not store copies of all formats/quantizations at once. Use one shared, content-addressed model cache per node where feasible, verify hashes, and limit downloads to the next approved stage. Remove only task-owned disposable data; never delete someone else's cache.

## Deciding whether clustering is worth it

Report three distinct judgments: (1) capability gained (model/context fits), (2) single-user latency, (3) total useful work per hour and per Wh. Compare against the strongest single-node setup and the two-replica alternative. A capacity-only win is still valuable, but must be labeled that way. Do not claim “2× faster” from total memory or total GPU core count.

## Sources checked September 29, 2026

- [MLX distributed backends and RDMA requirements](https://github.com/ml-explore/mlx/blob/main/docs/src/usage/distributed.rst)
- [MLX host/network configuration](https://github.com/ml-explore/mlx/blob/main/docs/src/usage/launching_distributed.rst)
- [JACCL](https://github.com/ml-explore/mlx/blob/main/mlx/distributed/jaccl/lib/README.md)
- [Apple distributed MLX session](https://developer.apple.com/videos/play/wwdc2026/233/)
- [EXO](https://github.com/exo-explore/exo)

Recheck against pinned versions before execution, particularly mixed-generation support and RDMA enablement on macOS 27.
