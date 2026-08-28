#!/usr/bin/env python3
"""Build Understat EPL masters + serving + data dictionary."""

from __future__ import annotations

import argparse
import logging
import sys

from pipeline.understat.config import LOGS_DIR, SEASONS
from pipeline.understat.derive import build_derived
from pipeline.understat.dictionary import write_data_dictionary
from pipeline.understat.ingest import ingest_seasons
from pipeline.understat.serve import build_all_serving, build_preview_tables


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seasons", nargs="+", default=list(SEASONS.keys()))
    p.add_argument("--force", action="store_true", help="Bypass all JSON caches")
    p.add_argument(
        "--refresh",
        action="store_true",
        help="Re-pull league indexes + context; reuse cached match shots; derive + serve",
    )
    p.add_argument("--skip-shots", action="store_true")
    p.add_argument("--derive-only", action="store_true")
    p.add_argument("--serving-only", action="store_true")
    p.add_argument("--dict-only", action="store_true", help="Only regenerate data dictionary")
    args = p.parse_args(argv)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "understat.log", encoding="utf-8"),
        ],
    )
    log = logging.getLogger("understat")

    try:
        if args.dict_only:
            path = write_data_dictionary()
            print(f"Dictionary → {path}")
            return 0

        derived = None
        if args.serving_only:
            payloads = build_all_serving()
        elif args.derive_only:
            derived = build_derived()
            payloads = build_all_serving(derived)
        else:
            ingest_seasons(
                args.seasons,
                force=args.force,
                shots=not args.skip_shots,
                refresh_index=args.refresh or args.force,
            )
            derived = build_derived()
            payloads = build_all_serving(derived)

        dict_path = write_data_dictionary()
        meta = payloads["us_team_situation"].get("meta", {})
        print(
            "Understat OK | "
            f"seasons={meta.get('seasons')} "
            f"matches={meta.get('matches')} "
            f"finished={meta.get('finished_matches')} "
            f"shots={meta.get('shots')} "
            f"| serving/us_team_situation.json + us_player_situation.json "
            f"| dict={dict_path.name}"
        )
        preview = build_preview_tables(derived)
        for label, key in (
            ("Open-play us_xg", "open_play_xg"),
            ("Open-play us_xga faced", "open_play_xga_faced"),
            ("Avg PPDA (lower=more intense press)", "avg_ppda"),
            ("Fast attackSpeed us_xg", "fast_attack_xg"),
        ):
            df = preview.get(key)
            if df is not None and df.height:
                print(f"\n{label}:")
                print(df.head(8))
        return 0
    except Exception:
        log.exception("Understat build failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
