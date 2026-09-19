"""Understat match_id → FPL match_id + gw (Premier League only)."""

from __future__ import annotations

from datetime import date

import polars as pl

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR
from pipeline.pl_merge.config import MATCH_OVERRIDE_COLS, PREMIER_LEAGUE
from pipeline.pl_merge.io_csv import ensure_csv, write_csv
from pipeline.understat.maps import load_team_map


def _date_str(value: str | None) -> str | None:
    if not value:
        return None
    s = str(value).strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    return None


def _parse_date(value: str | None) -> date | None:
    s = _date_str(value)
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def load_fpl_pl_fixtures(seasons: list[str]) -> pl.DataFrame:
    parts: list[pl.DataFrame] = []
    for season in seasons:
        path = (
            FPL_MASTER_DIR
            / "team_match"
            / f"season={season}"
            / f"competition={PREMIER_LEAGUE}"
            / "part.parquet"
        )
        if path.exists():
            parts.append(pl.read_parquet(path))
    if not parts:
        return pl.DataFrame()
    tm = pl.concat(parts, how="diagonal_relaxed")
    home = tm.filter(pl.col("is_home")) if "is_home" in tm.columns else tm
    kick = (
        pl.when(pl.col("kickoff_utc").is_not_null() & (pl.col("kickoff_utc").cast(pl.Utf8) != ""))
        .then(pl.col("kickoff_utc").cast(pl.Utf8))
        .otherwise(pl.col("kickoff_raw").cast(pl.Utf8))
        if "kickoff_raw" in home.columns
        else pl.col("kickoff_utc").cast(pl.Utf8)
    )
    return (
        home.select(
            "season",
            "gw",
            "match_id",
            "team_code",
            "opponent_code",
            "finished",
            kick.alias("kickoff"),
        )
        .with_columns(
            pl.col("match_id").cast(pl.Utf8),
            pl.col("team_code").cast(pl.Int64).alias("home_code"),
            pl.col("opponent_code").cast(pl.Int64).alias("away_code"),
            pl.col("gw").cast(pl.Int64),
            pl.col("kickoff").map_elements(_date_str, return_dtype=pl.Utf8).alias("kick_date"),
        )
        .select("season", "gw", "match_id", "home_code", "away_code", "finished", "kick_date", "kickoff")
        .unique(subset=["match_id"])
        .rename({"match_id": "fpl_match_id"})
    )


def _us_fixtures(matches: pl.DataFrame, team_map: pl.DataFrame) -> pl.DataFrame:
    tm = team_map.select(
        pl.col("understat_team_id").cast(pl.Utf8).alias("uid"),
        pl.col("team_code").cast(pl.Int64),
        pl.col("understat_title"),
    )
    home = tm.rename({"uid": "home_team_id", "team_code": "home_code", "understat_title": "home_team"})
    away = tm.rename({"uid": "away_team_id", "team_code": "away_code", "understat_title": "away_team"})
    return (
        matches.select("match_id", "season", "kickoff_raw", "home_team_id", "away_team_id", "is_result")
        .with_columns(
            pl.col("match_id").cast(pl.Utf8),
            pl.col("home_team_id").cast(pl.Utf8),
            pl.col("away_team_id").cast(pl.Utf8),
        )
        .join(home.select("home_team_id", "home_code", "home_team"), on="home_team_id", how="left")
        .join(away.select("away_team_id", "away_code", "away_team"), on="away_team_id", how="left")
        .with_columns(
            pl.col("kickoff_raw").map_elements(_date_str, return_dtype=pl.Utf8).alias("kick_date")
        )
        .rename({"match_id": "understat_match_id"})
    )


