"""docs/sofascore_data_dictionary.md stub from live masters."""

from __future__ import annotations

from pipeline.sofascore.config import DOCS_DIR
from pipeline.sofascore.ingest import read_master
from pipeline.sofascore.normalize import now_utc

TABLES = [
    ("event", "1 row per Premier League fixture", "SofaScore event_id, kickoff, teams, score"),
    ("shot", "1 row per shot", "Native situation, shotType, coords 0–100, xg/xgot, zones"),
    ("player_match", "1 row per player × event from lineups", "Native bigChancesCreated/Missed, expectedAssists"),
]


def write_data_dictionary() -> str:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = DOCS_DIR / "sofascore_data_dictionary.md"
    lines = [
        "# SofaScore data dictionary",
        "",
        f"Generated `{now_utc()}`. Parallel to Understat; never coalesced.",
        "",
        "| Table | Grain | Notes | Rows |",
        "|---|---|---|---|",
    ]
    for table, grain, notes in TABLES:
        df = read_master(table)
        lines.append(f"| `{table}` | {grain} | {notes} | {df.height} |")
        if df.height:
            cols = ", ".join(f"`{c}`" for c in df.columns[:24])
            more = " …" if len(df.columns) > 24 else ""
            lines.append("")
            lines.append(f"**{table} columns:** {cols}{more}")
    lines.append("")
    lines.append("Site player chips `BCC_sf` / `BCM_sf` / `SiB_sf` left-join this `player_match` + shot zone onto FPL `player_code`. Null when unmapped.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)
