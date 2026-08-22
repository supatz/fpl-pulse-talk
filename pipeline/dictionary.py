from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

from pipeline.config import DOCS_DIR
from pipeline.io_utils import atomic_write_text

DESCRIPTIONS = {
    "season": "Season folder name (YYYY-YYYY).",
    "competition": "Tournament folder name. Dashboard filters; ingest keeps every competition.",
    "gw": "FPL gameweek from the GW folder number (includes 0 for pre-season).",
    "match_id": "Stable match identifier from the source repo.",
    "player_id": "Season-scoped FPL player id. Do not join across seasons.",
    "player_code": "Stable cross-season player identity.",
    "team_code": "Stable club code (teams.code), not season id.",
    "opponent_code": "Opponent club code.",
    "is_home": "True if the row's team/player is the home side.",
    "venue": "H or A.",
    "minutes": "Minutes played (Opta/match layer). Missing is unknown, not zero.",
    "xg": "Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG.",
    "xa": "Opta expected assists.",
    "np_xg": "Non-penalty xG aggregated from shots.situation.",
    "set_piece_xg": "Shot-model xG on set-piece situations.",
    "open_play_xg": "Shot-model xG on open-play situations.",
    "fpl_points": "FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows.",
    "is_dgw": "True when the player has 2+ Premier League matches in this GW.",
    "gw_match_count": "Player-match rows for this player in the GW (all competitions).",
    "gw_match_index": "1-based index of this match within the player's GW.",
    "now_cost": "FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10.",
    "expected_goals": "FPL-API xG family on player_gw. Do not mix with Opta xg.",
    "xga": "Expected goals against (opponent xG) on team_match.",
    "source_commit": "Git SHA of olbauday/FPL-Core-Insights at ingest.",
    "ingested_at_utc": "UTC timestamp of this pipeline run.",
    "source_files": "Source files contributing to the row (truncated list).",
}


def write_data_dictionary(tables: dict[str, pl.DataFrame]) -> None:
    lines = [
        "# FPL master datasets — data dictionary",
        "",
        f"Generated `{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}`.",
        "",
        "Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).",
        "",
        "Missing values are null, never filled with zero. `player_id` is season-scoped;",
        "`player_code` and `team_code` are stable. FPL points live on `player_gw`;",
        "`player_match` is the football grain.",
        "",
    ]
    for name, df in tables.items():
        if df is None:
            continue
        lines.append(f"## `{name}`")
        lines.append("")
        lines.append(f"Rows: **{df.height:,}**. Columns: **{len(df.columns)}**.")
        lines.append("")
        lines.append("| Column | Dtype | Nulls | Notes |")
        lines.append("|---|---|---:|---|")
        n = max(df.height, 1)
        for col, dtype in zip(df.columns, df.dtypes):
            nulls = df[col].null_count()
            note = DESCRIPTIONS.get(col, "")
            lines.append(f"| `{col}` | `{dtype}` | {nulls:,} ({nulls / n:.1%}) | {note} |")
        lines.append("")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_text("\n".join(lines) + "\n", DOCS_DIR / "data_dictionary.md")
