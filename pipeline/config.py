from __future__ import annotations

from pathlib import Path

SOURCE_REPO = "https://github.com/olbauday/FPL-Core-Insights"
SOURCE_NAME = "olbauday/FPL-Core-Insights"

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache"
SOURCE_DIR = CACHE_DIR / "FPL-Core-Insights"
MASTER_DIR = ROOT / "master"
SERVING_DIR = ROOT / "serving"
DOCS_DIR = ROOT / "docs"
LOGS_DIR = ROOT / "logs"
MANIFEST_PATH = ROOT / "manifest.json"
INCREMENTAL_PATH = ROOT / ".incremental.json"

# Files we hash for incremental rebuilds of a GW slice.
SLICE_FILES = (
    "matches.csv",
    "fixtures.csv",
    "playermatchstats.csv",
    "player_match_enrichment.csv",
    "player_gameweek_stats.csv",
    "shots.csv",
    "lineups.csv",
    "incidents.csv",
    "average_positions.csv",
    "match_enrichment.csv",
)

SEASON_FILES = ("players.csv", "teams.csv")

# Required columns if the file is present. Extra columns are allowed.
REQUIRED_COLUMNS: dict[str, list[str]] = {
    "players": ["player_code", "player_id", "web_name", "team_code", "position"],
    "teams": ["code", "id", "name", "short_name"],
    "playermatchstats": ["player_id", "match_id"],
    "player_match_enrichment": ["player_id", "match_id"],
    "player_gameweek_stats": ["id", "gw"],
    "matches": ["match_id", "home_team", "away_team", "finished"],
    "fixtures": ["match_id", "home_team", "away_team", "finished"],
    "shots": ["match_id", "player_id"],
    "lineups": ["match_id", "player_id"],
    "incidents": ["match_id"],
    "match_enrichment": ["match_id"],
}

OPTIONAL_SLICE_FILES = {
    "player_match_enrichment.csv",
    "player_gameweek_stats.csv",
    "shots.csv",
    "lineups.csv",
    "incidents.csv",
    "average_positions.csv",
    "match_enrichment.csv",
    "momentum.csv",
    "xg_by_minute.csv",
    "players.csv",
    "playerstats.csv",
    "teams.csv",
}

CORE_SLICE_FILES = {"matches.csv", "playermatchstats.csv"}

SHOT_PENALTY = {"penalty"}
SHOT_SET_PIECE = {"corner", "set-piece", "throw-in-set-piece", "free-kick"}
SHOT_OPEN_PLAY = {"assisted", "regular", "fast-break"}

PREMIER_LEAGUE = "Premier League"

MEASURE_NULL_NEVER_ZERO = {
    "xg",
    "xa",
    "xgot",
    "minutes",
    "elo",
    "goals_prevented",
    "expected_goals",
    "expected_assists",
}

PROVENANCE_COLS = ("source_commit", "ingested_at_utc", "source_files")
