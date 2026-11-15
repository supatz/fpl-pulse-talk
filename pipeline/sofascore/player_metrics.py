"""Slim SofaScore player-match metrics for FPL serving left-join (never fill 0)."""

from __future__ import annotations

import polars as pl

from pipeline.sofascore.config import MAPS_DIR, SEASONS
from pipeline.sofascore.ingest import read_master


def sofascore_player_match_metrics(seasons: list[str] | None = None) -> pl.DataFrame:
    """season, player_code, match_id, BCC_sf, BCM_sf, SiB_sf.

    Unmapped players are omitted (site join leaves null, not 0).
    SofaScore lineups publish created + missed only — no taken/scored.
    """
    seasons = seasons or list(SEASONS.keys())
    pmap_path = MAPS_DIR / "player_map.csv"
    mmap_path = MAPS_DIR / "match_map.csv"
    empty = pl.DataFrame(
        schema={
            "season": pl.Utf8,
            "player_code": pl.Int64,
            "match_id": pl.Utf8,
            "BCC_sf": pl.Float64,
            "BCM_sf": pl.Float64,
            "SiB_sf": pl.Float64,
        }
    )
    if not pmap_path.exists() or not mmap_path.exists():
        return empty
    pmap = (
        pl.read_csv(pmap_path)
        .filter(pl.col("status") == "accepted")
        .select(
            pl.col("sofascore_player_id").cast(pl.Utf8).alias("player_id"),
            pl.col("player_code").cast(pl.Int64),
        )
        .unique(subset=["player_id"])
    )
    mmap = (
        pl.read_csv(mmap_path)
        .select(
            pl.col("sofascore_event_id").cast(pl.Utf8).alias("event_id"),
            pl.col("fpl_match_id").cast(pl.Utf8).alias("match_id"),
            pl.col("season").cast(pl.Utf8),
        )
        .unique(subset=["event_id"])
    )
    if pmap.is_empty() or mmap.is_empty():
        return empty

    lineups = read_master("player_match", seasons)
    shots = read_master("shot", seasons)
    out = empty
    if lineups.height:
        out = (
            lineups.with_columns(pl.col("player_id").cast(pl.Utf8), pl.col("event_id").cast(pl.Utf8))
            .join(pmap, on="player_id", how="inner")
            .join(mmap.drop("season"), on="event_id", how="inner")
            .group_by(["season", "player_code", "match_id"])
            .agg(
                pl.col("big_chances_created").sum().alias("BCC_sf"),
                pl.col("big_chances_missed").sum().alias("BCM_sf"),
            )
        )
    if shots.height:
        in_box = (
            shots.filter(pl.col("shot_zone").is_in(["six_yard", "penalty_area"]))
            .with_columns(pl.col("player_id").cast(pl.Utf8), pl.col("event_id").cast(pl.Utf8))
            .join(pmap, on="player_id", how="inner")
            .join(mmap.drop("season"), on="event_id", how="inner")
            .group_by(["season", "player_code", "match_id"])
            .agg(pl.len().alias("SiB_sf"))
        )
        if out.height:
            out = out.join(in_box, on=["season", "player_code", "match_id"], how="outer", coalesce=True)
        else:
            out = in_box
    if "BCC_sf" not in out.columns:
        out = out.with_columns(pl.lit(None).cast(pl.Float64).alias("BCC_sf"))
    if "BCM_sf" not in out.columns:
        out = out.with_columns(pl.lit(None).cast(pl.Float64).alias("BCM_sf"))
    if "SiB_sf" not in out.columns:
        out = out.with_columns(pl.lit(None).cast(pl.Float64).alias("SiB_sf"))
    return out.select("season", "player_code", "match_id", "BCC_sf", "BCM_sf", "SiB_sf")
