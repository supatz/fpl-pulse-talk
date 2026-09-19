"""Tests for Premier League FPL × Understat merge helpers (no network)."""

from __future__ import annotations

import polars as pl

from pipeline.pl_merge.match_map import pair_matches
from pipeline.pl_merge.names import first_initial, last_name, normalize_name
from pipeline.pl_merge.player_map import match_players
from pipeline.understat.normalize import normalize_match_roster


def test_normalize_name_accents_and_punct():
    assert normalize_name("João Félix") == "joao felix"
    assert normalize_name("B.Fernandes") == "b fernandes"
    assert normalize_name("Matt O&#039;Riley") == "matt oriley"
    assert normalize_name("Martin Ødegaard") == "martin odegaard"
    assert last_name("Bruno Fernandes") == "fernandes"
    assert first_initial("Bruno Fernandes") == "b"


def test_player_override_wins():
    us = pl.DataFrame(
        {
            "understat_player_id": ["1"],
            "player_name": ["Wrong Name"],
            "seasons": ["2026-2027"],
            "team_codes": ["1"],
        }
    )
    fpl = pl.DataFrame(
        {
            "player_code": [99, 100],
            "player_id": [1, 2],
            "web_name": ["A", "B"],
            "team_code": [1, 1],
            "position": ["MID", "MID"],
            "first_name": ["Alpha", "Beta"],
            "second_name": ["One", "Two"],
            "season": ["2026-2027", "2026-2027"],
        }
    )
    ov = pl.DataFrame(
        {"understat_player_id": ["1"], "player_code": [100], "reason": ["manual"]}
    )
    accepted, amb, unmatched = match_players(us, fpl, overrides=ov)
    assert not amb and not unmatched
    assert accepted[0]["player_code"] == 100
    assert accepted[0]["method"] == "override"


def test_unique_last_initial_auto_accept():
    us = pl.DataFrame(
        {
            "understat_player_id": ["899"],
            "player_name": ["Bruno Fernandes"],
            "seasons": ["2026-2027"],
            "team_codes": ["1"],
        }
    )
    fpl = pl.DataFrame(
        {
            "player_code": [141746],
            "player_id": [10],
            "web_name": ["B.Fernandes"],
            "team_code": [1],
            "position": ["MID"],
            "first_name": ["Bruno"],
            "second_name": ["Fernandes"],
            "season": ["2026-2027"],
        }
    )
    accepted, amb, unmatched = match_players(us, fpl, overrides=pl.DataFrame())
    assert not amb and not unmatched
    assert accepted[0]["player_code"] == 141746


def test_name_collision_does_not_auto_accept():
    us = pl.DataFrame(
        {
            "understat_player_id": ["50"],
            "player_name": ["J. Murphy"],
            "seasons": ["2025-2026"],
            "team_codes": ["11"],
        }
    )
    fpl = pl.DataFrame(
        {
            "player_code": [11, 12],
            "player_id": [1, 2],
            "web_name": ["J.Murphy", "J.Murphy"],
            "team_code": [11, 11],
            "position": ["MID", "FWD"],
            "first_name": ["Jacob", "James"],
            "second_name": ["Murphy", "Murphy"],
            "season": ["2025-2026", "2025-2026"],
        }
    )
    accepted, amb, unmatched = match_players(us, fpl, overrides=pl.DataFrame())
    assert accepted == []
    assert amb or unmatched


def test_exact_name_beats_sibling_last_name():
    us = pl.DataFrame(
        {
            "understat_player_id": ["50"],
            "player_name": ["Lewis Miley"],
            "seasons": ["2025-2026"],
            "team_codes": ["4"],
        }
    )
    fpl = pl.DataFrame(
        {
            "player_code": [547719, 665243],
            "player_id": [1, 2],
            "web_name": ["L.Miley", "M.Miley"],
            "team_code": [4, 4],
            "position": ["MID", "GK"],
            "first_name": ["Lewis", "Mason"],
            "second_name": ["Miley", "Miley"],
            "season": ["2025-2026", "2025-2026"],
        }
    )
    accepted, amb, unmatched = match_players(us, fpl, overrides=pl.DataFrame())
    assert not amb and not unmatched
    assert accepted[0]["player_code"] == 547719
    assert accepted[0]["method"] == "exact_name"


def test_match_same_date_teams():
    us = pl.DataFrame(
        {
            "understat_match_id": ["u1"],
            "season": ["2026-2027"],
            "kick_date": ["2026-09-14"],
            "home_code": [2],
            "away_code": [4],
            "home_team": ["Leeds"],
            "away_team": ["Newcastle"],
            "is_result": [True],
        }
    )
    fpl = pl.DataFrame(
        {
            "fpl_match_id": ["f1"],
            "season": ["2026-2027"],
            "gw": [4],
            "kick_date": ["2026-09-14"],
            "home_code": [2],
            "away_code": [4],
            "finished": [True],
            "kickoff": ["2026-09-14T19:00:00Z"],
        }
    )
    mapped, unmatched = pair_matches(us, fpl)
    assert unmatched.height == 0
    assert mapped.row(0, named=True)["fpl_match_id"] == "f1"
    assert mapped.row(0, named=True)["method"] == "date_teams"


def test_match_date_pm1_unique():
    us = pl.DataFrame(
        {
            "understat_match_id": ["u1"],
            "season": ["2026-2027"],
            "kick_date": ["2026-09-14"],
            "home_code": [2],
            "away_code": [4],
        }
    )
    fpl = pl.DataFrame(
        {
            "fpl_match_id": ["f1"],
            "season": ["2026-2027"],
            "gw": [4],
            "kick_date": ["2026-09-13"],
            "home_code": [2],
            "away_code": [4],
        }
    )
    mapped, unmatched = pair_matches(us, fpl)
    assert unmatched.height == 0
    assert mapped.row(0, named=True)["method"] == "date_pm1"


def test_match_two_candidates_stay_unmatched():
    us = pl.DataFrame(
        {
            "understat_match_id": ["u1"],
            "season": ["2026-2027"],
            "kick_date": ["2026-09-14"],
            "home_code": [2],
            "away_code": [4],
        }
    )
    fpl = pl.DataFrame(
        {
            "fpl_match_id": ["f1", "f2"],
            "season": ["2026-2027", "2026-2027"],
            "gw": [4, 4],
            "kick_date": ["2026-09-13", "2026-09-15"],
            "home_code": [2, 2],
            "away_code": [4, 4],
        }
    )
    mapped, unmatched = pair_matches(us, fpl)
    assert mapped.height == 0
    assert unmatched.height == 1
    assert unmatched.row(0, named=True)["reason"] == "ambiguous_date_pm1"


def test_normalize_match_roster_keeps_player_id():
    raw = {
        "h": {
            "10": {
                "id": "10",
                "player_id": "8995",
                "player": "Hugo Ekitike",
                "time": "90",
                "xG": "0.4",
                "xGChain": "0.5",
                "xGBuildup": "0.1",
            }
        },
        "a": {},
    }
    rows = normalize_match_roster(
        raw,
        match_row={
            "match_id": "28778",
            "understat_season": "2025",
            "home_team_id": "87",
            "away_team_id": "73",
        },
    )
    assert len(rows) == 1
    assert rows[0]["player_id"] == "8995"
    assert rows[0]["roster_id"] == "10"
    assert rows[0]["xg_chain"] == 0.5
