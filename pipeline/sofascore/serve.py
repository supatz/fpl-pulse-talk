"""Write SofaScore serving JSON (ss_*)."""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from pipeline.sofascore.config import SERVING_DIR, SEASONS, WEB_DATA_DIR
from pipeline.sofascore.ingest import read_master
from pipeline.sofascore.normalize import now_utc
from pipeline.sofascore.shot_treemap import build_shot_treemap_serving
from pipeline.sofascore.side_channels import build_side_channels_serving
from pipeline.sofascore.team_timing import build_team_timing_serving


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    if WEB_DATA_DIR.exists():
        (WEB_DATA_DIR / path.name).write_text(text, encoding="utf-8")


def build_all_serving() -> dict[str, dict]:
    seasons = list(SEASONS.keys())
    shots = read_master("shot", seasons)
    events = read_master("event", seasons)
    treemap = build_shot_treemap_serving(fpl_seasons=seasons)
    timing = build_team_timing_serving(shots, events, fpl_seasons=seasons)
    _write_json(SERVING_DIR / "ss_team_timing.json", timing)
    sides = build_side_channels_serving(shots, events, fpl_seasons=seasons)
    payloads = {
        "ss_shot_treemap": treemap,
        "ss_team_timing": timing,
        "ss_team_side_channels": sides,
        "meta": {
            "source": "sofascore.com",
            "built_at_utc": now_utc(),
            "seasons": seasons,
            "events": events.height,
            "finished_matches": int(events.filter(pl.col("is_result")).height) if events.height and "is_result" in events.columns else 0,
            "shots": shots.height,
        },
    }
    return payloads
