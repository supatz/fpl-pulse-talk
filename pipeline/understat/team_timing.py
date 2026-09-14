"""Match-clock timing from Understat shots + FPL gameweeks → us_team_timing.json."""

from __future__ import annotations

import math
from typing import Any

import polars as pl

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR
from pipeline.understat.config import SEASONS
from pipeline.understat.maps import load_team_map
from pipeline.understat.normalize import now_utc

INTERVALS = ["1-15", "16-30", "31-45", "46-60", "61-75", "76+"]

METRICS = [
    {"id": "G", "field": "goals", "name": "Goals scored"},
    {"id": "xG", "field": "us_xg", "name": "Expected goals"},
    {"id": "Sh", "field": "shots", "name": "Shots taken"},
    {"id": "ShC", "field": "against_shots", "name": "Shots conceded"},
    {"id": "GC", "field": "against_goals", "name": "Goals conceded"},
    {"id": "xGC", "field": "against_us_xg", "name": "Expected goals against"},
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
        "schema_version": 2,
        "source": "understat.com",
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
            "note": "Built from Understat shots; FPL GW via Premier League team_match. Shares computed client-side for the selected GW range."
        },
    }


def _read_fpl_pl_team_match(seasons: list[str]) -> pl.DataFrame:
    parts = []
    for season in seasons:
        path = FPL_MASTER_DIR / "team_match" / f"season={season}" / "competition=Premier League" / "part.parquet"
        if path.exists():
            parts.append(pl.read_parquet(path))
    if not parts:
        # fallback: any competition named Premier League under season dirs
        for season in seasons:
            base = FPL_MASTER_DIR / "team_match" / f"season={season}"
            for p in base.glob("competition=*/part.parquet"):
                if "Premier" in p.parent.name:
                    parts.append(pl.read_parquet(p))
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed")


def _gw_bridge(seasons: list[str], matches: pl.DataFrame, team_map: pl.DataFrame) -> pl.DataFrame:
    """Understat match_id → FPL gw (Premier League only)."""
    if matches is None or matches.is_empty():
        return pl.DataFrame()

    tm = team_map.select(
        pl.col("understat_team_id").alias("uid"),
        pl.col("team_code"),
        pl.col("fpl_short").alias("team_short"),
        pl.col("fpl_name").alias("team"),
    )
    m = matches.filter(pl.col("season").is_in(seasons) if "season" in matches.columns else True)
    if m.is_empty():
        return pl.DataFrame()

    home = tm.rename({"uid": "home_team_id", "team_code": "home_code"})
    away = tm.rename({"uid": "away_team_id", "team_code": "away_code"})
    us = (
        m.select("match_id", "season", "kickoff_raw", "home_team_id", "away_team_id")
        .with_columns(pl.col("home_team_id").cast(pl.Utf8), pl.col("away_team_id").cast(pl.Utf8))
        .join(home.select("home_team_id", "home_code"), on="home_team_id", how="left")
        .join(away.select("away_team_id", "away_code"), on="away_team_id", how="left")
        .with_columns(pl.col("kickoff_raw").str.slice(0, 10).alias("kick_date"))
        .filter(pl.col("home_code").is_not_null() & pl.col("away_code").is_not_null())
    )

    fpl = _read_fpl_pl_team_match(seasons)
    if fpl.is_empty():
        return pl.DataFrame()
    fpl_home = (
        fpl.filter(pl.col("is_home"))
        .select("season", "gw", "kickoff_utc", "team_code", "opponent_code", "finished")
        .with_columns(
            pl.col("kickoff_utc").str.slice(0, 10).alias("kick_date"),
            pl.col("team_code").cast(pl.Int64).alias("home_code"),
            pl.col("opponent_code").cast(pl.Int64).alias("away_code"),
            pl.col("gw").cast(pl.Int64),
        )
        .select("season", "gw", "kick_date", "home_code", "away_code", "finished")
    )

    bridge = us.join(fpl_home, on=["season", "kick_date", "home_code", "away_code"], how="inner").select(
        "match_id", "season", "gw", "finished"
    )
    return bridge.unique(subset=["match_id"])


