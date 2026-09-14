"""Season attackSpeed splits from team_context_season → us_team_attack_speed.json."""

from __future__ import annotations

import math
from typing import Any

import polars as pl

from pipeline.understat.config import SEASONS
from pipeline.understat.normalize import now_utc

# Fast → Slow reading order for the tempo ribbon
SPEEDS = ["Fast", "Standard", "Normal", "Slow"]

METRICS = [
    {"id": "G", "field": "goals", "name": "Goals scored"},
    {"id": "xG", "field": "us_xg", "name": "Expected goals"},
    {"id": "Sh", "field": "shots", "name": "Shots taken"},
    {"id": "ShC", "field": "against_shots", "name": "Shots conceded"},
    {"id": "GC", "field": "against_goals", "name": "Goals conceded"},
    {"id": "xGC", "field": "against_us_xg", "name": "Expected goals against"},
]


def _round(v: Any, nd: int = 3):
    if v is None:
        return None
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, nd)
    if hasattr(v, "item"):
        return _round(v.item(), nd)
    return v


def _metric_val(v: float, metric_id: str):
    val = _round(float(v or 0), 3 if metric_id in ("xG", "xGC") else 2)
    if metric_id in ("G", "Sh", "ShC", "GC") and val is not None and float(val).is_integer():
        return int(val)
    return val


def build_team_attack_speed_serving(
    context: pl.DataFrame | None = None,
    fpl_seasons: list[str] | None = None,
) -> dict:
    seasons = fpl_seasons or list(SEASONS.values())
    empty = {
        "schema_version": 1,
        "source": "understat.com",
        "built_at_utc": now_utc(),
        "context_family": "attackSpeed",
        "grain": "team × season × attackSpeed (Understat context — not GW-filterable)",
        "speeds": SPEEDS,
        "metrics": METRICS,
        "seasons": seasons,
        "default_season": seasons[-1] if seasons else None,
        "teams": [],
        "meta": {
            "note": "Understat attackSpeed is season-only (not on shots). Fast≈direct/transition; Slow≈build-up. Shares are of each team's season total."
        },
    }
    if context is None or context.is_empty() or "context_family" not in context.columns:
        return empty

    df = context.filter(pl.col("context_family") == "attackSpeed")
    if fpl_seasons:
        df = df.filter(pl.col("season").is_in(fpl_seasons))
    if df.is_empty():
        return empty

    fields = [m["field"] for m in METRICS]
    keep = ["season", "team_code", "team", "team_short", "context_value", *fields]
    keep = [c for c in keep if c in df.columns]
    df = df.select(keep).with_columns(
        pl.col("context_value").cast(pl.Utf8),
        pl.col("team_code").cast(pl.Int64, strict=False),
    )

    teams_out: list[dict] = []
    for (season, team_code), g in df.group_by(["season", "team_code"], maintain_order=True):
        row0 = g.row(0, named=True)
        totals = {m["id"]: float(g[m["field"]].sum() or 0) for m in METRICS if m["field"] in g.columns}
        by_speed: dict[str, dict] = {}
        for r in g.to_dicts():
            sp = r.get("context_value")
            if sp not in SPEEDS:
                continue
            values = {}
            share = {}
            for m in METRICS:
                field = m["field"]
                if field not in r:
                    continue
                raw = float(r[field] or 0)
                values[m["id"]] = _metric_val(raw, m["id"])
                tot = totals[m["id"]]
                share[m["id"]] = _round((raw / tot) if tot else 0.0, 4)
            by_speed[sp] = {"values": values, "share": share}

        for sp in SPEEDS:
            if sp not in by_speed:
                by_speed[sp] = {
                    "values": {m["id"]: 0 for m in METRICS},
                    "share": {m["id"]: 0.0 for m in METRICS},
                }

        teams_out.append(
            {
                "season": season,
                "team_code": int(team_code) if team_code is not None else None,
                "team": row0.get("team"),
                "team_short": row0.get("team_short"),
                "totals": {k: _metric_val(v, k) for k, v in totals.items()},
                "speeds": by_speed,
            }
        )

    teams_out.sort(key=lambda t: (t["season"] or "", t["team_short"] or ""))
    present = sorted({t["season"] for t in teams_out if t.get("season")})
    return {
        **empty,
        "seasons": present or seasons,
        "default_season": present[-1] if present else empty["default_season"],
        "teams": teams_out,
        "meta": {
            **empty["meta"],
            "team_rows": len(teams_out),
            "speeds": SPEEDS,
        },
    }
