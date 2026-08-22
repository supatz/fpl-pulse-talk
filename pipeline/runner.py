from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import polars as pl

from pipeline.build_tables import (
    build_slice,
    concat_or_none,
    load_fixtures_only,
    finalize_fixtures,
    finalize_player_gw,
    finalize_player_match,
    finalize_team_match,
    load_season_dims,
    slice_hash,
)
from pipeline.config import (
    INCREMENTAL_PATH,
    MANIFEST_PATH,
    MASTER_DIR,
    SOURCE_DIR,
    SOURCE_NAME,
)
from pipeline.dictionary import write_data_dictionary
from pipeline.discover import Discovery, GwSlice, discover
from pipeline.fetch import fetch_source
from pipeline.io_utils import atomic_write_json
from pipeline.quality import run_quality
from pipeline.schema_drift import ValidationResult
from build_serving import build_from_disk
from pipeline.write import hive_path, merge_partition_gws, read_partition, write_partitioned

log = logging.getLogger("fpl")


def run_pipeline(
    *,
    refresh: bool = True,
    full: bool = False,
    serving_only: bool = False,
    source_dir: Path | None = None,
) -> dict:
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if serving_only:
        return _serving_from_masters()

    if refresh or full:
        if source_dir is None:
            source_root, source_commit = fetch_source(SOURCE_DIR)
        else:
            source_root = Path(source_dir)
            source_commit = _existing_commit(source_root)
    else:
        source_root = Path(source_dir or SOURCE_DIR)
        source_commit = _existing_commit(source_root)

    discovery = discover(source_root)
    validation = ValidationResult()
    prev = {} if full else _load_incremental()
    prev_hashes: dict[str, str] = prev.get("slice_hashes", {})

    season_dims: dict[str, tuple[pl.DataFrame, pl.DataFrame]] = {}
    for season in discovery.seasons_with_tournaments:
        season_dims[season] = load_season_dims(discovery.data_root / season, validation)

    rebuilt_pm: dict[tuple[str, str], list[pl.DataFrame]] = defaultdict(list)
    rebuilt_tm: dict[tuple[str, str], list[pl.DataFrame]] = defaultdict(list)
    rebuilt_pgw: dict[str, list[pl.DataFrame]] = defaultdict(list)
    fixture_parts: list[pl.DataFrame] = []
    join_logs: list[dict] = []
    source_files: list[str] = []
    new_hashes: dict[str, str] = {}
    reused: list[str] = []
    rebuilt_keys: list[str] = []
    gws_rebuilt: dict[tuple[str, str], set[int]] = defaultdict(set)
    gws_reused: dict[tuple[str, str], set[int]] = defaultdict(set)
    pgw_rebuilt: dict[str, set[int]] = defaultdict(set)
    pgw_reused: dict[str, set[int]] = defaultdict(set)

    for slice_ in discovery.slices:
        season_dir = discovery.data_root / slice_.season
        digest = slice_hash(slice_, season_dir)
        new_hashes[slice_.key] = digest
        part_key = (slice_.season, slice_.competition)
        can_reuse = (
            not full
            and prev_hashes.get(slice_.key) == digest
            and _partition_exists(slice_)
        )
        if can_reuse:
            reused.append(slice_.key)
            gws_reused[part_key].add(slice_.gw)
            if slice_.competition == "Premier League":
                pgw_reused[slice_.season].add(slice_.gw)
            fx_only = load_fixtures_only(slice_, slice_.season)
            if fx_only is not None:
                fixture_parts.append(fx_only)
            continue

        rebuilt_keys.append(slice_.key)
        players, teams = season_dims[slice_.season]
        built = build_slice(slice_, players, teams, slice_.season, validation)
        join_logs.extend(built.join_logs)
        source_files.extend(built.source_files)
        if built.player_match is not None:
            rebuilt_pm[part_key].append(built.player_match)
            gws_rebuilt[part_key].add(slice_.gw)
        if built.team_match is not None:
            rebuilt_tm[part_key].append(built.team_match)
            gws_rebuilt[part_key].add(slice_.gw)
        if built.player_gw is not None:
            rebuilt_pgw[slice_.season].append(built.player_gw)
            pgw_rebuilt[slice_.season].add(slice_.gw)
        if built.fixtures is not None:
            fixture_parts.append(built.fixtures)

    player_match = _assemble_player_or_team(
        discovery,
        rebuilt_pm,
        gws_reused,
        gws_rebuilt,
        table="player_match",
    )
    team_match = _assemble_player_or_team(
        discovery,
        rebuilt_tm,
        gws_reused,
        gws_rebuilt,
        table="team_match",
    )
    player_gw = _assemble_player_gw(discovery, rebuilt_pgw, pgw_reused, pgw_rebuilt)
    fixtures = concat_or_none(fixture_parts)

    player_match = (
        finalize_player_match(player_match, player_gw, source_commit, ingested_at, source_files)
        if player_match is not None
        else None
    )
    player_gw = (
        finalize_player_gw(player_gw, source_commit, ingested_at, source_files)
        if player_gw is not None
        else None
    )
    team_match = (
        finalize_team_match(team_match, source_commit, ingested_at, source_files)
        if team_match is not None
        else None
    )
    fixtures = (
        finalize_fixtures(fixtures, source_commit, ingested_at, source_files)
        if fixtures is not None
        else None
    )

    quality = run_quality(
        player_match,
        player_gw,
        team_match,
        fixtures,
        {s: season_dims[s][0] for s in season_dims},
        {s: season_dims[s][1] for s in season_dims},
    )
    if quality["issues"]:
        log.warning("Quality issues (rows not dropped): %s", quality["issues"])

    written: list[str] = []
    if player_match is not None:
        written += write_partitioned(player_match, "player_match", competition=True)
    if team_match is not None:
        written += write_partitioned(team_match, "team_match", competition=True)
    if player_gw is not None:
        written += write_partitioned(player_gw, "player_gw", competition=False)
    if fixtures is not None:
        written += write_partitioned(fixtures, "fixtures", competition=False)

    tables = {
        "player_match": player_match,
        "player_gw": player_gw,
        "team_match": team_match,
        "fixtures": fixtures,
    }
    write_data_dictionary({k: v for k, v in tables.items() if v is not None})
    from build_serving import build_from_disk

    serving = build_from_disk()

    schema_hashes = _collect_schema_hashes(validation)
    competitions = sorted({s.competition for s in discovery.slices})
    manifest = {
        "built_at_utc": ingested_at,
        "source": SOURCE_NAME,
        "source_repo": "https://github.com/olbauday/FPL-Core-Insights",
        "source_commit": source_commit,
        "seasons": discovery.seasons_with_tournaments,
        "seasons_all": discovery.seasons_all,
        "seasons_skipped": discovery.seasons_skipped,
        "competitions": competitions,
        "row_counts": {k: (v.height if v is not None else 0) for k, v in tables.items()},
        "null_rate": {
            name: quality["tables"].get(name, {}).get("null_rate", {})
            for name in tables
        },
        "quality_issues": quality["issues"],
        "schema_hash": schema_hashes,
        "incremental": {
            "full_rebuild": full,
            "slices_reused": len(reused),
            "slices_rebuilt": len(rebuilt_keys),
        },
        "written_partitions": written,
        "join_log_sample": join_logs[:30],
    }
    atomic_write_json(manifest, MANIFEST_PATH)
    atomic_write_json(
        {
            "source_commit": source_commit,
            "slice_hashes": new_hashes,
            "updated_at_utc": ingested_at,
        },
        INCREMENTAL_PATH,
    )
    log.info(
        "Build complete. rows=%s reused=%s rebuilt=%s",
        manifest["row_counts"],
        len(reused),
        len(rebuilt_keys),
    )
    return manifest