def pair_matches(
    us: pl.DataFrame,
    fpl: pl.DataFrame,
    overrides: pl.DataFrame | None = None,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    mapped_rows: list[dict] = []
    used_us: set[str] = set()
    used_fpl: set[str] = set()
    if overrides is None:
        overrides = pl.DataFrame()

    if not overrides.is_empty():
        ov = overrides.with_columns(
            pl.col("understat_match_id").cast(pl.Utf8),
            pl.col("fpl_match_id").cast(pl.Utf8),
        )
        fpl_idx = {r["fpl_match_id"]: r for r in fpl.iter_rows(named=True)}
        us_idx = {r["understat_match_id"]: r for r in us.iter_rows(named=True)}
        for row in ov.iter_rows(named=True):
            uid, fid = row["understat_match_id"], row["fpl_match_id"]
            if not uid or not fid:
                continue
            u = us_idx.get(uid, {})
            f = fpl_idx.get(fid, {})
            mapped_rows.append(
                {
                    "understat_match_id": uid,
                    "fpl_match_id": fid,
                    "season": f.get("season") or u.get("season"),
                    "gw": f.get("gw"),
                    "home_code": f.get("home_code") or u.get("home_code"),
                    "away_code": f.get("away_code") or u.get("away_code"),
                    "kick_date": f.get("kick_date") or u.get("kick_date"),
                    "method": "override",
                    "reason": row.get("reason"),
                }
            )
            used_us.add(uid)
            used_fpl.add(fid)

    fpl_by_key: dict[tuple, list[dict]] = {}
    for row in fpl.iter_rows(named=True):
        if row["fpl_match_id"] in used_fpl:
            continue
        key = (row["season"], row["kick_date"], row["home_code"], row["away_code"])
        fpl_by_key.setdefault(key, []).append(row)

    unmatched_us: list[dict] = []
    for u in us.iter_rows(named=True):
        uid = u["understat_match_id"]
        if uid in used_us:
            continue
        if u.get("home_code") is None or u.get("away_code") is None:
            unmatched_us.append({**u, "reason": "unmapped_team"})
            continue
        key = (u["season"], u["kick_date"], u["home_code"], u["away_code"])
        hits = [h for h in fpl_by_key.get(key, []) if h["fpl_match_id"] not in used_fpl]
        if len(hits) == 1:
            h = hits[0]
            mapped_rows.append(
                {
                    "understat_match_id": uid,
                    "fpl_match_id": h["fpl_match_id"],
                    "season": h["season"],
                    "gw": h["gw"],
                    "home_code": h["home_code"],
                    "away_code": h["away_code"],
                    "kick_date": h["kick_date"],
                    "method": "date_teams",
                    "reason": None,
                }
            )
            used_us.add(uid)
            used_fpl.add(h["fpl_match_id"])
            continue
        if len(hits) > 1:
            unmatched_us.append({**u, "reason": "ambiguous_same_date"})
            continue
        unmatched_us.append(u)

    still: list[dict] = []
    for u in unmatched_us:
        if u.get("reason") in {"unmapped_team", "ambiguous_same_date"}:
            still.append(u)
            continue
        uid = u["understat_match_id"]
        ud = _parse_date(u.get("kick_date"))
        if ud is None or u.get("home_code") is None:
            still.append({**u, "reason": u.get("reason") or "no_kick_date"})
            continue
        candidates = []
        for f in fpl.iter_rows(named=True):
            if f["fpl_match_id"] in used_fpl:
                continue
            if f["season"] != u["season"]:
                continue
            if f["home_code"] != u["home_code"] or f["away_code"] != u["away_code"]:
                continue
            fd = _parse_date(f.get("kick_date"))
            if fd is None:
                continue
            delta = abs((fd - ud).days)
            if delta <= 1:
                candidates.append((delta, f))
        if len(candidates) == 1:
            f = candidates[0][1]
            mapped_rows.append(
                {
                    "understat_match_id": uid,
                    "fpl_match_id": f["fpl_match_id"],
                    "season": f["season"],
                    "gw": f["gw"],
                    "home_code": f["home_code"],
                    "away_code": f["away_code"],
                    "kick_date": f["kick_date"],
                    "method": "date_pm1",
                    "reason": None,
                }
            )
            used_us.add(uid)
            used_fpl.add(f["fpl_match_id"])
        elif len(candidates) > 1:
            still.append({**u, "reason": "ambiguous_date_pm1"})
        else:
            still.append({**u, "reason": u.get("reason") or "no_fpl_fixture"})

    mapped = pl.DataFrame(mapped_rows) if mapped_rows else pl.DataFrame(
        schema={
            "understat_match_id": pl.Utf8,
            "fpl_match_id": pl.Utf8,
            "season": pl.Utf8,
            "gw": pl.Int64,
            "home_code": pl.Int64,
            "away_code": pl.Int64,
            "kick_date": pl.Utf8,
            "method": pl.Utf8,
            "reason": pl.Utf8,
        }
    )
    unmatched = pl.DataFrame(still) if still else pl.DataFrame()
    return mapped, unmatched


def build_match_map(
    matches: pl.DataFrame,
    seasons: list[str],
    *,
    override_path,
    out_path,
    unmatched_path,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    overrides = ensure_csv(override_path, MATCH_OVERRIDE_COLS)
    team_map = load_team_map()
    us = _us_fixtures(matches, team_map)
    fpl = load_fpl_pl_fixtures(seasons)
    mapped, unmatched = pair_matches(us, fpl, overrides)
    write_csv(out_path, mapped.sort(["season", "gw", "understat_match_id"]) if mapped.height else mapped)
    write_csv(unmatched_path, unmatched)
    return mapped, unmatched
