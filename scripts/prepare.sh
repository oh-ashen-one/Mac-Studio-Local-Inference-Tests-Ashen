#!/bin/bash
# Preparation only: installs tools, downloads files, hashes them. Never loads a model.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "$(uname -s)" != Darwin || "$(uname -m)" != arm64 ]]; then
  echo 'This kit targets Apple Silicon macOS.' >&2; exit 1
fi
if ! xcrun --find clang >/dev/null 2>&1; then
  echo 'Apple developer tools are missing. Complete xcode-select --install, then rerun this command.' >&2
  exit 1
fi
if ! command -v uv >/dev/null; then
  mkdir -p .tools work
  curl --fail --location --proto '=https' --tlsv1.2 https://astral.sh/uv/0.11.28/install.sh -o work/uv-install.sh
  UV_INSTALL_DIR="$PWD/.tools" UV_NO_MODIFY_PATH=1 sh work/uv-install.sh
  export PATH="$PWD/.tools:$PATH"
fi
if [[ ! -x .venv/bin/python ]]; then
  bash scripts/bootstrap.sh
else
  uv pip sync --python .venv/bin/python requirements-macos-arm64.lock
fi
if [[ ! -x vendor/dwarfstar/ds4 || ! -x vendor/dwarfstar/ds4-bench || ! -x vendor/dwarfstar/ds4-server ]]; then
  .venv/bin/python scripts/build_native.py
fi
.venv/bin/python scripts/models.py download
.venv/bin/python scripts/finish_prepare.py
