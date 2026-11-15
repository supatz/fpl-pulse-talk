"""HTTP client for unofficial SofaScore JSON endpoints."""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request
from typing import Any

from pipeline.sofascore.cache import cache_path, read_json, write_json
from pipeline.sofascore.config import API_BASE, REQUEST_SLEEP_S, SEASON_IDS, UNIQUE_TOURNAMENT_ID, USER_AGENT

log = logging.getLogger("sofascore")

_NETWORK_ERRORS = (OSError, urllib.error.URLError, TimeoutError, ConnectionError)


class SofaScoreError(RuntimeError):
    pass


class SofaScoreFetcher:
    def __init__(self, *, force: bool = False, sleep_s: float = REQUEST_SLEEP_S):
        self.force = force
        self.sleep_s = sleep_s
        self.live_calls = 0
        self.cache_hits = 0

    def _live(self, path: str) -> Any:
        if self.live_calls and self.sleep_s > 0:
            time.sleep(self.sleep_s)
        self.live_calls += 1
        url = f"{API_BASE}{path}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://www.sofascore.com/",
                "Origin": "https://www.sofascore.com",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise SofaScoreError(f"HTTP {exc.code} {url}") from exc
        except _NETWORK_ERRORS as exc:
            raise SofaScoreError(f"network {url}: {exc}") from exc
        return json.loads(raw)

    def _get(self, key: str, path: str) -> Any:
        p = cache_path(*key.split("/"))
        if not self.force:
            hit = read_json(p)
            if hit is not None:
                self.cache_hits += 1
                return hit
        data = self._live(path)
        if data is None:
            return None
        write_json(p, data)
        return data

    def tournament_seasons(self) -> list[dict]:
        data = self._get(
            f"unique-tournament/{UNIQUE_TOURNAMENT_ID}/seasons.json",
            f"/unique-tournament/{UNIQUE_TOURNAMENT_ID}/seasons",
        )
        if not data:
            return []
        return data.get("seasons") or []

    def resolve_season_id(self, fpl_season: str) -> int | None:
        """Map FPL 2025-2026 → SofaScore season id whose year/name covers 2025/26."""
        if fpl_season in SEASON_IDS:
            return SEASON_IDS[fpl_season]
        start = fpl_season.split("-")[0]
        end = fpl_season.split("-")[-1][-2:] if "-" in fpl_season else ""
        needles = {
            fpl_season,
            f"{start}/{end}" if end else start,
            f"{start[-2:]}/{end}" if end else start,
            start,
        }
        for row in self.tournament_seasons():
            year = str(row.get("year") or "")
            name = str(row.get("name") or "")
            blob = f"{year} {name} {row.get('id')}"
            if any(n and n in blob for n in needles):
                return int(row["id"])
        return None

    def rounds(self, season_id: int) -> list[dict]:
        data = self._get(
            f"unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/rounds.json",
            f"/unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/rounds",
        )
        if not data:
            return []
        return data.get("rounds") or []

    def events_round(self, season_id: int, round_obj: dict) -> list[dict]:
        n = round_obj.get("round")
        if n is None:
            n = round_obj.get("id")
        key = f"unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/events-round-{n}.json"
        path = f"/unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/events/round/{n}"
        data = self._get(key, path)
        if not data:
            return []
        return data.get("events") or []

    def events_last_pages(self, season_id: int, *, max_pages: int = 20) -> list[dict]:
        """Fallback listing when rounds are missing."""
        out: list[dict] = []
        seen: set[int] = set()
        for kind in ("last", "next"):
            for page in range(max_pages):
                data = self._get(
                    f"unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/events-{kind}-{page}.json",
                    f"/unique-tournament/{UNIQUE_TOURNAMENT_ID}/season/{season_id}/events/{kind}/{page}",
                )
                events = (data or {}).get("events") or []
                if not events:
                    break
                for ev in events:
                    eid = ev.get("id")
                    if eid in seen:
                        continue
                    seen.add(eid)
                    out.append(ev)
        return out

    def shotmap(self, event_id: int) -> dict | None:
        return self._get(f"event/{event_id}/shotmap.json", f"/event/{event_id}/shotmap")

    def lineups(self, event_id: int) -> dict | None:
        return self._get(f"event/{event_id}/lineups.json", f"/event/{event_id}/lineups")
