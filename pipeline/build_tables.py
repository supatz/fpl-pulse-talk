from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import polars as pl

from pipeline.config import (
    CORE_SLICE_FILES,
    OPTIONAL_SLICE_FILES,
    PREMIER_LEAGUE,
    SEASON_FILES,
    SLICE_FILES,
)
from pipeline.discover import GwSlice
from pipeline.io_utils import (
    as_float,
    as_int,
    hash_paths,
    log_join,
    read_csv,
    validate_columns,
)
from pipeline.schema_drift import SchemaReport, ValidationResult
from pipeline.transforms import (
    add_dgw_flags,
    aggregate_shots,
    attach_side_context,
    filter_valid_fixtures,
    kickoff_utc_expr,
    normalize_enrichment,
    normalize_lineups,
    normalize_match_enrichment,
    normalize_matches,
    normalize_player_gw,
    normalize_players,
    normalize_teams,
    own_goals_from_incidents,
    rename_defence_cols,
    unpivot_team_match,
)

log = logging.getLogger("fpl")

PMS_RENAME = {
    "minutes_played": "minutes",
}


@dataclass
class SliceBuild:
    player_match: pl.DataFrame | None
    team_match: pl.DataFrame | None
    player_gw: pl.DataFrame | None
    fixtures: pl.DataFrame | None
    join_logs: list[dict] = field(default_factory=list)
    schema_reports: list[SchemaReport] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    source_files: list[str] = field(default_factory=list)


def slice_hash(slice_: GwSlice, season_dir: Path) -> str:
    paths = [slice_.path / name for name in SLICE_FILES]
    paths.extend(season_dir / name for name in SEASON_FILES)
    return hash_paths(paths)


def load_season_dims(season_dir: Path, validation: ValidationResult) -> tuple[pl.DataFrame, pl.DataFrame]:
    players_path = season_dir / "players.csv"
    teams_path = season_dir / "teams.csv"
    players_raw = read_csv(players_path)
    teams_raw = read_csv(teams_path)
    if players_raw is None:
        raise FileNotFoundError(f"Missing required {players_path}")
    if teams_raw is None:
        raise FileNotFoundError(f"Missing required {teams_path}")
    validation.reports.append(validate_columns("players", players_path, players_raw))
    validation.reports.append(validate_columns("teams", teams_path, teams_raw))
    validation.fail_if_drift()
    return normalize_players(players_raw), normalize_teams(teams_raw)


