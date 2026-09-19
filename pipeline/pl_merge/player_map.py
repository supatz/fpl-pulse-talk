"""Understat player_id → FPL player_code. Fuzzy is a proposal; overrides win."""

from __future__ import annotations

from collections import defaultdict

import polars as pl
from rapidfuzz import fuzz

from pipeline.config import SOURCE_DIR
from pipeline.pl_merge.config import (
    FUZZY_AMBIGUOUS_MIN,
    FUZZY_AUTO_MIN,
    PLAYER_OVERRIDE_COLS,
    PREMIER_LEAGUE,
)
from pipeline.pl_merge.io_csv import ensure_csv, write_csv
from pipeline.pl_merge.names import (
    first_initial,
    full_name,
    last_name,
    normalize_name,
    web_name_key,
)
from pipeline.transforms import normalize_players
from pipeline.understat.maps import load_team_map

from pipeline.config import MASTER_DIR as FPL_MASTER_DIR


def load_fpl_players(seasons: list[str]) -> pl.DataFrame:
    parts: list[pl.DataFrame] = []
    for season in seasons:
        path = SOURCE_DIR / "data" / season / "players.csv"
        if not path.exists():
            continue
        raw = pl.read_csv(path)
        dims = normalize_players(raw).with_columns(pl.lit(season).alias("season"))
        parts.append(dims)
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed")


def load_fpl_pl_minutes(seasons: list[str]) -> pl.DataFrame:
    parts: list[pl.DataFrame] = []
    for season in seasons:
        path = (
            FPL_MASTER_DIR
            / "player_match"
            / f"season={season}"
            / f"competition={PREMIER_LEAGUE}"
            / "part.parquet"
        )
        if path.exists():
            df = pl.read_parquet(path)
            keep = [c for c in ("player_code", "season", "minutes", "web_name", "team_code") if c in df.columns]
            parts.append(df.select(keep))
    if not parts:
        return pl.DataFrame()
    pm = pl.concat(parts, how="diagonal_relaxed")
    return (
        pm.group_by("player_code", "season")
        .agg(
            pl.col("minutes").sum().alias("pl_minutes"),
            pl.col("web_name").first(),
            pl.col("team_code").last(),
        )
    )


def _team_title_to_code() -> dict[str, int]:
    m = load_team_map()
    out: dict[str, int] = {}
    for row in m.iter_rows(named=True):
        code = int(row["team_code"])
        for key in (row.get("understat_title"), row.get("fpl_name"), row.get("fpl_short")):
            if key:
                out[str(key).strip().lower()] = code
    return out


def understat_player_teams(roster: pl.DataFrame, league_player: pl.DataFrame) -> pl.DataFrame:
    """Stable understat player_id with names and FPL team_code set (from roster + league_player)."""
    team_map = load_team_map()
    id_to_code = dict(
        zip(team_map["understat_team_id"].cast(pl.Utf8).to_list(), team_map["team_code"].cast(pl.Int64).to_list())
    )
    title_to_code = _team_title_to_code()
    by_id: dict[str, dict] = {}

    def _touch(pid: str, name: str | None, season: str | None, codes: list[int]):
        if not pid:
            return
        rec = by_id.setdefault(
            pid,
            {"understat_player_id": pid, "player_name": name, "seasons": set(), "team_codes": set()},
        )
        if name and not rec.get("player_name"):
            rec["player_name"] = name
        elif name:
            rec["player_name"] = name
        if season:
            rec["seasons"].add(season)
        rec["team_codes"].update(c for c in codes if c is not None)

    if roster is not None and not roster.is_empty():
        for row in roster.iter_rows(named=True):
            pid = str(row.get("player_id") or "")
            tid = str(row.get("team_id") or "")
            code = id_to_code.get(tid)
            _touch(pid, row.get("player_name"), row.get("season"), [code] if code is not None else [])

    if league_player is not None and not league_player.is_empty():
        for row in league_player.iter_rows(named=True):
            pid = str(row.get("player_id") or "")
            titles = str(row.get("team_title") or "")
            codes = []
            for part in titles.split(","):
                code = title_to_code.get(part.strip().lower())
                if code is not None:
                    codes.append(code)
            _touch(pid, row.get("player_name"), row.get("season"), codes)

    rows = []
    for rec in by_id.values():
        rows.append(
            {
                "understat_player_id": rec["understat_player_id"],
                "player_name": rec["player_name"],
                "seasons": ",".join(sorted(rec["seasons"])),
                "team_codes": ",".join(str(c) for c in sorted(rec["team_codes"])),
            }
        )
    return pl.DataFrame(rows) if rows else pl.DataFrame()


def _fpl_index(players: pl.DataFrame) -> list[dict]:
    out = []
    for row in players.iter_rows(named=True):
        fn = full_name(row.get("first_name"), row.get("second_name"))
        out.append(
            {
                **row,
                "full_name": fn,
                "norm_full": normalize_name(fn),
                "norm_web": web_name_key(row.get("web_name")),
                "last": last_name(fn or row.get("web_name")),
                "initial": first_initial(fn) or first_initial(row.get("web_name")),
                "player_code": int(row["player_code"]) if row.get("player_code") is not None else None,
                "team_code": int(row["team_code"]) if row.get("team_code") is not None else None,
                "season": row.get("season"),
            }
        )
    return out


