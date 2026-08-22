from __future__ import annotations

import polars as pl

from pipeline.config import SHOT_OPEN_PLAY, SHOT_PENALTY, SHOT_SET_PIECE
from pipeline.io_utils import as_bool, as_float, as_int, blank_or_zero_to_null


def normalize_players(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        as_int(pl.col("player_code")).alias("player_code"),
        as_int(pl.col("player_id")).alias("player_id"),
        pl.col("web_name").cast(pl.Utf8),
        as_int(pl.col("team_code")).alias("team_code"),
        pl.col("position").cast(pl.Utf8),
        pl.col("first_name").cast(pl.Utf8) if "first_name" in df.columns else pl.lit(None).alias("first_name"),
        pl.col("second_name").cast(pl.Utf8) if "second_name" in df.columns else pl.lit(None).alias("second_name"),
    ).unique(subset=["player_id"], keep="first")


def normalize_teams(df: pl.DataFrame) -> pl.DataFrame:
    strength_cols = [
        c
        for c in df.columns
        if c.startswith("strength")
    ]
    out = df.select(
        as_int(pl.col("code")).alias("code"),
        as_int(pl.col("id")).alias("id"),
        pl.col("name").cast(pl.Utf8),
        pl.col("short_name").cast(pl.Utf8),
        *[blank_or_zero_to_null(pl.col(c)).alias(c) for c in strength_cols],
        blank_or_zero_to_null(pl.col("elo")).alias("elo") if "elo" in df.columns else pl.lit(None).alias("elo"),
        pl.col("pulse_id") if "pulse_id" in df.columns else pl.lit(None).alias("pulse_id"),
        pl.col("fotmob_name") if "fotmob_name" in df.columns else pl.lit(None).alias("fotmob_name"),
    )
    return out.unique(subset=["code"], keep="first")


def normalize_matches(df: pl.DataFrame, folder_gw: int, competition: str) -> pl.DataFrame:
    gw_src = as_int(pl.col("gameweek")) if "gameweek" in df.columns else pl.lit(None)
    tournament = pl.col("tournament").cast(pl.Utf8) if "tournament" in df.columns else pl.lit(None)
    return df.with_columns(
        gw_src.alias("match_gw"),
        pl.lit(folder_gw).cast(pl.Int64).alias("gw"),
        pl.lit(competition).alias("competition"),
        as_int(pl.col("home_team")).alias("home_team"),
        as_int(pl.col("away_team")).alias("away_team"),
        as_bool(pl.col("finished")).alias("finished"),
        pl.col("match_id").cast(pl.Utf8),
        pl.col("kickoff_time").cast(pl.Utf8).alias("kickoff_raw")
        if "kickoff_time" in df.columns
        else pl.lit(None).alias("kickoff_raw"),
        tournament.alias("tournament"),
        blank_or_zero_to_null(pl.col("home_team_elo")).alias("home_team_elo")
        if "home_team_elo" in df.columns
        else pl.lit(None).alias("home_team_elo"),
        blank_or_zero_to_null(pl.col("away_team_elo")).alias("away_team_elo")
        if "away_team_elo" in df.columns
        else pl.lit(None).alias("away_team_elo"),
        as_float(pl.col("home_score")).alias("home_score") if "home_score" in df.columns else pl.lit(None).alias("home_score"),
        as_float(pl.col("away_score")).alias("away_score") if "away_score" in df.columns else pl.lit(None).alias("away_score"),
    )


def kickoff_utc_expr() -> pl.Expr:
    return (
        pl.col("kickoff_raw")
        .cast(pl.Utf8, strict=False)
        .str.to_datetime(strict=False, time_zone="UTC")
        .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        .alias("kickoff_utc")
    )


