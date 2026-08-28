"""Cached UnderstatClient wrappers — single place for all live pulls."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from understatapi import UnderstatClient

from pipeline.understat.cache import cached_get
from pipeline.understat.config import LEAGUE, REQUEST_SLEEP_S

log = logging.getLogger("understat")


class UnderstatFetcher:
    """Session-scoped client with on-disk cache and rate limiting."""

    def __init__(self, *, force: bool = False, sleep_s: float = REQUEST_SLEEP_S):
        self.force = force
        self.sleep_s = sleep_s
        self._client: UnderstatClient | None = None
        self.live_calls = 0
        self.cache_hits = 0

    def __enter__(self) -> "UnderstatFetcher":
        self._client = UnderstatClient()
        self._client.__enter__()
        return self

    def __exit__(self, *exc) -> None:
        if self._client is not None:
            self._client.__exit__(*exc)
            self._client = None

    def _live(self, fn: Callable[[], Any]) -> Any:
        if self.live_calls and self.sleep_s > 0:
            time.sleep(self.sleep_s)
        self.live_calls += 1
        return fn()

    def _get(self, key: str, fn: Callable[[], Any]) -> Any:
        path_hint = key

        def wrapped():
            return self._live(fn)

        # detect cache hit cheaply
        from pipeline.understat.cache import cache_path, read_json

        p = cache_path(*key.split("/"))
        if not self.force and read_json(p) is not None:
            self.cache_hits += 1
            return read_json(p)
        data = cached_get(key, wrapped, force=self.force)
        log.debug("fetched %s", path_hint)
        return data

    def league_matches(self, season: str) -> list[dict]:
        assert self._client is not None
        c = self._client
        return self._get(
            f"league/{LEAGUE}/{season}/matches.json",
            lambda: c.league(LEAGUE).get_match_data(season=season),
        )

    def league_teams(self, season: str) -> dict:
        assert self._client is not None
        c = self._client
        return self._get(
            f"league/{LEAGUE}/{season}/teams.json",
            lambda: c.league(LEAGUE).get_team_data(season=season),
        )

    def league_players(self, season: str) -> list[dict]:
        assert self._client is not None
        c = self._client
        return self._get(
            f"league/{LEAGUE}/{season}/players.json",
            lambda: c.league(LEAGUE).get_player_data(season=season),
        )

    def match_shots(self, match_id: str) -> dict:
        assert self._client is not None
        c = self._client
        return self._get(
            f"match/{match_id}/shots.json",
            lambda: c.match(str(match_id)).get_shot_data(),
        )

    def match_roster(self, match_id: str) -> dict:
        assert self._client is not None
        c = self._client
        return self._get(
            f"match/{match_id}/roster.json",
            lambda: c.match(str(match_id)).get_roster_data(),
        )

    def match_info(self, match_id: str) -> dict:
        assert self._client is not None
        c = self._client
        return self._get(
            f"match/{match_id}/info.json",
            lambda: c.match(str(match_id)).get_match_info(),
        )

    def team_context(self, team_slug: str, season: str) -> dict:
        assert self._client is not None
        c = self._client
        slug = team_slug.replace(" ", "_")
        return self._get(
            f"team/{slug}/{season}/context.json",
            lambda: c.team(slug).get_context_data(season=season),
        )
