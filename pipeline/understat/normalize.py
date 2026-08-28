"""Normalize raw Understat payloads into typed row dicts / frames."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import polars as pl

from pipeline.understat.config import SEASONS
from pipeline.understat.zones import shot_zone


def _f(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _i_str(v: Any) -> str | None:
    if v is None or v == "":
        return None
    return str(v)


def _bool(v: Any) -> bool:
    return bool(v)


def fpl_season(understat_season: str) -> str:
    return SEASONS.get(str(understat_season), str(understat_season))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_match(raw: dict, *, understat_season: str) -> dict:
    h, a = raw.get("h") or {}, raw.get("a") or {}
    goals, xg, forecast = raw.get("goals") or {}, raw.get("xG") or {}, raw.get("forecast") or {}
    return {
        "match_id": _i_str(raw.get("id")),
        "understat_season": str(understat_season),
        "season": fpl_season(understat_season),
        "league": "EPL",
        "is_result": _bool(raw.get("isResult")),
        "kickoff_raw": raw.get("datetime"),
        "home_team_id": _i_str(h.get("id")),
        "away_team_id": _i_str(a.get("id")),
        "home_team": h.get("title"),
        "away_team": a.get("title"),
        "home_short": h.get("short_title"),
        "away_short": a.get("short_title"),
        "home_goals": _f(goals.get("h")),
        "away_goals": _f(goals.get("a")),
        "home_xg": _f(xg.get("h")),
        "away_xg": _f(xg.get("a")),
        "forecast_w": _f(forecast.get("w")),
        "forecast_d": _f(forecast.get("d")),
        "forecast_l": _f(forecast.get("l")),
    }


def _shots_from_side(
    shots: list[dict],
    *,
    side: str,
    team_id: str | None,
    opponent_id: str | None,
    understat_season: str,
) -> list[dict]:
    rows = []
    for s in shots or []:
        x, y = _f(s.get("X")), _f(s.get("Y"))
        result = s.get("result")
        rows.append(
            {
                "shot_id": _i_str(s.get("id")),
                "match_id": _i_str(s.get("match_id")),
                "understat_season": str(understat_season),
                "season": fpl_season(s.get("season") or understat_season),
                "minute": _f(s.get("minute")),
                "date": s.get("date"),
                "side": side,
                "is_home": side == "h",
                "team_id": team_id,
                "opponent_id": opponent_id,
                "h_team": s.get("h_team"),
                "a_team": s.get("a_team"),
                "h_goals": _f(s.get("h_goals")),
                "a_goals": _f(s.get("a_goals")),
                "player_id": _i_str(s.get("player_id")),
                "player_name": s.get("player"),
                "player_assisted": s.get("player_assisted"),
                "situation": s.get("situation"),
                "last_action": s.get("lastAction"),
                "shot_type": s.get("shotType"),
                "result": result,
                "xg": _f(s.get("xG")),
                "x": x,
                "y": y,
                "shot_zone": shot_zone(x, y, result=result),
                "is_goal": result == "Goal",
            }
        )
    return rows


def normalize_match_shots(
    raw_shots: dict,
    *,
    match_row: dict,
) -> list[dict]:
    return _shots_from_side(
        raw_shots.get("h") or [],
        side="h",
        team_id=match_row.get("home_team_id"),
        opponent_id=match_row.get("away_team_id"),
        understat_season=match_row["understat_season"],
    ) + _shots_from_side(
        raw_shots.get("a") or [],
        side="a",
        team_id=match_row.get("away_team_id"),
        opponent_id=match_row.get("home_team_id"),
        understat_season=match_row["understat_season"],
    )


def _ppda_ratio(ppda: Any) -> float | None:
    if not isinstance(ppda, dict):
        return None
    att, deff = _f(ppda.get("att")), _f(ppda.get("def"))
    if att is None or deff is None or deff == 0:
        return None
    return att / deff


def normalize_team_history_row(
    hist: dict,
    *,
    team_id: str,
    team_title: str,
    understat_season: str,
) -> dict:
    ppda, ppda_a = hist.get("ppda") or {}, hist.get("ppda_allowed") or {}
    return {
        "understat_season": str(understat_season),
        "season": fpl_season(understat_season),
        "team_id": str(team_id),
        "team_title": team_title,
        "kickoff_raw": hist.get("date"),
        "is_home": hist.get("h_a") == "h",
        "h_a": hist.get("h_a"),
        "result": hist.get("result"),
        "scored": _f(hist.get("scored")),
        "conceded": _f(hist.get("missed")),
        "xg": _f(hist.get("xG")),
        "xga": _f(hist.get("xGA")),
        "npxg": _f(hist.get("npxG")),
        "npxga": _f(hist.get("npxGA")),
        "npxgd": _f(hist.get("npxGD")),
        "xpts": _f(hist.get("xpts")),
        "deep": _f(hist.get("deep")),
        "deep_allowed": _f(hist.get("deep_allowed")),
        "ppda_att": _f(ppda.get("att")),
        "ppda_def": _f(ppda.get("def")),
        "ppda": _ppda_ratio(ppda),
        "ppda_allowed_att": _f(ppda_a.get("att")),
        "ppda_allowed_def": _f(ppda_a.get("def")),
        "ppda_allowed": _ppda_ratio(ppda_a),
        "wins_cum": _f(hist.get("wins")),
        "draws_cum": _f(hist.get("draws")),
        "losses_cum": _f(hist.get("loses")),
        "pts_cum": _f(hist.get("pts")),
    }


def flatten_team_context(
    context: dict,
    *,
    team_id: str,
    team_title: str,
    team_slug: str,
    understat_season: str,
) -> list[dict]:
    """Long-form rows: team × season × context_family × context_value."""
    rows: list[dict] = []
    for family, values in (context or {}).items():
        if not isinstance(values, dict):
            continue
        for value, stats in values.items():
            if not isinstance(stats, dict):
                continue
            against = stats.get("against") or {}
            rows.append(
                {
                    "understat_season": str(understat_season),
                    "season": fpl_season(understat_season),
                    "team_id": str(team_id),
                    "team_title": team_title,
                    "team_slug": team_slug,
                    "context_family": family,
                    "context_value": str(value),
                    "stat_label": stats.get("stat"),
                    "time_minutes": _f(stats.get("time")),
                    "shots": _f(stats.get("shots")),
                    "goals": _f(stats.get("goals")),
                    "us_xg": _f(stats.get("xG")),
                    "against_shots": _f(against.get("shots")),
                    "against_goals": _f(against.get("goals")),
                    "against_us_xg": _f(against.get("xG")),
                }
            )
    return rows


def normalize_league_player(raw: dict, *, understat_season: str) -> dict:
    return {
        "understat_season": str(understat_season),
        "season": fpl_season(understat_season),
        "player_id": _i_str(raw.get("id")),
        "player_name": raw.get("player_name"),
        "team_title": raw.get("team_title"),
        "position": raw.get("position"),
        "games": _f(raw.get("games")),
        "time": _f(raw.get("time")),
        "goals": _f(raw.get("goals")),
        "assists": _f(raw.get("assists")),
        "shots": _f(raw.get("shots")),
        "key_passes": _f(raw.get("key_passes")),
        "xg": _f(raw.get("xG")),
        "xa": _f(raw.get("xA")),
        "npxg": _f(raw.get("npxG")),
        "npg": _f(raw.get("npg")),
        "xg_chain": _f(raw.get("xGChain")),
        "xg_buildup": _f(raw.get("xGBuildup")),
        "yellow_cards": _f(raw.get("yellow_cards")),
        "red_cards": _f(raw.get("red_cards")),
    }


def matches_frame(rows: list[dict]) -> pl.DataFrame:
    return pl.DataFrame(rows) if rows else pl.DataFrame()


def shots_frame(rows: list[dict]) -> pl.DataFrame:
    return pl.DataFrame(rows) if rows else pl.DataFrame()
