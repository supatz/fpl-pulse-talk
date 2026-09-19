"""Paths and thresholds for the Premier League merge (not wired to the site)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MAPS_DIR = ROOT / "data" / "pl_merge" / "maps"
REVIEW_DIR = ROOT / "data" / "pl_merge" / "review"
MASTER_DIR = ROOT / "master" / "pl_merge"
LOGS_DIR = ROOT / "logs"

SEASONS = {
    "2025": "2025-2026",
    "2026": "2026-2027",
}

PREMIER_LEAGUE = "Premier League"
FUZZY_AUTO_MIN = 95
FUZZY_AMBIGUOUS_MIN = 90

PLAYER_OVERRIDE_COLS = ("understat_player_id", "player_code", "reason")
MATCH_OVERRIDE_COLS = ("understat_match_id", "fpl_match_id", "reason")
