"""Derived Understat analytics from shot / style / context masters."""

from __future__ import annotations

import logging

import polars as pl

from pipeline.understat.config import MASTER_DIR, ROLLING_WINDOWS, SEASONS
from pipeline.understat.ingest import read_master
from pipeline.understat.maps import load_team_map
from pipeline.understat.normalize import now_utc

log = logging.getLogger("understat")


def _attach_team_codes(shots: pl.DataFrame, matches: pl.DataFrame) -> pl.DataFrame:
    team_map = load_team_map().select(
        pl.col("understat_team_id").alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_name").alias("team"),
        pl.col("fpl_short").alias("team_short"),
    )
    opp_map = load_team_map().select(
        pl.col("understat_team_id").alias("opponent_id"),
        pl.col("team_code").alias("opponent_code"),
        pl.col("fpl_name").alias("opponent"),
        pl.col("fpl_short").alias("opponent_short"),
    )
    m = matches.select(
        "match_id",
        "kickoff_raw",
        "is_result",
        "home_team_id",
        "away_team_id",
        "home_goals",
        "away_goals",
        "home_xg",
        "away_xg",
    )
    return (
        shots.join(m, on="match_id", how="left")
        .join(team_map, on="team_id", how="left")
        .join(opp_map, on="opponent_id", how="left")
    )


def _write_by_season(name: str, df: pl.DataFrame) -> None:
    if df.is_empty() or "season" not in df.columns:
        out = MASTER_DIR / name / "part.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(out)
        log.info("%s rows=%s", name, df.height)
        return
    for season_val in df["season"].unique().to_list():
        part = df.filter(pl.col("season") == season_val)
        out_dir = MASTER_DIR / name / f"season={season_val}"
        out_dir.mkdir(parents=True, exist_ok=True)
        part.write_parquet(out_dir / "part.parquet")
    log.info("%s rows=%s", name, df.height)


