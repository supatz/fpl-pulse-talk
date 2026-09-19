#!/usr/bin/env bash
# Double-click in Finder: serve web/ locally and keep running until this window is closed.
# Port comes from $1 or FPL_PORT, else serve.py's default.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${1:-${FPL_PORT:-8765}}"
PY=".venv/bin/python"
[ -x "$PY" ] || PY="python3"

echo "Serving web/ on http://127.0.0.1:${PORT}/ — close this window to stop."
exec "$PY" serve.py --port "$PORT"
