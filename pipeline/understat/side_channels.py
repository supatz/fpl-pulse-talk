"""Team shot side-channel (Left / Center / Right) for and against from Understat X/Y."""

from __future__ import annotations

import json
import math
from pathlib import Path

import polars as pl

from pipeline.understat.config import SERVING_DIR, WEB_DATA_DIR
from pipeline.understat.derive import _attach_team_codes
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
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    if WEB_DATA_DIR.exists():
        (WEB_DATA_DIR / path.name).write_text(text, encoding="utf-8")


def build_side_channels_serving(
    shots: pl.DataFrame,
    matches: pl.DataFrame,
    *,
    fpl_seasons: list[str] | None = None,
) -> dict:
    """Aggregate Understat shots into Left/Center/Right for and against per team × season × GW."""
    if shots.is_empty():
        payload = {
            "schema_version": 3,
            "source": "understat.com",
            "built_at_utc": now_utc(),
            "sides": ["Left", "Center", "Right"],
            "note": "Y thirds from attacking view: low Y=Right, mid=Center, high Y=Left.",
            "rows": [],
            "points": [],
        }
        _write_json(SERVING_DIR / "us_team_side_channels.json", payload)
        return payload

    s = _attach_team_codes(shots, matches).filter(
        pl.col("team_code").is_not_null()
        & pl.col("opponent_code").is_not_null()
        & (pl.col("result") != "OwnGoal")
    )
    if fpl_seasons:
        s = s.filter(pl.col("season").is_in(list(fpl_seasons)))

    # Join FPL GW from pl_merge match map when available
    gw_map = _fpl_gw_map()
    if gw_map is not None and not gw_map.is_empty():
        s = s.join(gw_map, on=["season", "match_id"], how="left")
    else:
        s = s.with_columns(pl.lit(None, pl.Int64).alias("gw"))

    y = pl.col("y").cast(pl.Float64, strict=False)
    s = s.with_columns(
        pl.when(y.is_null())
        .then(None)
        .when(y < 1.0 / 3.0)
        .then(pl.lit("Right"))
        .when(y > 2.0 / 3.0)
        .then(pl.lit("Left"))
        .otherwise(pl.lit("Center"))
        .alias("side")
    ).filter(pl.col("side").is_not_null())

    for_rows = (
        s.group_by(["season", "gw", "team_code", "team", "team_short", "side"])
        .agg(
            pl.len().alias("shots"),
            pl.col("xg").sum().alias("xg"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
        )
        .with_columns(pl.lit("for").alias("dir"))
    )
    against_rows = (
        s.group_by(["season", "gw", "opponent_code", "opponent", "opponent_short", "side"])
        .agg(
            pl.len().alias("shots"),
            pl.col("xg").sum().alias("xg"),
            pl.col("is_goal").fill_null(False).sum().alias("goals"),
        )
        .rename(
            {
                "opponent_code": "team_code",
                "opponent": "team",
                "opponent_short": "team_short",
            }
        )
        .with_columns(pl.lit("against").alias("dir"))
    )
    all_rows = pl.concat([for_rows, against_rows], how="diagonal_relaxed").sort(
        ["season", "team_code", "gw", "dir", "side"]
    )

    rows = []
    for r in all_rows.to_dicts():
        rows.append(
            {
                "season": r.get("season"),
                "gw": r.get("gw"),
                "team_code": int(r["team_code"]) if r.get("team_code") is not None else None,
                "team": r.get("team"),
                "team_short": r.get("team_short"),
                "dir": r.get("dir"),
                "side": r.get("side"),
                "shots": int(r.get("shots") or 0),
                "xg": _round(r.get("xg")),
                "goals": int(r.get("goals") or 0),
            }
        )

    # Per-shot points for pitch viz (compact keys). Against = defending team_code.
    # Assister xA = shot xG when player_assisted is set (Understat convention).
    points = []
    for r in s.select(
        "season",
        "gw",
        "team_code",
        "team_short",
        "opponent_code",
        "opponent_short",
        "player_name",
        "player_assisted",
        "x",
        "y",
        "xg",
        "is_goal",
        "side",
    ).to_dicts():
        x = _round(r.get("x"), 3)
        y = _round(r.get("y"), 3)
        xg = _round(r.get("xg"), 3) or 0
        if x is None or y is None:
            continue
        gw = r.get("gw")
        season = r.get("season")
        goal = bool(r.get("is_goal"))
        side = r.get("side")
        shooter = (r.get("player_name") or "").strip() or None
        assister = (r.get("player_assisted") or "").strip() or None
        xa = xg if assister else None
        base = {
            "s": season,
            "gw": gw,
            "side": side,
            "x": x,
            "y": y,
            "xg": xg,
            "g": goal,
            "pn": shooter,
            "an": assister,
            "xa": xa,
        }
        tc = r.get("team_code")
        oc = r.get("opponent_code")
        if tc is not None:
            points.append(
                {
                    **base,
                    "tc": int(tc),
                    "tm": r.get("team_short"),
                    "dir": "for",
                }
            )
        if oc is not None:
            points.append(
                {
                    **base,
                    "tc": int(oc),
                    "tm": r.get("opponent_short"),
                    "dir": "against",
                }
            )

    payload = {
        "schema_version": 3,
        "source": "understat.com",
        "built_at_utc": now_utc(),
        "sides": ["Left", "Center", "Right"],
        "note": "Y thirds from attacking view: low Y=Right, mid=Center, high Y=Left. Against flips to the defending team. Pitch points include shooter (pn) + xG and assister (an) + xA (= shot xG when assisted).",
        "rows": rows,
        "points": points,
    }
    _write_json(SERVING_DIR / "us_team_side_channels.json", payload)
    return payload


def _fpl_gw_map() -> pl.DataFrame | None:
    """Map Understat match_id → FPL gw via pl_merge match_map."""
    from pipeline.pl_merge.config import MAPS_DIR

    path = MAPS_DIR / "match_map.csv"
    if not path.exists():
        return None
    m = pl.read_csv(path)
    cols = set(m.columns)
    if "understat_match_id" not in cols or "gw" not in cols:
        return None
    exprs = [
        pl.col("understat_match_id").cast(pl.Utf8).alias("match_id"),
        pl.col("gw").cast(pl.Int64),
    ]
    if "season" in cols:
        exprs.append(pl.col("season").cast(pl.Utf8))
        return m.select(exprs).unique(subset=["season", "match_id"])
    return m.select(exprs).unique(subset=["match_id"])