def _score_pair(us_name: str, cand: dict) -> tuple[str, float]:
    us_norm = normalize_name(us_name)
    us_last = last_name(us_name)
    us_init = first_initial(us_name)
    cand_full = cand["norm_full"]
    if us_norm and us_norm == cand_full:
        return "exact_name", 100.0
    if cand["norm_web"] and us_norm == cand["norm_web"]:
        return "exact_web", 99.0
    if us_norm and cand_full and len(us_norm) >= 4 and (us_norm in cand_full or cand_full in us_norm):
        return "contains_name", 97.0
    if us_last and us_last == cand["last"] and us_init and us_init == cand["initial"]:
        return "last_initial", 96.0
    if cand["norm_web"]:
        web_toks = cand["norm_web"].split()
        if len(web_toks) >= 2 and web_toks[-1] == us_last and web_toks[0][:1] == us_init:
            return "web_last_initial", 95.5
    ratio = max(
        float(fuzz.token_sort_ratio(us_norm, cand_full or cand["norm_web"])),
        float(fuzz.token_set_ratio(us_norm, cand_full or cand["norm_web"])),
    )
    return "fuzzy", ratio


def match_players(
    us_players: pl.DataFrame,
    fpl_players: pl.DataFrame,
    *,
    overrides: pl.DataFrame,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (accepted, ambiguous, unmatched_us)."""
    ov: dict[str, dict] = {}
    if overrides is not None and not overrides.is_empty():
        for row in overrides.iter_rows(named=True):
            pid = str(row.get("understat_player_id") or "")
            if pid:
                ov[pid] = row

    fpl_rows = _fpl_index(fpl_players)
    by_season_team: dict[tuple, list[dict]] = defaultdict(list)
    by_season: dict[str, list[dict]] = defaultdict(list)
    for c in fpl_rows:
        if c["player_code"] is None:
            continue
        by_season[str(c["season"])].append(c)
        by_season_team[(str(c["season"]), c["team_code"])].append(c)

    accepted: list[dict] = []
    ambiguous: list[dict] = []
    unmatched: list[dict] = []
    taken_codes: dict[str, set[int]] = defaultdict(set)  # season -> player_codes used

    for u in us_players.iter_rows(named=True):
        pid = str(u.get("understat_player_id") or "")
        name = u.get("player_name") or ""
        seasons = [s for s in str(u.get("seasons") or "").split(",") if s]
        codes = [int(x) for x in str(u.get("team_codes") or "").split(",") if x]

        if pid in ov:
            row = ov[pid]
            accepted.append(
                {
                    "understat_player_id": pid,
                    "player_code": int(row["player_code"]),
                    "player_name": name,
                    "web_name": None,
                    "fpl_full_name": None,
                    "team_codes": u.get("team_codes"),
                    "seasons": u.get("seasons"),
                    "method": "override",
                    "score": 100.0,
                    "status": "accepted",
                    "reason": row.get("reason") or "",
                }
            )
            continue

        pool: list[dict] = []
        seen: set[tuple] = set()
        for season in seasons or [None]:
            for code in codes or [None]:
                if season and code is not None:
                    for c in by_season_team.get((season, code), []):
                        key = (c["season"], c["player_code"])
                        if key in seen:
                            continue
                        seen.add(key)
                        pool.append(c)
            if season and not pool:
                for c in by_season.get(season, []):
                    key = (c["season"], c["player_code"])
                    if key in seen:
                        continue
                    seen.add(key)
                    pool.append(c)

        scored: list[tuple[str, float, dict]] = []
        for c in pool:
            if seasons and c["season"] in taken_codes and c["player_code"] in taken_codes[c["season"]]:
                # allow same FPL code across seasons; skip if already paired this season to someone else
                continue
            method, score = _score_pair(name, c)
            scored.append((method, score, c))
        scored.sort(key=lambda t: t[1], reverse=True)

        chosen = None
        for method in ("exact_name", "exact_web", "contains_name", "last_initial", "web_last_initial"):
            hits = [t for t in scored if t[0] == method]
            codes = {t[2]["player_code"] for t in hits}
            if len(codes) == 1:
                chosen = hits[0]
                break
            if len(codes) > 1:
                # collision at this precision; do not fall through to a weaker auto method
                chosen = None
                break
        if chosen is None:
            us_last = last_name(name)
            if us_last and len(us_last) >= 5:
                last_hits = [t for t in scored if t[2]["last"] == us_last]
                last_codes = {t[2]["player_code"] for t in last_hits}
                if len(last_codes) == 1:
                    method, score, c = last_hits[0]
                    chosen = ("last_unique", score, c)
        if chosen is None:
            fuzzy_hits = [t for t in scored if t[0] == "fuzzy" and t[1] >= FUZZY_AUTO_MIN]
            codes = {t[2]["player_code"] for t in fuzzy_hits}
            if len(codes) == 1:
                chosen = fuzzy_hits[0]

        if chosen is not None:
            method, score, c = chosen
            accepted.append(
                {
                    "understat_player_id": pid,
                    "player_code": c["player_code"],
                    "player_name": name,
                    "web_name": c.get("web_name"),
                    "fpl_full_name": c.get("full_name"),
                    "team_codes": u.get("team_codes"),
                    "seasons": u.get("seasons"),
                    "method": method if method != "fuzzy" else "fuzzy_team",
                    "score": score,
                    "status": "accepted",
                    "reason": "",
                }
            )
            for season in seasons:
                taken_codes[season].add(c["player_code"])
            continue

        near = [t for t in scored if t[1] >= FUZZY_AMBIGUOUS_MIN]
        if len({t[2]["player_code"] for t in near}) > 1:
            top = near[:5]
            ambiguous.append(
                {
                    "understat_player_id": pid,
                    "player_name": name,
                    "team_codes": u.get("team_codes"),
                    "seasons": u.get("seasons"),
                    "candidates": "; ".join(
                        f"{t[2]['player_code']}|{t[2].get('full_name') or t[2].get('web_name')}|{t[0]}|{t[1]:.1f}"
                        for t in top
                    ),
                    "reason": "multiple_candidates",
                }
            )
            continue

        unmatched.append(
            {
                "understat_player_id": pid,
                "player_name": name,
                "team_codes": u.get("team_codes"),
                "seasons": u.get("seasons"),
                "best": (
                    f"{scored[0][2]['player_code']}|{scored[0][2].get('full_name')}|{scored[0][0]}|{scored[0][1]:.1f}"
                    if scored
                    else None
                ),
                "reason": "no_unique_high_confidence",
            }
        )

    return accepted, ambiguous, unmatched


def build_player_map(
    roster: pl.DataFrame,
    league_player: pl.DataFrame,
    seasons: list[str],
    *,
    override_path,
    out_path,
    ambiguous_path,
    unmatched_us_path,
    unmatched_fpl_path,
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    overrides = ensure_csv(override_path, PLAYER_OVERRIDE_COLS)
    us_players = understat_player_teams(roster, league_player)
    fpl_players = load_fpl_players(seasons)
    mins = load_fpl_pl_minutes(seasons)

    accepted, ambiguous, unmatched_us = match_players(us_players, fpl_players, overrides=overrides)
    mapped = pl.DataFrame(accepted) if accepted else pl.DataFrame(
        schema={
            "understat_player_id": pl.Utf8,
            "player_code": pl.Int64,
            "player_name": pl.Utf8,
            "web_name": pl.Utf8,
            "fpl_full_name": pl.Utf8,
            "team_codes": pl.Utf8,
            "seasons": pl.Utf8,
            "method": pl.Utf8,
            "score": pl.Float64,
            "status": pl.Utf8,
            "reason": pl.Utf8,
        }
    )

    mapped_codes = set(mapped["player_code"].to_list()) if mapped.height else set()
    unmatched_fpl_rows = []
    if mins.height and fpl_players.height:
        played = mins.filter(pl.col("pl_minutes").fill_null(0) > 0)
        fpl_lookup = {
            (int(r["player_code"]), r["season"]): r
            for r in fpl_players.iter_rows(named=True)
            if r.get("player_code") is not None
        }
        for row in played.iter_rows(named=True):
            code = int(row["player_code"])
            if code in mapped_codes:
                continue
            dim = fpl_lookup.get((code, row["season"]), {})
            unmatched_fpl_rows.append(
                {
                    "player_code": code,
                    "season": row["season"],
                    "web_name": row.get("web_name") or dim.get("web_name"),
                    "first_name": dim.get("first_name"),
                    "second_name": dim.get("second_name"),
                    "team_code": row.get("team_code") or dim.get("team_code"),
                    "pl_minutes": row.get("pl_minutes"),
                    "reason": "no_understat_player",
                }
            )

    amb = pl.DataFrame(ambiguous) if ambiguous else pl.DataFrame(
        {"understat_player_id": [], "player_name": [], "team_codes": [], "seasons": [], "candidates": [], "reason": []}
    )
    uus = pl.DataFrame(unmatched_us) if unmatched_us else pl.DataFrame(
        {"understat_player_id": [], "player_name": [], "team_codes": [], "seasons": [], "best": [], "reason": []}
    )
    ufpl = pl.DataFrame(unmatched_fpl_rows) if unmatched_fpl_rows else pl.DataFrame(
        {
            "player_code": [],
            "season": [],
            "web_name": [],
            "first_name": [],
            "second_name": [],
            "team_code": [],
            "pl_minutes": [],
            "reason": [],
        }
    )

    write_csv(out_path, mapped.sort(["player_name", "understat_player_id"]))
    write_csv(ambiguous_path, amb)
    write_csv(unmatched_us_path, uus)
    write_csv(unmatched_fpl_path, ufpl)
    return mapped, amb, uus, ufpl
