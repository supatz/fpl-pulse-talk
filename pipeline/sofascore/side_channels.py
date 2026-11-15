"""Team shot side-channel from SofaScore coords (0–100, x from attacked goal)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import polars as pl

from pipeline.sofascore.config import MAPS_DIR, SERVING_DIR, WEB_DATA_DIR
from pipeline.sofascore.maps import load_team_map
from pipeline.sofascore.normalize import now_utc, side_channel


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


def _match_gw() -> pl.DataFrame:
    path = MAPS_DIR / "match_map.csv"
    if not path.exists():
        return pl.DataFrame()
    m = pl.read_csv(path)
    if m.is_empty():
        return pl.DataFrame()
    return m.select(
        pl.col("sofascore_event_id").cast(pl.Utf8).alias("event_id"),
        pl.col("gw").cast(pl.Int64),
        pl.col("season").cast(pl.Utf8) if "season" in m.columns else pl.lit(None).alias("season"),
    )


def build_side_channels_serving(
    shots: pl.DataFrame,
    matches: pl.DataFrame | None = None,
    *,
    fpl_seasons: list[str] | None = None,
) -> dict:
    note = (
        "SofaScore x is % from the attacked goal (0 = six-yard). Serving remaps to Understat-like "
        "x' = 1 − x/100 so attack plots toward the top. Y 0–100, high Y = Left (same as Understat). "
        "Against flips to the defending team. Circle size = SofaScore xG. Spider remains Opta."
    )
    if shots.is_empty():
        payload = {
            "schema_version": 1,
            "source": "sofascore.com",
            "built_at_utc": now_utc(),
            "sides": ["Left", "Center", "Right"],
            "note": note,
            "rows": [],
            "points": [],
        }
        _write_json(SERVING_DIR / "ss_team_side_channels.json", payload)
        return payload

    team_map = load_team_map().filter(pl.col("team_code").is_not_null())
    id_map = team_map.select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("team_id"),
        pl.col("team_code"),
        pl.col("fpl_name").alias("team"),
        pl.col("fpl_short").alias("team_short"),
    )
    opp_map = team_map.select(
        pl.col("sofascore_team_id").cast(pl.Utf8).alias("opponent_id"),
        pl.col("team_code").alias("opponent_code"),
        pl.col("fpl_name").alias("opponent"),
        pl.col("fpl_short").alias("opponent_short"),
    )
    s = (
        shots.with_columns(pl.col("team_id").cast(pl.Utf8), pl.col("opponent_id").cast(pl.Utf8), pl.col("event_id").cast(pl.Utf8))
        .join(id_map, on="team_id", how="left")
        .join(opp_map, on="opponent_id", how="left")
        .filter(
            pl.col("team_code").is_not_null()
            & pl.col("opponent_code").is_not_null()
            & ~pl.col("is_own_goal").fill_null(False)
        )
    )
    if fpl_seasons:
        s = s.filter(pl.col("season").is_in(list(fpl_seasons)))
    gw_map = _match_gw()
    if gw_map.height:
        s = s.join(gw_map.select("event_id", "gw"), on="event_id", how="left")
    else:
        s = s.with_columns(pl.lit(None, pl.Int64).alias("gw"))

    if "side" not in s.columns:
        sides = [side_channel(y) for y in s["y"].to_list()]
        s = s.with_columns(pl.Series("side", sides))
    s = s.filter(pl.col("side").is_not_null())

    for_rows = (
        s.group_by(["season", "gw", "team_code", "team", "team_short", "side"])
        .agg(pl.len().alias("shots"), pl.col("xg").sum().alias("xg"), pl.col("is_goal").fill_null(False).sum().alias("goals"))
        .with_columns(pl.lit("for").alias("dir"))
    )
    against_rows = (
        s.group_by(["season", "gw", "opponent_code", "opponent", "opponent_short", "side"])
        .agg(pl.len().alias("shots"), pl.col("xg").sum().alias("xg"), pl.col("is_goal").fill_null(False).sum().alias("goals"))
        .rename({"opponent_code": "team_code", "opponent": "team", "opponent_short": "team_short"})
        .with_columns(pl.lit("against").alias("dir"))
    )
    all_rows = pl.concat([for_rows, against_rows], how="diagonal_relaxed").sort(
        ["season", "team_code", "gw", "dir", "side"]
    )
    rows = [
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
        for r in all_rows.to_dicts()
    ]

    points = []
    for r in s.select(
        "season", "gw", "team_code", "team_short", "opponent_code", "opponent_short",
        "player_name", "x", "y", "xg", "is_goal", "side",
    ).to_dicts():
        x_raw = r.get("x")
        y_raw = r.get("y")
        if x_raw is None or y_raw is None:
            continue
        # native 0–100 → Understat-like 0–1 with near-goal as high x
        x = _round(1.0 - float(x_raw) / 100.0, 3)
        y = _round(float(y_raw) / 100.0, 3)
        xg = _round(r.get("xg"), 3) or 0
        base = {
            "s": r.get("season"),
            "gw": r.get("gw"),
            "side": r.get("side"),
            "x": x,
            "y": y,
            "xg": xg,
            "g": bool(r.get("is_goal")),
            "pn": (r.get("player_name") or "").strip() or None,
            "an": None,
            "xa": None,
        }
        if r.get("team_code") is not None:
            points.append({**base, "tc": int(r["team_code"]), "tm": r.get("team_short"), "dir": "for"})
        if r.get("opponent_code") is not None:
            points.append({**base, "tc": int(r["opponent_code"]), "tm": r.get("opponent_short"), "dir": "against"})

    payload = {
        "schema_version": 1,
        "source": "sofascore.com",
        "built_at_utc": now_utc(),
        "sides": ["Left", "Center", "Right"],
        "note": note,
        "rows": rows,
        "points": points,
    }
    _write_json(SERVING_DIR / "ss_team_side_channels.json", payload)
    return payload
