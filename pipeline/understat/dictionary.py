"""Generate docs/understat_data_dictionary.md from live masters (headers + samples)."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.understat.config import DOCS_DIR, MASTER_DIR, SEASONS
from pipeline.understat.ingest import read_master
from pipeline.understat.normalize import now_utc

# table → grain description
TABLES: list[tuple[str, str, str]] = [
    ("match", "1 row per EPL fixture", "Fixture index + score/xG/forecast"),
    ("shot", "1 row per shot", "Atomic fact: situation, last_action, coords, zone, player"),
    (
        "team_match_style",
        "1 row per team per match",
        "PPDA, deep completions, match xG/xGA from team history",
    ),
    (
        "team_context_season",
        "1 row per team × season × context_family × context_value",
        "Season splits incl. attackSpeed (for + against)",
    ),
    ("league_player", "1 row per player per season", "Understat season totals (xg_chain, etc.)"),
    (
        "team_situation_match",
        "1 row per team × match × situation",
        "Shots/goals/us_xg created (for)",
    ),
    (
        "team_situation_against_match",
        "1 row per team × match × situation",
        "Shots/goals/us_xga faced (against)",
    ),
    (
        "team_situation_rolling",
        "1 row per team × match × situation × window",
        "Rolling for-metrics over last 5/10/15 matches",
    ),
    (
        "team_situation_against_rolling",
        "1 row per team × match × situation × window",
        "Rolling against-metrics over last 5/10/15 matches",
    ),
    ("team_zone_match", "1 row per team × match × shot_zone", "Box / six-yard / outside-box"),
    (
        "player_situation_season",
        "1 row per understat player × season × situation",
        "Taker volume/quality by situation (player_code map TBD)",
    ),
    (
        "player_create_situation_season",
        "1 row per creator name × season × situation",
        "Assisted-shot xG by situation (player_code map TBD)",
    ),
]


def _sample_rows(df: pl.DataFrame, n: int = 3) -> str:
    if df.is_empty():
        return "_empty_\n"
    view = df
    if "is_result" in df.columns:
        finished = df.filter(pl.col("is_result") == True)  # noqa: E712
        if finished.height:
            view = finished
    if "kickoff_raw" in view.columns:
        view = view.sort("kickoff_raw", descending=True)
    elif "us_xg" in view.columns:
        view = view.sort("us_xg", descending=True)
    elif "assisted_us_xg" in view.columns:
        view = view.sort("assisted_us_xg", descending=True)
    rows = view.head(n).to_dicts()
    lines = ["```json"]
    import json

    def clean(r):
        out = {}
        for k, v in r.items():
            if isinstance(v, float):
                out[k] = round(v, 4)
            else:
                out[k] = v
        return out

    lines.append(json.dumps([clean(r) for r in rows], indent=2, ensure_ascii=False))
    lines.append("```\n")
    return "\n".join(lines)


def _headers_table(df: pl.DataFrame) -> str:
    if df.is_empty():
        return "| (no columns) |\n"
    lines = ["| Column | Dtype | Role |", "|---|---|---|"]
    dim_hints = {
        "season",
        "understat_season",
        "match_id",
        "team_code",
        "team",
        "team_short",
        "team_id",
        "opponent_code",
        "opponent",
        "player_id",
        "player_name",
        "situation",
        "shot_zone",
        "context_family",
        "context_value",
        "window",
        "is_home",
        "kickoff_raw",
        "attack_speed",
    }
    for name, dtype in zip(df.columns, df.dtypes):
        role = "dimension" if name in dim_hints or name.endswith("_id") else "metric/attr"
        lines.append(f"| `{name}` | `{dtype}` | {role} |")
    return "\n".join(lines) + "\n"


def write_data_dictionary() -> Path:
    parts = [
        "# Understat masters — data dictionary (samples)",
        "",
        f"Generated `{now_utc()}`.",
        "",
        "FPL dimensions on the **site** come from FPL sources. These tables hold Understat metrics.",
        "Team-facing derived tables are joined to FPL `team_code` via `data/understat/maps/team_map.csv`.",
        "Player tables still key on Understat `player_id` until a curated `player_map` exists.",
        "",
        f"Seasons in scope: {', '.join(SEASONS.values())} (Understat {', '.join(SEASONS.keys())}).",
        "",
    ]
    for table, grain, summary in TABLES:
        df = read_master(table, list(SEASONS.values()))
        # also try without season filter for non-partitioned
        if df.is_empty():
            base = MASTER_DIR / table
            files = list(base.rglob("*.parquet")) if base.exists() else []
            if files:
                df = pl.concat([pl.read_parquet(f) for f in files], how="diagonal_relaxed")
        parts.append(f"## `{table}`")
        parts.append("")
        parts.append(f"**Grain:** {grain}  ")
        parts.append(f"**What:** {summary}  ")
        parts.append(f"**Rows:** {df.height:,}")
        parts.append("")
        parts.append("### Headers")
        parts.append("")
        parts.append(_headers_table(df))
        parts.append("### Sample rows")
        parts.append("")
        parts.append(_sample_rows(df, 3))
        parts.append("")

    out = DOCS_DIR / "understat_data_dictionary.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out
