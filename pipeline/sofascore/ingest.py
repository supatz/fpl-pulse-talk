"""Ingest SofaScore PL masters (events, shots, player_match). Keep existing on network failure."""

from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

from pipeline.pl_merge.io_csv import write_csv
from pipeline.sofascore.cache import cache_path, read_json, write_json
from pipeline.sofascore.client import SofaScoreError, SofaScoreFetcher
from pipeline.sofascore.config import MASTER_DIR, MAPS_DIR, REVIEW_DIR, SEASONS
from pipeline.sofascore.maps import (
    MATCH_MAP_COLS,
    PLAYER_MAP_COLS,
    TEAM_MAP_COLS,
    combine_player_overrides,
    load_fpl_pl_fixtures,
    load_fpl_players,
    load_team_map,
    load_worksheet_overrides,
    pair_matches,
    pair_players,
    persist_worksheet_overrides,
    write_player_mapping_worksheet,
)
from pipeline.sofascore.normalize import (
    lineup_player_rows,
    normalize_event,
    normalize_shot,
    now_utc,
)
from pipeline.config import SOURCE_DIR
from pipeline.transforms import normalize_teams

log = logging.getLogger("sofascore")

_NETWORK_ERRORS = (OSError, ConnectionError, TimeoutError, SofaScoreError)


def _stamp(df: pl.DataFrame) -> pl.DataFrame:
    if df.is_empty():
        return df
    return df.with_columns(
        pl.lit(now_utc()).alias("ingested_at_utc"),
        pl.lit("sofascore.com").alias("source"),
    )


def _write_partition(table: str, season: str, df: pl.DataFrame) -> Path:
    out_dir = MASTER_DIR / table / f"season={season}"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "part.parquet"
    df.write_parquet(path)
    return path


def read_master(table: str, seasons: list[str] | None = None) -> pl.DataFrame:
    base = MASTER_DIR / table
    if not base.exists():
        return pl.DataFrame()
    parts = []
    for p in sorted(base.glob("season=*/part.parquet")):
        season = p.parent.name.split("=", 1)[-1]
        if seasons and season not in seasons:
            continue
        parts.append(pl.read_parquet(p))
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed")


def _load_fpl_teams(seasons: list[str]) -> pl.DataFrame:
    parts = []
    for season in seasons:
        path = SOURCE_DIR / "data" / season / "teams.csv"
        if path.exists():
            parts.append(normalize_teams(pl.read_csv(path)))
    if not parts:
        return pl.DataFrame()
    return pl.concat(parts, how="diagonal_relaxed").unique(subset=["code"], keep="last")


def _name_key(s: str | None) -> str:
    if not s:
        return ""
    return (
        str(s)
        .lower()
        .replace("fc", "")
        .replace("afc", "")
        .replace("united", "utd")
        .replace("city", "")
        .replace("wanderers", "")
        .replace("hotspur", "")
        .replace(".", "")
        .replace("-", " ")
        .replace("'", "")
        .split()
    ) and "".join(
        str(s)
        .lower()
        .replace("fc", "")
        .replace("afc", "")
        .replace("united", "utd")
        .replace("hotspur", "")
        .replace(".", "")
        .replace("-", " ")
        .replace("'", "")
        .split()
    )


def upsert_team_map(events: pl.DataFrame, fpl_seasons: list[str]) -> pl.DataFrame:
    """Hand map first; fill exact/normalized FPL names for newly seen SofaScore clubs."""
    existing = load_team_map()
    known = set(existing["sofascore_team_id"].cast(pl.Utf8).to_list()) if existing.height else set()
    fpl = _load_fpl_teams(fpl_seasons)
    by_name = {}
    for r in fpl.to_dicts() if fpl.height else []:
        by_name[_name_key(r.get("name"))] = r
        by_name[_name_key(r.get("short_name"))] = r
    rows = existing.to_dicts() if existing.height else []
    seen: dict[str, dict] = {}
    for ev in events.iter_rows(named=True):
        for side, tid_k, name_k, short_k in (
            ("home", "home_team_id", "home_team", "home_short"),
            ("away", "away_team_id", "away_team", "away_short"),
        ):
            tid = ev.get(tid_k)
            if tid is None or str(tid).strip() == "":
                continue
            sid = str(tid)
            if sid in known or sid in seen:
                continue
            name = ev.get(name_k)
            short = ev.get(short_k)
            hit = by_name.get(_name_key(name)) or by_name.get(_name_key(short))
            rec = {
                "sofascore_team_id": sid,
                "sofascore_name": name,
                "team_code": int(hit["code"]) if hit else None,
                "fpl_name": hit.get("name") if hit else None,
                "fpl_short": hit.get("short_name") if hit else None,
                "notes": "auto_name" if hit else "unmapped",
            }
            seen[sid] = rec
            rows.append(rec)
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    df = pl.DataFrame(rows) if rows else pl.DataFrame({c: [] for c in TEAM_MAP_COLS})
    write_csv(MAPS_DIR / "team_map.csv", df.select(list(TEAM_MAP_COLS)))
    unmapped = df.filter(pl.col("team_code").is_null())
    if unmapped.height:
        REVIEW_DIR.mkdir(parents=True, exist_ok=True)
        write_csv(REVIEW_DIR / "unmapped_teams.csv", unmapped)
        log.warning("SofaScore teams without FPL team_code: %s", unmapped.height)
    return load_team_map()


