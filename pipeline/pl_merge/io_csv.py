"""CSV helpers for curated maps and review queues."""

from __future__ import annotations

from pathlib import Path

import polars as pl


def ensure_csv(path: Path, columns: tuple[str, ...] | list[str]) -> pl.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        empty = pl.DataFrame({c: [] for c in columns})
        empty.write_csv(path)
        return empty
    df = pl.read_csv(path)
    for c in columns:
        if c not in df.columns:
            df = df.with_columns(pl.lit(None).alias(c))
    return df


def write_csv(path: Path, df: pl.DataFrame) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if df.is_empty() and not df.columns:
        path.write_text("", encoding="utf-8")
        return path
    df.write_csv(path)
    return path
