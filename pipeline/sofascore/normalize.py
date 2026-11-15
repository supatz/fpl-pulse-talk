"""Normalize SofaScore payloads. Keep situation labels native."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pipeline.sofascore.config import (
    SOT_TYPES,
    ZONE_PENALTY_X,
    ZONE_PENALTY_Y_MAX,
    ZONE_PENALTY_Y_MIN,
    ZONE_SIX_YARD_X,
    ZONE_SIX_YARD_Y_MAX,
    ZONE_SIX_YARD_Y_MIN,
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _f(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _i(v: Any) -> int | None:
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _s(v: Any) -> str | None:
    if v is None or v == "":
        return None
    return str(v)


def shot_zone(x: float | None, y: float | None, *, is_own_goal: bool = False) -> str | None:
    if is_own_goal:
        return "own_goal"
    if x is None or y is None:
        return None
    xf, yf = float(x), float(y)
    if xf <= ZONE_SIX_YARD_X and ZONE_SIX_YARD_Y_MIN <= yf <= ZONE_SIX_YARD_Y_MAX:
        return "six_yard"
    if xf <= ZONE_PENALTY_X and ZONE_PENALTY_Y_MIN <= yf <= ZONE_PENALTY_Y_MAX:
        return "penalty_area"
    return "outside_box"


def side_channel(y: float | None) -> str | None:
    """Attacking view: SofaScore y 0–100, 100 = shooter's left touchline → high Y = Left."""
    if y is None:
        return None
    yf = float(y)
    if yf < 100.0 / 3.0:
        return "Right"
    if yf > 200.0 / 3.0:
        return "Left"
    return "Center"


def kick_date_from_timestamp(ts: Any) -> str | None:
    n = _i(ts)
    if n is None:
        return None
    return datetime.fromtimestamp(n, tz=timezone.utc).strftime("%Y-%m-%d")


def kickoff_iso(ts: Any) -> str | None:
    n = _i(ts)
    if n is None:
        return None
    return datetime.fromtimestamp(n, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_event(raw: dict, *, fpl_season: str, ss_season_id: int) -> dict:
    home = raw.get("homeTeam") or {}
    away = raw.get("awayTeam") or {}
    score = raw.get("homeScore") or {}
    ascore = raw.get("awayScore") or {}
    status = (raw.get("status") or {}).get("type")
    finished = status == "finished" or bool(raw.get("status", {}).get("code") == 100)
    return {
        "event_id": _i(raw.get("id")),
        "ss_season_id": ss_season_id,
        "season": fpl_season,
        "kickoff_ts": _i(raw.get("startTimestamp")),
        "kickoff_utc": kickoff_iso(raw.get("startTimestamp")),
        "kick_date": kick_date_from_timestamp(raw.get("startTimestamp")),
        "is_result": finished,
        "home_team_id": _i(home.get("id")),
        "away_team_id": _i(away.get("id")),
        "home_team": home.get("name"),
        "away_team": away.get("name"),
        "home_short": home.get("shortName") or home.get("nameCode"),
        "away_short": away.get("shortName") or away.get("nameCode"),
        "home_goals": _i(score.get("current") if finished else score.get("normaltime")),
        "away_goals": _i(ascore.get("current") if finished else ascore.get("normaltime")),
        "round": (raw.get("roundInfo") or {}).get("round"),
        "has_xg": bool(raw.get("hasXg")),
    }


def _player_blob(p: Any) -> tuple[int | None, str | None]:
    if not isinstance(p, dict):
        return None, None
    return _i(p.get("id")), p.get("name") or p.get("shortName")


def normalize_shot(raw: dict, *, event: dict) -> dict | None:
    if (raw.get("incidentType") or "shot") not in ("shot", None):
        # still a shotmap row
        pass
    pid, pname = _player_blob(raw.get("player") or {})
    gtype = _s(raw.get("goalType"))
    situation = _s(raw.get("situation")) or "regular"
    is_penalty = gtype == "penalty" or situation == "penalty"
    if is_penalty:
        situation = "penalty"
    shot_type = _s(raw.get("shotType")) or _s(raw.get("type"))
    is_own = gtype == "own"
    coords = raw.get("playerCoordinates") or raw.get("coordinates") or {}
    x, y = _f(coords.get("x")), _f(coords.get("y"))
    is_home = bool(raw.get("isHome"))
    team_id = event["home_team_id"] if is_home else event["away_team_id"]
    opp_id = event["away_team_id"] if is_home else event["home_team_id"]
    return {
        "shot_id": _i(raw.get("id")),
        "event_id": event["event_id"],
        "season": event["season"],
        "minute": _i(raw.get("time") if raw.get("time") is not None else raw.get("minute")),
        "time_seconds": _i(raw.get("timeSeconds")),
        "is_home": is_home,
        "team_id": team_id,
        "opponent_id": opp_id,
        "player_id": pid,
        "player_name": pname,
        "situation": situation,
        "shot_type": shot_type,
        "body_part": _s(raw.get("bodyPart") or raw.get("body_part")),
        "goal_type": gtype,
        "xg": _f(raw.get("xg") if "xg" in raw else raw.get("expectedGoals")),
        "xgot": _f(raw.get("xgot") if "xgot" in raw else raw.get("expectedGoalsOnTarget")),
        "x": x,
        "y": y,
        "x01": None if x is None else round(float(x) / 100.0, 4),
        "y01": None if y is None else round(float(y) / 100.0, 4),
        "shot_zone": shot_zone(x, y, is_own_goal=is_own),
        "side": side_channel(y),
        "is_goal": shot_type == "goal" and not is_own,
        "is_sot": (shot_type or "") in SOT_TYPES and not is_own,
        "is_penalty": is_penalty,
        "is_own_goal": is_own,
    }


def _stat(stats: dict, *keys: str) -> float | None:
    for k in keys:
        if k in stats and stats[k] is not None:
            return _f(stats[k])
    return None


def lineup_player_rows(lineups: dict | None, *, event: dict) -> list[dict]:
    if not lineups:
        return []
    rows: list[dict] = []
    for side, is_home in (("home", True), ("away", False)):
        blob = lineups.get(side) or {}
        team_id = event["home_team_id"] if is_home else event["away_team_id"]
        players = list(blob.get("players") or [])
        for item in players:
            player = item.get("player") or {}
            stats = item.get("statistics") or {}
            pid = _i(player.get("id"))
            if pid is None:
                continue
            rows.append(
                {
                    "event_id": event["event_id"],
                    "season": event["season"],
                    "team_id": team_id,
                    "is_home": is_home,
                    "player_id": pid,
                    "player_name": player.get("name") or player.get("shortName"),
                    "position": player.get("position") or item.get("position"),
                    "minutes": _stat(stats, "minutesPlayed", "minutes_played"),
                    "expected_goals": _stat(stats, "expectedGoals", "expected_goals"),
                    "expected_assists": _stat(stats, "expectedAssists", "expected_assists"),
                    "big_chances_created": _stat(
                        stats, "bigChancesCreated", "bigChanceCreated", "big_chances_created"
                    ),
                    "big_chances_missed": _stat(
                        stats, "bigChancesMissed", "bigChanceMissed", "big_chances_missed"
                    ),
                    "big_chances_scored": _stat(
                        stats, "bigChancesScored", "bigChanceScored", "big_chances_scored"
                    ),
                    "key_passes": _stat(stats, "keyPasses", "key_passes"),
                    "total_shots": _stat(stats, "shots", "totalShots", "onTargetScoringAttempt"),
                    "rating": _stat(stats, "rating"),
                }
            )
    return rows