def _collect_events(fetcher: SofaScoreFetcher, fpl_season: str, ss_season_id: int) -> list[dict]:
    events: list[dict] = []
    seen: set[int] = set()
    try:
        rounds = fetcher.rounds(ss_season_id)
    except SofaScoreError:
        rounds = []
    for rnd in rounds:
        try:
            batch = fetcher.events_round(ss_season_id, rnd)
        except SofaScoreError as err:
            log.warning("round events failed season_id=%s round=%s: %s", ss_season_id, rnd, err)
            continue
        for ev in batch:
            eid = ev.get("id")
            if eid in seen:
                continue
            seen.add(eid)
            events.append(ev)
    if not events:
        events = fetcher.events_last_pages(ss_season_id)
    return events


def ingest_season_events(fetcher: SofaScoreFetcher, fpl_season: str, *, force_index: bool = False) -> pl.DataFrame:
    p = cache_path("unique-tournament", "17", "season", fpl_season, "events-index.json")
    bak = p.with_suffix(".json.bak")
    stale = read_json(p) if p.exists() else (read_json(bak) if bak.exists() else None)
    if not force_index and not fetcher.force and stale is not None:
        payload = stale
        sid = int(payload.get("season_id") or 0)
        rows = [normalize_event(e, fpl_season=fpl_season, ss_season_id=sid) for e in (payload.get("events") or [])]
        df = _stamp(pl.DataFrame(rows) if rows else pl.DataFrame())
        path = _write_partition("event", fpl_season, df)
        log.info(
            "event season=%s from cache rows=%s finished=%s → %s",
            fpl_season,
            df.height,
            int(df.filter(pl.col("is_result")).height) if df.height and "is_result" in df.columns else 0,
            path,
        )
        return df
    if force_index and p.exists():
        p.replace(bak)
        stale = read_json(bak)

    try:
        sid = fetcher.resolve_season_id(fpl_season)
        if sid is None:
            raise SofaScoreError(f"could not resolve SofaScore season id for {fpl_season}")
        raw = _collect_events(fetcher, fpl_season, sid)
        payload = {"season_id": sid, "fpl_season": fpl_season, "events": raw}
        write_json(p, payload)
        if bak.exists():
            bak.unlink(missing_ok=True)
    except _NETWORK_ERRORS as err:
        log.warning("SofaScore event index unreachable for %s (%s). Falling back.", fpl_season, err)
        if stale is not None:
            write_json(p, stale)
            if bak.exists():
                bak.unlink(missing_ok=True)
            payload = stale
        else:
            existing = read_master("event", [fpl_season])
            if not existing.is_empty():
                log.warning("Using existing master/sofascore/event for %s (%s rows)", fpl_season, existing.height)
                return existing
            raise

    sid = int(payload.get("season_id") or 0)
    rows = [normalize_event(e, fpl_season=fpl_season, ss_season_id=sid) for e in (payload.get("events") or [])]
    df = _stamp(pl.DataFrame(rows) if rows else pl.DataFrame())
    path = _write_partition("event", fpl_season, df)
    log.info(
        "event season=%s ss_season_id=%s rows=%s finished=%s → %s",
        fpl_season,
        sid,
        df.height,
        int(df.filter(pl.col("is_result")).height) if df.height and "is_result" in df.columns else 0,
        path,
    )
    return df