def unpivot_team_match(matches: pl.DataFrame) -> pl.DataFrame:
    """One row per team per match (home + away)."""
    home_map, away_map = _side_metric_maps(matches.columns)

    home = matches.select(
        pl.col("season") if "season" in matches.columns else pl.lit(None).alias("season"),
        "competition",
        "gw",
        "match_id",
        pl.col("home_team").alias("team_code"),
        pl.col("away_team").alias("opponent_code"),
        pl.lit(True).alias("is_home"),
        "finished",
        pl.col("home_score").alias("goals_for"),
        pl.col("away_score").alias("goals_against"),
        pl.col("home_team_elo").alias("elo"),
        *[pl.col(src).alias(dest) for src, dest in home_map.items() if src in matches.columns],
        *[pl.col(src).alias(f"{dest}_against") for src, dest in away_map.items() if src in matches.columns],
        "kickoff_raw" if "kickoff_raw" in matches.columns else pl.lit(None).alias("kickoff_raw"),
        "tournament" if "tournament" in matches.columns else pl.lit(None).alias("tournament"),
    )
    away = matches.select(
        pl.col("season") if "season" in matches.columns else pl.lit(None).alias("season"),
        "competition",
        "gw",
        "match_id",
        pl.col("away_team").alias("team_code"),
        pl.col("home_team").alias("opponent_code"),
        pl.lit(False).alias("is_home"),
        "finished",
        pl.col("away_score").alias("goals_for"),
        pl.col("home_score").alias("goals_against"),
        pl.col("away_team_elo").alias("elo"),
        *[pl.col(src).alias(dest) for src, dest in away_map.items() if src in matches.columns],
        *[pl.col(src).alias(f"{dest}_against") for src, dest in home_map.items() if src in matches.columns],
        "kickoff_raw" if "kickoff_raw" in matches.columns else pl.lit(None).alias("kickoff_raw"),
        "tournament" if "tournament" in matches.columns else pl.lit(None).alias("tournament"),
    )
    both = pl.concat([home, away], how="diagonal_relaxed")
    return both.with_columns(
        kickoff_utc_expr(),
        pl.when(pl.col("goals_for") > pl.col("goals_against"))
        .then(pl.lit("W"))
        .when(pl.col("goals_for") < pl.col("goals_against"))
        .then(pl.lit("L"))
        .when(pl.col("goals_for").is_not_null() & pl.col("goals_against").is_not_null())
        .then(pl.lit("D"))
        .otherwise(None)
        .alias("result"),
        pl.when(~pl.col("finished"))
        .then(None)
        .when(pl.col("goals_for") > pl.col("goals_against"))
        .then(pl.lit(3, dtype=pl.Int64))
        .when(pl.col("goals_for") < pl.col("goals_against"))
        .then(pl.lit(0, dtype=pl.Int64))
        .when(pl.col("goals_for").is_not_null())
        .then(pl.lit(1, dtype=pl.Int64))
        .otherwise(None)
        .alias("points"),
        pl.when(pl.col("finished") & pl.col("goals_against").is_not_null())
        .then(pl.col("goals_against") == 0)
        .otherwise(None)
        .alias("clean_sheet"),
        pl.when(pl.col("is_home")).then(pl.lit("H")).otherwise(pl.lit("A")).alias("venue"),
    )


