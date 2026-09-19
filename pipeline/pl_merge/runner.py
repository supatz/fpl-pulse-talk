"""Run roster ingest (if needed) then Premier League identity maps + merge."""

from __future__ import annotations

import logging
from pathlib import Path

from pipeline.pl_merge.config import MAPS_DIR, REVIEW_DIR
from pipeline.pl_merge.match_map import build_match_map
from pipeline.pl_merge.merge import load_fpl_pl_player_match, write_merged_player_match
from pipeline.pl_merge.player_map import build_player_map
from pipeline.understat.config import SEASONS as US_SEASONS
from pipeline.understat.ingest import ingest_season_matches, ingest_season_roster, read_master
from pipeline.understat.client import UnderstatFetcher

log = logging.getLogger("pl_merge")


def _ensure_roster(seasons_us: list[str], *, force: bool, skip_roster: bool) -> pl.DataFrame:
    fpl_seasons = [US_SEASONS[s] for s in seasons_us if s in US_SEASONS]
    existing = read_master("roster", fpl_seasons)
    if skip_roster:
        return existing
    # Revisit every requested season. UnderstatFetcher reuses cached roster JSON,
    # so only newly finished matches hit the network; each season partition is
    # then rewritten with all cached + new appearances.
    with UnderstatFetcher(force=force) as fetcher:
        for us in seasons_us:
            matches = ingest_season_matches(fetcher, us, force_index=False)
            ingest_season_roster(fetcher, us, matches)
    return read_master("roster", fpl_seasons)


def run_pl_merge(
    *,
    seasons: list[str] | None = None,
    force_roster: bool = False,
    skip_roster: bool = False,
    maps_only: bool = False,
) -> dict:
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    us_keys = seasons or list(US_SEASONS.keys())
    fpl_seasons = [US_SEASONS[s] for s in us_keys if s in US_SEASONS]

    roster = _ensure_roster(us_keys, force=force_roster, skip_roster=skip_roster)
    matches = read_master("match", fpl_seasons)
    league_player = read_master("league_player", fpl_seasons)

    match_map, match_unmatched = build_match_map(
        matches,
        fpl_seasons,
        override_path=MAPS_DIR / "match_overrides.csv",
        out_path=MAPS_DIR / "match_map.csv",
        unmatched_path=REVIEW_DIR / "match_unmatched.csv",
    )
    player_map, amb, unmatched_us, unmatched_fpl = build_player_map(
        roster,
        league_player,
        fpl_seasons,
        override_path=MAPS_DIR / "player_overrides.csv",
        out_path=MAPS_DIR / "player_map.csv",
        ambiguous_path=REVIEW_DIR / "player_ambiguous.csv",
        unmatched_us_path=REVIEW_DIR / "player_unmatched_understat.csv",
        unmatched_fpl_path=REVIEW_DIR / "player_unmatched_fpl.csv",
    )

    written: dict[str, Path] = {}
    if not maps_only:
        fpl_pm = load_fpl_pl_player_match(fpl_seasons)
        written = write_merged_player_match(fpl_pm, roster, match_map, player_map)

    summary = {
        "fpl_seasons": fpl_seasons,
        "roster_rows": roster.height,
        "match_map_rows": match_map.height,
        "match_unmatched": match_unmatched.height,
        "player_map_rows": player_map.height,
        "player_ambiguous": amb.height,
        "player_unmatched_understat": unmatched_us.height,
        "player_unmatched_fpl": unmatched_fpl.height,
        "merged_paths": {k: str(v) for k, v in written.items()},
    }
    log.info("pl_merge summary %s", summary)
    return summary
