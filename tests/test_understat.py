"""Smoke tests for understat helpers (no network)."""

from __future__ import annotations

from pipeline.understat.maps import load_team_map
from pipeline.understat.zones import shot_zone


def test_team_map_unique_codes():
    m = load_team_map()
    assert m.height >= 20
    assert m["understat_team_id"].n_unique() == m.height
    assert m["team_code"].null_count() == 0


def test_shot_zones():
    assert shot_zone(0.95, 0.5) == "six_yard"
    assert shot_zone(0.88, 0.5) == "penalty_area"
    assert shot_zone(0.7, 0.5) == "outside_box"
    assert shot_zone(0.9, 0.5, result="OwnGoal") == "own_goal"
