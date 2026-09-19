#!/usr/bin/env bash
# Refresh Understat EPL masters, PL merge, and both site serving layers.
# Uses cached match shots; re-pulls league indexes so new results appear.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "Missing $ROOT/.venv — create it with:"
  echo "  /opt/homebrew/bin/python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

mkdir -p "$ROOT/logs"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] understat refresh start" | tee -a "$ROOT/logs/understat_refresh.log"
"$ROOT/.venv/bin/python" "$ROOT/build_understat.py" --refresh --ingest-only
"$ROOT/.venv/bin/python" "$ROOT/build_pl_merge.py"
"$ROOT/.venv/bin/python" "$ROOT/build_serving.py"
"$ROOT/.venv/bin/python" "$ROOT/build_understat.py" --serving-only
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] understat refresh done" | tee -a "$ROOT/logs/understat_refresh.log"
