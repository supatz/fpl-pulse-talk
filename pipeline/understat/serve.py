"""Serving JSON for Understat analytics — FPL team_code keys on team views."""

from __future__ import annotations

import json
import math
from pathlib import Path

import polars as pl

from pipeline.understat.config import ROLLING_WINDOWS, SERVING_DIR, WEB_DATA_DIR, SEASONS
from pipeline.understat.derive import build_derived
from pipeline.understat.normalize import now_utc


def _round(v, nd=3):
    if v is None:
        return None
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, nd)
    if hasattr(v, "item"):
        return _round(v.item(), nd)
    return v


def _rows(df: pl.DataFrame) -> list[dict]:
    out = []
    for r in df.to_dicts():
        out.append({k: _round(v) if isinstance(v, float) else v for k, v in r.items()})
    return out


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if WEB_DATA_DIR.exists():
        (WEB_DATA_DIR / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _latest_rolling(roll: pl.DataFrame, metric_cols: list[str]) -> pl.DataFrame:
    if roll.is_empty():
        return roll
    return (
        roll.sort("kickoff_raw")
        .group_by(["season", "team_code", "team", "team_short", "situation", "window"])
        .agg(
            *[pl.col(c).last() for c in metric_cols if c in roll.columns],
            pl.col("kickoff_raw").last().alias("as_of_kickoff"),
            pl.col("match_id").last().alias("as_of_match_id"),
        )
        .sort(["season", "team_code", "window", "situation"])
    )


def build_all_serving(derived: dict[str, pl.DataFrame] | None = None) -> dict[str, dict]:
    d = derived or build_derived()
    sit = d["team_situation_match"]
    sit_ag = d["team_situation_against_match"]
    roll = d["team_situation_rolling"]
    roll_ag = d["team_situation_against_rolling"]
    zones = d["team_zone_match"]
    style = d.get("team_match_style", pl.DataFrame())
    context = d.get("team_context_season", pl.DataFrame())
    player_sit = d.get("player_situation_season", pl.DataFrame())
    player_create = d.get("player_create_situation_season", pl.DataFrame())
    shots = d["shot"]
    matches = d["match"]

    season_sit = (
        sit.group_by(["season", "team_code", "team", "team_short", "situation"])
        .agg(pl.col("shots").sum(), pl.col("goals").sum(), pl.col("us_xg").sum())
        .with_columns(
            (pl.col("us_xg") / pl.sum("us_xg").over(["season", "team_code"])).alias("us_xg_share"),
            (pl.col("shots") / pl.sum("shots").over(["season", "team_code"])).alias("shot_share"),
        )
        .sort(["season", "team_code", "situation"])
        if sit.height
        else sit
    )
    season_against = (
        sit_ag.group_by(["season", "team_code", "team", "team_short", "situation"])
        .agg(
            pl.col("shots_faced").sum(),
            pl.col("goals_against").sum(),
            pl.col("us_xga").sum(),
        )
        .with_columns(
            (pl.col("us_xga") / pl.sum("us_xga").over(["season", "team_code"])).alias("us_xga_share"),
        )
        .sort(["season", "team_code", "situation"])
        if sit_ag.height
        else sit_ag
    )
    season_zone = (
        zones.group_by(["season", "team_code", "team", "team_short", "shot_zone"])
        .agg(pl.col("shots").sum(), pl.col("goals").sum(), pl.col("us_xg").sum())
        .with_columns(
            (pl.col("us_xg") / pl.sum("us_xg").over(["season", "team_code"])).alias("us_xg_share"),
        )
        .sort(["season", "team_code", "shot_zone"])
        if zones.height
        else zones
    )

    # Style season averages (finished rows with match_id)
    style_season = pl.DataFrame()
    if style.height and "team_code" in style.columns:
        st = style.filter(pl.col("match_id").is_not_null()) if "match_id" in style.columns else style
        style_season = (
            st.group_by(["season", "team_code", "team", "team_short"])
            .agg(
                pl.col("xg").mean().alias("avg_us_xg"),
                pl.col("xga").mean().alias("avg_us_xga"),
                pl.col("ppda").mean().alias("avg_ppda"),
                pl.col("ppda_allowed").mean().alias("avg_ppda_allowed"),
                pl.col("deep").mean().alias("avg_deep"),
                pl.col("deep_allowed").mean().alias("avg_deep_allowed"),
                pl.col("npxgd").mean().alias("avg_npxgd"),
                pl.len().alias("matches"),
            )
            .sort(["season", "team_code"])
        )

    attack_speed = pl.DataFrame()
    if context.height and "context_family" in context.columns:
        attack_speed = (
            context.filter(pl.col("context_family") == "attackSpeed")
            .select(
                "season",
                "team_code",
                "team",
                "team_short",
                pl.col("context_value").alias("attack_speed"),
                "shots",
                "goals",
                "us_xg",
                "against_shots",
                "against_goals",
                "against_us_xg",
            )
            .sort(["season", "team_code", "attack_speed"])
        )

    meta = {
        "matches": matches.height,
        "finished_matches": int(matches.filter(pl.col("is_result")).height)
        if matches.height and "is_result" in matches.columns
        else None,
        "shots": shots.height,
        "seasons": sorted(matches["season"].unique().to_list()) if matches.height else [],
        "note": "Understat metrics only. Team keys = FPL team_code. Player tables use understat player_id until player_map exists.",
    }

    team_payload = {
        "schema_version": 2,
        "source": "understat.com",
        "built_at_utc": now_utc(),
        "windows": list(ROLLING_WINDOWS),
        "meta": meta,
        "season_situation": _rows(season_sit),
        "season_situation_against": _rows(season_against),
        "rolling_situation": _rows(
            _latest_rolling(roll, ["shots", "goals", "us_xg", "us_xg_per_shot"])
        ),
        "rolling_situation_against": _rows(
            _latest_rolling(roll_ag, ["shots_faced", "goals_against", "us_xga", "us_xga_per_shot"])
        ),
        "season_zone": _rows(season_zone),
        "season_style": _rows(style_season),
        "attack_speed": _rows(attack_speed),
        "match_situation_sample": _rows(sit.sort("kickoff_raw", descending=True).head(40))
        if sit.height
        else [],
        "match_style_sample": _rows(
            style.filter(pl.col("match_id").is_not_null()).sort("kickoff_raw", descending=True).head(20)
        )
        if style.height and "match_id" in style.columns
        else [],
    }
    _write_json(SERVING_DIR / "us_team_situation.json", team_payload)

    # Player serving: understat ids for inspection (not FPL-joined yet)
    player_payload = {
        "schema_version": 1,
        "source": "understat.com",
        "built_at_utc": now_utc(),
        "meta": {
            **meta,
            "player_rows": player_sit.height,
            "create_rows": player_create.height,
            "join_status": "understat player_id only — FPL player_code map not applied yet",
        },
        "taker_situation_sample": _rows(
            player_sit.sort("us_xg", descending=True).head(40) if player_sit.height else player_sit
        ),
        "creator_situation_sample": _rows(
            player_create.sort("assisted_us_xg", descending=True).head(40)
            if player_create.height
            else player_create
        ),
    }
    _write_json(SERVING_DIR / "us_player_situation.json", player_payload)

    from pipeline.understat.shot_treemap import build_shot_treemap_serving

    treemap_payload = build_shot_treemap_serving(fpl_seasons=meta.get("seasons") or list(SEASONS.values()))

    return {
        "us_team_situation": team_payload,
        "us_player_situation": player_payload,
        "us_shot_treemap": treemap_payload,
    }


# Back-compat alias
def build_team_situation_serving(derived: dict[str, pl.DataFrame] | None = None) -> dict:
    return build_all_serving(derived)["us_team_situation"]


def build_preview_tables(derived: dict[str, pl.DataFrame] | None = None) -> dict[str, pl.DataFrame]:
    d = derived or build_derived()
    sit = d["team_situation_match"]
    sit_ag = d["team_situation_against_match"]
    style = d.get("team_match_style", pl.DataFrame())
    ctx = d.get("team_context_season", pl.DataFrame())
    op = (
        sit.filter(pl.col("situation") == "OpenPlay")
        .group_by(["season", "team_code", "team"])
        .agg(pl.col("us_xg").sum().alias("open_play_xg"), pl.col("shots").sum(), pl.col("goals").sum())
        .sort(["season", "open_play_xg"], descending=[False, True])
        if sit.height
        else sit
    )
    against_op = (
        sit_ag.filter(pl.col("situation") == "OpenPlay")
        .group_by(["season", "team_code", "team"])
        .agg(
            pl.col("us_xga").sum().alias("open_play_xga"),
            pl.col("shots_faced").sum(),
            pl.col("goals_against").sum(),
        )
        .sort(["season", "open_play_xga"], descending=[False, True])
        if sit_ag.height
        else sit_ag
    )
    ppda = (
        style.filter(pl.col("match_id").is_not_null())
        .group_by(["season", "team_code", "team"])
        .agg(pl.col("ppda").mean().alias("avg_ppda"), pl.col("deep").mean().alias("avg_deep"))
        .sort(["season", "avg_ppda"])
        if style.height and "ppda" in style.columns
        else pl.DataFrame()
    )
    fast = (
        ctx.filter((pl.col("context_family") == "attackSpeed") & (pl.col("context_value") == "Fast"))
        .select("season", "team_code", "team", "us_xg", "goals", "shots")
        .sort(["season", "us_xg"], descending=[False, True])
        if ctx.height
        else pl.DataFrame()
    )
    return {
        "open_play_xg": op,
        "open_play_xga_faced": against_op,
        "avg_ppda": ppda,
        "fast_attack_xg": fast,
        "shot_head": d["shot"].head(5),
        "style_head": style.head(5) if style.height else style,
    }
