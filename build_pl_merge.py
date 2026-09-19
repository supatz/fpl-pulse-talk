#!/usr/bin/env python3
"""Build Premier League FPL × Understat maps and player-match merge (not wired to the site)."""

from __future__ import annotations

import argparse
import logging
import sys

from pipeline.pl_merge.config import LOGS_DIR
from pipeline.pl_merge.runner import run_pl_merge
from pipeline.understat.config import SEASONS


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seasons", nargs="+", default=list(SEASONS.keys()), help="Understat season years, e.g. 2025 2026")
    p.add_argument("--force-roster", action="store_true", help="Re-fetch Understat match roster JSON")
    p.add_argument("--skip-roster", action="store_true", help="Use existing master/understat/roster parquet only")
    p.add_argument("--maps-only", action="store_true", help="Write maps + review CSVs, skip merged parquet")
    args = p.parse_args(argv)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "pl_merge.log", encoding="utf-8"),
        ],
    )
    log = logging.getLogger("pl_merge")
    try:
        summary = run_pl_merge(
            seasons=args.seasons,
            force_roster=args.force_roster,
            skip_roster=args.skip_roster,
            maps_only=args.maps_only,
        )
        print(
            "PL merge OK | "
            f"seasons={summary['fpl_seasons']} "
            f"roster={summary['roster_rows']} "
            f"match_map={summary['match_map_rows']} unmatched_matches={summary['match_unmatched']} "
            f"player_map={summary['player_map_rows']} "
            f"ambiguous={summary['player_ambiguous']} "
            f"unmatched_us={summary['player_unmatched_understat']} "
            f"unmatched_fpl={summary['player_unmatched_fpl']}"
        )
        for season, path in (summary.get("merged_paths") or {}).items():
            print(f"  merged {season} → {path}")
        return 0
    except Exception:
        log.exception("PL merge failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