def _side_metric_maps(columns: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    rename = {
        "possession": "possession",
        "expected_goals_xg": "xg",
        "non_penalty_xg": "np_xg",
        "xg_open_play": "xg_open_play",
        "xg_set_play": "xg_set_play",
        "xg_on_target_xgot": "xgot",
        "total_shots": "total_shots",
        "shots_on_target": "shots_on_target",
        "shots_inside_box": "shots_inside_box",
        "shots_outside_box": "shots_outside_box",
        "big_chances": "big_chances",
        "big_chances_missed": "big_chances_missed",
        "touches_in_opposition_box": "touches_in_opposition_box",
        "corners": "corners",
        "accurate_passes": "accurate_passes",
        "accurate_passes_pct": "accurate_passes_pct",
        "accurate_long_balls": "accurate_long_balls",
        "accurate_long_balls_pct": "accurate_long_balls_pct",
        "accurate_crosses": "accurate_crosses",
        "accurate_crosses_pct": "accurate_crosses_pct",
        "tackles_won": "tackles_won",
        "tackles_won_pct": "tackles_won_pct",
        "interceptions": "interceptions",
        "blocks": "blocks",
        "clearances": "clearances",
        "duels_won": "duels_won",
        "aerial_duels_won": "aerial_duels_won",
        "aerial_duels_won_pct": "aerial_duels_won_pct",
        "ground_duels_won": "ground_duels_won",
        "ground_duels_won_pct": "ground_duels_won_pct",
        "fouls_committed": "fouls_committed",
        "offsides": "offsides",
        "yellow_cards": "yellow_cards",
        "red_cards": "red_cards",
        "keeper_saves": "keeper_saves",
        "successful_dribbles": "successful_dribbles",
        "successful_dribbles_pct": "successful_dribbles_pct",
    }
    home = {f"home_{src}": dest for src, dest in rename.items() if f"home_{src}" in columns}
    away = {f"away_{src}": dest for src, dest in rename.items() if f"away_{src}" in columns}
    return home, away


def rename_defence_cols(df: pl.DataFrame) -> pl.DataFrame:
    mapping = {
        "xg_against": "xga",
        "total_shots_against": "shots_conceded",
        "shots_on_target_against": "sot_conceded",
        "big_chances_against": "big_chances_conceded",
        "keeper_saves": "keeper_saves",
    }
    return df.rename({k: v for k, v in mapping.items() if k in df.columns})


def aggregate_shots(shots: pl.DataFrame) -> pl.DataFrame:
    sit = pl.col("situation").cast(pl.Utf8).str.to_lowercase()
    xg = as_float(pl.col("xg")) if "xg" in shots.columns else pl.lit(None)
    return (
        shots.with_columns(
            as_int(pl.col("player_id")).alias("player_id"),
            pl.col("match_id").cast(pl.Utf8),
            sit.alias("situation_norm"),
            xg.alias("shot_xg"),
        )
        .group_by(["match_id", "player_id"])
        .agg(
            pl.col("shot_xg")
            .filter(~pl.col("situation_norm").is_in(list(SHOT_PENALTY)))
            .sum()
            .alias("np_xg"),
            pl.col("shot_xg")
            .filter(pl.col("situation_norm").is_in(list(SHOT_SET_PIECE)))
            .sum()
            .alias("set_piece_xg"),
            pl.col("shot_xg")
            .filter(pl.col("situation_norm").is_in(list(SHOT_OPEN_PLAY)))
            .sum()
            .alias("open_play_xg"),
            pl.col("situation_norm")
            .filter(pl.col("situation_norm").is_in(list(SHOT_PENALTY)))
            .len()
            .alias("penalty_shots"),
        )
    )


def own_goals_from_incidents(incidents: pl.DataFrame) -> pl.DataFrame:
    itype = pl.col("incident_type").cast(pl.Utf8).str.to_lowercase()
    gtype = (
        pl.col("goal_type").cast(pl.Utf8).str.to_lowercase()
        if "goal_type" in incidents.columns
        else pl.lit("")
    )
    return (
        incidents.with_columns(
            as_int(pl.col("player_id")).alias("player_id"),
            pl.col("match_id").cast(pl.Utf8),
            itype.alias("itype"),
            gtype.alias("gtype"),
        )
        .filter(pl.col("itype").eq("goal") & pl.col("gtype").eq("owngoal") & pl.col("player_id").is_not_null())
        .group_by(["match_id", "player_id"])
        .len()
        .rename({"len": "own_goals"})
    )


def normalize_lineups(df: pl.DataFrame) -> pl.DataFrame:
    started = (
        as_bool(pl.col("is_starting"))
        if "is_starting" in df.columns
        else pl.lit(None).cast(pl.Boolean)
    )
    return df.select(
        pl.col("match_id").cast(pl.Utf8),
        as_int(pl.col("player_id")).alias("player_id"),
        started.alias("started"),
        pl.col("formation").cast(pl.Utf8) if "formation" in df.columns else pl.lit(None).alias("formation"),
        pl.col("lineup_status").cast(pl.Utf8)
        if "lineup_status" in df.columns
        else pl.lit(None).alias("lineup_status"),
        as_int(pl.col("team_code")).alias("lineup_team_code")
        if "team_code" in df.columns
        else pl.lit(None).cast(pl.Int64).alias("lineup_team_code"),
    ).unique(subset=["match_id", "player_id"], keep="first")


def normalize_enrichment(df: pl.DataFrame) -> pl.DataFrame:
    cols = {
        "rating": as_float(pl.col("rating")) if "rating" in df.columns else pl.lit(None),
        "yellow_cards": as_float(pl.col("yellow_cards")) if "yellow_cards" in df.columns else pl.lit(None),
        "red_cards": as_float(pl.col("red_cards")) if "red_cards" in df.columns else pl.lit(None),
    }
    return df.select(
        pl.col("match_id").cast(pl.Utf8),
        as_int(pl.col("player_id")).alias("player_id"),
        *[expr.alias(name) for name, expr in cols.items()],
    ).unique(subset=["match_id", "player_id"], keep="first")


def normalize_match_enrichment(df: pl.DataFrame) -> pl.DataFrame:
    keep = [
        "travel_distance_km",
        "weather_description",
        "temperature_c",
        "wind_speed",
        "pitch_condition",
        "is_local_derby",
        "is_neutral_ground",
        "lineup_status",
        "home_shot_model_xg",
        "away_shot_model_xg",
        "incident_timing_coverage",
        "unlocated_card_count",
        "quarantined_incident_count",
    ]
    exprs = [pl.col("match_id").cast(pl.Utf8)]
    for col in keep:
        if col not in df.columns:
            continue
        if col in {"is_local_derby", "is_neutral_ground"}:
            exprs.append(as_bool(pl.col(col)).alias(col))
        else:
            exprs.append(pl.col(col))
    return df.select(exprs).unique(subset=["match_id"], keep="first")


def normalize_player_gw(df: pl.DataFrame) -> pl.DataFrame:
    rename = {"id": "player_id"}
    out = df.rename({k: v for k, v in rename.items() if k in df.columns})
    wanted = [
        "player_id",
        "gw",
        "web_name",
        "status",
        "news",
        "now_cost",
        "selected_by_percent",
        "form",
        "event_points",
        "total_points",
        "bonus",
        "bps",
        "points_per_game",
        "ep_next",
        "ep_this",
        "transfers_in_event",
        "transfers_out_event",
        "corners_and_indirect_freekicks_order",
        "direct_freekicks_order",
        "penalties_order",
        "set_piece_threat",
        "minutes",
        "goals_scored",
        "assists",
        "clean_sheets",
        "goals_conceded",
        "own_goals",
        "penalties_saved",
        "penalties_missed",
        "yellow_cards",
        "red_cards",
        "saves",
        "starts",
        "expected_goals",
        "expected_assists",
        "expected_goal_involvements",
        "expected_goals_conceded",
        "influence",
        "creativity",
        "threat",
        "ict_index",
        "tackles",
        "clearances_blocks_interceptions",
        "recoveries",
        "defensive_contribution",
    ]
    exprs = []
    for col in wanted:
        if col not in out.columns:
            exprs.append(pl.lit(None).alias(col))
            continue
        if col in {"player_id", "gw"}:
            exprs.append(as_int(pl.col(col)).alias(col))
        else:
            exprs.append(pl.col(col))
    return out.select(exprs)


def attach_side_context(player_rows: pl.DataFrame, matches: pl.DataFrame) -> pl.DataFrame:
    match_ctx = matches.select(
        "match_id",
        "gw",
        "competition",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "finished",
        "kickoff_raw",
        "tournament",
        "match_gw",
    ).unique(subset=["match_id"], keep="first")
    joined = player_rows.join(match_ctx, on="match_id", how="left")
    team = pl.col("team_code")
    return joined.with_columns(
        kickoff_utc_expr(),
        (team == pl.col("home_team")).alias("is_home"),
        pl.when(team == pl.col("home_team"))
        .then(pl.col("away_team"))
        .when(team == pl.col("away_team"))
        .then(pl.col("home_team"))
        .otherwise(None)
        .alias("opponent_code"),
        pl.when(team == pl.col("home_team"))
        .then(pl.col("home_score"))
        .when(team == pl.col("away_team"))
        .then(pl.col("away_score"))
        .otherwise(None)
        .alias("team_goals_for"),
        pl.when(team == pl.col("home_team"))
        .then(pl.col("away_score"))
        .when(team == pl.col("away_team"))
        .then(pl.col("home_score"))
        .otherwise(None)
        .alias("team_goals_against"),
    ).with_columns(
        pl.when(pl.col("is_home")).then(pl.lit("H")).otherwise(pl.lit("A")).alias("venue"),
        pl.when(pl.col("team_goals_for") > pl.col("team_goals_against"))
        .then(pl.lit("W"))
        .when(pl.col("team_goals_for") < pl.col("team_goals_against"))
        .then(pl.lit("L"))
        .when(pl.col("team_goals_for").is_not_null() & pl.col("team_goals_against").is_not_null())
        .then(pl.lit("D"))
        .otherwise(None)
        .alias("result"),
    )


def add_dgw_flags(player_match: pl.DataFrame, competition_col: str = "competition") -> pl.DataFrame:
    counts = (
        player_match.group_by(["season", "gw", "player_id"])
        .len()
        .rename({"len": "gw_match_count"})
    )
    pl_counts = (
        player_match.filter(pl.col(competition_col) == "Premier League")
        .group_by(["season", "gw", "player_id"])
        .len()
        .rename({"len": "pl_gw_match_count"})
    )
    indexed = player_match.sort(["season", "gw", "player_id", "kickoff_utc", "match_id"]).with_columns(
        (pl.int_range(1, pl.len() + 1).over(["season", "gw", "player_id"])).alias("gw_match_index")
    )
    return (
        indexed.join(counts, on=["season", "gw", "player_id"], how="left")
        .join(pl_counts, on=["season", "gw", "player_id"], how="left")
        .with_columns(
            (pl.col("pl_gw_match_count").fill_null(0) >= 2).alias("is_dgw"),
        )
        .drop("pl_gw_match_count")
    )


def filter_valid_fixtures(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        ~pl.col("finished")
        & pl.col("home_team").is_not_null()
        & pl.col("away_team").is_not_null()
        & pl.col("match_id").is_not_null()
    )
