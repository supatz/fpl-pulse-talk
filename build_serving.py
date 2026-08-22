#!/usr/bin/env python3
"""Masters → small per-view JSON. Never writes Parquet. Safe to re-run after UI-only work."""

from __future__ import annotations

import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master"
SERVING = ROOT / "serving"
WEB_DATA = ROOT / "web" / "data"
CACHE = ROOT / ".cache" / "FPL-Core-Insights" / "data"
SOURCE = "olbauday/FPL-Core-Insights"
FDR_URL = "https://premierfantasytools.com/fpl-fixture-difficulty/"
WINDOWS = (5, 10, 15)
HOME_NUDGE = 1.08
SCHEMA_VERSION = 1
PL = "Premier League"

SUM_KEYS = {
    "G": "goals",
    "A": "assists",
    "PenG": "penalties_scored",
    "xG": "xg",
    "xA": "xa",
    "Sh": "total_shots",
    "SoT": "shots_on_target",
    "CC": "chances_created",
    "TiB": "touches_opposition_box",
    "BCM": "big_chances_missed",
    "xGOT": "xgot",
    "Saves": "saves",
    "GC": "goals_conceded",
    "xGOTf": "xgot_faced",
    "xGP": "goals_prevented",
    "Tkl": "tackles_num",
    "CBI": "cbi",
    "DefCon": "defcon",
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load(table: str) -> pl.DataFrame:
    files = list((MASTER / table).rglob("*.parquet"))
    if not files:
        return pl.DataFrame()
    return pl.concat([pl.read_parquet(p) for p in files], how="diagonal_relaxed")


def _f(df: pl.DataFrame, cols: list[str]) -> pl.DataFrame:
    casts = [pl.col(c).cast(pl.Float64, strict=False).alias(c) for c in cols if c in df.columns]
    return df.with_columns(casts) if casts else df


def _round(v, nd=2):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return None
    if isinstance(v, (int, float)):
        return round(float(v), nd)
    return v


def _clean(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        if v is None:
            out[k] = None
        elif isinstance(v, float):
            out[k] = None if math.isnan(v) else round(v, 3)
        elif isinstance(v, bool):
            out[k] = v
        else:
            out[k] = v
    return out


def _write(name: str, payload) -> str:
    SERVING.mkdir(parents=True, exist_ok=True)
    WEB_DATA.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    (SERVING / name).write_text(text + "\n", encoding="utf-8")
    shutil.copy2(SERVING / name, WEB_DATA / name)
    return name


def load_teams() -> pl.DataFrame:
    frames = []
    if CACHE.exists():
        for path in sorted(CACHE.glob("*/teams.csv")):
            frames.append(
                pl.read_csv(path, infer_schema_length=5000, null_values=["", "NA", "NaN"]).with_columns(
                    pl.lit(path.parent.name).alias("season")
                )
            )
    if not frames:
        return pl.DataFrame(
            {"team_code": pl.Series([], dtype=pl.Int64), "team": [], "short": []}
        )
    t = pl.concat(frames, how="diagonal_relaxed").with_columns(
        pl.col("code").cast(pl.Float64, strict=False).cast(pl.Int64).alias("team_code"),
        pl.col("name").cast(pl.Utf8).alias("team"),
        pl.col("short_name").cast(pl.Utf8).alias("short"),
        pl.col("strength_overall_home").cast(pl.Float64, strict=False),
        pl.col("strength_overall_away").cast(pl.Float64, strict=False),
    )
    # Prefer latest season names
    return t.sort("season").unique(subset=["team_code"], keep="last")


def current_roster_and_prices(gw: pl.DataFrame, current_season: str) -> tuple[list[int], dict[str, float]]:
    if gw.is_empty():
        return [], {}
    cur = gw.filter(pl.col("season") == current_season)
    if cur.is_empty():
        cur = gw
    codes = sorted({int(c) for c in cur["player_code"].drop_nulls().to_list()})
    latest = (
        cur.sort("gw")
        .group_by("player_code")
        .agg(pl.col("now_cost").last().alias("now_cost"))
    )
    prices = {}
    for r in latest.to_dicts():
        if r.get("player_code") is None:
            continue
        prices[str(int(r["player_code"]))] = _round(r.get("now_cost"), 1)
    return codes, prices


def build_player_matches(pm: pl.DataFrame, gw: pl.DataFrame, teams: pl.DataFrame) -> list[dict]:
    if pm.is_empty():
        return []
    extra = [
        "final_third_passes",
        "successful_dribbles",
        "yellow_cards",
        "aerial_duels_won",
        "saves_inside_box",
        "high_claim",
        "sweeper_actions",
        "np_xg",
        "recoveries",
    ]
    pm = prepare_player_match(pm)
    pm = _f(pm, extra)
    if not gw.is_empty():
        pts = gw.select(
            "season",
            "player_id",
            "gw",
            pl.col("total_points").cast(pl.Float64, strict=False).alias("pts"),
            pl.col("clean_sheets").cast(pl.Float64, strict=False).alias("cs"),
        ).unique(subset=["season", "player_id", "gw"], keep="last")
        pm = pm.join(pts, on=["season", "player_id", "gw"], how="left")
    else:
        pm = pm.with_columns(pl.lit(None).alias("pts"), pl.lit(None).alias("cs"))
    pm = pm.join(teams.select("team_code", "short"), on="team_code", how="left")
    keep = {
        "season": "s",
        "competition": "c",
        "gw": "gw",
        "match_id": "mid",
        "player_id": "pid",
        "player_code": "pc",
        "web_name": "n",
        "team_code": "tc",
        "short": "tm",
        "position": "pos",
        "is_home": "h",
        "minutes": "m",
        "goals": "G",
        "assists": "A",
        "penalties_scored": "PenG",
        "xg": "xG",
        "xa": "xA",
        "xgi": "xGI",
        "total_shots": "Sh",
        "shots_on_target": "SoT",
        "chances_created": "CC",
        "touches_opposition_box": "TiB",
        "big_chances_missed": "BCM",
        "xgot": "xGOT",
        "saves": "Sv",
        "goals_conceded": "GC",
        "xgot_faced": "xGOTf",
        "goals_prevented": "xGP",
        "tackles_num": "Tkl",
        "cbi": "CBI",
        "defcon": "DefCon",
        "np_xg": "npxG",
        "final_third_passes": "F3",
        "successful_dribbles": "Dr",
        "yellow_cards": "YC",
        "aerial_duels_won": "Aer",
        "clearances": "Clr",
        "interceptions": "Int",
        "blocks": "Blk",
        "recoveries": "Rec",
        "saves_inside_box": "SiB",
        "high_claim": "HC",
        "sweeper_actions": "SW",
        "pts": "pts",
        "cs": "cs",
    }
    exprs = []
    for src, dest in keep.items():
        if src in pm.columns:
            exprs.append(pl.col(src).alias(dest))
        else:
            exprs.append(pl.lit(None).alias(dest))
    slim = pm.select(exprs).filter(pl.col("m").is_not_null())
    return [_clean(r) for r in slim.to_dicts()]


def prepare_player_match(pm: pl.DataFrame) -> pl.DataFrame:
    if pm.is_empty():
        return pm
    pm = _f(
        pm,
        [
            "minutes",
            "goals",
            "assists",
            "penalties_scored",
            "xg",
            "xa",
            "total_shots",
            "shots_on_target",
            "chances_created",
            "touches_opposition_box",
            "big_chances_missed",
            "xgot",
            "saves",
            "goals_conceded",
            "xgot_faced",
            "goals_prevented",
            "tackles",
            "tackles_won",
            "clearances",
            "blocks",
            "interceptions",
            "defensive_contributions",
            "fpl_points",
        ],
    )
    tackles = (
        pl.coalesce([pl.col("tackles"), pl.col("tackles_won")])
        if "tackles" in pm.columns
        else pl.col("tackles_won")
    )
    cbi = pl.col("clearances").fill_null(0) + pl.col("blocks").fill_null(0) + pl.col("interceptions").fill_null(0)
    # CBI should be null if all three missing
    all_null = (
        pl.col("clearances").is_null() & pl.col("blocks").is_null() & pl.col("interceptions").is_null()
    )
    return pm.with_columns(
        tackles.alias("tackles_num"),
        pl.when(all_null).then(None).otherwise(cbi).alias("cbi"),
        pl.col("defensive_contributions").alias("defcon")
        if "defensive_contributions" in pm.columns
        else pl.lit(None).alias("defcon"),
        (pl.col("xg").fill_null(0) + pl.col("xa").fill_null(0)).alias("xgi_raw"),
        pl.when(pl.col("xg").is_null() & pl.col("xa").is_null())
        .then(None)
        .otherwise(pl.col("xg").fill_null(0) + pl.col("xa").fill_null(0))
        .alias("xgi"),
    )


def window_rows(matches: pl.DataFrame, n: int) -> pl.DataFrame:
    return (
        matches.sort(["player_id", "competition", "kickoff_utc", "match_id"])
        .with_columns(pl.int_range(0, pl.len()).over(["player_id", "competition"]).alias("_i"))
        .with_columns(pl.len().over(["player_id", "competition"]).alias("_n"))
        .filter(pl.col("_i") >= pl.col("_n") - n)
    )


def aggregate_window(chunk: pl.DataFrame, suffix: str, gw_pts: pl.DataFrame) -> pl.DataFrame:
    aggs = [
        pl.len().alias(f"apps{suffix}"),
        pl.col("minutes").sum().alias(f"mins{suffix}"),
        pl.col("gw").min().alias(f"gw_from{suffix}"),
        pl.col("gw").max().alias(f"gw_to{suffix}"),
    ]
    for key, src in SUM_KEYS.items():
        if src in chunk.columns:
            aggs.append(pl.col(src).sum().alias(f"{key}{suffix}"))
        else:
            aggs.append(pl.lit(None).alias(f"{key}{suffix}"))
    if "xgi" in chunk.columns:
        aggs.append(pl.col("xgi").sum().alias(f"xGI{suffix}"))
    rolled = chunk.group_by(["season", "competition", "player_id"]).agg(aggs)

    keys = chunk.select(["season", "player_id", "gw"]).unique()
    pts = (
        gw_pts.join(keys, on=["season", "player_id", "gw"], how="inner")
        .group_by(["season", "player_id"])
        .agg(
            pl.col("total_points").sum().alias(f"Pts{suffix}"),
            pl.col("clean_sheets").sum().alias(f"CS{suffix}"),
        )
    )
    # Points/CS are PL-only; attach on player_id+season then copy onto every competition row
    return rolled.join(pts, on=["season", "player_id"], how="left")


def career_mins(matches: pl.DataFrame) -> pl.DataFrame:
    apps = matches.filter(pl.col("minutes").is_not_null() & (pl.col("minutes") > 0))
    return apps.group_by(["season", "competition", "player_id"]).agg(
        pl.col("minutes").mean().alias("mins_per_app"),
        pl.len().alias("apps"),
        pl.col("web_name").last().alias("player"),
        pl.col("team_code").last().alias("team_code"),
        pl.col("position").last().alias("pos"),
    )


def build_all_comp_matches(pm: pl.DataFrame) -> pl.DataFrame:
    tagged = pm.with_columns(pl.lit("all").alias("competition"))
    return pl.concat([pm, tagged], how="diagonal_relaxed")


def build_player_files(pm: pl.DataFrame, gw: pl.DataFrame, teams: pl.DataFrame) -> dict[str, list]:
    if pm.is_empty():
        return {"attackers": [], "defenders": [], "gk": []}
    pm = prepare_player_match(pm)
    finished = pm.filter(pl.col("finished").fill_null(False) | pl.col("minutes").is_not_null())
    finished = finished.filter(pl.col("minutes").is_not_null())
    finished = build_all_comp_matches(finished)

    ident = career_mins(finished)
    ident = ident.join(teams.select("team_code", "team", "short"), on="team_code", how="left")

    gw_slim = pl.DataFrame()
    if not gw.is_empty():
        gw_slim = gw.select(
            "season",
            "player_id",
            "gw",
            pl.col("total_points").cast(pl.Float64, strict=False),
            pl.col("clean_sheets").cast(pl.Float64, strict=False),
        )

    parts = [ident]
    for n in WINDOWS:
        w = window_rows(finished, n)
        if gw_slim.is_empty():
            empty_gw = pl.DataFrame(
                {
                    "season": pl.Series([], dtype=pl.Utf8),
                    "player_id": pl.Series([], dtype=pl.Int64),
                    "gw": pl.Series([], dtype=pl.Int64),
                    "total_points": pl.Series([], dtype=pl.Float64),
                    "clean_sheets": pl.Series([], dtype=pl.Float64),
                }
            )
            parts.append(aggregate_window(w, f"_{n}", empty_gw))
        else:
            parts.append(aggregate_window(w, f"_{n}", gw_slim))

    out = parts[0]
    for p in parts[1:]:
        out = out.join(p, on=["season", "competition", "player_id"], how="left")

    rows = [_clean(r) for r in out.to_dicts()]
    attackers = [r for r in rows if r.get("pos") in {"Forward", "Midfielder"}]
    defenders = [r for r in rows if r.get("pos") == "Defender"]
    gk = [r for r in rows if r.get("pos") == "Goalkeeper"]
    return {"attackers": attackers, "defenders": defenders, "gk": gk}


def build_insights(attackers: list[dict], season: str) -> dict:
    pl_rows = [r for r in attackers if r.get("competition") == PL and r.get("season") == season]

    def top(key, n=8, pred=None):
        pool = [r for r in pl_rows if r.get(key) is not None]
        if pred:
            pool = [r for r in pool if pred(r)]
        pool.sort(key=lambda r: r.get(key) or 0, reverse=True)
        return [
            {
                "player": r.get("player"),
                "team": r.get("short") or r.get("team"),
                "value": r.get(key),
                "mins_per_app": r.get("mins_per_app"),
            }
            for r in pool[:n]
        ]

    rising = []
    for r in pl_rows:
        cur = r.get("xGI_5")
        # prior-5 is not stored separately; approximate with (xGI_10 - xGI_5)
        ten = r.get("xGI_10")
        mins5 = r.get("mins_5") or 0
        mins10 = r.get("mins_10") or 0
        prior_mins = (mins10 or 0) - (mins5 or 0)
        if cur is None or ten is None or mins5 < 180 or prior_mins < 180:
            continue
        prior = ten - cur
        cur90 = cur * 90 / mins5
        prior90 = prior * 90 / prior_mins
        delta = cur90 - prior90
        rising.append({**r, "rise": round(delta, 3), "cur90": round(cur90, 3), "prior90": round(prior90, 3)})
    rising.sort(key=lambda r: r["rise"], reverse=True)

    finish = []
    for r in pl_rows:
        g, xg, mins = r.get("G_15"), r.get("xG_15"), r.get("mins_15") or 0
        if g is None or xg is None or mins < 450:
            continue
        finish.append({**r, "over": round(g - xg, 3)})
    finish.sort(key=lambda r: abs(r["over"]), reverse=True)

    quiet = []
    for r in pl_rows:
        xgi, g, a, mins = r.get("xGI_10"), r.get("G_10"), r.get("A_10"), r.get("mins_10") or 0
        if xgi is None or mins < 300:
            continue
        ret = (g or 0) + (a or 0)
        if xgi >= 1.5 and ret <= xgi * 0.55:
            quiet.append({**r, "xGI": xgi, "return": ret, "gap": round(xgi - ret, 3)})
    quiet.sort(key=lambda r: r["gap"], reverse=True)

    def slim(r, extra):
        base = {"player": r.get("player"), "team": r.get("short") or r.get("team"), "mins_per_app": r.get("mins_per_app")}
        base.update(extra)
        return base

    return {
        "top_xgi5": top("xGI_5"),
        "rising_xgi90": [slim(r, {"value": r["rise"], "cur90": r["cur90"], "prior90": r["prior90"]}) for r in rising[:8]],
        "finishing": [slim(r, {"value": r["over"], "G": r.get("G_15"), "xG": r.get("xG_15")}) for r in finish[:8]],
        "high_xgi_low_return": [slim(r, {"value": r["gap"], "xGI": r["xGI"], "return": r["return"]}) for r in quiet[:8]],
    }


def build_teams_gw(tm: pl.DataFrame, teams: pl.DataFrame) -> list[dict]:
    if tm.is_empty():
        return []
    tm = _f(tm, ["goals_for", "goals_against", "xg", "xga", "possession", "total_shots", "shots_on_target", "points"])
    tm = tm.with_columns(
        pl.when(pl.col("total_shots").is_not_null())
        .then(pl.col("total_shots").cast(pl.Float64, strict=False))
        .otherwise(None)
        .alias("shots")
    )
    tm = tm.join(teams.select("team_code", "team", "short"), on="team_code", how="left")
    opp = teams.select(pl.col("team_code").alias("opponent_code"), pl.col("short").alias("opp"))
    tm = tm.join(opp, on="opponent_code", how="left")
    keep = [
        "season",
        "competition",
        "gw",
        "match_id",
        "team_code",
        "team",
        "short",
        "opponent_code",
        "opp",
        "is_home",
        "finished",
        "goals_for",
        "goals_against",
        "xg",
        "xga",
        "shots",
        "shots_on_target",
        "possession",
        "points",
        "clean_sheet",
        "result",
    ]
    cols = [c for c in keep if c in tm.columns]
    return [_clean(r) for r in tm.select(cols).sort(["season", "competition", "team_code", "gw"]).to_dicts()]


def team_rates(tm: pl.DataFrame, season: str, n: int = 10) -> dict[int, dict]:
    plm = tm.filter(
        (pl.col("competition") == PL)
        & (pl.col("season") == season)
        & pl.col("finished").fill_null(False)
        & pl.col("team_code").is_not_null()
    )
    if plm.is_empty():
        return {}
    plm = _f(plm, ["xg", "xga", "goals_for", "goals_against"])
    last = (
        plm.sort(["team_code", "gw", "kickoff_utc"])
        .with_columns(pl.int_range(0, pl.len()).over("team_code").alias("_i"))
        .with_columns(pl.len().over("team_code").alias("_n"))
        .filter(pl.col("_i") >= pl.col("_n") - n)
        .group_by("team_code")
        .agg(
            pl.col("xg").mean().alias("xgf"),
            pl.col("xga").mean().alias("xga"),
            pl.col("goals_for").mean().alias("gf"),
            pl.col("goals_against").mean().alias("ga"),
            pl.len().alias("apps"),
        )
    )
    return {int(r["team_code"]): r for r in last.to_dicts() if r.get("team_code") is not None}


def season_totals(tm: pl.DataFrame, season: str) -> dict[int, dict]:
    plm = tm.filter((pl.col("competition") == PL) & (pl.col("season") == season) & pl.col("finished").fill_null(False))
    if plm.is_empty():
        return {}
    plm = _f(plm, ["goals_for", "goals_against"])
    g = plm.group_by("team_code").agg(
        pl.col("goals_for").sum().alias("gf"),
        pl.col("goals_against").sum().alias("ga"),
        pl.len().alias("apps"),
    )
    return {int(r["team_code"]): r for r in g.to_dicts() if r.get("team_code") is not None}


def standout_attackers(attackers: list[dict], season: str) -> dict[int, dict]:
    best: dict[int, dict] = {}
    for r in attackers:
        if r.get("season") != season or r.get("competition") != PL:
            continue
        code = r.get("team_code")
        if code is None:
            continue
        cur = best.get(int(code))
        if cur is None or (r.get("xGI_5") or -1) > (cur.get("xGI_5") or -1):
            best[int(code)] = r
    return best


def predict_xg(home_code, away_code, rates, promoted: set[int]) -> tuple:
    hr = rates.get(home_code, {})
    ar = rates.get(away_code, {})
    hxgf, hxga = hr.get("xgf"), hr.get("xga")
    axgf, axga = ar.get("xgf"), ar.get("xga")
    est_h = home_code in promoted or hxgf is None
    est_a = away_code in promoted or axgf is None
    # Neutral league average fallback
    lg_xgf = 1.35
    hxgf = hxgf if hxgf is not None else lg_xgf
    hxga = hxga if hxga is not None else lg_xgf
    axgf = axgf if axgf is not None else lg_xgf
    axga = axga if axga is not None else lg_xgf
    pred_h = 0.5 * (hxgf + axga) * HOME_NUDGE
    pred_a = 0.5 * (axgf + hxga)
    return _round(pred_h, 2), _round(pred_a, 2), est_h, est_a


def difficulty(opp_code: int, is_home: bool, teams: pl.DataFrame, rates: dict) -> int:
    row = teams.filter(pl.col("team_code") == opp_code)
    if row.height:
        col = "strength_overall_away" if is_home else "strength_overall_home"
        if col in row.columns:
            val = row[col][0]
            if val is not None and val > 0:
                return int(max(1, min(5, round(float(val)))))
    # Fallback: rank opponent xgf (higher attack = harder)
    xgf = (rates.get(opp_code) or {}).get("xgf")
    if xgf is None:
        return 3
    if xgf >= 1.8:
        return 5
    if xgf >= 1.5:
        return 4
    if xgf >= 1.2:
        return 3
    if xgf >= 0.95:
        return 2
    return 1


def build_fixtures(
    fx: pl.DataFrame,
    tm: pl.DataFrame,
    teams: pl.DataFrame,
    attackers: list[dict],
    current_season: str,
    prior_season: str,
) -> dict:
    rates = team_rates(tm, prior_season, 10)
    if not rates:
        rates = team_rates(tm, current_season, 10)
    prior_tot = season_totals(tm, prior_season)
    stars = standout_attackers(attackers, prior_season) or standout_attackers(attackers, current_season)

    prior_pl_codes = set()
    if not tm.is_empty():
        prior_pl_codes = set(
            tm.filter((pl.col("season") == prior_season) & (pl.col("competition") == PL) & pl.col("team_code").is_not_null())[
                "team_code"
            ].to_list()
        )
    current_pl = set()
    if not fx.is_empty():
        current_pl = set(
            fx.filter((pl.col("season") == current_season) & (pl.col("competition") == PL))["home_team"].to_list()
        ) | set(
            fx.filter((pl.col("season") == current_season) & (pl.col("competition") == PL))["away_team"].to_list()
        )
    promoted = {int(c) for c in current_pl if c is not None and int(c) not in {int(x) for x in prior_pl_codes if x is not None}}

    name = {int(r["team_code"]): r for r in teams.to_dicts() if r.get("team_code") is not None}

    upcoming = []
    if not fx.is_empty():
        rows = fx.filter(~pl.col("finished").fill_null(False)).sort(["kickoff_utc", "gw", "match_id"])
        for i, r in enumerate(rows.to_dicts()):
            h, a = r.get("home_team"), r.get("away_team")
            if h is None or a is None:
                continue
            h, a = int(h), int(a)
            ph, pa, eh, ea = predict_xg(h, a, rates, promoted)
            hs = stars.get(h) or {}
            aws = stars.get(a) or {}
            ht = prior_tot.get(h) or {}
            at = prior_tot.get(a) or {}
            upcoming.append(
                _clean(
                    {
                        "id": f"fx-{i+1}",
                        "season": r.get("season"),
                        "competition": r.get("competition"),
                        "gw": r.get("gw"),
                        "kickoff_utc": r.get("kickoff_utc"),
                        "match_id": r.get("match_id"),
                        "home_code": h,
                        "away_code": a,
                        "home": (name.get(h) or {}).get("team"),
                        "away": (name.get(a) or {}).get("team"),
                        "home_short": (name.get(h) or {}).get("short"),
                        "away_short": (name.get(a) or {}).get("short"),
                        "pred_home": ph,
                        "pred_away": pa,
                        "estimate_home": eh or h in promoted,
                        "estimate_away": ea or a in promoted,
                        "home_star": hs.get("player"),
                        "away_star": aws.get("player"),
                        "home_gf": _round((ht.get("gf") or 0) / ht["apps"], 2) if ht.get("apps") else None,
                        "home_ga": _round((ht.get("ga") or 0) / ht["apps"], 2) if ht.get("apps") else None,
                        "away_gf": _round((at.get("gf") or 0) / at["apps"], 2) if at.get("apps") else None,
                        "away_ga": _round((at.get("ga") or 0) / at["apps"], 2) if at.get("apps") else None,
                    }
                )
            )

    # Next-6-GW ticker for current-season PL
    ticker = []
    pl_fx = [u for u in upcoming if u.get("competition") == PL and u.get("season") == current_season]
    by_team: dict[int, list] = {}
    for u in pl_fx:
        by_team.setdefault(u["home_code"], []).append({**u, "is_home": True, "opp_code": u["away_code"]})
        by_team.setdefault(u["away_code"], []).append({**u, "is_home": False, "opp_code": u["home_code"]})
    for code, items in sorted(by_team.items(), key=lambda kv: (name.get(kv[0]) or {}).get("short") or ""):
        items = sorted(items, key=lambda x: (x.get("gw") or 99, x.get("kickoff_utc") or ""))[:6]
        cells = []
        for it in items:
            opp = it["opp_code"]
            cells.append(
                {
                    "gw": it.get("gw"),
                    "opp": (name.get(opp) or {}).get("short") or str(opp),
                    "venue": "H" if it["is_home"] else "A",
                    "diff": difficulty(opp, it["is_home"], teams, rates),
                }
            )
        ticker.append(
            {
                "team_code": code,
                "team": (name.get(code) or {}).get("team"),
                "short": (name.get(code) or {}).get("short"),
                "fixtures": cells,
            }
        )

    next_gw = None
    if pl_fx:
        next_gw = min(u["gw"] for u in pl_fx if u.get("gw") is not None)

    return {
        "upcoming": upcoming,
        "ticker": ticker,
        "fdr_url": FDR_URL,
        "next_gw": next_gw,
        "promoted": sorted(promoted),
    }


def build_players_gw(gw: pl.DataFrame, teams: pl.DataFrame, season: str) -> list[dict]:
    if gw.is_empty():
        return []
    df = gw.filter(pl.col("season") == season).select(
        "player_id",
        "gw",
        "web_name",
        "team_code",
        "position",
        "total_points",
        "now_cost",
        "selected_by_percent",
        "form",
        "minutes",
        "status",
    )
    df = df.join(teams.select("team_code", "short"), on="team_code", how="left")
    return [_clean(r) for r in df.sort(["player_id", "gw"]).to_dicts()]


def pick_seasons(pm: pl.DataFrame, fx: pl.DataFrame) -> tuple[str, str]:
    seasons = sorted(set(pm["season"].to_list()) | (set(fx["season"].to_list()) if not fx.is_empty() else set()))
    current = seasons[-1] if seasons else "2026-2027"
    prior = seasons[-2] if len(seasons) > 1 else current
    return current, prior


def build_from_disk() -> dict:
    pm = _load("player_match")
    gw = _load("player_gw")
    tm = _load("team_match")
    fx = _load("fixtures")
    teams = load_teams()
    current, prior = pick_seasons(pm, fx)

    matches = build_player_matches(pm, gw, teams)
    players = build_player_files(pm, gw, teams)
    insights = build_insights(players["attackers"], prior)
    teams_gw = build_teams_gw(tm, teams)
    fixtures = build_fixtures(fx, tm, teams, players["attackers"], current, prior)
    players_gw = build_players_gw(gw, teams, current)
    roster, prices = current_roster_and_prices(gw, current)
    seasons = sorted({r.get("s") for r in matches if r.get("s")})
    competitions = sorted({r.get("c") for r in matches if r.get("c")})
    if not competitions:
        competitions = [PL]

    meta = {
        "schema_version": SCHEMA_VERSION + 1,
        "built_at_utc": _now(),
        "source": SOURCE,
        "source_url": "https://github.com/olbauday/FPL-Core-Insights",
        "current_season": current,
        "analysis_season": prior,
        "seasons": seasons,
        "upcoming_gw": fixtures.get("next_gw"),
        "windows": list(range(1, 39)),
        "insight_windows": list(range(1, 11)),
        "default_competition": PL,
        "competitions": competitions,
        "roster_codes": roster,
        "prices": prices,
        "counts": {
            "matches": len(matches),
            "teams_gw": len(teams_gw),
            "fixtures": len(fixtures.get("upcoming") or []),
            "roster": len(roster),
        },
        "notes": [
            "Football tables use player_match (Opta). FPL Pts/CS come from player_gw and are Premier League only.",
            "Big chances created is not available; CC, xA and TiB are creation proxies.",
            "now_cost is already in £m. Price column is the current-season FPL price.",
            "Predicted xG blends a team's recent xG-for with the opponent's xG-against, with a small home nudge.",
            "Current-squad filter hides players who are not in this season's FPL list.",
        ],
        "fdr_url": FDR_URL,
    }

    written = [
        _write("meta.json", meta),
        _write("players_matches.json", matches),
        _write("players_gw.json", players_gw),
        _write("fixtures.json", fixtures),
        _write("teams_gw.json", teams_gw),
        _write("insights.json", insights),
    ]
    print("serving wrote", ", ".join(written))
    return {"meta": meta, "written": written}


def main() -> int:
    build_from_disk()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
