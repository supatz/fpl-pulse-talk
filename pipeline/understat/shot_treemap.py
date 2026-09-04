"""Build shot explore serving payload (treemap + matrices + chances created)."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path

import polars as pl

from pipeline.understat.config import SERVING_DIR, SEASONS, WEB_DATA_DIR
from pipeline.understat.ingest import read_master
from pipeline.understat.last_action_groups import (
    LAST_ACTION_GROUP_ORDER,
    SOT_RESULTS,
    groups_for_site,
    last_action_group,
)
from pipeline.understat.maps import load_team_map
from pipeline.understat.normalize import now_utc


def _round(v, nd=3):
    if v is None:
        return None
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, nd)
    if hasattr(v, "item"):
        return _round(v.item(), nd)
    return v


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if WEB_DATA_DIR.exists():
        (WEB_DATA_DIR / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _p90(metric: str, minutes_col: str = "minutes") -> pl.Expr:
    return (
        pl.when(pl.col(minutes_col).is_not_null() & (pl.col(minutes_col) > 0))
        .then(pl.col(metric) * 90.0 / pl.col(minutes_col))
        .otherwise(None)
        .alias(f"{metric}_p90")
    )


def build_shot_treemap_serving(
    *,
    fpl_seasons: list[str] | None = None,
    top_players: int = 12,
) -> dict:
    fpl_seasons = fpl_seasons or list(SEASONS.values())
    shots = read_master("shot", fpl_seasons)
    matches = read_master("match", fpl_seasons)
    league_player = read_master("league_player", fpl_seasons)
    if shots.is_empty():
        raise RuntimeError("No understat shots — run ingest first")

    team_map = load_team_map().select(
        pl.col("understat_team_id").alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_name").alias("team"),
        pl.col("fpl_short").alias("team_short"),
    )

    la = [last_action_group(v) for v in shots["last_action"].to_list()]
    sot = [(v in SOT_RESULTS) for v in shots["result"].to_list()]
    s = (
        shots.with_columns(
            pl.Series("last_action_group", la),
            pl.Series("is_sot", sot),
        )
        .join(team_map, on="team_id", how="left")
        .filter(pl.col("team_code").is_not_null())
    )

    finished = matches.filter(pl.col("is_result")) if matches.height else matches
    team_matches = pl.DataFrame()
    if finished.height:
        home = finished.select("season", pl.col("home_team_id").alias("team_id"), "match_id")
        away = finished.select("season", pl.col("away_team_id").alias("team_id"), "match_id")
        team_matches = (
            pl.concat([home, away])
            .join(team_map, on="team_id", how="left")
            .filter(pl.col("team_code").is_not_null())
            .group_by(["season", "team_code"])
            .agg(pl.col("match_id").n_unique().alias("matches"))
        )

    minutes = pl.DataFrame()
    if league_player.height:
        keep = ["season", "player_id", pl.col("time").alias("minutes")]
        if "games" in league_player.columns:
            keep.append(pl.col("games").alias("games"))
        minutes = league_player.select(keep)

    player_matches = (
        s.group_by(["season", "team_code", "player_id"])
        .agg(pl.col("match_id").n_unique().alias("shot_matches"))
        if s.height
        else pl.DataFrame()
    )
    player_sit = (
        s.group_by(["season", "team_code", "player_id", "situation"])
        .agg(pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot"))
        if s.height
        else pl.DataFrame()
    )
    player_lag = (
        s.group_by(["season", "team_code", "player_id", "last_action_group"])
        .agg(pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot"))
        if s.height
        else pl.DataFrame()
    )

    # Name → id within season (for chances created / assisted-by)
    name_id = (
        s.filter(pl.col("player_name").is_not_null() & pl.col("player_id").is_not_null())
        .group_by(["season", "player_name"])
        .agg(
            pl.col("player_id").first().alias("player_id"),
            pl.col("team_code").first().alias("creator_team_code"),
            pl.col("team").first().alias("creator_team"),
            pl.col("team_short").first().alias("creator_team_short"),
        )
    )

    # Taker (shot) aggregates
    taker = (
        s.group_by(["season", "team_code", "team", "team_short", "player_id", "player_name"])
        .agg(
            pl.col("xg").sum().alias("xg"),
            pl.len().alias("shots"),
            pl.col("is_sot").sum().alias("sot"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
        )
        .join(minutes, on=["season", "player_id"], how="left")
        .join(player_matches, on=["season", "team_code", "player_id"], how="left")
        .with_columns(_p90("xg"), _p90("shots"), _p90("sot"), _p90("goals"))
    )

    # Chances created = preceding passer/assister on the shot
    created = (
        s.filter(pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != ""))
        .group_by(["season", pl.col("player_assisted").alias("player_name"), "team_code", "team", "team_short"])
        .agg(
            pl.len().alias("cc"),
            pl.col("xg").sum().alias("cc_xg"),
            pl.col("is_sot").sum().alias("cc_sot"),
            pl.col("is_goal").fill_null(False).sum().alias("cc_goals"),
        )
        .join(name_id.select("season", "player_name", "player_id"), on=["season", "player_name"], how="left")
        .join(minutes, on=["season", "player_id"], how="left")
        .with_columns(_p90("cc"), _p90("cc_xg"), _p90("cc_sot"))
    )

    # Merge taker + creator onto one player row set
    created_slim = created.select(
        "season",
        "player_id",
        "team_code",
        "player_name",
        "team",
        "team_short",
        "cc",
        "cc_xg",
        "cc_sot",
        "cc_goals",
        "minutes",
        "cc_p90",
        "cc_xg_p90",
        "cc_sot_p90",
    )
    player_agg = (
        taker.join(
            created_slim.select(
                "season",
                "player_id",
                "team_code",
                "cc",
                "cc_xg",
                "cc_sot",
                "cc_goals",
                "cc_p90",
                "cc_xg_p90",
                "cc_sot_p90",
            ),
            on=["season", "team_code", "player_id"],
            how="left",
        )
        .with_columns(
            pl.col("cc").fill_null(0),
            pl.col("cc_xg").fill_null(0.0),
            pl.col("cc_sot").fill_null(0),
            pl.col("cc_goals").fill_null(0),
        )
    )
    # Creators who never took a shot in this team-season
    only_creators = created_slim.join(
        taker.select("season", "team_code", "player_id"),
        on=["season", "team_code", "player_id"],
        how="anti",
    ).with_columns(
        pl.lit(0.0).alias("xg"),
        pl.lit(0).alias("shots"),
        pl.lit(0).alias("sot"),
        pl.lit(0).alias("goals"),
        pl.lit(None).alias("xg_p90"),
        pl.lit(None).alias("shots_p90"),
        pl.lit(None).alias("sot_p90"),
        pl.lit(None).alias("goals_p90"),
    )
    player_agg = pl.concat([player_agg, only_creators], how="diagonal_relaxed")

    team_agg = (
        s.group_by(["season", "team_code", "team", "team_short"])
        .agg(
            pl.col("xg").sum().alias("xg"),
            pl.len().alias("shots"),
            pl.col("is_sot").sum().alias("sot"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
            (
                pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != "")
            )
            .sum()
            .alias("cc"),
            pl.when(pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != ""))
            .then(pl.col("xg"))
            .otherwise(None)
            .sum()
            .alias("cc_xg"),
            pl.when(pl.col("player_assisted").is_not_null() & (pl.col("player_assisted") != ""))
            .then(pl.col("is_sot").cast(pl.Int64))
            .otherwise(None)
            .sum()
            .alias("cc_sot"),
        )
        .join(team_matches, on=["season", "team_code"], how="left")
        .with_columns(
            pl.when(pl.col("matches") > 0).then(pl.col("xg") / pl.col("matches")).otherwise(None).alias("xg_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("shots") / pl.col("matches")).otherwise(None).alias("shots_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("sot") / pl.col("matches")).otherwise(None).alias("sot_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("cc") / pl.col("matches")).otherwise(None).alias("cc_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("cc_xg") / pl.col("matches")).otherwise(None).alias("cc_xg_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("cc_sot") / pl.col("matches")).otherwise(None).alias("cc_sot_p90"),
        )
    )

    # For / against situation & last-action (team matrices)
    for_sit = (
        s.group_by(["season", "team_code", "situation"])
        .agg(pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot"))
    )
    for_lag = (
        s.group_by(["season", "team_code", "last_action_group"])
        .agg(pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot"))
    )

    # Against = flip to opponent
    against = s.select(
        "season",
        "situation",
        "last_action_group",
        "xg",
        "is_sot",
        "is_goal",
        pl.col("opponent_id").alias("team_id"),
    ).join(team_map, on="team_id", how="left").filter(pl.col("team_code").is_not_null())

    ag_sit = (
        against.group_by(["season", "team_code", "situation"])
        .agg(
            pl.col("xg").sum().alias("xga"),
            pl.len().alias("shots_faced"),
            pl.col("is_sot").sum().alias("sot_faced"),
        )
    )
    ag_lag = (
        against.group_by(["season", "team_code", "last_action_group"])
        .agg(
            pl.col("xg").sum().alias("xga"),
            pl.len().alias("shots_faced"),
            pl.col("is_sot").sum().alias("sot_faced"),
        )
    )

    situations = sorted(s["situation"].drop_nulls().unique().to_list())
    teams_out: list[dict] = []

    def clean_player(p: dict) -> dict:
        games = p.get("games")
        shot_matches = p.get("shot_matches")
        matches = games if games not in (None, 0) else shot_matches
        mins = p.get("minutes")
        mins_per90 = None
        if mins is not None and matches:
            mins_per90 = mins / matches
        return {
            "player_id": p.get("player_id"),
            "player_name": html.unescape(p.get("player_name") or "") or None,
            "xg": _round(p.get("xg") or 0),
            "shots": int(p.get("shots") or 0),
            "sot": int(p.get("sot") or 0),
            "goals": int(p.get("goals") or 0),
            "cc": int(p.get("cc") or 0),
            "cc_xg": _round(p.get("cc_xg") or 0),
            "cc_sot": int(p.get("cc_sot") or 0),
            "minutes": _round(mins, 1),
            "matches": int(matches) if matches is not None else None,
            "mins_per90": _round(mins_per90, 1),
            "xg_p90": _round(p.get("xg_p90")),
            "shots_p90": _round(p.get("shots_p90")),
            "sot_p90": _round(p.get("sot_p90")),
            "cc_p90": _round(p.get("cc_p90")),
            "cc_xg_p90": _round(p.get("cc_xg_p90")),
            "cc_sot_p90": _round(p.get("cc_sot_p90")),
        }

    for t in team_agg.sort(["season", "xg"], descending=[False, True]).to_dicts():
        season, code = t["season"], t["team_code"]
        plist = (
            player_agg.filter((pl.col("season") == season) & (pl.col("team_code") == code))
            .sort("xg", descending=True)
            .head(top_players)
            .to_dicts()
        )
        # also ensure top creators are present if not in top takers
        creators = (
            player_agg.filter((pl.col("season") == season) & (pl.col("team_code") == code) & (pl.col("cc") > 0))
            .sort("cc_xg", descending=True)
            .head(top_players)
            .to_dicts()
        )
        by_id = {p.get("player_id"): clean_player(p) for p in plist if p.get("player_id")}
        for c in creators:
            pid = c.get("player_id")
            if not pid:
                continue
            if pid in by_id:
                continue
            by_id[pid] = clean_player(c)
        for pid, row in by_id.items():
            sit_rows = (
                player_sit.filter(
                    (pl.col("season") == season) & (pl.col("team_code") == code) & (pl.col("player_id") == pid)
                ).to_dicts()
                if player_sit.height
                else []
            )
            lag_rows = (
                player_lag.filter(
                    (pl.col("season") == season) & (pl.col("team_code") == code) & (pl.col("player_id") == pid)
                ).to_dicts()
                if player_lag.height
                else []
            )
            row["by_situation"] = [
                {"situation": r["situation"], "xg": _round(r["xg"]), "shots": int(r["shots"]), "sot": int(r["sot"])}
                for r in sit_rows
            ]
            row["by_last_action_group"] = [
                {
                    "group": r["last_action_group"],
                    "xg": _round(r["xg"]),
                    "shots": int(r["shots"]),
                    "sot": int(r["sot"]),
                }
                for r in lag_rows
            ]
        players = list(by_id.values())

        sit = for_sit.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()
        lag = for_lag.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()
        asit = ag_sit.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()
        alag = ag_lag.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()

        teams_out.append(
            {
                "season": season,
                "team_code": code,
                "team": t["team"],
                "team_short": t["team_short"],
                "matches": int(t["matches"]) if t.get("matches") is not None else None,
                "xg": _round(t["xg"]),
                "shots": int(t["shots"]),
                "sot": int(t["sot"]),
                "goals": int(t["goals"]),
                "cc": int(t.get("cc") or 0),
                "cc_xg": _round(t.get("cc_xg") or 0),
                "cc_sot": int(t.get("cc_sot") or 0),
                "xg_p90": _round(t.get("xg_p90")),
                "shots_p90": _round(t.get("shots_p90")),
                "sot_p90": _round(t.get("sot_p90")),
                "cc_p90": _round(t.get("cc_p90")),
                "cc_xg_p90": _round(t.get("cc_xg_p90")),
                "cc_sot_p90": _round(t.get("cc_sot_p90")),
                "players": players,
                "by_situation": [
                    {"situation": r["situation"], "xg": _round(r["xg"]), "shots": int(r["shots"]), "sot": int(r["sot"])}
                    for r in sit
                ],
                "by_last_action_group": [
                    {
                        "group": r["last_action_group"],
                        "xg": _round(r["xg"]),
                        "shots": int(r["shots"]),
                        "sot": int(r["sot"]),
                    }
                    for r in lag
                ],
                "against_situation": [
                    {
                        "situation": r["situation"],
                        "xga": _round(r["xga"]),
                        "shots_faced": int(r["shots_faced"]),
                        "sot_faced": int(r["sot_faced"]),
                    }
                    for r in asit
                ],
                "against_last_action_group": [
                    {
                        "group": r["last_action_group"],
                        "xga": _round(r["xga"]),
                        "shots_faced": int(r["shots_faced"]),
                        "sot_faced": int(r["sot_faced"]),
                    }
                    for r in alag
                ],
            }
        )

    payload = {
        "schema_version": 2,
        "source": "understat.com",
        "built_at_utc": now_utc(),
        "default_season": "2026-2027",
        "default_metric": "xg",
        "default_view": "treemap",
        "metric_labels": {
            "xg": "xG",
            "shots": "Shots",
            "sot": "Shots on target",
            "cc": "Chances created",
            "cc_xg": "xG assisted",
        },
        "situation_order": situations,
        "last_action_group_order": LAST_ACTION_GROUP_ORDER,
        "notes": {
            "source": "Shot model metrics from Understat (not Opta / FPL expected_goals).",
            "sot": "On target = Goal + SavedShot + ShotOnPost. Blocked shots are excluded.",
            "cc": "Chances created = shot preceded by this player as player_assisted (passer before the shot).",
            "per90_team": "Team per-90 uses finished matches (metric ÷ matches).",
            "per90_player": "Player per-90 uses Understat season minutes when available.",
            "display": "Team header shows metric plus S (shots) and SoT (on target).",
            "views": "Treemap = players in team. Matrices = situation / last-action creation and defensive concede.",
        },
        "last_action_groups": groups_for_site(),
        "seasons": sorted({t["season"] for t in teams_out}),
        "teams": teams_out,
    }
    _write_json(SERVING_DIR / "us_shot_treemap.json", payload)
    return payload
