from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("fpl")

GW_RE = re.compile(r"^GW(\d+)$", re.IGNORECASE)
SEASON_RE = re.compile(r"^\d{4}-\d{4}$")


@dataclass(frozen=True)
class GwSlice:
    season: str
    competition: str
    gw: int
    path: Path

    @property
    def key(self) -> str:
        return f"{self.season}|{self.competition}|{self.gw}"


@dataclass
class Discovery:
    data_root: Path
    seasons_all: list[str]
    seasons_with_tournaments: list[str]
    seasons_skipped: list[dict[str, str]]
    slices: list[GwSlice]


def discover(source_root: Path) -> Discovery:
    data_root = source_root / "data"
    if not data_root.exists():
        raise FileNotFoundError(f"No data/ directory under {source_root}")

    seasons_all = sorted(
        p.name for p in data_root.iterdir() if p.is_dir() and SEASON_RE.match(p.name)
    )
    slices: list[GwSlice] = []
    with_tournaments: list[str] = []
    skipped: list[dict[str, str]] = []

    for season in seasons_all:
        season_dir = data_root / season
        tournaments = season_dir / "By Tournament"
        if not tournaments.is_dir():
            skipped.append(
                {
                    "season": season,
                    "reason": "No By Tournament/ tree — not ingested (By Gameweek is never read).",
                }
            )
            log.warning("Skipping season %s: no By Tournament directory", season)
            continue
        with_tournaments.append(season)
        for comp_dir in sorted(tournaments.iterdir(), key=lambda p: p.name.lower()):
            if not comp_dir.is_dir():
                continue
            competition = comp_dir.name
            for gw_dir in sorted(comp_dir.iterdir(), key=_gw_sort):
                if not gw_dir.is_dir():
                    continue
                match = GW_RE.match(gw_dir.name)
                if not match:
                    continue
                slices.append(
                    GwSlice(
                        season=season,
                        competition=competition,
                        gw=int(match.group(1)),
                        path=gw_dir,
                    )
                )

    log.info(
        "Discovered %d slices across %d seasons (%d skipped)",
        len(slices),
        len(with_tournaments),
        len(skipped),
    )
    return Discovery(
        data_root=data_root,
        seasons_all=seasons_all,
        seasons_with_tournaments=with_tournaments,
        seasons_skipped=skipped,
        slices=slices,
    )


def _gw_sort(path: Path) -> tuple[int, str]:
    match = GW_RE.match(path.name)
    return (int(match.group(1)) if match else 999, path.name)
