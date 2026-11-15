"""Match-clock timing from SofaScore shots + FPL gameweeks → ss_team_timing.json."""

from __future__ import annotations

import math
from typing import Any

import polars as pl

from pipeline.sofascore.config import MAPS_DIR, SEASONS
from pipeline.sofascore.maps import load_team_map
from pipeline.sofascore.normalize import now_utc

INTERVALS = ["1-15", "16-30", "31-45", "46-60", "61-75", "76+"]
METRICS = [
    {"id": "G", "field": "goals", "name": "Goals scored"},
    {"id": "xG", "field": "ss_xg", "name": "Expected goals"},
    {"id": "Sh", "field": "shots", "name": "Shots taken"},
    {"id": "ShC", "field": "against_shots", "name": "Shots conceded"},
    {"id": "GC", "field": "against_goals", "name": "Goals conceded"},
    {"id": "xGC", "field": "against_ss_xg", "name": "Expected goals against"},
]
METRIC_IDS = [m["id"] for m in METRICS]


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


def _interval_expr(minute_col: str = "minute") -> pl.Expr:
    m = pl.col(minute_col).fill_null(0)
    return (
        pl.when(m <= 15)
        .then(pl.lit("1-15"))
        .when(m <= 30)
        .then(pl.lit("16-30"))
        .when(m <= 45)
        .then(pl.lit("31-45"))
        .when(m <= 60)
        .then(pl.lit("46-60"))
        .when(m <= 75)
        .then(pl.lit("61-75"))
        .otherwise(pl.lit("76+"))
    )


def _empty(seasons: list[str]) -> dict:
    return {
        "schema_version": 1,
        "source": "sofascore.com",
        "built_at_utc": now_utc(),
        "context_family": "timing",
        "grain": "team × season × gw × interval (from shots)",
        "intervals": INTERVALS,
        "metrics": METRICS,
        "seasons": seasons,
        "default_season": seasons[-1] if seasons else None,
        "gw_meta": {},
        "teams": [],
        "meta": {
            "note": "Built from SofaScore shots; FPL GW via sofascore match_map. No attack-tempo family."
        },
    }


def _match_bridge() -> pl.DataFrame:
    path = MAPS_DIR / "match_map.csv"
    if not path.exists():
        return pl.DataFrame()
    m = pl.read_csv(path)
    if m.is_empty() or "sofascore_event_id" not in m.columns:
        return pl.DataFrame()
    return m.select(
        pl.col("sofascore_event_id").cast(pl.Utf8).alias("event_id"),
        pl.col("season").cast(pl.Utf8) if "season" in m.columns else pl.lit(None).alias("season"),
        pl.col("gw").cast(pl.Int64),
        pl.col("fpl_match_id").cast(pl.Utf8),
    )