def build_slice(
    slice_: GwSlice,
    players: pl.DataFrame,
    teams: pl.DataFrame,
    season: str,
    validation: ValidationResult,
) -> SliceBuild:
    join_logs: list[dict] = []
    reports: list[SchemaReport] = []
    missing: list[str] = []
    used: list[str] = []

    def load(name: str, key: str | None = None) -> pl.DataFrame | None:
        path = slice_.path / name
        df = read_csv(path)
        if df is None:
            missing.append(str(path))
            if name not in OPTIONAL_SLICE_FILES and name in CORE_SLICE_FILES:
                log.warning("Core file missing in %s: %s", slice_.key, name)
            return None
        used.append(str(path.relative_to(slice_.path.parent.parent.parent.parent)))
        if key:
            report = validate_columns(key, path, df)
            reports.append(report)
            validation.reports.append(report)
        return df

    matches_raw = load("matches.csv", "matches")
    pms_raw = load("playermatchstats.csv", "playermatchstats")
    fixtures_raw = load("fixtures.csv", "fixtures")
    enrich_raw = load("player_match_enrichment.csv", "player_match_enrichment")
    gw_raw = load("player_gameweek_stats.csv", "player_gameweek_stats")
    shots_raw = load("shots.csv", "shots")
    lineups_raw = load("lineups.csv", "lineups")
    incidents_raw = load("incidents.csv", "incidents")
    match_enr_raw = load("match_enrichment.csv", "match_enrichment")

    validation.skipped_missing_files.extend(missing)
    validation.fail_if_drift()

    matches = None
    if matches_raw is not None:
        matches = normalize_matches(matches_raw, slice_.gw, slice_.competition).with_columns(
            pl.lit(season).alias("season")
        )

    team_match = None
    if matches is not None and matches.height:
        team_match = rename_defence_cols(unpivot_team_match(matches))
        if match_enr_raw is not None:
            menr = normalize_match_enrichment(match_enr_raw)
            team_match = team_match.join(menr, on="match_id", how="left")
            join_logs.append(log_join("team_match_enrichment", team_match, menr, team_match, ["match_id"]))
        team_match = team_match.join(
            teams.rename({"code": "team_code"}).select(
                "team_code",
                *[c for c in teams.columns if c.startswith("strength")],
            ),
            on="team_code",
            how="left",
        )
        team_match = team_match.filter(pl.col("team_code").is_not_null())

    player_match = None
    if pms_raw is not None and matches is not None and pms_raw.height:
        pms = pms_raw.rename({k: v for k, v in PMS_RENAME.items() if k in pms_raw.columns})
        pms = pms.with_columns(
            as_int(pl.col("player_id")).alias("player_id"),
            pl.col("match_id").cast(pl.Utf8),
        )
        if "minutes" in pms.columns:
            pms = pms.with_columns(as_float(pl.col("minutes")).alias("minutes"))

        before = pms.height
        pms = pms.join(
            players.select("player_id", "player_code", "web_name", "position", "team_code"),
            on="player_id",
            how="left",
        )
        join_logs.append(
            log_join(
                f"players:{slice_.key}",
                pms_raw,
                players,
                pms,
                ["player_id"],
            )
        )
        if pms.height != before:
            log.warning("player join changed row count %s -> %s", before, pms.height)

        pms = attach_side_context(pms, matches)

        if lineups_raw is not None:
            lineups = normalize_lineups(lineups_raw)
            pms = pms.join(lineups, on=["match_id", "player_id"], how="left")
            join_logs.append(log_join(f"lineups:{slice_.key}", pms, lineups, pms, ["match_id", "player_id"]))
        else:
            pms = pms.with_columns(
                pl.lit(None).cast(pl.Boolean).alias("started"),
                pl.lit(None).cast(pl.Utf8).alias("formation"),
                pl.lit(None).cast(pl.Utf8).alias("lineup_status"),
            )

        if enrich_raw is not None:
            enrich = normalize_enrichment(enrich_raw)
            pms = pms.join(enrich, on=["match_id", "player_id"], how="left")
            join_logs.append(log_join(f"enrich:{slice_.key}", pms, enrich, pms, ["match_id", "player_id"]))
        else:
            pms = pms.with_columns(
                pl.lit(None).alias("rating"),
                pl.lit(None).alias("yellow_cards"),
                pl.lit(None).alias("red_cards"),
            )

        if shots_raw is not None:
            shot_agg = aggregate_shots(shots_raw)
            pms = pms.join(shot_agg, on=["match_id", "player_id"], how="left")
            join_logs.append(log_join(f"shots:{slice_.key}", pms, shot_agg, pms, ["match_id", "player_id"]))
        else:
            pms = pms.with_columns(
                pl.lit(None).alias("np_xg"),
                pl.lit(None).alias("set_piece_xg"),
                pl.lit(None).alias("open_play_xg"),
                pl.lit(None).alias("penalty_shots"),
            )

        if incidents_raw is not None:
            ogs = own_goals_from_incidents(incidents_raw)
            pms = pms.join(ogs, on=["match_id", "player_id"], how="left")
        else:
            pms = pms.with_columns(pl.lit(None).alias("own_goals"))

        pms = pms.with_columns(pl.lit(season).alias("season"))
        player_match = pms

    player_gw = None
    if gw_raw is not None and slice_.competition == PREMIER_LEAGUE and gw_raw.height:
        player_gw = normalize_player_gw(gw_raw).with_columns(
            pl.lit(season).alias("season"),
            pl.lit(slice_.gw).alias("folder_gw"),
        )
        player_gw = player_gw.with_columns(
            pl.coalesce([pl.col("gw"), pl.col("folder_gw")]).alias("gw")
        ).drop("folder_gw")
        player_gw = player_gw.join(
            players.select("player_id", "player_code", "team_code", "position"),
            on="player_id",
            how="left",
        )
        join_logs.append(log_join(f"player_gw:{slice_.key}", player_gw, players, player_gw, ["player_id"]))

    fixtures = None
    if fixtures_raw is not None:
        fx = normalize_matches(fixtures_raw, slice_.gw, slice_.competition).with_columns(
            pl.lit(season).alias("season")
        )
        fixtures = filter_valid_fixtures(fx).with_columns(kickoff_utc_expr())

    return SliceBuild(
        player_match=player_match,
        team_match=team_match,
        player_gw=player_gw,
        fixtures=fixtures,
        join_logs=join_logs,
        schema_reports=reports,
        missing_files=missing,
        source_files=used,
    )


def load_fixtures_only(slice_: GwSlice, season: str) -> pl.DataFrame | None:
    raw = read_csv(slice_.path / "fixtures.csv")
    if raw is None:
        return None
    fx = normalize_matches(raw, slice_.gw, slice_.competition).with_columns(
        pl.lit(season).alias("season")
    )
    return filter_valid_fixtures(fx).with_columns(kickoff_utc_expr())


def concat_or_none(frames: list[pl.DataFrame]) -> pl.DataFrame | None:
    frames = [f for f in frames if f is not None and f.height]
    if not frames:
        return None
    return pl.concat(frames, how="diagonal_relaxed")


