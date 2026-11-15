"""Curated SofaScore ↔ FPL identity maps (separate from Understat / pl_merge)."""

from __future__ import annotations

from datetime import date

import polars as pl
from rapidfuzz import fuzz

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR, SOURCE_DIR
from pipeline.pl_merge.names import first_initial, last_name, normalize_name, web_name_key
from pipeline.sofascore.config import MAPS_DIR, REVIEW_DIR
from pipeline.transforms import normalize_players

PREMIER_LEAGUE = "Premier League"
FUZZY_AUTO_MIN = 95
TEAM_MAP_COLS = (
    "sofascore_team_id",
    "sofascore_name",
    "team_code",
    "fpl_name",
    "fpl_short",
    "notes",
)
MATCH_MAP_COLS = (
    "sofascore_event_id",
    "fpl_match_id",
    "season",
    "gw",
    "home_code",
    "away_code",
    "kick_date",
    "method",
    "reason",
)
PLAYER_MAP_COLS = (
    "sofascore_player_id",
    "player_code",
    "player_name",
    "web_name",
    "fpl_full_name",
    "team_code",
    "seasons",
    "method",
    "score",
    "status",
    "notes",
)


def _ensure(path, columns) -> pl.DataFrame:
    from pipeline.pl_merge.io_csv import ensure_csv

    return ensure_csv(path, columns)


def load_team_map() -> pl.DataFrame:
    path = MAPS_DIR / "team_map.csv"
    df = _ensure(path, TEAM_MAP_COLS)
    if df.is_empty():
        return df
    return df.with_columns(
        pl.col("sofascore_team_id").cast(pl.Utf8),
        pl.col("team_code").cast(pl.Int64),
    )


def _date_str(value: str | None) -> str | None:
    if not value:
        return None
    s = str(value).strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
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
        home.select("season", "gw", "match_id", "team_code", "opponent_code", "finished", kick.alias("kickoff"))
        .with_columns(
            pl.col("match_id").cast(pl.Utf8),
            pl.col("team_code").cast(pl.Int64).alias("home_code"),
            pl.col("opponent_code").cast(pl.Int64).alias("away_code"),
            pl.col("gw").cast(pl.Int64),
            pl.col("kickoff").map_elements(_date_str, return_dtype=pl.Utf8).alias("kick_date"),
        )
        .select("season", "gw", "match_id", "home_code", "away_code", "finished", "kick_date")
        .unique(subset=["match_id"])
        .rename({"match_id": "fpl_match_id"})
    )


