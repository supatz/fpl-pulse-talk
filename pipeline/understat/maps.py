"""Curated Understat ↔ FPL identity maps (not fuzzy at serve time)."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.understat.config import MAPS_DIR


def team_map_path() -> Path:
    return MAPS_DIR / "team_map.csv"


def load_team_map() -> pl.DataFrame:
    path = team_map_path()
    if not path.exists():
        raise FileNotFoundError(f"Missing curated team map: {path}")
    df = pl.read_csv(path)
    required = {"understat_team_id", "understat_title", "team_code", "fpl_name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"team_map.csv missing columns: {sorted(missing)}")
    return df.with_columns(
        pl.col("understat_team_id").cast(pl.Utf8),
        pl.col("team_code").cast(pl.Int64),
    )


def team_id_to_code(df: pl.DataFrame | None = None) -> dict[str, int]:
    m = df if df is not None else load_team_map()
    return dict(zip(m["understat_team_id"].to_list(), m["team_code"].to_list()))


def team_title_to_code(df: pl.DataFrame | None = None) -> dict[str, int]:
    m = df if df is not None else load_team_map()
    return dict(zip(m["understat_title"].to_list(), m["team_code"].to_list()))