def build_team_timing_serving(
    shots: pl.DataFrame | None = None,
    matches: pl.DataFrame | None = None,
    context: pl.DataFrame | None = None,  # unused; kept for call-site compat
    fpl_seasons: list[str] | None = None,
) -> dict:
    """Aggregate shot minutes into timing intervals per team × GW."""
    seasons = fpl_seasons or list(SEASONS.values())
    empty = _empty(seasons)
    if shots is None or shots.is_empty():
        return empty

    team_map = load_team_map()
    bridge = _gw_bridge(seasons, matches if matches is not None else pl.DataFrame(), team_map)
    if bridge.is_empty():
        empty["meta"]["warning"] = "No Understat↔FPL GW bridge (Premier League team_match)."
        return empty

    id_map = team_map.select(
        pl.col("understat_team_id").alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_short").alias("team_short"),
        pl.col("fpl_name").alias("team"),
    )
    opp_map = team_map.select(
        pl.col("understat_team_id").alias("opponent_id"),
        pl.col("team_code").alias("opponent_code"),
    )

    s = (
        shots.filter(pl.col("season").is_in(seasons) if "season" in shots.columns else True)
        .with_columns(
            pl.col("team_id").cast(pl.Utf8),
            pl.col("opponent_id").cast(pl.Utf8),
            pl.col("match_id").cast(pl.Utf8),
            _interval_expr().alias("interval"),
        )
        .join(id_map, on="team_id", how="left")
        .join(opp_map, on="opponent_id", how="left")
        .join(bridge.select("match_id", "gw"), on="match_id", how="inner")
        .filter(pl.col("team_code").is_not_null() & pl.col("gw").is_not_null())
    )
    if s.is_empty():
        empty["meta"]["warning"] = "Shots did not join to FPL gameweeks."
        return empty

    # For events: OwnGoal is credited to the beneficiary for G / own team for GC.
    for_rows = s.with_columns(
        (pl.col("result") != "OwnGoal").alias("is_shot_for"),
        ((pl.col("result") == "Goal") | (pl.col("result") == "OwnGoal")).alias("is_goal_event"),
    )

    # Team-for metrics from shooter perspective, then OwnGoal flip for G
    # Build long team-event rows for BOTH sides of each shot.
    shooter = for_rows.select(
        "season",
        "gw",
        "match_id",
        "interval",
        pl.col("team_code"),
        pl.col("team"),
        pl.col("team_short"),
        pl.when(pl.col("result") == "OwnGoal")
        .then(0)
        .otherwise(1)
        .alias("Sh"),
        pl.when(pl.col("result") == "Goal")
        .then(1)
        .otherwise(0)
        .alias("G"),
        pl.when(pl.col("result") == "OwnGoal")
        .then(0.0)
        .otherwise(pl.col("xg").fill_null(0.0))
        .alias("xG"),
        pl.lit(0).alias("ShC"),
        pl.when(pl.col("result") == "OwnGoal")
        .then(1)
        .otherwise(0)
        .alias("GC"),
        pl.lit(0.0).alias("xGC"),
    )

    # OwnGoal: beneficiary (opponent) gets G
    og_for = (
        for_rows.filter(pl.col("result") == "OwnGoal")
        .select(
            "season",
            "gw",
            "match_id",
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

    # Against: defending team = opponent_code
    against = for_rows.select(
        "season",
        "gw",
        "match_id",
        "interval",
        pl.col("opponent_code").alias("team_code"),
        pl.lit(None).cast(pl.Utf8).alias("team"),
        pl.lit(None).cast(pl.Utf8).alias("team_short"),
        pl.lit(0).alias("Sh"),
        pl.lit(0).alias("G"),
        pl.lit(0.0).alias("xG"),
        pl.when(pl.col("result") == "OwnGoal")
        .then(0)
        .otherwise(1)
        .alias("ShC"),
        pl.when(pl.col("result") == "Goal")
        .then(1)
        .otherwise(0)
        .alias("GC"),
        pl.when(pl.col("result") == "OwnGoal")
        .then(0.0)
        .otherwise(pl.col("xg").fill_null(0.0))
        .alias("xGC"),
    ).filter(pl.col("team_code").is_not_null())

    events = pl.concat([shooter, og_for, against], how="vertical_relaxed")

    # Fill team names from map
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

    agg = (
        events.group_by(["season", "team_code", "team", "team_short", "gw", "interval"])
        .agg(
            pl.col("G").sum().alias("G"),
            pl.col("xG").sum().alias("xG"),
            pl.col("Sh").sum().alias("Sh"),
            pl.col("ShC").sum().alias("ShC"),
            pl.col("GC").sum().alias("GC"),
            pl.col("xGC").sum().alias("xGC"),
        )
        .sort(["season", "team_code", "gw", "interval"])
    )

    # GW meta from bridge + finished flags
    gw_meta: dict[str, dict] = {}
    for season in seasons:
        b = bridge.filter(pl.col("season") == season)
        if b.is_empty():
            continue
        gws = sorted(int(x) for x in b["gw"].unique().to_list() if x is not None)
        if not gws:
            continue
        finished = b.filter(pl.col("finished") == True) if "finished" in b.columns else b  # noqa: E712
        fin_gws = sorted(int(x) for x in finished["gw"].unique().to_list() if x is not None) if finished.height else gws
        default_to = max(fin_gws) if fin_gws else max(gws)
        gw_meta[season] = {
            "min": min(gws),
            "max": max(gws),
            "default_from": min(gws),
            "default_to": default_to,
        }

    teams_out: list[dict] = []
    for (season, team_code), g in agg.group_by(["season", "team_code"], maintain_order=True):
        row0 = g.row(0, named=True)
        gws_map: dict[str, dict] = {}
        for gw, gg in g.group_by("gw", maintain_order=True):
            gw_key = str(int(gw[0] if isinstance(gw, tuple) else gw))
            iv_map: dict[str, dict] = {iv: {mid: 0 for mid in METRIC_IDS} for iv in INTERVALS}
            for r in gg.to_dicts():
                iv = r["interval"]
                if iv not in iv_map:
                    continue
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
        "meta": {
            **empty["meta"],
            "team_rows": len(teams_out),
            "bridge_matches": bridge.height,
            "shot_events": s.height,
        },
    }
