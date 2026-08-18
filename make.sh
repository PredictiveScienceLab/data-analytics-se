#!/usr/bin/env bash
set -euo pipefail

# This script builds the lecture book. Use --publish to deploy to gh-pages.
# Dependencies are locked and installed with uv.

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is required but was not found on PATH."
  exit 1
fi

if [[ ! -f uv.lock ]]; then
  echo "Error: uv.lock was not found. Run 'uv lock' first."
  exit 1
fi

uv sync --locked

# This repository uses classic Jupyter Book (_config.yml / _toc.yml).
# The new mystmd jupyter-book CLI is incompatible with this format.
if uv run --locked jupyter-book --help 2>&1 | grep -q "powered by mystmd"; then
  cat <<'EOF'
Error: You are using jupyter-book v2 (mystmd CLI), but this repo needs classic Jupyter Book.

Restore the locked Python 3.11 environment with:
  uv sync --locked

Then run:
  ./make.sh          # build only
  ./make.sh --publish
EOF
  exit 1
fi

# Make it
uv run --locked jupyter-book build lecturebook --all

if [[ "${1:-}" == "--publish" ]]; then
  if ! uv run --locked ghp-import --help >/dev/null 2>&1; then
    echo "Error: ghp-import is not available in the uv environment."
    exit 1
  fi
  if [[ ! -d lecturebook/_build/html ]]; then
    echo "Error: build output lecturebook/_build/html was not found."
    exit 1
  fi
  uv run --locked ghp-import -n -p -f lecturebook/_build/html
fi
