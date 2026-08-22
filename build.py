#!/usr/bin/env python3
"""Build FPL master datasets from olbauday/FPL-Core-Insights."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from pipeline.config import LOGS_DIR, SOURCE_DIR
from pipeline.runner import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Shallow-clone/update the public source repo, then incremental build.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Ignore incremental cache and rebuild every partition.",
    )
    parser.add_argument(
        "--serving-only",
        action="store_true",
        help="Rebuild dashboard JSON from existing Parquet masters (no network).",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help="Use an existing checkout instead of cloning (offline / tests).",
    )
    args = parser.parse_args(argv)

    if not (args.refresh or args.full or args.serving_only):
        args.refresh = True

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "pipeline.log", encoding="utf-8"),
        ],
    )

    try:
        result = run_pipeline(
            refresh=args.refresh,
            full=args.full,
            serving_only=args.serving_only,
            source_dir=args.source_dir,
        )
    except Exception:
        logging.getLogger("fpl").exception("Pipeline failed")
        return 1

    if args.serving_only:
        print("Serving layer rebuilt.")
        return 0
    counts = result.get("row_counts", {})
    print(
        "Build OK | "
        + " ".join(f"{k}={v:,}" for k, v in counts.items())
        + f" | commit={result.get('source_commit', '')[:12]}"
    )
    issues = result.get("quality_issues") or []
    if issues:
        print(f"Quality flags ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
