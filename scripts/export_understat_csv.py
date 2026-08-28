#!/usr/bin/env python3
"""Export Understat parquet masters to CSV for exploration."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.understat.config import MASTER_DIR, ROOT, SEASONS


def main() -> int:
    out = ROOT / "exports" / "understat"
    out.mkdir(parents=True, exist_ok=True)
    starter = out / "starter_2025-2026"
    starter.mkdir(exist_ok=True)

    for table_dir in sorted(MASTER_DIR.iterdir()):
        if not table_dir.is_dir():
            continue
        files = list(table_dir.rglob("*.parquet"))
        if not files:
            continue
        df = pl.concat([pl.read_parquet(f) for f in files], how="diagonal_relaxed")
        df.write_csv(out / f"{table_dir.name}.csv")
        if "season" in df.columns:
            s = df.filter(pl.col("season") == "2025-2026")
            if s.height:
                s.write_csv(starter / f"{table_dir.name}.csv")
        print(f"{table_dir.name}: {df.height:,} rows → {out / (table_dir.name + '.csv')}")
    print(f"\nAll seasons: {out}")
    print(f"2025-2026 only: {starter}")
    print(f"Seasons in masters: {list(SEASONS.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