def build_team_timing_serving(
    shots: pl.DataFrame | None = None,
    matches: pl.DataFrame | None = None,
    fpl_seasons: list[str] | None = None,
) -> dict:
    seasons = fpl_seasons or list(SEASONS.keys())
    empty = _empty(seasons)
    if shots is None or shots.is_empty():
        return empty
    team_map = load_team_map().filter(pl.col("team_code").is_not_null())
    bridge = _match_bridge()
    if bridge.is_empty():
        empty["meta"]["warning"] = "No SofaScore↔FPL match_map."
        return empty
    id_map = team_map.select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_short").alias("team_short"),
        pl.col("fpl_name").alias("team"),
    )
    opp_map = team_map.select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("opponent_id"),
        pl.col("team_code").alias("opponent_code"),
    )
    s = (
        shots.filter(pl.col("season").is_in(seasons) if "season" in shots.columns else True)
        .with_columns(
            pl.col("team_id").cast(pl.Utf8),
            pl.col("opponent_id").cast(pl.Utf8),
            pl.col("event_id").cast(pl.Utf8),
            _interval_expr().alias("interval"),
        )
        .join(id_map, on="team_id", how="left")
        .join(opp_map, on="opponent_id", how="left")
        .join(bridge.select("event_id", "gw"), on="event_id", how="inner")
        .filter(pl.col("team_code").is_not_null() & pl.col("gw").is_not_null())
    )
    if s.is_empty():
        empty["meta"]["warning"] = "Shots did not join to FPL gameweeks."
        return empty

    own = pl.col("is_own_goal").fill_null(False)
    shooter = s.select(
        "season",
        "gw",
        "event_id",
        "interval",
        pl.col("team_code"),
        pl.col("team"),
        pl.col("team_short"),
        pl.when(own).then(0).otherwise(1).alias("Sh"),
        pl.when(pl.col("is_goal").fill_null(False)).then(1).otherwise(0).alias("G"),
        pl.when(own).then(0.0).otherwise(pl.col("xg").fill_null(0.0)).alias("xG"),
        pl.lit(0).alias("ShC"),
        pl.when(own).then(1).otherwise(0).alias("GC"),
        pl.lit(0.0).alias("xGC"),
    )
    og_for = (
        s.filter(own)
        .select(
            "season",
            "gw",
            "event_id",
            "interval",
            pl.col("opponent_code").alias("team_code"),
            pl.lit(None).cast(pl.Utf8).alias("team"),
            pl.lit(None).cast(pl.Utf8).alias("team_short"),
            pl.lit(0).alias("Sh"),
            pl.lit(1).alias("G"),
            pl.lit(0.0).alias("xG"),
            pl.lit(0).alias("ShC"),
            pl.lit(0).alias("GC"),
            pl.lit(0.0).alias("xGC"),
        )
        .filter(pl.col("team_code").is_not_null())
    )
    against = s.select(
        "season",
        "gw",
        "event_id",
        "interval",
        pl.col("opponent_code").alias("team_code"),
        pl.lit(None).cast(pl.Utf8).alias("team"),
        pl.lit(None).cast(pl.Utf8).alias("team_short"),
        pl.lit(0).alias("Sh"),
        pl.lit(0).alias("G"),
        pl.lit(0.0).alias("xG"),
        pl.when(own).then(0).otherwise(1).alias("ShC"),
        pl.when(pl.col("is_goal").fill_null(False)).then(1).otherwise(0).alias("GC"),
        pl.when(own).then(0.0).otherwise(pl.col("xg").fill_null(0.0)).alias("xGC"),
    ).filter(pl.col("team_code").is_not_null())
    events = pl.concat([shooter, og_for, against], how="vertical_relaxed")
    names = team_map.select(
        pl.col("team_code"),
        pl.col("fpl_name").alias("team_name"),
        pl.col("fpl_short").alias("team_short_name"),
    )
    events = (
        events.join(names, on="team_code", how="left")
        .with_columns(
            pl.coalesce([pl.col("team"), pl.col("team_name")]).alias("team"),
            pl.coalesce([pl.col("team_short"), pl.col("team_short_name")]).alias("team_short"),
        )
        .drop(["team_name", "team_short_name"])
    )
    agg = events.group_by(["season", "team_code", "team", "team_short", "gw", "interval"]).agg(
        pl.col("G").sum().alias("G"),
        pl.col("xG").sum().alias("xG"),
        pl.col("Sh").sum().alias("Sh"),
        pl.col("ShC").sum().alias("ShC"),
        pl.col("GC").sum().alias("GC"),
        pl.col("xGC").sum().alias("xGC"),
    )

    gw_meta: dict[str, dict] = {}
    for season in seasons:
        b = bridge
        if "season" in bridge.columns:
            b = bridge.filter(pl.col("season") == season)
        if b.is_empty():
            continue
        gws = sorted(int(x) for x in b["gw"].drop_nulls().unique().to_list())
        if not gws:
            continue
        gw_meta[season] = {"min": min(gws), "max": max(gws), "default_from": min(gws), "default_to": max(gws)}

    teams_out: list[dict] = []
    for (season, team_code), g in agg.group_by(["season", "team_code"], maintain_order=True):
        row0 = g.row(0, named=True)
        gws_map: dict[str, dict] = {}
        for gw, gg in g.group_by("gw", maintain_order=True):
            gw_key = str(int(gw[0] if isinstance(gw, tuple) else gw))
            iv_map = {iv: {mid: 0 for mid in METRIC_IDS} for iv in INTERVALS}
            for r in gg.to_dicts():
                iv = r["interval"]
                if iv in iv_map:
                    iv_map[iv] = {mid: _metric_val(r.get(mid, 0), mid) for mid in METRIC_IDS}
            gws_map[gw_key] = iv_map
        teams_out.append(
            {
                "season": season,
                "team_code": int(team_code) if team_code is not None else None,
                "team": row0.get("team"),
                "team_short": row0.get("team_short"),
                "gws": gws_map,
            }
        )
    teams_out.sort(key=lambda t: (t["season"] or "", t["team_short"] or ""))
    present = sorted({t["season"] for t in teams_out if t.get("season")})
    return {
        **empty,
        "seasons": present or seasons,
        "default_season": present[-1] if present else empty["default_season"],
        "gw_meta": gw_meta,
        "teams": teams_out,
        "meta": {**empty["meta"], "team_rows": len(teams_out), "shot_events": s.height},
    }
