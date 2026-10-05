# Darkbloom — context only; owner hold

**Current instruction, October 1:** the owner authorizes testing the local model files downloaded for Darkbloom once the download batch completes, using an independent local runtime. Reading those model files and provenance/completion metadata is allowed. Do not turn on Darkbloom/provider serving, launch its app or CLI, install/reinstall it, change accounts/settings, or interfere with existing downloads. No provider/account action is needed to benchmark the files independently.

Darkbloom is a network connecting inference customers with participating Apple Silicon Macs. Its coordinator routes requests to providers; claimed privacy mechanisms include encrypted routing and hardware attestation. Provider earnings come from actual billed work and depend on demand and availability. This session reviewed public documentation only and made no change to the downloaded application.

The owner previously requested Darkbloom last. Its homepage redirects from darkbloom.dev to darkbloom.ai. On October 1 the official release endpoint reports **0.9.14, native mlx-swift**; some prose documentation still describes a Python-based installer. The reviewed current installer is authoritative for the actual package behavior.

`config/darkbloom-install.lock.json` pins the installer SHA256 and advertised package/binary/Metal hashes. `scripts/install_darkbloom.py` refuses changed metadata or a changed installer, requires macOS 27+, preserves an existing installation and takes a GPU slot for the vendor runtime verification. The official installer validates the package and Apple signature. This stage must follow model tests and close the task's Blender instance first.

Installation does not start a provider, download a network-selected model, log in, configure payouts or measure earnings. On macOS 27 the reviewed script directs users to App Attest and does not install a management profile. The owner can link their account in the vendor's browser flow afterward; no password, token or account data belongs in this repository.

For a daily-rate experiment, record actual elapsed time, connected/serving/idle hours, completed jobs, model mix, token counts, credited earnings and measured energy. An extrapolated token-throughput ceiling is not an earned daily rate. Demand and availability affect paid utilization. No daily dollar value is claimed until measured.

Official references: [installation](https://docs.darkbloom.dev/provider/install), [earnings](https://docs.darkbloom.dev/provider/earnings), [live release metadata](https://api.darkbloom.dev/v1/releases/latest).
