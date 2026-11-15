"""SofaScore shot explore serving (treemap + situation matrices). No last-action."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path

import polars as pl

from pipeline.pl_merge.config import MASTER_DIR as PL_MERGE_MASTER_DIR
from pipeline.sofascore.config import MAPS_DIR, SERVING_DIR, SEASONS, SITUATION_ORDER, WEB_DATA_DIR
from pipeline.sofascore.ingest import read_master
from pipeline.sofascore.maps import load_team_map
from pipeline.sofascore.normalize import now_utc


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


def _fpl_minutes(fpl_seasons: list[str]) -> pl.DataFrame:
    parts = []
    for season in fpl_seasons:
        path = PL_MERGE_MASTER_DIR / "player_match" / f"season={season}" / "part.parquet"
        if path.exists():
            parts.append(pl.read_parquet(path))
    if not parts:
        return pl.DataFrame()
    merged = pl.concat(parts, how="diagonal_relaxed")
    return (
        merged.group_by("season", "team_code", "player_code")
        .agg(
            pl.col("minutes").sum().alias("minutes"),
            pl.col("match_id")
            .filter(pl.col("minutes").fill_null(0) > 0)
            .n_unique()
            .alias("games"),
        )
    )


def _player_map() -> pl.DataFrame:
    path = MAPS_DIR / "player_map.csv"
    if not path.exists():
        return pl.DataFrame()
    return (
        pl.read_csv(path)
        .filter(pl.col("status") == "accepted")
        .select(
            pl.col("sofascore_player_id").cast(pl.Utf8).alias("player_id"),
            pl.col("player_code").cast(pl.Int64),
            pl.col("web_name").alias("fpl_web_name"),
            pl.col("fpl_full_name"),
        )
        .unique(subset=["player_id"])
    )


def build_shot_treemap_serving(*, fpl_seasons: list[str] | None = None, top_players: int = 12) -> dict:
    fpl_seasons = fpl_seasons or list(SEASONS.keys())
    shots = read_master("shot", fpl_seasons)
    matches = read_master("event", fpl_seasons)
    lineups = read_master("player_match", fpl_seasons)
    if shots.is_empty():
        payload = {
            "schema_version": 1,
            "source": "sofascore.com",
            "built_at_utc": now_utc(),
            "teams": [],
            "notes": {"missing": "SofaScore shots not ingested yet"},
        }
        _write_json(SERVING_DIR / "ss_shot_treemap.json", payload)
        return payload

    team_map = load_team_map().filter(pl.col("team_code").is_not_null()).select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_name").alias("team"),
        pl.col("fpl_short").alias("team_short"),
    )
    identity = _player_map()
    minutes = _fpl_minutes(fpl_seasons)

    s = (
        shots.with_columns(pl.col("team_id").cast(pl.Utf8), pl.col("player_id").cast(pl.Utf8))
        .join(team_map, on="team_id", how="left")
        .join(identity, on="player_id", how="left")
        .filter(pl.col("team_code").is_not_null() & pl.col("player_code").is_not_null())
    )
    if s.is_empty():
        payload = {
            "schema_version": 1,
            "source": "sofascore.com",
            "built_at_utc": now_utc(),
            "teams": [],
            "notes": {"missing": "SofaScore shots did not join FPL team/player maps"},
        }
        _write_json(SERVING_DIR / "ss_shot_treemap.json", payload)
        return payload

    finished = matches.filter(pl.col("is_result")) if matches.height else matches
    team_matches = pl.DataFrame()
    if finished.height:
        home = finished.select("season", pl.col("home_team_id").cast(pl.Utf8).alias("team_id"), "event_id")
        away = finished.select("season", pl.col("away_team_id").cast(pl.Utf8).alias("team_id"), "event_id")
        team_matches = (
            pl.concat([home, away])
            .join(team_map, on="team_id", how="left")
            .filter(pl.col("team_code").is_not_null())
            .group_by(["season", "team_code"])
            .agg(pl.col("event_id").n_unique().alias("matches"))
        )

    xa_src = pl.DataFrame()
    if lineups.height and identity.height:
        xa_src = (
            lineups.with_columns(pl.col("player_id").cast(pl.Utf8), pl.col("team_id").cast(pl.Utf8))
            .join(identity, on="player_id", how="left")
            .join(team_map, on="team_id", how="left")
            .filter(pl.col("player_code").is_not_null() & pl.col("team_code").is_not_null())
            .group_by(["season", "team_code", "player_code"])
            .agg(pl.col("expected_assists").sum().alias("xa"))
        )

    player_sit = s.group_by(["season", "team_code", "player_id", "situation"]).agg(
        pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot")
    )
    player_matches = s.group_by(["season", "team_code", "player_code"]).agg(
        pl.col("event_id").n_unique().alias("shot_matches")
    )
    taker = (
        s.group_by(["season", "team_code", "team", "team_short", "player_id", "player_code", "player_name", "fpl_web_name"])
        .agg(
            pl.col("xg").sum().alias("xg"),
            pl.len().alias("shots"),
            pl.col("is_sot").sum().alias("sot"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
        )
        .join(minutes, on=["season", "team_code", "player_code"], how="left")
        .join(player_matches, on=["season", "team_code", "player_code"], how="left")
    )
    if xa_src.height:
        taker = taker.join(xa_src, on=["season", "team_code", "player_code"], how="left")
    else:
        taker = taker.with_columns(pl.lit(None).cast(pl.Float64).alias("xa"))
    taker = taker.with_columns(_p90("xg"), _p90("shots"), _p90("sot"), _p90("goals"), _p90("xa"))

    team_agg = (
        s.group_by(["season", "team_code", "team", "team_short"])
        .agg(
            pl.col("xg").sum().alias("xg"),
            pl.len().alias("shots"),
            pl.col("is_sot").sum().alias("sot"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
        )
        .join(team_matches, on=["season", "team_code"], how="left")
        .with_columns(
            pl.when(pl.col("matches") > 0).then(pl.col("xg") / pl.col("matches")).otherwise(None).alias("xg_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("shots") / pl.col("matches")).otherwise(None).alias("shots_p90"),
            pl.when(pl.col("matches") > 0).then(pl.col("sot") / pl.col("matches")).otherwise(None).alias("sot_p90"),
        )
    )
    for_sit = s.group_by(["season", "team_code", "situation"]).agg(
        pl.col("xg").sum().alias("xg"), pl.len().alias("shots"), pl.col("is_sot").sum().alias("sot")
    )
    against = (
        s.select("season", "situation", "xg", "is_sot", pl.col("opponent_id").cast(pl.Utf8).alias("team_id"))
        .join(team_map, on="team_id", how="left")
        .filter(pl.col("team_code").is_not_null())
    )
    ag_sit = against.group_by(["season", "team_code", "situation"]).agg(
        pl.col("xg").sum().alias("xga"),
        pl.len().alias("shots_faced"),
        pl.col("is_sot").sum().alias("sot_faced"),
    )
    situations = [x for x in SITUATION_ORDER if x in set(s["situation"].drop_nulls().unique().to_list())]
    extra = sorted(set(s["situation"].drop_nulls().unique().to_list()) - set(situations))
    situations = situations + extra

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
            "player_code": p.get("player_code"),
            "player_name": p.get("fpl_web_name") or html.unescape(p.get("player_name") or "") or None,
            "xg": _round(p.get("xg") or 0),
            "shots": int(p.get("shots") or 0),
            "sot": int(p.get("sot") or 0),
            "goals": int(p.get("goals") or 0),
            "cc": None,
            "cc_xg": None,
            "xa": _round(p.get("xa")),
            "xa_p90": _round(p.get("xa_p90")),
            "minutes": _round(mins, 1),
            "matches": int(matches) if matches is not None else None,
            "mins_per90": _round(mins_per90, 1),
            "xg_p90": _round(p.get("xg_p90")),
            "shots_p90": _round(p.get("shots_p90")),
            "sot_p90": _round(p.get("sot_p90")),
        }

    teams_out: list[dict] = []
    for t in team_agg.sort(["season", "xg"], descending=[False, True]).to_dicts():
        season, code = t["season"], t["team_code"]
        plist = (
            taker.filter((pl.col("season") == season) & (pl.col("team_code") == code))
            .sort("xg", descending=True)
            .head(top_players)
            .to_dicts()
        )
        by_id = {p.get("player_id"): clean_player(p) for p in plist if p.get("player_id")}
        for pid, row in by_id.items():
            sit_rows = (
                player_sit.filter(
                    (pl.col("season") == season) & (pl.col("team_code") == code) & (pl.col("player_id") == pid)
                ).to_dicts()
                if player_sit.height
                else []
            )
            row["by_situation"] = [
                {"situation": r["situation"], "xg": _round(r["xg"]), "shots": int(r["shots"]), "sot": int(r["sot"])}
                for r in sit_rows
            ]
            row["by_last_action_group"] = []
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
                "xg_p90": _round(t.get("xg_p90")),
                "shots_p90": _round(t.get("shots_p90")),
                "sot_p90": _round(t.get("sot_p90")),
                "players": list(by_id.values()),
                "by_situation": [
                    {"situation": r["situation"], "xg": _round(r["xg"]), "shots": int(r["shots"]), "sot": int(r["sot"])}
                    for r in for_sit.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()
                ],
                "by_last_action_group": [],
                "against_situation": [
                    {
                        "situation": r["situation"],
                        "xga": _round(r["xga"]),
                        "shots_faced": int(r["shots_faced"]),
                        "sot_faced": int(r["sot_faced"]),
                    }
                    for r in ag_sit.filter((pl.col("season") == season) & (pl.col("team_code") == code)).to_dicts()
                ],
                "against_last_action_group": [],
            }
        )

    payload = {
        "schema_version": 1,
        "source": "sofascore.com",
        "built_at_utc": now_utc(),
        "default_season": "2026-2027" if "2026-2027" in (fpl_seasons or []) else (fpl_seasons[-1] if fpl_seasons else None),
        "default_metric": "xg",
        "default_view": "treemap",
        "metric_labels": {
            "xg": "xG",
            "shots": "Shots",
            "sot": "Shots on target",
            "xa": "xA_sf",
        },
        "situation_order": situations,
        "last_action_group_order": [],
        "notes": {
            "source": "Shot model metrics from SofaScore (not Understat / Opta / FPL expected_goals).",
            "sot": "On target = goal + save + post. Own goals excluded.",
            "xa": "xA_sf is lineup expectedAssists (match totals), not per-shot assister.",
            "per90_player": "Player per-90 uses FPL/Opta Premier League minutes after player_code map.",
            "situations": "Native SofaScore situation labels. Penalty shots are only in the penalty slice.",
        },
        "seasons": sorted({t["season"] for t in teams_out}),
        "teams": teams_out,
    }
    _write_json(SERVING_DIR / "ss_shot_treemap.json", payload)
    return payload
