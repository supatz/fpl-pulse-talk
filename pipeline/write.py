from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

from pipeline.config import MASTER_DIR
from pipeline.io_utils import atomic_write_parquet

log = logging.getLogger("fpl")


def hive_path(table: str, season: str, competition: str | None = None) -> Path:
    parts = [MASTER_DIR, table, f"season={season}"]
    if competition is not None:
        parts.append(f"competition={competition}")
    return Path(*parts) / "part.parquet"


def read_partition(table: str, season: str, competition: str | None = None) -> pl.DataFrame | None:
    path = hive_path(table, season, competition)
    if not path.exists():
        return None
    return pl.read_parquet(path)


def write_partitioned(
    df: pl.DataFrame,
    table: str,
    competition: bool,
) -> list[str]:
    written: list[str] = []
    group_cols = ["season", "competition"] if competition else ["season"]
    for key, part in df.group_by(group_cols, maintain_order=True):
        rec = dict(zip(group_cols, key if isinstance(key, tuple) else (key,)))
        season = rec["season"]
        comp = rec.get("competition")
        dest = hive_path(table, season, comp if competition else None)
        atomic_write_parquet(part, dest)
        written.append(str(dest.relative_to(MASTER_DIR)))
        log.info("Wrote %s rows=%s", dest, part.height)
    return written


def merge_partition_gws(
    existing: pl.DataFrame | None,
    rebuilt: pl.DataFrame | None,
    reused_gws: set[int],
    rebuilt_gws: set[int],
) -> pl.DataFrame | None:
    frames: list[pl.DataFrame] = []
    if existing is not None and reused_gws:
        frames.append(existing.filter(pl.col("gw").is_in(list(reused_gws - rebuilt_gws))))
    if rebuilt is not None and rebuilt.height:
        frames.append(rebuilt)
    if not frames:
        return existing
    return pl.concat(frames, how="diagonal_relaxed")
