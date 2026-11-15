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
        if ev.get("is_result") is False:
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
    seen_club_code: set[tuple[int, int]] = set()
    for r in fpl_rows:
        code = r.get("player_code")
        if code is None or int(code) in used_codes:
            continue
        tc = r.get("team_code")
        if tc is None:
            continue
        key = (int(tc), int(code))
        if key in seen_club_code:
            continue
        seen_club_code.add(key)
        rec = {
            **r,
            "norm": normalize_name(r.get("full_name") or r.get("web_name")),
            "last": last_name(r.get("full_name") or r.get("web_name")),
            "ini": first_initial(r.get("full_name") or r.get("web_name")),
            "webk": web_name_key(r.get("web_name")),
            "fullk": normalize_name(r.get("full_name")),
        }
        by_club.setdefault(int(tc), []).append(rec)

    unmatched = []
    ambiguous = []
    for row in ss_players.iter_rows(named=True):
        sid = str(row.get("player_id") or "")
        if not sid or sid in used_ss:
            continue
        name = row.get("player_name")
        tc = row.get("team_code")
        raw_pool = by_club.get(int(tc), []) if tc is not None else []
        pool = [p for p in raw_pool if int(p["player_code"]) not in used_codes]
        nn = normalize_name(name)
        last = last_name(name)
        ini = first_initial(name)
        exact = _unique_codes([p for p in pool if p["norm"] == nn or p["webk"] == nn or p.get("fullk") == nn])
        if len(exact) == 1:
            p = exact[0]
            accepted.append(_acc(sid, p, name, tc, "exact_name", 100.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        li = _unique_codes([p for p in pool if p["last"] == last and p["ini"] == ini and last])
        if len(li) == 1:
            p = li[0]
            accepted.append(_acc(sid, p, name, tc, "last_initial", 99.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        extra = _unique_codes(
            [
                p
                for p in pool
                if nn
                and (
                    (p.get("fullk") or "").startswith(nn + " ")
                    or (p.get("norm") or "").startswith(nn + " ")
                    or nn.startswith((p.get("fullk") or "") + " ")
                )
            ]
        )
        if len(extra) == 1:
            p = extra[0]
            accepted.append(_acc(sid, p, name, tc, "extra_surname", 98.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        ss_tok = set(nn.split())
        swapped = _unique_codes(
            [p for p in pool if ss_tok and set((p.get("fullk") or p["norm"] or "").split()) == ss_tok]
        )
        if len(swapped) == 1:
            p = swapped[0]
            accepted.append(_acc(sid, p, name, tc, "token_set", 98.0, row.get("season")))
            used_ss.add(sid)
            used_codes.add(int(p["player_code"]))
            continue
        scored = []
        seen_sc = set()
        for p in pool:
            pc = int(p["player_code"])
            if pc in seen_sc:
                continue
            sc = max(fuzz.ratio(nn, p["norm"]), fuzz.ratio(nn, p["webk"]), fuzz.ratio(nn, p.get("fullk") or ""))
            if sc >= FUZZY_AUTO_MIN:
                seen_sc.add(pc)
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


def _unique_codes(rows: list[dict]) -> list[dict]:
    by: dict[int, dict] = {}
    for p in rows:
        by[int(p["player_code"])] = p
    return list(by.values())


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


WORKSHEET_COLS = (
    "sofascore_player_id",
    "sofascore_player_name",
    "sofascore_team_id",
    "sofascore_team_name",
    "fpl_team_code",
    "fpl_team_name",
    "fpl_team_short",
    "seasons",
    "ss_appearances",
    "ss_minutes",
    "ss_bcc",
    "ss_bcm",
    "map_status",
    "player_code",
    "fpl_element_id",
    "fpl_web_name",
    "fpl_full_name",
    "suggested_player_code",
    "suggested_method",
    "suggested_score",
    "understat_player_id",
    "understat_player_name",
    "cand2_player_code",
    "cand2_web_name",
    "cand2_full_name",
    "cand2_score",
    "cand2_understat_player_id",
    "cand3_player_code",
    "cand3_web_name",
    "cand3_full_name",
    "cand3_score",
    "cand3_understat_player_id",
    "notes",
)


def load_worksheet_overrides() -> pl.DataFrame:
    """Rows where the user filled player_code on the mapping worksheet."""
    path = REVIEW_DIR / "player_mapping_worksheet.csv"
    if not path.exists():
        return pl.DataFrame({c: [] for c in PLAYER_MAP_COLS})
    df = pl.read_csv(path, infer_schema_length=4000)
    if df.is_empty() or "player_code" not in df.columns:
        return pl.DataFrame({c: [] for c in PLAYER_MAP_COLS})
    filled = df.filter(pl.col("player_code").is_not_null())
    if filled.is_empty():
        return pl.DataFrame({c: [] for c in PLAYER_MAP_COLS})
    rows = []
    for row in filled.iter_rows(named=True):
        sid = str(row.get("sofascore_player_id") or "")
        try:
            code = int(row["player_code"])
        except (TypeError, ValueError):
            continue
        if not sid:
            continue
        rows.append(
            {
                "sofascore_player_id": sid,
                "player_code": code,
                "player_name": row.get("sofascore_player_name"),
                "web_name": row.get("fpl_web_name"),
                "fpl_full_name": row.get("fpl_full_name"),
                "team_code": row.get("fpl_team_code"),
                "seasons": row.get("seasons"),
                "method": "override",
                "score": 100.0,
                "status": "accepted",
                "notes": "worksheet",
            }
        )
    return pl.DataFrame(rows) if rows else pl.DataFrame({c: [] for c in PLAYER_MAP_COLS})


def combine_player_overrides(file_overrides: pl.DataFrame, worksheet: pl.DataFrame) -> pl.DataFrame:
    """File overrides win when both name the same SofaScore id."""
    parts = [d for d in (file_overrides, worksheet) if d is not None and d.height]
    if not parts:
        return pl.DataFrame({c: [] for c in PLAYER_MAP_COLS})
    out = pl.concat(parts, how="diagonal_relaxed")
    if "sofascore_player_id" not in out.columns:
        return out
    return out.unique(subset=["sofascore_player_id"], keep="first")


def persist_worksheet_overrides(file_overrides: pl.DataFrame, worksheet: pl.DataFrame) -> pl.DataFrame:
    """Keep worksheet fills in player_overrides.csv so the next rebuild does not depend on the queue file."""
    from pipeline.pl_merge.io_csv import write_csv

    have = set()
    if file_overrides.height and "sofascore_player_id" in file_overrides.columns:
        have = {str(x) for x in file_overrides["sofascore_player_id"].to_list() if x is not None}
    add = []
    if worksheet.height:
        for row in worksheet.iter_rows(named=True):
            sid = str(row.get("sofascore_player_id") or "")
            if not sid or sid in have:
                continue
            add.append({c: row.get(c) for c in PLAYER_MAP_COLS})
    if not add:
        return file_overrides
    extra = pl.DataFrame(add)
    merged = pl.concat([file_overrides, extra], how="diagonal_relaxed") if file_overrides.height else extra
    write_csv(MAPS_DIR / "player_overrides.csv", merged.select(list(PLAYER_MAP_COLS)))
    return merged


def _understat_by_code() -> dict[int, dict]:
    from pipeline.pl_merge.config import MAPS_DIR as PL_MERGE_MAPS_DIR

    path = PL_MERGE_MAPS_DIR / "player_map.csv"
    if not path.exists():
        return {}
    df = pl.read_csv(path)
    if df.is_empty() or "player_code" not in df.columns:
        return {}
    if "status" in df.columns:
        df = df.filter(pl.col("status") == "accepted")
    out: dict[int, dict] = {}
    for row in df.iter_rows(named=True):
        code = row.get("player_code")
        if code is None:
            continue
        out[int(code)] = {
            "understat_player_id": row.get("understat_player_id"),
            "understat_player_name": row.get("player_name") or row.get("web_name"),
        }
    return out


def _fpl_index(fpl_players: pl.DataFrame) -> tuple[dict[int, list[dict]], dict[int, dict]]:
    by_club: dict[int, list[dict]] = {}
    by_code: dict[int, dict] = {}
    seen: set[tuple[int, int]] = set()
    if fpl_players.is_empty():
        return by_club, by_code
    for r in fpl_players.iter_rows(named=True):
        code = r.get("player_code")
        tc = r.get("team_code")
        if code is None or tc is None:
            continue
        rec = {
            **r,
            "norm": normalize_name(r.get("full_name") or r.get("web_name")),
            "last": last_name(r.get("full_name") or r.get("web_name")),
            "ini": first_initial(r.get("full_name") or r.get("web_name")),
            "webk": web_name_key(r.get("web_name")),
            "fullk": normalize_name(r.get("full_name")),
        }
        by_code[int(code)] = rec
        key = (int(tc), int(code))
        if key in seen:
            continue
        seen.add(key)
        by_club.setdefault(int(tc), []).append(rec)
    return by_club, by_code


def _rank_club_candidates(name: str | None, pool: list[dict], *, top: int = 3) -> list[tuple[float, dict, str]]:
    nn = normalize_name(name)
    last = last_name(name)
    ini = first_initial(name)
    scored: list[tuple[float, dict, str]] = []
    seen: set[int] = set()
    for p in pool:
        pc = int(p["player_code"])
        if pc in seen:
            continue
        seen.add(pc)
        if p["norm"] == nn or p["webk"] == nn or p.get("fullk") == nn:
            scored.append((100.0, p, "exact_name"))
            continue
        if last and p["last"] == last and p["ini"] == ini:
            scored.append((99.0, p, "last_initial"))
            continue
        fk = p.get("fullk") or ""
        if nn and (fk.startswith(nn + " ") or (p.get("norm") or "").startswith(nn + " ") or nn.startswith(fk + " ")):
            scored.append((98.0, p, "extra_surname"))
            continue
        if nn and set(nn.split()) == set(fk.split()):
            scored.append((98.0, p, "token_set"))
            continue
        sc = max(fuzz.ratio(nn, p["norm"]), fuzz.ratio(nn, p["webk"]), fuzz.ratio(nn, p.get("fullk") or ""))
        scored.append((float(sc), p, "fuzzy"))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def write_player_mapping_worksheet(
    *,
    unmatched: pl.DataFrame,
    ambiguous: pl.DataFrame,
    ss_detail: pl.DataFrame,
    fpl_players: pl.DataFrame,
    team_map: pl.DataFrame,
) -> pl.DataFrame:
    """One row per unmapped/ambiguous SofaScore player, with FPL + Understat ids to fill player_code."""
    from pipeline.pl_merge.io_csv import write_csv

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    prev_path = REVIEW_DIR / "player_mapping_worksheet.csv"
    prev_codes: dict[str, object] = {}
    if prev_path.exists():
        prev = pl.read_csv(prev_path, infer_schema_length=4000)
        if prev.height and "player_code" in prev.columns:
            for row in prev.iter_rows(named=True):
                if row.get("player_code") is not None and row.get("sofascore_player_id") is not None:
                    prev_codes[str(row["sofascore_player_id"])] = row["player_code"]

    queue: list[dict] = []
    if unmatched.height:
        for row in unmatched.iter_rows(named=True):
            queue.append({**row, "map_status": "unmapped"})
    if ambiguous.height:
        for row in ambiguous.iter_rows(named=True):
            queue.append(
                {
                    "sofascore_player_id": row.get("sofascore_player_id"),
                    "player_name": row.get("player_name"),
                    "team_code": row.get("team_code"),
                    "season": None,
                    "map_status": "ambiguous",
                    "notes": f"auto-match candidates={row.get('candidates')}",
                }
            )
    if not queue:
        empty = pl.DataFrame({c: [] for c in WORKSHEET_COLS})
        write_csv(prev_path, empty)
        return empty

    detail_by_id: dict[str, dict] = {}
    if ss_detail.height:
        for row in ss_detail.iter_rows(named=True):
            detail_by_id[str(row.get("player_id"))] = row

    team_by_code: dict[int, dict] = {}
    team_by_ss: dict[str, dict] = {}
    if team_map.height:
        for row in team_map.iter_rows(named=True):
            if row.get("team_code") is not None:
                team_by_code[int(row["team_code"])] = row
            if row.get("sofascore_team_id") is not None:
                team_by_ss[str(row["sofascore_team_id"])] = row

    by_club, by_code = _fpl_index(fpl_players)
    us_by_code = _understat_by_code()

    rows = []
    for item in queue:
        sid = str(item.get("sofascore_player_id") or "")
        det = detail_by_id.get(sid, {})
        name = item.get("player_name") or det.get("player_name")
        tc = item.get("team_code") if item.get("team_code") is not None else det.get("team_code")
        ss_team_id = det.get("team_id")
        tss = team_by_ss.get(str(ss_team_id) if ss_team_id is not None else "") or {}
        tfpl = team_by_code.get(int(tc) if tc is not None else -1) or {}
        pool = by_club.get(int(tc), []) if tc is not None else []
        cands = _rank_club_candidates(name, pool, top=3)
        top = cands[0] if cands else None
        c2 = cands[1] if len(cands) > 1 else None
        c3 = cands[2] if len(cands) > 2 else None

        def _cand_us(c):
            empty = (None, None, None, None, None, None, None, None)
            if not c:
                return empty
            sc, p, method = c
            us = us_by_code.get(int(p["player_code"]), {})
            return (
                int(p["player_code"]),
                p.get("web_name"),
                p.get("full_name") or p.get("web_name"),
                sc,
                method,
                us.get("understat_player_id"),
                us.get("understat_player_name"),
                p.get("player_id"),
            )

        s_code, s_web, s_full, s_score, s_method, s_us, s_usn, s_eid = _cand_us(top)
        c2_code, c2_web, c2_full, c2_score, _, c2_us, _, _ = _cand_us(c2)
        c3_code, c3_web, c3_full, c3_score, _, c3_us, _, _ = _cand_us(c3)
        filled = prev_codes.get(sid)
        rows.append(
            {
                "sofascore_player_id": sid,
                "sofascore_player_name": name,
                "sofascore_team_id": ss_team_id,
                "sofascore_team_name": tss.get("sofascore_name") or det.get("sofascore_team_name"),
                "fpl_team_code": int(tc) if tc is not None else None,
                "fpl_team_name": tfpl.get("fpl_name"),
                "fpl_team_short": tfpl.get("fpl_short"),
                "seasons": det.get("seasons") or item.get("season"),
                "ss_appearances": det.get("ss_appearances"),
                "ss_minutes": det.get("ss_minutes"),
                "ss_bcc": det.get("ss_bcc"),
                "ss_bcm": det.get("ss_bcm"),
                "map_status": item.get("map_status"),
                "player_code": filled,
                "fpl_element_id": s_eid,
                "fpl_web_name": s_web,
                "fpl_full_name": s_full,
                "suggested_player_code": s_code,
                "suggested_method": s_method,
                "suggested_score": s_score,
                "understat_player_id": s_us,
                "understat_player_name": s_usn,
                "cand2_player_code": c2_code,
                "cand2_web_name": c2_web,
                "cand2_full_name": c2_full,
                "cand2_score": c2_score,
                "cand2_understat_player_id": c2_us,
                "cand3_player_code": c3_code,
                "cand3_web_name": c3_web,
                "cand3_full_name": c3_full,
                "cand3_score": c3_score,
                "cand3_understat_player_id": c3_us,
                "notes": item.get("notes") or "Fill player_code (FPL code) then rebuild maps. Leave blank if unknown.",
            }
        )
    out = pl.DataFrame(rows).select(list(WORKSHEET_COLS)).sort(["fpl_team_short", "sofascore_player_name"])
    write_csv(prev_path, out)
    return out
