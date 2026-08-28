"""Ingest Understat EPL masters (matches, shots, team style, context, players)."""

from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

from pipeline.understat.cache import cache_path
from pipeline.understat.client import UnderstatFetcher
from pipeline.understat.config import MASTER_DIR, SEASONS
from pipeline.understat.maps import load_team_map
from pipeline.understat.normalize import (
    flatten_team_context,
    matches_frame,
    normalize_league_player,
    normalize_match,
    normalize_match_shots,
    normalize_team_history_row,
    now_utc,
    shots_frame,
)

log = logging.getLogger("understat")


def _write_partition(table: str, season_fpl: str, df: pl.DataFrame) -> Path:
    out_dir = MASTER_DIR / table / f"season={season_fpl}"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "part.parquet"
    df.write_parquet(path)
    return path


def _stamp(df: pl.DataFrame) -> pl.DataFrame:
    if df.is_empty():
        return df
    return df.with_columns(
        pl.lit(now_utc()).alias("ingested_at_utc"),
        pl.lit("understat.com").alias("source"),
    )


def ingest_season_matches(
    fetcher: UnderstatFetcher,
    understat_season: str,
    *,
    force_index: bool = False,
) -> pl.DataFrame:
    # Refresh fixture list when asked (so new results appear); individual match
    # shot pulls still hit cache unless force.
    if force_index:
        from pipeline.understat.cache import cache_path

        p = cache_path("league", "EPL", understat_season, "matches.json")
        if p.exists():
            p.unlink()
    raw = fetcher.league_matches(understat_season)
    rows = [normalize_match(m, understat_season=understat_season) for m in raw]
    df = _stamp(matches_frame(rows))
    path = _write_partition("match", SEASONS[understat_season], df)
    log.info(
        "match season=%s rows=%s finished=%s → %s",
        understat_season,
        df.height,
        int(df.filter(pl.col("is_result")).height) if df.height else 0,
        path,
    )
    return df


def ingest_season_shots(
    fetcher: UnderstatFetcher,
    understat_season: str,
    matches: pl.DataFrame,
) -> pl.DataFrame:
    finished = matches.filter(pl.col("is_result"))
    all_rows: list[dict] = []
    total = finished.height
    for i, row in enumerate(finished.iter_rows(named=True), start=1):
        mid = row["match_id"]
        if not mid:
            continue
        raw = fetcher.match_shots(mid)
        all_rows.extend(normalize_match_shots(raw, match_row=row))
        if i % 50 == 0 or i == total:
            log.info(
                "shots %s %s/%s matches (live=%s cache_hits=%s)",
                understat_season,
                i,
                total,
                fetcher.live_calls,
                fetcher.cache_hits,
            )
    df = _stamp(shots_frame(all_rows))
    path = _write_partition("shot", SEASONS[understat_season], df)
    log.info("shot season=%s rows=%s → %s", understat_season, df.height, path)
    return df


def ingest_season_team_match_style(
    fetcher: UnderstatFetcher,
    understat_season: str,
    matches: pl.DataFrame,
    *,
    force_index: bool = False,
) -> pl.DataFrame:
    if force_index:
        p = cache_path("league", "EPL", understat_season, "teams.json")
        if p.exists():
            p.unlink()
    raw_teams = fetcher.league_teams(understat_season)
    hist_rows: list[dict] = []
    for tid, blob in (raw_teams or {}).items():
        title = blob.get("title") or ""
        for h in blob.get("history") or []:
            hist_rows.append(
                normalize_team_history_row(
                    h,
                    team_id=str(tid),
                    team_title=title,
                    understat_season=understat_season,
                )
            )
    hist = pl.DataFrame(hist_rows) if hist_rows else pl.DataFrame()
    if hist.is_empty():
        return hist

    # Attach match_id via kickoff + side
    home = matches.select(
        pl.col("match_id"),
        pl.col("kickoff_raw"),
        pl.col("home_team_id").alias("team_id"),
        pl.lit(True).alias("is_home"),
        pl.col("away_team_id").alias("opponent_id"),
    )
    away = matches.select(
        pl.col("match_id"),
        pl.col("kickoff_raw"),
        pl.col("away_team_id").alias("team_id"),
        pl.lit(False).alias("is_home"),
        pl.col("home_team_id").alias("opponent_id"),
    )
    link = pl.concat([home, away], how="diagonal_relaxed")
    team_map = load_team_map().select(
        pl.col("understat_team_id").alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_name").alias("team"),
        pl.col("fpl_short").alias("team_short"),
    )
    opp_map = load_team_map().select(
        pl.col("understat_team_id").alias("opponent_id"),
        pl.col("team_code").alias("opponent_code"),
        pl.col("fpl_name").alias("opponent"),
        pl.col("fpl_short").alias("opponent_short"),
    )
    df = (
        hist.join(link, on=["kickoff_raw", "team_id", "is_home"], how="left")
        .join(team_map, on="team_id", how="left")
        .join(opp_map, on="opponent_id", how="left")
    )
    df = _stamp(df)
    path = _write_partition("team_match_style", SEASONS[understat_season], df)
    linked = int(df.filter(pl.col("match_id").is_not_null()).height) if "match_id" in df.columns else 0
    log.info(
        "team_match_style season=%s rows=%s linked_match_id=%s → %s",
        understat_season,
        df.height,
        linked,
        path,
    )
    return df


