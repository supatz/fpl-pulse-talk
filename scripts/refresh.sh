#!/usr/bin/env bash
# Manual trigger — refresh the FPL master datasets.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "Missing $ROOT/.venv — create it with:"
  echo "  /opt/homebrew/bin/python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

mkdir -p "$ROOT/logs"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] refresh start" | tee -a "$ROOT/logs/refresh.log"
"$ROOT/.venv/bin/python" "$ROOT/build.py" --refresh
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] refresh done" | tee -a "$ROOT/logs/refresh.log"