def _assemble_player_or_team(
    discovery: Discovery,
    rebuilt: dict[tuple[str, str], list[pl.DataFrame]],
    reused_gws: dict[tuple[str, str], set[int]],
    rebuilt_gws: dict[tuple[str, str], set[int]],
    table: str,
) -> pl.DataFrame | None:
    parts: list[pl.DataFrame] = []
    keys = {(s.season, s.competition) for s in discovery.slices}
    for season, competition in sorted(keys):
        key = (season, competition)
        existing = read_partition(table, season, competition)
        fresh = concat_or_none(rebuilt.get(key, []))
        merged = merge_partition_gws(
            existing,
            fresh,
            reused_gws.get(key, set()),
            rebuilt_gws.get(key, set()),
        )
        if merged is not None and merged.height:
            parts.append(merged)
    return concat_or_none(parts)


def _assemble_player_gw(
    discovery: Discovery,
    rebuilt: dict[str, list[pl.DataFrame]],
    reused_gws: dict[str, set[int]],
    rebuilt_gws: dict[str, set[int]],
) -> pl.DataFrame | None:
    parts: list[pl.DataFrame] = []
    seasons = {s.season for s in discovery.slices if s.competition == "Premier League"}
    for season in sorted(seasons):
        existing = read_partition("player_gw", season)
        fresh = concat_or_none(rebuilt.get(season, []))
        merged = merge_partition_gws(
            existing,
            fresh,
            reused_gws.get(season, set()),
            rebuilt_gws.get(season, set()),
        )
        if merged is not None and merged.height:
            parts.append(merged)
    return concat_or_none(parts)


def _partition_exists(slice_: GwSlice) -> bool:
    return hive_path("player_match", slice_.season, slice_.competition).exists() or hive_path(
        "team_match", slice_.season, slice_.competition
    ).exists()


def _serving_from_masters() -> dict:
    serving = build_from_disk()
    return {"serving": serving, "mode": "serving-only"}


def _existing_commit(source_root: Path) -> str:
    git = source_root / ".git"
    if not git.exists():
        return "unknown"
    import subprocess

    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _load_incremental() -> dict:
    if not INCREMENTAL_PATH.exists():
        return {}
    return json.loads(INCREMENTAL_PATH.read_text(encoding="utf-8"))


def _collect_schema_hashes(validation: ValidationResult) -> dict[str, str]:
    out: dict[str, str] = {}
    for report in validation.reports:
        out[report.path] = report.schema_hash
    # Also hash a few season-level files by content header if reports missed them
    return out
