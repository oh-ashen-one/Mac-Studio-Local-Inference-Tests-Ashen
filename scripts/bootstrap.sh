#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "$(uname -s)" != Darwin || "$(uname -m)" != arm64 ]]; then
  echo 'This lock targets Apple Silicon macOS.' >&2; exit 1
fi
command -v uv >/dev/null || { echo 'Install uv from https://docs.astral.sh/uv/getting-started/installation/ first.' >&2; exit 1; }
uv python install 3.12.13
uv venv --python 3.12.13 .venv
uv pip sync --python .venv/bin/python requirements-macos-arm64.lock
.venv/bin/python -c 'import mlx.core as mx; assert mx.metal.is_available(); print("MLX Metal ready")'
echo 'Next: .venv/bin/python scripts/models.py download'
