"""SofaScore EPL pipeline — separate masters, join to FPL at serving time."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT / ".cache" / "sofascore"
MASTER_DIR = ROOT / "master" / "sofascore"
MAPS_DIR = ROOT / "data" / "sofascore" / "maps"
REVIEW_DIR = ROOT / "data" / "sofascore" / "review"
SERVING_DIR = ROOT / "serving"
WEB_DATA_DIR = ROOT / "web" / "data"
DOCS_DIR = ROOT / "docs"
LOGS_DIR = ROOT / "logs"

UNIQUE_TOURNAMENT_ID = 17  # Premier League
# FPL season label → expected SofaScore year strings (resolved live)
SEASONS: dict[str, str] = {
    "2025-2026": "2025-2026",
    "2026-2027": "2026-2027",
}

REQUEST_SLEEP_S = 0.25
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
API_BASE = "https://www.sofascore.com/api/v1"
# Discovered from SofaScore tournament page (unique-tournament 17).
SEASON_IDS: dict[str, int] = {
    "2025-2026": 76986,
    "2026-2027": 96668,
}

# Shotmap: x = % of pitch length from the attacked goal (small = close).
# six-yard ~ 5.5/105 ≈ 5.2%; penalty area ~ 16.5/105 ≈ 15.7%.
ZONE_SIX_YARD_X = 6.0
ZONE_PENALTY_X = 16.5
ZONE_SIX_YARD_Y_MIN = 36.0
ZONE_SIX_YARD_Y_MAX = 64.0
ZONE_PENALTY_Y_MIN = 21.0
ZONE_PENALTY_Y_MAX = 79.0

SOT_TYPES = frozenset({"goal", "save", "post"})
SITUATION_ORDER = [
    "regular",
    "assisted",
    "fast-break",
    "corner",
    "set-piece",
    "throw-in-set-piece",
    "free-kick",
    "penalty",
]
