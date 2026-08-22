from __future__ import annotations

import logging
from datetime import datetime, timezone

import polars as pl

from pipeline.config import PREMIER_LEAGUE, SERVING_DIR
from pipeline.io_utils import atomic_write_json

log = logging.getLogger("fpl")

MIN_MINUTES = 60
WINDOWS = (5, 10, 15)


def _round_df(df: pl.DataFrame, digits: int = 3) -> list[dict]:
    out = df
    for col in out.columns:
        if out[col].dtype in (pl.Float32, pl.Float64):
            out = out.with_columns(pl.col(col).round(digits))
    return out.to_dicts()


def build_serving(
    player_match: pl.DataFrame | None,
    player_gw: pl.DataFrame | None,
    team_match: pl.DataFrame | None,
    fixtures: pl.DataFrame | None,
) -> dict:
    SERVING_DIR.mkdir(parents=True, exist_ok=True)
    artefacts: dict[str, str] = {}

    if player_match is not None and player_match.height:
        pl_only = player_match.filter(pl.col("competition") == PREMIER_LEAGUE)
        artefacts["player_rolling_pl.json"] = _write(
            "player_rolling_pl.json",
            {
                "generated_at_utc": _now(),
                "competition": PREMIER_LEAGUE,
                "min_minutes_per_appearance": MIN_MINUTES,
                "windows": {str(w): _player_window(pl_only, w) for w in WINDOWS},
            },
        )
        artefacts["player_rolling_all.json"] = _write(
            "player_rolling_all.json",
            {
                "generated_at_utc": _now(),
                "competition": "all",
                "min_minutes_per_appearance": MIN_MINUTES,
                "windows": {str(w): _player_window(player_match, w) for w in WINDOWS},
            },
        )

    if team_match is not None and team_match.height:
        pl_teams = team_match.filter(
            (pl.col("competition") == PREMIER_LEAGUE) & pl.col("finished")
        )
        artefacts["team_rolling_pl.json"] = _write(
            "team_rolling_pl.json",
            {
                "generated_at_utc": _now(),
                "competition": PREMIER_LEAGUE,
                "windows": {str(w): _team_window(pl_teams, w) for w in WINDOWS},
            },
        )

    if player_gw is not None and player_gw.height:
        latest_season = player_gw.select(pl.col("season").max()).item()
        season_df = player_gw.filter(pl.col("season") == latest_season).sort(
            ["player_id", "gw"]
        )
        slim = season_df.select(
            [
                c
                for c in [
                    "season",
                    "gw",
                    "player_id",
                    "player_code",
                    "web_name",
                    "team_code",
                    "position",
                    "total_points",
                    "event_points",
                    "now_cost",
                    "selected_by_percent",
                    "form",
                    "minutes",
                    "expected_goals",
                    "expected_assists",
                    "status",
                ]
                if c in season_df.columns
            ]
        )
        artefacts["player_gw_latest.json"] = _write(
            "player_gw_latest.json",
            {"generated_at_utc": _now(), "season": latest_season, "rows": _round_df(slim)},
        )

    if fixtures is not None and fixtures.height:
        upcoming = fixtures.sort(["kickoff_utc", "match_id"]).head(80)
        artefacts["fixtures_ticker.json"] = _write(
            "fixtures_ticker.json",
            {"generated_at_utc": _now(), "rows": _round_df(upcoming)},
        )

    index = {
        "generated_at_utc": _now(),
        "artefacts": artefacts,
        "notes": "Compact pre-aggregates for a static HTML dashboard. Masters remain in Parquet.",
    }
    _write("index.json", index)
    log.info("Serving artefacts written to %s", SERVING_DIR)
    return index


def _player_window(df: pl.DataFrame, window: int) -> list[dict]:
    if "kickoff_utc" in df.columns:
        df = df.sort(["player_id", "season", "kickoff_utc"])
    else:
        df = df.sort(["player_id", "season", "gw"])
    rolled = (
        df.with_columns(
            pl.col("minutes").cast(pl.Float64),
            pl.col("xg").cast(pl.Float64) if "xg" in df.columns else pl.lit(None).alias("xg"),
            pl.col("xa").cast(pl.Float64) if "xa" in df.columns else pl.lit(None).alias("xa"),
        )
        .with_columns(
            pl.col("xg").rolling_sum(window_size=window, min_samples=1).over("player_id").alias("xg_w"),
            pl.col("xa").rolling_sum(window_size=window, min_samples=1).over("player_id").alias("xa_w"),
            pl.col("minutes").rolling_mean(window_size=window, min_samples=1).over("player_id").alias("mins_avg"),
            pl.len().over("player_id").alias("appearances"),
        )
        .sort(["player_id", "season", "gw", "kickoff_utc"])
        .group_by(["season", "player_id"], maintain_order=True)
        .last()
    )
    ident = [c for c in ["web_name", "position", "team_code", "player_code"] if c in rolled.columns]
    out = (
        rolled.select(
            "season",
            "player_id",
            *ident,
            pl.col("xg_w").alias("xg"),
            pl.col("xa_w").alias("xa"),
            (pl.col("xg_w").fill_null(0) + pl.col("xa_w").fill_null(0)).alias("xg_xa"),
            pl.col("mins_avg").alias("minutes_per_appearance"),
            "appearances",
        )
        .filter(pl.col("minutes_per_appearance") >= MIN_MINUTES)
        .filter(pl.col("xg").is_not_null() | pl.col("xa").is_not_null())
        .sort("xg_xa", descending=True, nulls_last=True)
        .head(50)
    )
    return _round_df(out)


def _team_window(df: pl.DataFrame, window: int) -> list[dict]:
    df = df.sort(["team_code", "season", "kickoff_utc", "gw"])
    rolled = (
        df.with_columns(
            pl.col("xg").cast(pl.Float64) if "xg" in df.columns else pl.lit(None).alias("xg"),
            pl.col("xga").cast(pl.Float64) if "xga" in df.columns else pl.lit(None).alias("xga"),
        )
        .with_columns(
            pl.col("xg").rolling_sum(window_size=window, min_samples=1).over("team_code").alias("xg_w"),
            pl.col("xga").rolling_sum(window_size=window, min_samples=1).over("team_code").alias("xga_w"),
        )
        .group_by(["season", "team_code", "is_home"], maintain_order=True)
        .last()
        .select(
            "season",
            "team_code",
            "is_home",
            pl.col("xg_w").alias("xg"),
            pl.col("xga_w").alias("xga"),
        )
    )
    return _round_df(rolled.sort(["season", "team_code", "is_home"]))


def _write(name: str, payload: dict) -> str:
    dest = SERVING_DIR / name
    atomic_write_json(payload, dest)
    return name


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
