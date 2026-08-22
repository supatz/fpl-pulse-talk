from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any

import polars as pl

from pipeline.config import REQUIRED_COLUMNS
from pipeline.schema_drift import SchemaReport

log = logging.getLogger("fpl")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def header_schema_hash(columns: list[str]) -> str:
    payload = "\n".join(columns)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_paths(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for path in sorted(paths, key=lambda p: str(p)):
        h.update(str(path).encode())
        if path.exists() and path.is_file():
            h.update(file_sha256(path).encode())
        else:
            h.update(b"MISSING")
    return h.hexdigest()


def read_csv(path: Path) -> pl.DataFrame | None:
    if not path.exists():
        return None
    return pl.read_csv(
        path,
        infer_schema_length=20_000,
        null_values=["", "NA", "NaN", "nan", "None", "null", "NULL"],
        try_parse_dates=True,
        ignore_errors=False,
    )


def validate_columns(file_key: str, path: Path, df: pl.DataFrame) -> SchemaReport:
    required = REQUIRED_COLUMNS.get(file_key, [])
    present = list(df.columns)
    missing = [c for c in required if c not in present]
    extra = [c for c in present if c not in required]
    return SchemaReport(
        file_key=file_key,
        path=str(path),
        present=present,
        missing=missing,
        extra=extra,
        schema_hash=header_schema_hash(present),
    )


def as_int(expr: pl.Expr) -> pl.Expr:
    return expr.cast(pl.Float64, strict=False).round(0).cast(pl.Int64, strict=False)


def as_float(expr: pl.Expr) -> pl.Expr:
    return expr.cast(pl.Float64, strict=False)


def as_bool(expr: pl.Expr) -> pl.Expr:
    return (
        expr.cast(pl.Utf8, strict=False)
        .str.to_lowercase()
        .is_in(["true", "1", "yes", "t"])
    )


def blank_or_zero_to_null(expr: pl.Expr) -> pl.Expr:
    numeric = expr.cast(pl.Float64, strict=False)
    return pl.when(numeric.is_null() | (numeric == 0)).then(None).otherwise(numeric)


def atomic_write_parquet(df: pl.DataFrame, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    df.write_parquet(tmp, compression="zstd")
    os.replace(tmp, dest)


def atomic_write_json(payload: Any, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    os.replace(tmp, dest)


def atomic_write_text(text: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, dest)


def log_join(
    name: str,
    left: pl.DataFrame,
    right: pl.DataFrame,
    result: pl.DataFrame,
    keys: list[str],
) -> dict[str, int]:
    if any(k not in left.columns or k not in right.columns for k in keys):
        stats = {
            "join": name,
            "left_rows": left.height,
            "right_rows": right.height,
            "out_rows": result.height,
            "skipped": "missing join keys on an input frame",
        }
        log.info("join %s", stats)
        return stats
    left_keys = left.select(keys).unique()
    right_keys = right.select(keys).unique()
    unmatched_left = left_keys.join(right_keys, on=keys, how="anti").height
    unmatched_right = right_keys.join(left_keys, on=keys, how="anti").height
    left_dupes = left.group_by(keys).len().filter(pl.col("len") > 1).height
    right_dupes = right.group_by(keys).len().filter(pl.col("len") > 1).height
    stats = {
        "join": name,
        "left_rows": left.height,
        "right_rows": right.height,
        "out_rows": result.height,
        "unmatched_left": unmatched_left,
        "unmatched_right": unmatched_right,
        "duplicate_keys_left": left_dupes,
        "duplicate_keys_right": right_dupes,
    }
    log.info("join %s", stats)
    return stats
