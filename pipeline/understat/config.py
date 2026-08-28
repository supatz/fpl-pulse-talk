"""Understat EPL pipeline — separate masters, join to FPL at serving time."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT / ".cache" / "understat"
MASTER_DIR = ROOT / "master" / "understat"
MAPS_DIR = ROOT / "data" / "understat" / "maps"
SERVING_DIR = ROOT / "serving"
WEB_DATA_DIR = ROOT / "web" / "data"
DOCS_DIR = ROOT / "docs"
LOGS_DIR = ROOT / "logs"

LEAGUE = "EPL"
# Understat start-year seasons → FPL season labels
SEASONS: dict[str, str] = {
    "2025": "2025-2026",
    "2026": "2026-2027",
}

# Polite delay between live understat.com requests (seconds)
REQUEST_SLEEP_S = 0.12

# Rolling windows for team situation pilot (matches)
ROLLING_WINDOWS = (5, 10, 15)

# Understat pitch: X→goal (0 own half … 1 opponent goal), Y width (0–1).
# Thresholds approximate understat shotZone bins; validated loosely vs context.
ZONE_SIX_YARD_X = 0.94
ZONE_PENALTY_X = 0.83
ZONE_SIX_YARD_Y_MIN = 0.36
ZONE_SIX_YARD_Y_MAX = 0.64
ZONE_PENALTY_Y_MIN = 0.21
ZONE_PENALTY_Y_MAX = 0.79
