from __future__ import annotations

import logging
from typing import Any

import polars as pl

log = logging.getLogger("fpl")


def _dupes(df: pl.DataFrame, keys: list[str]) -> int:
    return df.group_by(keys).len().filter(pl.col("len") > 1).height


def _null_rates(df: pl.DataFrame, cols: list[str] | None = None, limit: int = 25) -> dict[str, float]:
    use = cols or df.columns
    rates = {}
    n = max(df.height, 1)
    for col in use:
        if col not in df.columns:
            continue
        rates[col] = round(df[col].null_count() / n, 4)
    # keep the highest-null columns for the manifest summary
    return dict(sorted(rates.items(), key=lambda kv: kv[1], reverse=True)[:limit])


def run_quality(
    player_match: pl.DataFrame | None,
    player_gw: pl.DataFrame | None,
    team_match: pl.DataFrame | None,
    fixtures: pl.DataFrame | None,
    players: dict[str, pl.DataFrame],
    teams: dict[str, pl.DataFrame],
) -> dict[str, Any]:
    issues: list[str] = []
    tables: dict[str, Any] = {}

    if player_match is not None:
        grain = ["season", "competition", "gw", "match_id", "player_id"]
        dupes = _dupes(player_match, grain)
        if dupes:
            issues.append(f"player_match has {dupes} duplicate grain keys")
        if "minutes" in player_match.columns:
            mins = pl.col("minutes").cast(pl.Float64, strict=False)
            bad = player_match.filter(
                mins.is_not_null() & ((mins < 0) | (mins > 120))
            ).height
            if bad:
                issues.append(f"player_match minutes outside 0–120: {bad} rows")
        if "xg" in player_match.columns:
            xg = pl.col("xg").cast(pl.Float64, strict=False)
            bad = player_match.filter(xg.is_not_null() & (xg < 0)).height
            if bad:
                issues.append(f"player_match xg < 0: {bad} rows")
        unresolved = 0
        for season, dim in players.items():
            part = player_match.filter(pl.col("season") == season)
            if not part.height:
                continue
            unresolved += part.join(dim.select("player_id"), on="player_id", how="anti").height
        if unresolved:
            issues.append(f"player_match player_id unmatched to season players: {unresolved}")
        tables["player_match"] = {
            "rows": player_match.height,
            "duplicate_keys": dupes,
            "null_rate": _null_rates(player_match),
        }

    if player_gw is not None:
        grain = ["season", "gw", "player_id"]
        dupes = _dupes(player_gw, grain)
        if dupes:
            issues.append(f"player_gw has {dupes} duplicate grain keys")
        if "now_cost" in player_gw.columns:
            bad = player_gw.filter(
                pl.col("now_cost").is_not_null() & ((pl.col("now_cost") < 3) | (pl.col("now_cost") > 16))
            ).height
            if bad:
                issues.append(f"player_gw now_cost outside 3–16: {bad} rows (flagged, not dropped)")
        tables["player_gw"] = {
            "rows": player_gw.height,
            "duplicate_keys": dupes,
            "null_rate": _null_rates(player_gw),
        }

    if team_match is not None:
        grain = ["season", "competition", "gw", "match_id", "team_code"]
        dupes = _dupes(team_match, grain)
        if dupes:
            issues.append(f"team_match has {dupes} duplicate grain keys")
        complete = team_match.filter(
            pl.col("finished")
            & pl.col("team_code").is_not_null()
            & pl.col("opponent_code").is_not_null()
        )
        per_match = (
            complete.group_by(["season", "match_id"]).len().filter(pl.col("len") != 2).height
        )
        if per_match:
            issues.append(f"team_match matches without exactly 2 team rows: {per_match}")
        unresolved = 0
        for season, dim in teams.items():
            part = team_match.filter(pl.col("season") == season)
            unresolved += part.join(dim.select(pl.col("code").alias("team_code")), on="team_code", how="anti").height
        if unresolved:
            issues.append(f"team_match team_code unmatched to season teams: {unresolved}")
        tables["team_match"] = {
            "rows": team_match.height,
            "duplicate_keys": dupes,
            "null_rate": _null_rates(team_match),
        }

    if fixtures is not None:
        grain = ["match_id"]
        dupes = _dupes(fixtures, grain)
        if dupes:
            issues.append(f"fixtures has {dupes} duplicate match_id")
        nan_teams = fixtures.filter(pl.col("home_team").is_null() | pl.col("away_team").is_null()).height
        if nan_teams:
            issues.append(f"fixtures still has {nan_teams} rows with null team codes")
        tables["fixtures"] = {
            "rows": fixtures.height,
            "duplicate_keys": dupes,
            "null_rate": _null_rates(fixtures),
        }

    for issue in issues:
        log.warning("quality: %s", issue)
    return {"issues": issues, "tables": tables}
