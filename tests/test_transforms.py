from __future__ import annotations

import polars as pl

from pipeline.schema_drift import SchemaDriftError, ValidationResult
from pipeline.io_utils import validate_columns
from pipeline.transforms import (
    add_dgw_flags,
    aggregate_shots,
    filter_valid_fixtures,
    own_goals_from_incidents,
    unpivot_team_match,
)


def test_unpivot_team_match_two_rows_and_result():
    matches = pl.DataFrame(
        {
            "season": ["2025-2026"],
            "competition": ["Premier League"],
            "gw": [1],
            "match_id": ["m1"],
            "home_team": [3],
            "away_team": [7],
            "finished": [True],
            "home_score": [2.0],
            "away_score": [1.0],
            "home_team_elo": [None],
            "away_team_elo": [0.0],
            "kickoff_raw": ["2025-08-16T15:00:00+00:00"],
            "tournament": ["prem"],
            "home_expected_goals_xg": [1.4],
            "away_expected_goals_xg": [0.6],
            "home_total_shots": [12],
            "away_total_shots": [8],
        }
    )
    out = unpivot_team_match(matches)
    assert out.height == 2
    home = out.filter(pl.col("is_home")).row(0, named=True)
    away = out.filter(~pl.col("is_home")).row(0, named=True)
    assert home["team_code"] == 3
    assert home["opponent_code"] == 7
    assert home["goals_for"] == 2
    assert home["result"] == "W"
    assert home["points"] == 3
    assert home["clean_sheet"] is False
    assert away["result"] == "L"
    assert away["points"] == 0
    assert home["xg"] == 1.4
    assert away["xg"] == 0.6


def test_shots_split_does_not_invent_bcc():
    shots = pl.DataFrame(
        {
            "match_id": ["m1", "m1", "m1"],
            "player_id": [10, 10, 10],
            "situation": ["penalty", "assisted", "corner"],
            "xg": [0.76, 0.20, 0.10],
        }
    )
    agg = aggregate_shots(shots).row(0, named=True)
    assert abs(agg["np_xg"] - 0.30) < 1e-9
    assert abs(agg["open_play_xg"] - 0.20) < 1e-9
    assert abs(agg["set_piece_xg"] - 0.10) < 1e-9
    assert agg["penalty_shots"] == 1
    assert "big_chances_created" not in agg


def test_own_goals_from_incidents():
    incidents = pl.DataFrame(
        {
            "match_id": ["m1", "m1", "m1"],
            "player_id": [1, 1, 2],
            "incident_type": ["goal", "goal", "card"],
            "goal_type": ["ownGoal", "regular", None],
        }
    )
    ogs = own_goals_from_incidents(incidents)
    assert ogs.height == 1
    assert ogs.row(0, named=True) == {"match_id": "m1", "player_id": 1, "own_goals": 1}


def test_skip_fixtures_with_null_team_codes():
    fx = pl.DataFrame(
        {
            "finished": [False, False, True],
            "home_team": [None, 3, 3],
            "away_team": [7, 9, 9],
            "match_id": ["a", "b", "c"],
        }
    )
    out = filter_valid_fixtures(fx)
    assert out.height == 1
    assert out["match_id"].to_list() == ["b"]


def test_dgw_flags():
    df = pl.DataFrame(
        {
            "season": ["2026-2027"] * 3,
            "competition": ["Premier League", "Premier League", "EFL Cup"],
            "gw": [10, 10, 10],
            "player_id": [1, 1, 1],
            "match_id": ["pl-a", "pl-b", "cup"],
            "kickoff_utc": [
                "2026-10-01T12:00:00Z",
                "2026-10-01T19:00:00Z",
                "2026-09-30T19:00:00Z",
            ],
        }
    )
    out = add_dgw_flags(df)
    assert set(out["gw_match_count"].to_list()) == {3}
    assert set(out["is_dgw"].to_list()) == {True}
    assert out.sort("kickoff_utc")["gw_match_index"].to_list() == [1, 2, 3]


def test_schema_drift_fails_loudly():
    df = pl.DataFrame({"player_id": [1]})
    report = validate_columns("playermatchstats", __import__("pathlib").Path("x.csv"), df)
    assert "match_id" in report.missing
    result = ValidationResult(reports=[report])
    try:
        result.fail_if_drift()
        raise AssertionError("expected SchemaDriftError")
    except SchemaDriftError as exc:
        assert "match_id" in str(exc)


def test_nulls_not_filled_with_zero():
    matches = pl.DataFrame(
        {
            "season": ["2026-2027"],
            "competition": ["Friendlies"],
            "gw": [0],
            "match_id": ["f1"],
            "home_team": [3],
            "away_team": [7],
            "finished": [True],
            "home_score": [1.0],
            "away_score": [1.0],
            "home_team_elo": [None],
            "away_team_elo": [None],
            "kickoff_raw": [None],
            "tournament": ["friendlies"],
        }
    )
    out = unpivot_team_match(matches)
    assert out["elo"].null_count() == 2
    assert "xg" not in out.columns or out["xg"].null_count() == 2
