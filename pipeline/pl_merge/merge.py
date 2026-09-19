"""Left-join Understat roster metrics onto FPL Premier League player_match."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR
from pipeline.pl_merge.config import MASTER_DIR, PREMIER_LEAGUE
from pipeline.understat.normalize import now_utc

US_METRIC_RENAME = {
    "time": "us_minutes",
    "goals": "us_goals",
    "own_goals": "us_own_goals",
    "assists": "us_assists",
    "shots": "us_shots",
    "key_passes": "us_key_passes",
    "xg": "us_xg",
    "xa": "us_xa",
    "npxg": "us_npxg",
    "xg_chain": "us_xg_chain",
    "xg_buildup": "us_xg_buildup",
    "yellow_cards": "us_yellow_cards",
    "red_cards": "us_red_cards",
    "position": "us_position",
}


def load_fpl_pl_player_match(seasons: list[str]) -> pl.DataFrame:
    parts: list[pl.DataFrame] = []
    for season in seasons:
        path = (
            FPL_MASTER_DIR
            / "player_match"
            / f"season={season}"
            / f"competition={PREMIER_LEAGUE}"
            / "part.parquet"
        )
        if path.exists():
            parts.append(pl.read_parquet(path))
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed")


def _mapped_roster(
    roster: pl.DataFrame,
    match_map: pl.DataFrame,
    player_map: pl.DataFrame,
) -> pl.DataFrame:
    if roster is None or roster.is_empty() or match_map.is_empty() or player_map.is_empty():
        return pl.DataFrame()
    r = roster.with_columns(
        pl.col("match_id").cast(pl.Utf8).alias("understat_match_id"),
        pl.col("player_id").cast(pl.Utf8).alias("understat_player_id"),
    )
    mm = match_map.select(
        pl.col("understat_match_id").cast(pl.Utf8),
        pl.col("fpl_match_id").cast(pl.Utf8),
        pl.col("gw").cast(pl.Int64).alias("us_gw"),
    )
    pm = (
        player_map.filter(pl.col("status") == "accepted")
        if "status" in player_map.columns
        else player_map
    ).select(
        pl.col("understat_player_id").cast(pl.Utf8),
        pl.col("player_code").cast(pl.Int64),
    )
    joined = r.join(mm, on="understat_match_id", how="inner").join(pm, on="understat_player_id", how="inner")
    metric_cols = [c for c in US_METRIC_RENAME if c in joined.columns]
    agg = (
        joined.group_by("fpl_match_id", "player_code")
        .agg(
            pl.col("understat_match_id").first(),
            pl.col("understat_player_id").first(),
            pl.col("us_gw").first(),
            *[pl.col(c).sum() for c in metric_cols if c not in {"position"}],
            *([pl.col("position").first()] if "position" in metric_cols else []),
        )
        .rename({k: v for k, v in US_METRIC_RENAME.items() if k in joined.columns and k != "position"})
    )
    if "position" in agg.columns:
        agg = agg.rename({"position": "us_position"})
    return agg.rename({"fpl_match_id": "match_id"})


def write_merged_player_match(
    fpl_pm: pl.DataFrame,
    roster: pl.DataFrame,
    match_map: pl.DataFrame,
    player_map: pl.DataFrame,
) -> dict[str, Path]:
    us = _mapped_roster(roster, match_map, player_map)
    if fpl_pm.is_empty():
        return {}
    fpl = fpl_pm.with_columns(
        pl.col("match_id").cast(pl.Utf8),
        pl.col("player_code").cast(pl.Int64),
    )
    if us.is_empty():
        merged = fpl.with_columns(
            pl.lit(None).cast(pl.Utf8).alias("understat_match_id"),
            pl.lit(None).cast(pl.Utf8).alias("understat_player_id"),
        )
    else:
        merged = fpl.join(us, on=["match_id", "player_code"], how="left")
    merged = merged.with_columns(
        pl.lit(now_utc()).alias("pl_merge_built_at_utc"),
        pl.lit("fpl_core+understat_roster").alias("pl_merge_source"),
    )

    written: dict[str, Path] = {}
    seasons = sorted(merged["season"].unique().to_list()) if "season" in merged.columns else []
    for season in seasons:
        out_dir = MASTER_DIR / "player_match" / f"season={season}"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "part.parquet"
        merged.filter(pl.col("season") == season).write_parquet(path)
        written[season] = path
    return written
