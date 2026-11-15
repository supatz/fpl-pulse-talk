#!/usr/bin/env python3
"""Build SofaScore EPL masters + serving. Does not touch Understat."""

from __future__ import annotations

import argparse
import logging
import sys

from pathlib import Path

from pipeline.sofascore.config import LOGS_DIR, SEASONS
from pipeline.sofascore.dictionary import write_data_dictionary
from pipeline.sofascore.ingest import ingest_seasons
from pipeline.sofascore.serve import build_all_serving


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seasons", nargs="+", default=list(SEASONS.keys()))
    p.add_argument("--force", action="store_true", help="Bypass JSON caches")
    p.add_argument("--refresh", action="store_true", help="Re-pull event indexes; reuse cached shotmaps")
    p.add_argument("--skip-shots", action="store_true")
    p.add_argument("--ingest-only", action="store_true")
    p.add_argument("--serving-only", action="store_true")
    p.add_argument("--dict-only", action="store_true")
    args = p.parse_args(argv)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "sofascore.log", encoding="utf-8"),
        ],
    )
    log = logging.getLogger("sofascore")

    try:
        if args.dict_only:
            print(f"Dictionary → {write_data_dictionary()}")
            return 0
        if not args.serving_only:
            ingest_seasons(
                args.seasons,
                force=args.force,
                shots=not args.skip_shots,
                refresh_index=args.refresh or args.force,
            )
            if args.ingest_only:
                print(f"SofaScore ingest OK | seasons={args.seasons} | serving deferred")
                return 0
        payloads = build_all_serving()
        dict_path = write_data_dictionary()
        meta = payloads.get("meta", {})
        print(
            "SofaScore OK | "
            f"seasons={meta.get('seasons')} "
            f"events={meta.get('events')} "
            f"finished={meta.get('finished_matches')} "
            f"shots={meta.get('shots')} "
            f"| serving/ss_shot_treemap.json + ss_team_timing.json + ss_team_side_channels.json "
            f"| dict={Path(dict_path).name}"
        )
        return 0
    except Exception:
        log.exception("SofaScore build failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