def team_situation_match(shots: pl.DataFrame, matches: pl.DataFrame) -> pl.DataFrame:
    """Grain: team_code × match_id × situation (shots taken / for)."""
    s = _attach_team_codes(shots, matches).filter(pl.col("team_code").is_not_null())
    if s.is_empty():
        return pl.DataFrame()
    return (
        s.group_by(["season", "match_id", "team_code", "team", "team_short", "situation", "is_home"])
        .agg(
            pl.len().alias("shots"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
            pl.col("xg").sum().alias("us_xg"),
            pl.col("kickoff_raw").first().alias("kickoff_raw"),
            pl.col("opponent_code").first().alias("opponent_code"),
            pl.col("opponent").first().alias("opponent"),
            pl.col("opponent_short").first().alias("opponent_short"),
        )
        .with_columns(
            (pl.col("us_xg") / pl.col("shots")).alias("us_xg_per_shot"),
            pl.lit(now_utc()).alias("built_at_utc"),
        )
        .sort(["season", "team_code", "kickoff_raw", "situation"])
    )


def team_situation_against_match(shots: pl.DataFrame, matches: pl.DataFrame) -> pl.DataFrame:
    """
    Grain: defending team_code × match_id × situation.
    Built by flipping shooter team → opponent (shots faced).
    """
    s = _attach_team_codes(shots, matches).filter(pl.col("opponent_code").is_not_null())
    if s.is_empty():
        return pl.DataFrame()
    flipped = s.select(
        "season",
        "match_id",
        "situation",
        "kickoff_raw",
        "is_goal",
        "xg",
        pl.col("opponent_code").alias("team_code"),
        pl.col("opponent").alias("team"),
        pl.col("opponent_short").alias("team_short"),
        (~pl.col("is_home")).alias("is_home"),
        pl.col("team_code").alias("opponent_code"),
        pl.col("team").alias("opponent"),
        pl.col("team_short").alias("opponent_short"),
    )
    return (
        flipped.group_by(
            ["season", "match_id", "team_code", "team", "team_short", "situation", "is_home"]
        )
        .agg(
            pl.len().alias("shots_faced"),
            pl.col("is_goal").fill_null(False).sum().alias("goals_against"),
            pl.col("xg").sum().alias("us_xga"),
            pl.col("kickoff_raw").first().alias("kickoff_raw"),
            pl.col("opponent_code").first().alias("opponent_code"),
            pl.col("opponent").first().alias("opponent"),
            pl.col("opponent_short").first().alias("opponent_short"),
        )
        .with_columns(
            (pl.col("us_xga") / pl.col("shots_faced")).alias("us_xga_per_shot"),
            pl.lit(now_utc()).alias("built_at_utc"),
        )
        .sort(["season", "team_code", "kickoff_raw", "situation"])
    )


def _rolling_metric(
    match_df: pl.DataFrame,
    *,
    value_cols: list[str],
    situations_from: str = "situation",
    windows: tuple[int, ...] = ROLLING_WINDOWS,
) -> pl.DataFrame:
    if match_df.is_empty():
        return pl.DataFrame()

    situations = sorted(match_df[situations_from].drop_nulls().unique().to_list())
    team_matches = (
        match_df.select(
            "season",
            "match_id",
            "team_code",
            "team",
            "team_short",
            "kickoff_raw",
            "is_home",
            "opponent_code",
            "opponent",
            "opponent_short",
        )
        .unique()
        .sort(["season", "team_code", "kickoff_raw"])
    )
    sit_df = pl.DataFrame({situations_from: situations})
    skeleton = team_matches.join(sit_df, how="cross")
    keep = ["season", "match_id", "team_code", situations_from, *value_cols]
    filled = (
        skeleton.join(match_df.select([c for c in keep if c in match_df.columns]), on=["season", "match_id", "team_code", situations_from], how="left")
        .with_columns([pl.col(c).fill_null(0) for c in value_cols])
        .sort(["season", "team_code", situations_from, "kickoff_raw"])
    )
    frames = []
    for w in windows:
        exprs = [
            pl.col(c)
            .rolling_sum(window_size=w, min_samples=1)
            .over(["season", "team_code", situations_from])
            .alias(c)
            for c in value_cols
        ]
        frames.append(filled.with_columns(*exprs, pl.lit(w).alias("window")))
    return pl.concat(frames, how="diagonal_relaxed").with_columns(pl.lit(now_utc()).alias("built_at_utc"))


def team_situation_rolling(match_sit: pl.DataFrame, windows: tuple[int, ...] = ROLLING_WINDOWS) -> pl.DataFrame:
    out = _rolling_metric(match_sit, value_cols=["shots", "goals", "us_xg"], windows=windows)
    if out.is_empty():
        return out
    return out.with_columns(
        (pl.col("us_xg") / pl.when(pl.col("shots") > 0).then(pl.col("shots")).otherwise(None)).alias(
            "us_xg_per_shot"
        )
    )


def team_situation_against_rolling(
    match_against: pl.DataFrame, windows: tuple[int, ...] = ROLLING_WINDOWS
) -> pl.DataFrame:
    out = _rolling_metric(
        match_against,
        value_cols=["shots_faced", "goals_against", "us_xga"],
        windows=windows,
    )
    if out.is_empty():
        return out
    return out.with_columns(
        (
            pl.col("us_xga")
            / pl.when(pl.col("shots_faced") > 0).then(pl.col("shots_faced")).otherwise(None)
        ).alias("us_xga_per_shot")
    )


def team_zone_match(shots: pl.DataFrame, matches: pl.DataFrame) -> pl.DataFrame:
    s = _attach_team_codes(shots, matches).filter(
        pl.col("team_code").is_not_null() & pl.col("shot_zone").is_not_null()
    )
    if s.is_empty():
        return pl.DataFrame()
    return (
        s.group_by(["season", "match_id", "team_code", "team", "team_short", "shot_zone", "is_home"])
        .agg(
            pl.len().alias("shots"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
            pl.col("xg").sum().alias("us_xg"),
            pl.col("kickoff_raw").first().alias("kickoff_raw"),
            pl.col("opponent_code").first().alias("opponent_code"),
            pl.col("opponent").first().alias("opponent"),
        )
        .sort(["season", "team_code", "kickoff_raw", "shot_zone"])
        .with_columns(pl.lit(now_utc()).alias("built_at_utc"))
    )


def player_situation_season(shots: pl.DataFrame) -> pl.DataFrame:
    """
    Grain: understat player_id × season × situation (shot taker).
    player_code attached later via map when available.
    """
    if shots.is_empty():
        return pl.DataFrame()
    return (
        shots.filter(pl.col("player_id").is_not_null())
        .group_by(["season", "player_id", "player_name", "situation"])
        .agg(
            pl.len().alias("shots"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
            pl.col("xg").sum().alias("us_xg"),
            pl.col("team_id").first().alias("primary_team_id"),
            pl.col("last_action").first().alias("sample_last_action"),
        )
        .with_columns(
            (pl.col("us_xg") / pl.col("shots")).alias("us_xg_per_shot"),
            pl.lit(now_utc()).alias("built_at_utc"),
        )
        .sort(["season", "player_id", "situation"])
    )


def player_create_situation_season(shots: pl.DataFrame) -> pl.DataFrame:
    """
    Grain: creator display name × season × situation (from player_assisted).
    Join to player_id via name lookup from same-season shots.
    """
    if shots.is_empty():
        return pl.DataFrame()
    name_id = (
        shots.filter(pl.col("player_name").is_not_null() & pl.col("player_id").is_not_null())
        .group_by(["season", "player_name"])
        .agg(pl.col("player_id").first().alias("player_id"))
    )
    created = (
        shots.filter(pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != ""))
        .group_by(["season", pl.col("player_assisted").alias("player_name"), "situation"])
        .agg(
            pl.len().alias("assisted_shots"),
            pl.col("is_goal").fill_null(False).sum().alias("assisted_goals"),
            pl.col("xg").sum().alias("assisted_us_xg"),
        )
        .join(name_id, on=["season", "player_name"], how="left")
        .with_columns(pl.lit(now_utc()).alias("built_at_utc"))
        .sort(["season", "player_name", "situation"])
    )
    return created


def build_derived(*, fpl_seasons: list[str] | None = None) -> dict[str, pl.DataFrame]:
    fpl_seasons = fpl_seasons or list(SEASONS.values())
    shots = read_master("shot", fpl_seasons)
    matches = read_master("match", fpl_seasons)
    if shots.is_empty() or matches.is_empty():
        raise RuntimeError("Missing understat shot/match masters — run ingest first")

    style = read_master("team_match_style", fpl_seasons)
    context = read_master("team_context_season", fpl_seasons)
    league_player = read_master("league_player", fpl_seasons)

    sit = team_situation_match(shots, matches)
    sit_against = team_situation_against_match(shots, matches)
    roll = team_situation_rolling(sit)
    roll_against = team_situation_against_rolling(sit_against)
    zones = team_zone_match(shots, matches)
    player_sit = player_situation_season(shots)
    player_create = player_create_situation_season(shots)

    for name, df in (
        ("team_situation_match", sit),
        ("team_situation_against_match", sit_against),
        ("team_situation_rolling", roll),
        ("team_situation_against_rolling", roll_against),
        ("team_zone_match", zones),
        ("player_situation_season", player_sit),
        ("player_create_situation_season", player_create),
    ):
        _write_by_season(name, df)

    return {
        "team_situation_match": sit,
        "team_situation_against_match": sit_against,
        "team_situation_rolling": roll,
        "team_situation_against_rolling": roll_against,
        "team_zone_match": zones,
        "player_situation_season": player_sit,
        "player_create_situation_season": player_create,
        "team_match_style": style,
        "team_context_season": context,
        "league_player": league_player,
        "shot": shots,
        "match": matches,
    }