FLOAT_MEASURES = (
    "minutes",
    "xg",
    "xa",
    "xgot",
    "np_xg",
    "set_piece_xg",
    "open_play_xg",
    "now_cost",
    "selected_by_percent",
    "form",
    "fpl_points",
    "expected_goals",
    "expected_assists",
    "xga",
    "possession",
    "elo",
)


def coerce_measures(df: pl.DataFrame) -> pl.DataFrame:
    casts = [
        as_float(pl.col(c)).alias(c)
        for c in FLOAT_MEASURES
        if c in df.columns
    ]
    return df.with_columns(casts) if casts else df


def finalize_player_match(
    df: pl.DataFrame,
    player_gw: pl.DataFrame | None,
    source_commit: str,
    ingested_at: str,
    source_files: list[str],
) -> pl.DataFrame:
    fpl_cols = [
        "total_points",
        "bonus",
        "bps",
        "now_cost",
        "selected_by_percent",
        "form",
        "penalties_order",
        "direct_freekicks_order",
        "corners_and_indirect_freekicks_order",
        "status",
        "own_goals",
    ]
    drop_if_present = [
        "fpl_points",
        "is_dgw",
        "gw_match_count",
        "gw_match_index",
        "source_commit",
        "ingested_at_utc",
        "source_files",
        "bonus",
        "bps",
        "now_cost",
        "selected_by_percent",
        "form",
        "penalties_order",
        "direct_freekicks_order",
        "corners_and_indirect_freekicks_order",
        "status",
    ]
    df = df.drop([c for c in drop_if_present if c in df.columns])
    if player_gw is not None:
        attach = player_gw.select(
            "season",
            "gw",
            "player_id",
            *[c for c in fpl_cols if c in player_gw.columns],
        ).unique(subset=["season", "gw", "player_id"], keep="first")
        rename = {"total_points": "fpl_points", "own_goals": "own_goals_gw"}
        attach = attach.rename({k: v for k, v in rename.items() if k in attach.columns})
        df = df.join(attach, on=["season", "gw", "player_id"], how="left")
        if "own_goals_gw" in df.columns:
            df = df.with_columns(pl.coalesce(["own_goals", "own_goals_gw"]).alias("own_goals")).drop("own_goals_gw")
    else:
        df = df.with_columns(
            pl.lit(None).alias("fpl_points"),
            *[pl.lit(None).alias(c) for c in fpl_cols if c != "own_goals" and c != "total_points"],
        )

    df = add_dgw_flags(df)
    df = coerce_measures(df)
    return add_provenance(df, source_commit, ingested_at, source_files)


def finalize_player_gw(
    df: pl.DataFrame,
    source_commit: str,
    ingested_at: str,
    source_files: list[str],
) -> pl.DataFrame:
    df = df.drop([c for c in ("source_commit", "ingested_at_utc", "source_files") if c in df.columns])
    df = df.unique(subset=["season", "gw", "player_id"], keep="first")
    df = coerce_measures(df)
    return add_provenance(df, source_commit, ingested_at, source_files)


def finalize_team_match(
    df: pl.DataFrame,
    source_commit: str,
    ingested_at: str,
    source_files: list[str],
) -> pl.DataFrame:
    df = df.drop([c for c in ("source_commit", "ingested_at_utc", "source_files") if c in df.columns])
    df = df.unique(subset=["season", "competition", "gw", "match_id", "team_code"], keep="first")
    df = coerce_measures(df)
    return add_provenance(df, source_commit, ingested_at, source_files)


def finalize_fixtures(
    df: pl.DataFrame,
    source_commit: str,
    ingested_at: str,
    source_files: list[str],
) -> pl.DataFrame:
    df = (
        df.unique(subset=["match_id"], keep="first")
        .filter(pl.col("home_team").is_not_null() & pl.col("away_team").is_not_null())
        .sort(["season", "gw", "kickoff_utc", "match_id"])
    )
    df = df.drop([c for c in ("source_commit", "ingested_at_utc", "source_files") if c in df.columns])
    keep = [
        "season",
        "competition",
        "gw",
        "match_id",
        "kickoff_utc",
        "home_team",
        "away_team",
        "finished",
        "tournament",
    ]
    existing = [c for c in keep if c in df.columns]
    return add_provenance(df.select(existing), source_commit, ingested_at, source_files)


def add_provenance(
    df: pl.DataFrame,
    source_commit: str,
    ingested_at: str,
    source_files: list[str],
) -> pl.DataFrame:
    files = ",".join(sorted(set(source_files))[:40])
    if len(set(source_files)) > 40:
        files += f",…(+{len(set(source_files)) - 40})"
    return df.with_columns(
        pl.lit(source_commit).alias("source_commit"),
        pl.lit(ingested_at).alias("ingested_at_utc"),
        pl.lit(files).alias("source_files"),
    )
