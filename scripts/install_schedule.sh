#!/usr/bin/env bash
# Install a Monday + Thursday 08:00 local-time launchd job.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.fpl.masterdataset.refresh"
PLIST_SRC="$ROOT/launchd/${LABEL}.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/logs"

# Rewrite the plist with this machine's project path and python/refresh script.
cat > "$PLIST_DEST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${ROOT}/scripts/refresh.sh</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${ROOT}</string>
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Weekday</key>
      <integer>1</integer>
      <key>Hour</key>
      <integer>8</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
    <dict>
      <key>Weekday</key>
      <integer>4</integer>
      <key>Hour</key>
      <integer>8</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
  </array>
  <key>StandardOutPath</key>
  <string>${ROOT}/logs/launchd.out.log</string>
  <key>StandardErrorPath</key>
  <string>${ROOT}/logs/launchd.err.log</string>
  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_DEST"
echo "Installed ${LABEL}"
echo "  Schedule: Monday and Thursday at 08:00 local time"
echo "  Manual run:  ${ROOT}/scripts/refresh.sh"
echo "  Or:          launchctl start ${LABEL}"
echo "  Uninstall:   ${ROOT}/scripts/uninstall_schedule.sh"
echo "  Logs:        ${ROOT}/logs/"
# Keep a copy in the repo for reference (paths are machine-specific in LaunchAgents).
cp "$PLIST_DEST" "$PLIST_SRC"
echo "Wrote reference plist to $PLIST_SRC"
