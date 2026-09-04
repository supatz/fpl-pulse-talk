#!/usr/bin/env bash
# Manual trigger — refresh datasets and/or push to GitHub (Netlify).
# Non-interactive (launchd): dataset only. Interactive Terminal: asks what to run.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

refresh_dataset() {
  if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
    echo "Missing $ROOT/.venv — create it with:"
    echo "  /opt/homebrew/bin/python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    return 1
  fi
  mkdir -p "$ROOT/logs"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] refresh start" | tee -a "$ROOT/logs/refresh.log"
  "$ROOT/.venv/bin/python" "$ROOT/build.py" --refresh
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] understat refresh start" | tee -a "$ROOT/logs/refresh.log" | tee -a "$ROOT/logs/understat_refresh.log"
  "$ROOT/.venv/bin/python" "$ROOT/build_understat.py" --refresh
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] understat refresh done" | tee -a "$ROOT/logs/refresh.log" | tee -a "$ROOT/logs/understat_refresh.log"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] refresh done" | tee -a "$ROOT/logs/refresh.log"
}

publish_git() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "This folder is not a git project yet."
    return 1
  fi
  if ! git remote get-url origin >/dev/null 2>&1; then
    echo "No GitHub remote named origin. Create the personal repo, then:"
    echo "  git remote add origin https://github.com/YOURUSER/YOURREPO.git"
    return 1
  fi
  git add -A
  if git diff --cached --quiet; then
    echo "No new file changes to commit."
  else
    echo
    read -r -p "Commit message [Update dashboard]: " msg || true
    msg="${msg:-Update dashboard}"
    if ! git commit -m "$msg"; then
      echo
      echo "Commit failed. If Git asked who you are, run these once in this folder"
      echo "(use your personal email, not the company one):"
      echo "  git config user.name \"Your Name\""
      echo "  git config user.email \"you@personal.com\""
      return 1
    fi
  fi
  echo "Pushing to GitHub (Netlify will pick this up)…"
  git push
}

MODE="dataset"
if [[ -t 0 ]]; then
  echo
  echo "FPL Pulse Talk — what do you want to update?"
  echo "  1) Dataset only   (FPL + Understat masters + serving JSON for the site)"
  echo "  2) Git push only  (commit local changes and update GitHub / Netlify)"
  echo "  3) Both           (refresh data, then commit and push)"
  echo "  q) Cancel"
  echo
  read -r -p "Choose 1, 2, 3, or q: " choice || true
  case "${choice:-}" in
    1) MODE="dataset" ;;
    2) MODE="git" ;;
    3) MODE="both" ;;
    q|Q|"") echo "Cancelled."; exit 0 ;;
    *) echo "Unknown choice."; exit 1 ;;
  esac
fi

case "$MODE" in
  dataset) refresh_dataset ;;
  git) publish_git ;;
  both) refresh_dataset && publish_git ;;
esac

if [[ -t 0 ]]; then
  echo
  read -r -p "Done. Press Return to close this window." _ || true
fi