def pair_matches(events: pl.DataFrame, fpl: pl.DataFrame, overrides: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    team_map = load_team_map()
    id_to_code = dict(
        zip(team_map["sofascore_team_id"].cast(pl.Utf8).to_list(), team_map["team_code"].cast(pl.Int64).to_list())
    )
    mapped: list[dict] = []
    used_ss: set[str] = set()
    used_fpl: set[str] = set()

    if not overrides.is_empty():
        for row in overrides.iter_rows(named=True):
            sid, fid = str(row.get("sofascore_event_id") or ""), str(row.get("fpl_match_id") or "")
            if not sid or not fid:
                continue
            mapped.append(
                {
                    "sofascore_event_id": sid,
                    "fpl_match_id": fid,
                    "season": row.get("season"),
                    "gw": row.get("gw"),
                    "home_code": row.get("home_code"),
                    "away_code": row.get("away_code"),
                    "kick_date": row.get("kick_date"),
                    "method": "override",
                    "reason": row.get("reason"),
                }
            )
            used_ss.add(sid)
            used_fpl.add(fid)

    fpl_by_key: dict[tuple, list[dict]] = {}
    for row in fpl.iter_rows(named=True):
        if row["fpl_match_id"] in used_fpl:
            continue
        key = (row["season"], row["kick_date"], row["home_code"], row["away_code"])
        fpl_by_key.setdefault(key, []).append(row)

    unmatched = []
    for ev in events.iter_rows(named=True):
        eid = str(ev.get("event_id") or "")
        if not eid or eid in used_ss:
            continue
        hc = id_to_code.get(str(ev.get("home_team_id")))
        ac = id_to_code.get(str(ev.get("away_team_id")))
        kd = ev.get("kick_date")
        season = ev.get("season")
        cands = fpl_by_key.get((season, kd, hc, ac), [])
        if not cands and kd and hc is not None and ac is not None:
            # ±1 day
            try:
                d0 = date.fromisoformat(kd)
            except ValueError:
                d0 = None
            if d0:
                for delta in (-1, 1):
                    alt = (d0.toordinal() + delta)
                    ds = date.fromordinal(alt).isoformat()
                    cands = fpl_by_key.get((season, ds, hc, ac), [])
                    if cands:
                        kd = ds
                        break
        if len(cands) == 1:
            f = cands[0]
            mapped.append(
                {
                    "sofascore_event_id": eid,
                    "fpl_match_id": f["fpl_match_id"],
                    "season": season,
                    "gw": f["gw"],
                    "home_code": hc,
                    "away_code": ac,
                    "kick_date": kd,
                    "method": "date_home_away",
                    "reason": None,
                }
            )
            used_ss.add(eid)
            used_fpl.add(f["fpl_match_id"])
        else:
            unmatched.append(
                {
                    "sofascore_event_id": eid,
                    "season": season,
                    "kick_date": kd,
                    "home_team_id": ev.get("home_team_id"),
                    "away_team_id": ev.get("away_team_id"),
                    "home_code": hc,
                    "away_code": ac,
                    "candidates": len(cands),
                }
            )
    return pl.DataFrame(mapped) if mapped else pl.DataFrame({c: [] for c in MATCH_MAP_COLS}), pl.DataFrame(unmatched)


def load_fpl_players(seasons: list[str]) -> pl.DataFrame:
    parts = []
    for season in seasons:
        path = SOURCE_DIR / "data" / season / "players.csv"
        if not path.exists():
            continue
        df = normalize_players(pl.read_csv(path)).with_columns(pl.lit(season).alias("season"))
        if "first_name" in df.columns:
            df = df.with_columns(
                (pl.col("first_name").fill_null("") + pl.lit(" ") + pl.col("second_name").fill_null(""))
                .str.strip_chars()
                .alias("full_name")
            )
        else:
            df = df.with_columns(pl.col("web_name").alias("full_name"))
        parts.append(df)
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed")


def pair_players(ss_players: pl.DataFrame, fpl_players: pl.DataFrame, overrides: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """Return accepted map, unmatched SS, ambiguous."""
    accepted: list[dict] = []
    used_codes: set[int] = set()
    used_ss: set[str] = set()

    if not overrides.is_empty():
        for row in overrides.iter_rows(named=True):
            sid = str(row.get("sofascore_player_id") or "")
            code = row.get("player_code")
            if not sid or code is None:
                continue
            accepted.append(
                {
                    "sofascore_player_id": sid,
                    "player_code": int(code),
                    "player_name": row.get("player_name"),
                    "web_name": row.get("web_name"),
                    "fpl_full_name": row.get("fpl_full_name"),
                    "team_code": row.get("team_code"),
                    "seasons": row.get("seasons"),
                    "method": "override",
                    "score": 100.0,
                    "status": "accepted",
                    "notes": row.get("reason") or row.get("notes"),
                }
            )
            used_ss.add(sid)
            used_codes.add(int(code))

    fpl_rows = list(fpl_players.iter_rows(named=True)) if fpl_players.height else []
    by_club: dict[int, list[dict]] = {}
    for r in fpl_rows:
        code = r.get("player_code")
        if code is None or int(code) in used_codes:
            continue
        tc = r.get("team_code")
        rec = {
            **r,
            "norm": normalize_name(r.get("web_name") or r.get("full_name")),
            "last": last_name(r.get("web_name") or r.get("full_name")),
            "ini": first_initial(r.get("full_name") or r.get("web_name")),
            "webk": web_name_key(r.get("web_name")),
        }
        if tc is not None:
            by_club.setdefault(int(tc), []).append(rec)

    unmatched = []
    ambiguous = []
    for row in ss_players.iter_rows(named=True):
        sid = str(row.get("player_id") or "")
        if not sid or sid in used_ss:
            continue
        name = row.get("player_name")
        tc = row.get("team_code")
        pool = by_club.get(int(tc), []) if tc is not None else []
        nn = normalize_name(name)
        last = last_name(name)
        ini = first_initial(name)
        exact = [p for p in pool if p["norm"] == nn or p["webk"] == nn]
        if len(exact) == 1:
            p = exact[0]
            accepted.append(_acc(sid, p, name, tc, "exact_name", 100.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        li = [p for p in pool if p["last"] == last and p["ini"] == ini and last]
        if len(li) == 1:
            p = li[0]
            accepted.append(_acc(sid, p, name, tc, "last_initial", 99.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        scored = []
        for p in pool:
            sc = max(fuzz.ratio(nn, p["norm"]), fuzz.ratio(nn, p["webk"]))
            if sc >= FUZZY_AUTO_MIN:
                scored.append((sc, p))
        scored.sort(key=lambda x: -x[0])
        if len(scored) == 1 or (len(scored) >= 2 and scored[0][0] - scored[1][0] >= 5):
            sc, p = scored[0]
            accepted.append(_acc(sid, p, name, tc, "fuzzy", float(sc), row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
        elif len(scored) >= 2:
            ambiguous.append({"sofascore_player_id": sid, "player_name": name, "team_code": tc, "candidates": len(scored)})
        else:
            unmatched.append({"sofascore_player_id": sid, "player_name": name, "team_code": tc, "season": row.get("season")})
    return (
        pl.DataFrame(accepted) if accepted else pl.DataFrame({c: [] for c in PLAYER_MAP_COLS}),
        pl.DataFrame(unmatched),
        pl.DataFrame(ambiguous),
    )


def _acc(sid, p, name, tc, method, score, season):
    return {
        "sofascore_player_id": sid,
        "player_code": int(p["player_code"]),
        "player_name": name,
        "web_name": p.get("web_name"),
        "fpl_full_name": p.get("full_name") or p.get("web_name"),
        "team_code": tc,
        "seasons": season,
        "method": method,
        "score": score,
        "status": "accepted",
        "notes": None,
    }
