"""Left-join Understat roster metrics onto FPL Premier League player_match."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR
from pipeline.pl_merge.config import MASTER_DIR, PREMIER_LEAGUE
from pipeline.pl_merge.names import normalize_name
from pipeline.understat.normalize import now_utc

# Understat-derived big chance: shot xG strictly above this threshold.
BIG_CHANCE_XG = 0.27

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


def _accepted_player_map(player_map: pl.DataFrame) -> pl.DataFrame:
    pm = (
        player_map.filter(pl.col("status") == "accepted")
        if "status" in player_map.columns
        else player_map
    )
    return pm.select(
        pl.col("understat_player_id").cast(pl.Utf8),
        pl.col("player_code").cast(pl.Int64),
    )


def _shot_name_to_id(shots: pl.DataFrame) -> pl.DataFrame:
    """Map normalized Understat display name → player_id within a season (from shooters)."""
    if shots.is_empty() or "player_name" not in shots.columns:
        return pl.DataFrame()
    names = (
        shots.filter(pl.col("player_name").is_not_null() & (pl.col("player_name") != ""))
        .select(
            pl.col("season").cast(pl.Utf8),
            pl.col("player_id").cast(pl.Utf8),
            pl.col("player_name").cast(pl.Utf8),
        )
        .unique()
    )
    if names.is_empty():
        return names
    return (
        names.with_columns(
            pl.col("player_name")
            .map_elements(normalize_name, return_dtype=pl.Utf8)
            .alias("name_key")
        )
        .filter(pl.col("name_key") != "")
        .group_by("season", "name_key")
        .agg(pl.col("player_id").n_unique().alias("n_ids"), pl.col("player_id").first())
        .filter(pl.col("n_ids") == 1)
        .select("season", "name_key", "player_id")
    )


def _mapped_big_chances(
    shots: pl.DataFrame,
    match_map: pl.DataFrame,
    player_map: pl.DataFrame,
) -> pl.DataFrame:
    """Match-level BCT/BCS/BCM (taker) and BCC (assister) from Understat shots with xG > 0.27."""
    if shots is None or shots.is_empty() or match_map.is_empty() or player_map.is_empty():
        return pl.DataFrame()
    needed = {"match_id", "player_id", "xg", "season"}
    if not needed.issubset(set(shots.columns)):
        return pl.DataFrame()

    goal_expr = (
        pl.col("is_goal").fill_null(False)
        if "is_goal" in shots.columns
        else pl.lit(False)
    )
    big = shots.filter(pl.col("xg").is_not_null() & (pl.col("xg") > BIG_CHANCE_XG)).with_columns(
        pl.col("match_id").cast(pl.Utf8).alias("understat_match_id"),
        pl.col("player_id").cast(pl.Utf8).alias("understat_player_id"),
        pl.col("season").cast(pl.Utf8),
        goal_expr.alias("is_goal"),
    )
    if big.is_empty():
        return pl.DataFrame()

    mm = match_map.select(
        pl.col("understat_match_id").cast(pl.Utf8),
        pl.col("fpl_match_id").cast(pl.Utf8),
    )
    pm = _accepted_player_map(player_map)

    # BCT = taken; BCS = scored; BCM = missed. BCS + BCM = BCT.
    bct = (
        big.join(mm, on="understat_match_id", how="inner")
        .join(pm, on="understat_player_id", how="inner")
        .group_by("fpl_match_id", "player_code")
        .agg(
            pl.len().alias("us_bct"),
            pl.col("is_goal").sum().cast(pl.UInt32).alias("us_bcs"),
            (~pl.col("is_goal")).sum().cast(pl.UInt32).alias("us_bcm"),
        )
    )

    if "player_assisted" not in big.columns:
        bcc = pl.DataFrame()
    else:
        name_id = _shot_name_to_id(shots)
        assisted = big.filter(
            pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != "")
        ).with_columns(
            pl.col("player_assisted")
            .map_elements(normalize_name, return_dtype=pl.Utf8)
            .alias("name_key")
        )
        if assisted.is_empty() or name_id.is_empty():
            bcc = pl.DataFrame()
        else:
            creators = name_id.rename({"player_id": "creator_understat_id"})
            bcc = (
                assisted.join(creators, on=["season", "name_key"], how="inner")
                .select(
                    "understat_match_id",
                    pl.col("creator_understat_id").alias("understat_player_id"),
                )
                .join(mm, on="understat_match_id", how="inner")
                .join(pm, on="understat_player_id", how="inner")
                .group_by("fpl_match_id", "player_code")
                .agg(pl.len().alias("us_bcc"))
            )

    zero = pl.lit(0).cast(pl.UInt32)
    if bct.is_empty() and bcc.is_empty():
        return pl.DataFrame()
    if bct.is_empty():
        out = bcc.with_columns(
            zero.alias("us_bct"),
            zero.alias("us_bcs"),
            zero.alias("us_bcm"),
        )
    elif bcc.is_empty():
        out = bct.with_columns(zero.alias("us_bcc"))
    else:
        out = bct.join(bcc, on=["fpl_match_id", "player_code"], how="full", coalesce=True).with_columns(
            pl.col("us_bct").fill_null(0),
            pl.col("us_bcs").fill_null(0),
            pl.col("us_bcm").fill_null(0),
            pl.col("us_bcc").fill_null(0),
        )
    return out.rename({"fpl_match_id": "match_id"}).select(
        "match_id", "player_code", "us_bcc", "us_bct", "us_bcs", "us_bcm"
    )


def write_merged_player_match(
    fpl_pm: pl.DataFrame,
    roster: pl.DataFrame,
    match_map: pl.DataFrame,
    player_map: pl.DataFrame,
    shots: pl.DataFrame | None = None,
) -> dict[str, Path]:
    us = _mapped_roster(roster, match_map, player_map)
    bc = _mapped_big_chances(shots if shots is not None else pl.DataFrame(), match_map, player_map)
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
    if not bc.is_empty():
        merged = merged.join(bc, on=["match_id", "player_code"], how="left")
    else:
        merged = merged.with_columns(
            pl.lit(None).cast(pl.UInt32).alias("us_bcc"),
            pl.lit(None).cast(pl.UInt32).alias("us_bct"),
            pl.lit(None).cast(pl.UInt32).alias("us_bcs"),
            pl.lit(None).cast(pl.UInt32).alias("us_bcm"),
        )
    merged = merged.with_columns(
        pl.lit(now_utc()).alias("pl_merge_built_at_utc"),
        pl.lit("fpl_core+understat_roster+us_big_chance").alias("pl_merge_source"),
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