def ingest_season_shots_and_lineups(
    fetcher: SofaScoreFetcher,
    fpl_season: str,
    events: pl.DataFrame,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    if events.is_empty():
        return pl.DataFrame(), pl.DataFrame()
    finished = events.filter(pl.col("is_result"))
    shot_rows: list[dict] = []
    lineup_rows: list[dict] = []
    total = finished.height
    for i, row in enumerate(finished.iter_rows(named=True), start=1):
        eid = row.get("event_id")
        if eid is None:
            continue
        try:
            sm = fetcher.shotmap(int(eid)) or {}
        except SofaScoreError as err:
            log.warning("shotmap event=%s: %s", eid, err)
            sm = {}
        shots = sm.get("shotmap") or sm.get("shots") or []
        for sh in shots:
            n = normalize_shot(sh, event=row)
            if n:
                shot_rows.append(n)
        try:
            lu = fetcher.lineups(int(eid))
        except SofaScoreError as err:
            log.warning("lineups event=%s: %s", eid, err)
            lu = None
        lineup_rows.extend(lineup_player_rows(lu, event=row))
        if i == 1 or i % 20 == 0 or i == total:
            log.info("shots+lineups %s %s/%s event_id=%s shots=%s", fpl_season, i, total, eid, len(shot_rows))

    shots = _stamp(pl.DataFrame(shot_rows) if shot_rows else pl.DataFrame())
    pmatch = _stamp(pl.DataFrame(lineup_rows) if lineup_rows else pl.DataFrame())
    sp = _write_partition("shot", fpl_season, shots)
    lp = _write_partition("player_match", fpl_season, pmatch)
    log.info("shot season=%s rows=%s → %s", fpl_season, shots.height, sp)
    log.info("player_match season=%s rows=%s → %s", fpl_season, pmatch.height, lp)
    return shots, pmatch


def rebuild_identity_maps(fpl_seasons: list[str] | None = None) -> None:
    seasons = fpl_seasons or list(SEASONS.keys())
    events = read_master("event", seasons)
    if events.is_empty():
        log.warning("No SofaScore events — skip maps")
        return
    upsert_team_map(events, seasons)
    from pipeline.pl_merge.io_csv import ensure_csv

    overrides_m = ensure_csv(MAPS_DIR / "match_overrides.csv", MATCH_MAP_COLS)
    fpl = load_fpl_pl_fixtures(seasons)
    mapped, unmatched = pair_matches(events, fpl, overrides_m)
    write_csv(MAPS_DIR / "match_map.csv", mapped.select(list(MATCH_MAP_COLS)) if mapped.height else mapped)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(REVIEW_DIR / "unmapped_matches.csv", unmatched)
    log.info("match_map rows=%s unmatched=%s", mapped.height, unmatched.height)

    pm = read_master("player_match", seasons)
    if pm.is_empty():
        return
    team_map = load_team_map()
    tm = team_map.select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("team_id"),
        pl.col("sofascore_name"),
        pl.col("team_code"),
        pl.col("fpl_name"),
        pl.col("fpl_short"),
    )
    joined = pm.with_columns(pl.col("team_id").cast(pl.Utf8), pl.col("player_id").cast(pl.Utf8)).join(
        tm, on="team_id", how="left"
    )
    players = joined.group_by("player_id").agg(
        pl.col("player_name").first(),
        pl.col("team_code").drop_nulls().first(),
        pl.col("season").first(),
    )
    ss_detail = joined.group_by("player_id").agg(
        pl.col("player_name").first(),
        pl.col("team_id").drop_nulls().first(),
        pl.col("sofascore_name").drop_nulls().first().alias("sofascore_team_name"),
        pl.col("team_code").drop_nulls().first(),
        pl.col("season").min().alias("seasons"),
        pl.col("event_id").n_unique().alias("ss_appearances"),
        pl.col("minutes").sum().alias("ss_minutes"),
        pl.col("big_chances_created").sum().alias("ss_bcc"),
        pl.col("big_chances_missed").sum().alias("ss_bcm"),
    )
    file_ov = ensure_csv(MAPS_DIR / "player_overrides.csv", PLAYER_MAP_COLS)
    sheet_ov = load_worksheet_overrides()
    persist_worksheet_overrides(file_ov, sheet_ov)
    overrides_p = combine_player_overrides(file_ov, sheet_ov)
    fpl_p = load_fpl_players(seasons)
    accepted, unmatched_p, amb = pair_players(players, fpl_p, overrides_p)
    write_csv(MAPS_DIR / "player_map.csv", accepted.select(list(PLAYER_MAP_COLS)) if accepted.height else accepted)
    write_csv(REVIEW_DIR / "unmapped_players.csv", unmatched_p)
    write_csv(REVIEW_DIR / "ambiguous_players.csv", amb)
    sheet = write_player_mapping_worksheet(
        unmatched=unmatched_p,
        ambiguous=amb,
        ss_detail=ss_detail,
        fpl_players=fpl_p,
        team_map=team_map,
    )
    log.info(
        "player_map rows=%s unmatched=%s ambiguous=%s worksheet=%s",
        accepted.height,
        unmatched_p.height,
        amb.height,
        sheet.height,
    )


def ingest_seasons(
    seasons: list[str] | None = None,
    *,
    force: bool = False,
    shots: bool = True,
    refresh_index: bool = False,
) -> dict[str, pl.DataFrame]:
    seasons = seasons or list(SEASONS.keys())
    out: dict[str, pl.DataFrame] = {}
    fetcher = SofaScoreFetcher(force=force)
    for fpl in seasons:
        if fpl not in SEASONS:
            raise ValueError(f"Unknown SofaScore season {fpl}; known={list(SEASONS)}")
        events = ingest_season_events(fetcher, fpl, force_index=refresh_index or force)
        out[f"event:{fpl}"] = events
        if shots:
            sh, pm = ingest_season_shots_and_lineups(fetcher, fpl, events)
            out[f"shot:{fpl}"] = sh
            out[f"player_match:{fpl}"] = pm
    rebuild_identity_maps(seasons)
    log.info("ingest done live_calls=%s cache_hits=%s", fetcher.live_calls, fetcher.cache_hits)
    return out