def ingest_season_team_context(
    fetcher: UnderstatFetcher,
    understat_season: str,
    *,
    force_index: bool = False,
) -> pl.DataFrame:
    if force_index:
        p = cache_path("league", "EPL", understat_season, "teams.json")
        # teams.json may already be fresh from style ingest; only wipe context files
        pass
    raw_teams = fetcher.league_teams(understat_season)
    team_map = load_team_map()
    id_to_slug = dict(zip(team_map["understat_team_id"].to_list(), team_map["understat_slug"].to_list()))
    id_to_code = dict(zip(team_map["understat_team_id"].to_list(), team_map["team_code"].to_list()))
    id_to_fpl = dict(zip(team_map["understat_team_id"].to_list(), team_map["fpl_name"].to_list()))
    id_to_short = dict(zip(team_map["understat_team_id"].to_list(), team_map["fpl_short"].to_list()))

    rows: list[dict] = []
    for tid, blob in (raw_teams or {}).items():
        tid_s = str(tid)
        title = blob.get("title") or ""
        slug = id_to_slug.get(tid_s) or title.replace(" ", "_")
        # force refresh context on refresh runs by deleting cache file
        if force_index:
            cp = cache_path("team", slug, understat_season, "context.json")
            if cp.exists():
                cp.unlink()
        ctx = fetcher.team_context(slug, understat_season)
        for r in flatten_team_context(
            ctx,
            team_id=tid_s,
            team_title=title,
            team_slug=slug,
            understat_season=understat_season,
        ):
            r["team_code"] = id_to_code.get(tid_s)
            r["team"] = id_to_fpl.get(tid_s)
            r["team_short"] = id_to_short.get(tid_s)
            rows.append(r)

    df = _stamp(pl.DataFrame(rows) if rows else pl.DataFrame())
    path = _write_partition("team_context_season", SEASONS[understat_season], df)
    log.info("team_context_season season=%s rows=%s → %s", understat_season, df.height, path)
    return df


def ingest_season_players(
    fetcher: UnderstatFetcher,
    understat_season: str,
    *,
    force_index: bool = False,
) -> pl.DataFrame:
    if force_index:
        p = cache_path("league", "EPL", understat_season, "players.json")
        if p.exists():
            p.unlink()
    raw = fetcher.league_players(understat_season)
    rows = [normalize_league_player(p, understat_season=understat_season) for p in raw]
    df = _stamp(pl.DataFrame(rows) if rows else pl.DataFrame())
    path = _write_partition("league_player", SEASONS[understat_season], df)
    log.info("league_player season=%s rows=%s → %s", understat_season, df.height, path)
    return df


def ingest_seasons(
    seasons: list[str] | None = None,
    *,
    force: bool = False,
    shots: bool = True,
    style: bool = True,
    context: bool = True,
    players: bool = True,
    refresh_index: bool = False,
) -> dict[str, pl.DataFrame]:
    """
    force: bypass all caches
    refresh_index: re-pull league fixture/team/player lists + team context
                   (new finished matches get shot pulls; cached shots reused)
    """
    seasons = seasons or list(SEASONS.keys())
    out: dict[str, pl.DataFrame] = {}
    with UnderstatFetcher(force=force) as fetcher:
        for us in seasons:
            if us not in SEASONS:
                raise ValueError(f"Unknown understat season {us}; known={list(SEASONS)}")
            force_idx = refresh_index or force
            matches = ingest_season_matches(fetcher, us, force_index=force_idx)
            out[f"match:{us}"] = matches
            if shots:
                out[f"shot:{us}"] = ingest_season_shots(fetcher, us, matches)
            if style:
                out[f"team_match_style:{us}"] = ingest_season_team_match_style(
                    fetcher, us, matches, force_index=force_idx
                )
            if context:
                out[f"team_context:{us}"] = ingest_season_team_context(
                    fetcher, us, force_index=force_idx
                )
            if players:
                out[f"league_player:{us}"] = ingest_season_players(
                    fetcher, us, force_index=force_idx
                )
        log.info(
            "ingest done live_calls=%s cache_hits=%s",
            fetcher.live_calls,
            fetcher.cache_hits,
        )
    return out


def read_master(table: str, seasons: list[str] | None = None) -> pl.DataFrame:
    """Load understat parquet partitions. seasons are FPL labels (2025-2026)."""
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
