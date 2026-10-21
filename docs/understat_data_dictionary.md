# Understat masters — data dictionary (samples)

Generated `2026-10-21T19:29:31Z`.

FPL dimensions on the **site** come from FPL sources. These tables hold Understat metrics.
Team-facing derived tables are joined to FPL `team_code` via `data/understat/maps/team_map.csv`.
Understat masters retain `player_id`; serving applies `data/pl_merge/maps/player_map.csv` to expose FPL `player_code`.

Seasons in scope: 2025-2026, 2026-2027 (Understat 2025, 2026).

## `match`

**Grain:** 1 row per EPL fixture  
**What:** Fixture index + score/xG/forecast  
**Rows:** 760

### Headers

| Column | Dtype | Role |
|---|---|---|
| `match_id` | `String` | dimension |
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `league` | `String` | metric/attr |
| `is_result` | `Boolean` | metric/attr |
| `kickoff_raw` | `String` | dimension |
| `home_team_id` | `String` | dimension |
| `away_team_id` | `String` | dimension |
| `home_team` | `String` | metric/attr |
| `away_team` | `String` | metric/attr |
| `home_short` | `String` | metric/attr |
| `away_short` | `String` | metric/attr |
| `home_goals` | `Float64` | metric/attr |
| `away_goals` | `Float64` | metric/attr |
| `home_xg` | `Float64` | metric/attr |
| `away_xg` | `Float64` | metric/attr |
| `forecast_w` | `Float64` | metric/attr |
| `forecast_d` | `Float64` | metric/attr |
| `forecast_l` | `Float64` | metric/attr |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "match_id": "31249",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-10-19 19:00:00",
    "home_team_id": "82",
    "away_team_id": "294",
    "home_team": "Tottenham",
    "away_team": "Coventry",
    "home_short": "TOT",
    "away_short": "COV",
    "home_goals": 3.0,
    "away_goals": 1.0,
    "home_xg": 0.9718,
    "away_xg": 1.1439,
    "forecast_w": 0.2845,
    "forecast_d": 0.3066,
    "forecast_l": 0.4089,
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  },
  {
    "match_id": "31248",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-10-18 15:30:00",
    "home_team_id": "249",
    "away_team_id": "83",
    "home_team": "Nottingham Forest",
    "away_team": "Arsenal",
    "home_short": "NOT",
    "away_short": "ARS",
    "home_goals": 0.0,
    "away_goals": 1.0,
    "home_xg": 0.7472,
    "away_xg": 0.9151,
    "forecast_w": 0.2706,
    "forecast_d": 0.3472,
    "forecast_l": 0.3822,
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  },
  {
    "match_id": "31245",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-10-18 13:00:00",
    "home_team_id": "220",
    "away_team_id": "78",
    "home_team": "Brighton",
    "away_team": "Crystal Palace",
    "home_short": "BRI",
    "away_short": "CRY",
    "home_goals": 5.0,
    "away_goals": 0.0,
    "home_xg": 2.2522,
    "away_xg": 0.6275,
    "forecast_w": 0.8337,
    "forecast_d": 0.1341,
    "forecast_l": 0.0322,
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  }
]
```


## `shot`

**Grain:** 1 row per shot  
**What:** Atomic fact: situation, last_action, coords, zone, player  
**Rows:** 11,456

### Headers

| Column | Dtype | Role |
|---|---|---|
| `shot_id` | `String` | dimension |
| `match_id` | `String` | dimension |
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `minute` | `Float64` | metric/attr |
| `date` | `String` | metric/attr |
| `side` | `String` | metric/attr |
| `is_home` | `Boolean` | dimension |
| `team_id` | `String` | dimension |
| `opponent_id` | `String` | dimension |
| `h_team` | `String` | metric/attr |
| `a_team` | `String` | metric/attr |
| `h_goals` | `Float64` | metric/attr |
| `a_goals` | `Float64` | metric/attr |
| `player_id` | `String` | dimension |
| `player_name` | `String` | dimension |
| `player_assisted` | `String` | metric/attr |
| `situation` | `String` | dimension |
| `last_action` | `String` | metric/attr |
| `shot_type` | `String` | metric/attr |
| `result` | `String` | metric/attr |
| `xg` | `Float64` | metric/attr |
| `x` | `Float64` | metric/attr |
| `y` | `Float64` | metric/attr |
| `shot_zone` | `String` | dimension |
| `is_goal` | `Boolean` | metric/attr |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "shot_id": "637500",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "minute": 2.0,
    "date": "2025-08-15 19:00:00",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "h_team": "Liverpool",
    "a_team": "Bournemouth",
    "h_goals": 4.0,
    "a_goals": 2.0,
    "player_id": "8995",
    "player_name": "Hugo Ekitike",
    "player_assisted": "Cody Gakpo",
    "situation": "OpenPlay",
    "last_action": "Pass",
    "shot_type": "RightFoot",
    "result": "SavedShot",
    "xg": 0.0146,
    "x": 0.762,
    "y": 0.699,
    "shot_zone": "outside_box",
    "is_goal": false,
    "ingested_at_utc": "2026-10-21T19:29:00Z",
    "source": "understat.com"
  },
  {
    "shot_id": "637501",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "minute": 3.0,
    "date": "2025-08-15 19:00:00",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "h_team": "Liverpool",
    "a_team": "Bournemouth",
    "h_goals": 4.0,
    "a_goals": 2.0,
    "player_id": "1250",
    "player_name": "Mohamed Salah",
    "player_assisted": "Hugo Ekitike",
    "situation": "OpenPlay",
    "last_action": "Pass",
    "shot_type": "LeftFoot",
    "result": "SavedShot",
    "xg": 0.0427,
    "x": 0.856,
    "y": 0.313,
    "shot_zone": "penalty_area",
    "is_goal": false,
    "ingested_at_utc": "2026-10-21T19:29:00Z",
    "source": "understat.com"
  },
  {
    "shot_id": "637502",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "minute": 4.0,
    "date": "2025-08-15 19:00:00",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "h_team": "Liverpool",
    "a_team": "Bournemouth",
    "h_goals": 4.0,
    "a_goals": 2.0,
    "player_id": "833",
    "player_name": "Virgil van Dijk",
    "player_assisted": "Mohamed Salah",
    "situation": "FromCorner",
    "last_action": "Cross",
    "shot_type": "Head",
    "result": "MissedShots",
    "xg": 0.258,
    "x": 0.914,
    "y": 0.505,
    "shot_zone": "penalty_area",
    "is_goal": false,
    "ingested_at_utc": "2026-10-21T19:29:00Z",
    "source": "understat.com"
  }
]
```


## `team_match_style`

**Grain:** 1 row per team per match  
**What:** PPDA, deep completions, match xG/xGA from team history  
**Rows:** 900

### Headers

| Column | Dtype | Role |
|---|---|---|
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `team_id` | `String` | dimension |
| `team_title` | `String` | metric/attr |
| `kickoff_raw` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `h_a` | `String` | metric/attr |
| `result` | `String` | metric/attr |
| `scored` | `Float64` | metric/attr |
| `conceded` | `Float64` | metric/attr |
| `xg` | `Float64` | metric/attr |
| `xga` | `Float64` | metric/attr |
| `npxg` | `Float64` | metric/attr |
| `npxga` | `Float64` | metric/attr |
| `npxgd` | `Float64` | metric/attr |
| `xpts` | `Float64` | metric/attr |
| `deep` | `Float64` | metric/attr |
| `deep_allowed` | `Float64` | metric/attr |
| `ppda_att` | `Float64` | metric/attr |
| `ppda_def` | `Float64` | metric/attr |
| `ppda` | `Float64` | metric/attr |
| `ppda_allowed_att` | `Float64` | metric/attr |
| `ppda_allowed_def` | `Float64` | metric/attr |
| `ppda_allowed` | `Float64` | metric/attr |
| `wins_cum` | `Float64` | metric/attr |
| `draws_cum` | `Float64` | metric/attr |
| `losses_cum` | `Float64` | metric/attr |
| `pts_cum` | `Float64` | metric/attr |
| `match_id` | `String` | dimension |
| `opponent_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `opponent_short` | `String` | metric/attr |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "82",
    "team_title": "Tottenham",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "h_a": "h",
    "result": "w",
    "scored": 3.0,
    "conceded": 1.0,
    "xg": 0.9718,
    "xga": 1.1439,
    "npxg": 0.9718,
    "npxga": 1.1439,
    "npxgd": -0.1721,
    "xpts": 1.1601,
    "deep": 5.0,
    "deep_allowed": 11.0,
    "ppda_att": 153.0,
    "ppda_def": 24.0,
    "ppda": 6.375,
    "ppda_allowed_att": 321.0,
    "ppda_allowed_def": 24.0,
    "ppda_allowed": 13.375,
    "wins_cum": 1.0,
    "draws_cum": 0.0,
    "losses_cum": 0.0,
    "pts_cum": 3.0,
    "match_id": "31249",
    "opponent_id": "294",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "ingested_at_utc": "2026-10-21T19:29:17Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "294",
    "team_title": "Coventry",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": false,
    "h_a": "a",
    "result": "l",
    "scored": 1.0,
    "conceded": 3.0,
    "xg": 1.1439,
    "xga": 0.9718,
    "npxg": 1.1439,
    "npxga": 0.9718,
    "npxgd": 0.1721,
    "xpts": 1.5333,
    "deep": 11.0,
    "deep_allowed": 5.0,
    "ppda_att": 321.0,
    "ppda_def": 24.0,
    "ppda": 13.375,
    "ppda_allowed_att": 153.0,
    "ppda_allowed_def": 24.0,
    "ppda_allowed": 6.375,
    "wins_cum": 0.0,
    "draws_cum": 0.0,
    "losses_cum": 1.0,
    "pts_cum": 0.0,
    "match_id": "31249",
    "opponent_id": "82",
    "team_code": 9,
    "team": "Coventry City",
    "team_short": "COV",
    "opponent_code": 6,
    "opponent": "Spurs",
    "opponent_short": "TOT",
    "ingested_at_utc": "2026-10-21T19:29:17Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "83",
    "team_title": "Arsenal",
    "kickoff_raw": "2026-10-18 15:30:00",
    "is_home": false,
    "h_a": "a",
    "result": "w",
    "scored": 1.0,
    "conceded": 0.0,
    "xg": 0.9151,
    "xga": 0.7472,
    "npxg": 0.9151,
    "npxga": 0.7472,
    "npxgd": 0.1679,
    "xpts": 1.4938,
    "deep": 10.0,
    "deep_allowed": 6.0,
    "ppda_att": 115.0,
    "ppda_def": 22.0,
    "ppda": 5.2273,
    "ppda_allowed_att": 360.0,
    "ppda_allowed_def": 15.0,
    "ppda_allowed": 24.0,
    "wins_cum": 1.0,
    "draws_cum": 0.0,
    "losses_cum": 0.0,
    "pts_cum": 3.0,
    "match_id": "31248",
    "opponent_id": "249",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "opponent_code": 17,
    "opponent": "Nott'm Forest",
    "opponent_short": "NFO",
    "ingested_at_utc": "2026-10-21T19:29:17Z",
    "source": "understat.com"
  }
]
```


## `team_context_season`

**Grain:** 1 row per team × season × context_family × context_value  
**What:** Season splits incl. attackSpeed (for + against)  
**Rows:** 1,349

### Headers

| Column | Dtype | Role |
|---|---|---|
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `team_id` | `String` | dimension |
| `team_title` | `String` | metric/attr |
| `team_slug` | `String` | metric/attr |
| `context_family` | `String` | dimension |
| `context_value` | `String` | dimension |
| `stat_label` | `String` | metric/attr |
| `time_minutes` | `Float64` | metric/attr |
| `shots` | `Float64` | metric/attr |
| `goals` | `Float64` | metric/attr |
| `us_xg` | `Float64` | metric/attr |
| `against_shots` | `Float64` | metric/attr |
| `against_goals` | `Float64` | metric/attr |
| `against_us_xg` | `Float64` | metric/attr |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "team_id": "88",
    "team_title": "Manchester City",
    "team_slug": "Manchester_City",
    "context_family": "situation",
    "context_value": "OpenPlay",
    "stat_label": null,
    "time_minutes": null,
    "shots": 451.0,
    "goals": 63.0,
    "us_xg": 67.2036,
    "against_shots": 283.0,
    "against_goals": 23.0,
    "against_us_xg": 36.8411,
    "team_code": 43,
    "team": "Man City",
    "team_short": "MCI",
    "ingested_at_utc": "2026-10-21T19:29:13Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "team_id": "73",
    "team_title": "Bournemouth",
    "team_slug": "Bournemouth",
    "context_family": "formation",
    "context_value": "4-2-3-1",
    "stat_label": "4-2-3-1",
    "time_minutes": 3436.0,
    "shots": 499.0,
    "goals": 54.0,
    "us_xg": 65.4317,
    "against_shots": 446.0,
    "against_goals": 48.0,
    "against_us_xg": 55.6593,
    "team_code": 91,
    "team": "Bournemouth",
    "team_short": "BOU",
    "ingested_at_utc": "2026-10-21T19:29:13Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "team_id": "80",
    "team_title": "Chelsea",
    "team_slug": "Chelsea",
    "context_family": "formation",
    "context_value": "4-2-3-1",
    "stat_label": "4-2-3-1",
    "time_minutes": 3066.0,
    "shots": 446.0,
    "goals": 50.0,
    "us_xg": 64.215,
    "against_shots": 333.0,
    "against_goals": 38.0,
    "against_us_xg": 48.1791,
    "team_code": 8,
    "team": "Chelsea",
    "team_short": "CHE",
    "ingested_at_utc": "2026-10-21T19:29:13Z",
    "source": "understat.com"
  }
]
```


## `league_player`

**Grain:** 1 row per player per season  
**What:** Understat season totals (xg_chain, etc.)  
**Rows:** 986

### Headers

| Column | Dtype | Role |
|---|---|---|
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `player_id` | `String` | dimension |
| `player_name` | `String` | dimension |
| `team_title` | `String` | metric/attr |
| `position` | `String` | metric/attr |
| `games` | `Float64` | metric/attr |
| `time` | `Float64` | metric/attr |
| `goals` | `Float64` | metric/attr |
| `assists` | `Float64` | metric/attr |
| `shots` | `Float64` | metric/attr |
| `key_passes` | `Float64` | metric/attr |
| `xg` | `Float64` | metric/attr |
| `xa` | `Float64` | metric/attr |
| `npxg` | `Float64` | metric/attr |
| `npg` | `Float64` | metric/attr |
| `xg_chain` | `Float64` | metric/attr |
| `xg_buildup` | `Float64` | metric/attr |
| `yellow_cards` | `Float64` | metric/attr |
| `red_cards` | `Float64` | metric/attr |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "player_id": "8260",
    "player_name": "Erling Haaland",
    "team_title": "Manchester City",
    "position": "F S",
    "games": 35.0,
    "time": 2979.0,
    "goals": 27.0,
    "assists": 8.0,
    "shots": 125.0,
    "key_passes": 25.0,
    "xg": 28.7953,
    "xa": 5.5077,
    "npxg": 25.7507,
    "npg": 24.0,
    "xg_chain": 32.7354,
    "xg_buildup": 5.1635,
    "yellow_cards": 2.0,
    "red_cards": 0.0,
    "ingested_at_utc": "2026-10-21T19:29:15Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "player_id": "13222",
    "player_name": "Thiago",
    "team_title": "Brentford",
    "position": "F S",
    "games": 38.0,
    "time": 3292.0,
    "goals": 22.0,
    "assists": 1.0,
    "shots": 84.0,
    "key_passes": 24.0,
    "xg": 24.6898,
    "xa": 3.45,
    "npxg": 17.8393,
    "npg": 14.0,
    "xg_chain": 22.6935,
    "xg_buildup": 4.9276,
    "yellow_cards": 7.0,
    "red_cards": 0.0,
    "ingested_at_utc": "2026-10-21T19:29:15Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2025",
    "season": "2025-2026",
    "player_id": "11363",
    "player_name": "Antoine Semenyo",
    "team_title": "Bournemouth,Manchester City",
    "position": "F M",
    "games": 37.0,
    "time": 3220.0,
    "goals": 17.0,
    "assists": 4.0,
    "shots": 83.0,
    "key_passes": 38.0,
    "xg": 12.8368,
    "xa": 4.1302,
    "npxg": 11.3144,
    "npg": 16.0,
    "xg_chain": 20.8706,
    "xg_buildup": 7.8937,
    "yellow_cards": 7.0,
    "red_cards": 0.0,
    "ingested_at_utc": "2026-10-21T19:29:15Z",
    "source": "understat.com"
  }
]
```


## `roster`

**Grain:** 1 row per player × finished match  
**What:** Understat match roster used by the PL merge  
**Rows:** 13,648

### Headers

| Column | Dtype | Role |
|---|---|---|
| `roster_id` | `String` | dimension |
| `match_id` | `String` | dimension |
| `understat_season` | `String` | dimension |
| `season` | `String` | dimension |
| `side` | `String` | metric/attr |
| `is_home` | `Boolean` | dimension |
| `team_id` | `String` | dimension |
| `opponent_id` | `String` | dimension |
| `player_id` | `String` | dimension |
| `player_name` | `String` | dimension |
| `position` | `String` | metric/attr |
| `position_order` | `Float64` | metric/attr |
| `time` | `Float64` | metric/attr |
| `goals` | `Float64` | metric/attr |
| `own_goals` | `Float64` | metric/attr |
| `assists` | `Float64` | metric/attr |
| `shots` | `Float64` | metric/attr |
| `key_passes` | `Float64` | metric/attr |
| `xg` | `Float64` | metric/attr |
| `xa` | `Float64` | metric/attr |
| `npxg` | `Null` | metric/attr |
| `xg_chain` | `Float64` | metric/attr |
| `xg_buildup` | `Float64` | metric/attr |
| `yellow_cards` | `Float64` | metric/attr |
| `red_cards` | `Float64` | metric/attr |
| `roster_in` | `String` | metric/attr |
| `roster_out` | `String` | metric/attr |
| `ingested_at_utc` | `String` | metric/attr |
| `source` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "roster_id": "731570",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "player_id": "1257",
    "player_name": "Alisson",
    "position": "GK",
    "position_order": 1.0,
    "time": 90.0,
    "goals": 0.0,
    "own_goals": 0.0,
    "assists": 0.0,
    "shots": 0.0,
    "key_passes": 0.0,
    "xg": 0.0,
    "xa": 0.0,
    "npxg": null,
    "xg_chain": 0.4187,
    "xg_buildup": 0.4187,
    "yellow_cards": 0.0,
    "red_cards": 0.0,
    "roster_in": "0",
    "roster_out": "0",
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  },
  {
    "roster_id": "731571",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "player_id": "9328",
    "player_name": "Jeremie Frimpong",
    "position": "DR",
    "position_order": 2.0,
    "time": 63.0,
    "goals": 0.0,
    "own_goals": 0.0,
    "assists": 0.0,
    "shots": 1.0,
    "key_passes": 0.0,
    "xg": 0.0156,
    "xa": 0.0,
    "npxg": null,
    "xg_chain": 0.0272,
    "xg_buildup": 0.0272,
    "yellow_cards": 0.0,
    "red_cards": 0.0,
    "roster_in": "731582",
    "roster_out": "0",
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  },
  {
    "roster_id": "731573",
    "match_id": "28778",
    "understat_season": "2025",
    "season": "2025-2026",
    "side": "h",
    "is_home": true,
    "team_id": "87",
    "opponent_id": "73",
    "player_id": "833",
    "player_name": "Virgil van Dijk",
    "position": "DC",
    "position_order": 3.0,
    "time": 90.0,
    "goals": 0.0,
    "own_goals": 0.0,
    "assists": 0.0,
    "shots": 2.0,
    "key_passes": 0.0,
    "xg": 0.3356,
    "xa": 0.0,
    "npxg": null,
    "xg_chain": 0.7136,
    "xg_buildup": 0.7136,
    "yellow_cards": 0.0,
    "red_cards": 0.0,
    "roster_in": "0",
    "roster_out": "0",
    "ingested_at_utc": "2026-10-21T19:29:28Z",
    "source": "understat.com"
  }
]
```


## `team_situation_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xg created (for)  
**Rows:** 2,427

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `match_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `situation` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `shots` | `UInt32` | metric/attr |
| `goals` | `UInt32` | metric/attr |
| `us_xg` | `Float64` | metric/attr |
| `kickoff_raw` | `String` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `opponent_short` | `String` | metric/attr |
| `us_xg_per_shot` | `Float64` | metric/attr |
| `built_at_utc` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "situation": "FromCorner",
    "is_home": true,
    "shots": 2,
    "goals": 0,
    "us_xg": 0.1158,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "us_xg_per_shot": 0.0579,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "situation": "OpenPlay",
    "is_home": true,
    "shots": 14,
    "goals": 3,
    "us_xg": 0.8593,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "us_xg_per_shot": 0.0614,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 9,
    "team": "Coventry City",
    "team_short": "COV",
    "situation": "OpenPlay",
    "is_home": false,
    "shots": 10,
    "goals": 1,
    "us_xg": 1.0579,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 6,
    "opponent": "Spurs",
    "opponent_short": "TOT",
    "us_xg_per_shot": 0.1058,
    "built_at_utc": "2026-10-21T19:29:30Z"
  }
]
```


## `team_situation_against_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xga faced (against)  
**Rows:** 2,427

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `match_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `situation` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `shots_faced` | `UInt32` | metric/attr |
| `goals_against` | `UInt32` | metric/attr |
| `us_xga` | `Float64` | metric/attr |
| `kickoff_raw` | `String` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `opponent_short` | `String` | metric/attr |
| `us_xga_per_shot` | `Float64` | metric/attr |
| `built_at_utc` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "situation": "OpenPlay",
    "is_home": true,
    "shots_faced": 10,
    "goals_against": 1,
    "us_xga": 1.0579,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "us_xga_per_shot": 0.1058,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "situation": "SetPiece",
    "is_home": true,
    "shots_faced": 2,
    "goals_against": 0,
    "us_xga": 0.086,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "us_xga_per_shot": 0.043,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 9,
    "team": "Coventry City",
    "team_short": "COV",
    "situation": "FromCorner",
    "is_home": false,
    "shots_faced": 2,
    "goals_against": 0,
    "us_xga": 0.1158,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 6,
    "opponent": "Spurs",
    "opponent_short": "TOT",
    "us_xga_per_shot": 0.0579,
    "built_at_utc": "2026-10-21T19:29:30Z"
  }
]
```


## `team_situation_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling for-metrics over last 5/10/15 matches  
**Rows:** 13,500

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `match_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `kickoff_raw` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `opponent_short` | `String` | metric/attr |
| `situation` | `String` | dimension |
| `shots` | `UInt32` | metric/attr |
| `goals` | `UInt32` | metric/attr |
| `us_xg` | `Float64` | metric/attr |
| `window` | `Int32` | dimension |
| `built_at_utc` | `String` | metric/attr |
| `us_xg_per_shot` | `Float64` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "DirectFreekick",
    "shots": 2,
    "goals": 0,
    "us_xg": 0.1572,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xg_per_shot": 0.0786
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "FromCorner",
    "shots": 17,
    "goals": 0,
    "us_xg": 1.183,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xg_per_shot": 0.0696
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "OpenPlay",
    "shots": 51,
    "goals": 5,
    "us_xg": 4.8928,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xg_per_shot": 0.0959
  }
]
```


## `team_situation_against_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling against-metrics over last 5/10/15 matches  
**Rows:** 13,500

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `match_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `kickoff_raw` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `opponent_short` | `String` | metric/attr |
| `situation` | `String` | dimension |
| `shots_faced` | `UInt32` | metric/attr |
| `goals_against` | `UInt32` | metric/attr |
| `us_xga` | `Float64` | metric/attr |
| `window` | `Int32` | dimension |
| `built_at_utc` | `String` | metric/attr |
| `us_xga_per_shot` | `Float64` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "DirectFreekick",
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0546,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xga_per_shot": 0.0546
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "FromCorner",
    "shots_faced": 7,
    "goals_against": 0,
    "us_xga": 0.346,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xga_per_shot": 0.0494
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "kickoff_raw": "2026-10-19 19:00:00",
    "is_home": true,
    "opponent_code": 9,
    "opponent": "Coventry City",
    "opponent_short": "COV",
    "situation": "OpenPlay",
    "shots_faced": 52,
    "goals_against": 5,
    "us_xga": 5.6382,
    "window": 5,
    "built_at_utc": "2026-10-21T19:29:30Z",
    "us_xga_per_shot": 0.1084
  }
]
```


## `team_zone_match`

**Grain:** 1 row per team × match × shot_zone  
**What:** Box / six-yard / outside-box  
**Rows:** 2,458

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `match_id` | `String` | dimension |
| `team_code` | `Int64` | dimension |
| `team` | `String` | dimension |
| `team_short` | `String` | dimension |
| `shot_zone` | `String` | dimension |
| `is_home` | `Boolean` | dimension |
| `shots` | `UInt32` | metric/attr |
| `goals` | `UInt32` | metric/attr |
| `us_xg` | `Float64` | metric/attr |
| `kickoff_raw` | `String` | dimension |
| `opponent_code` | `Int64` | dimension |
| `opponent` | `String` | dimension |
| `built_at_utc` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "shot_zone": "outside_box",
    "is_home": true,
    "shots": 6,
    "goals": 3,
    "us_xg": 0.2458,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 6,
    "team": "Spurs",
    "team_short": "TOT",
    "shot_zone": "penalty_area",
    "is_home": true,
    "shots": 10,
    "goals": 0,
    "us_xg": 0.7294,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 9,
    "opponent": "Coventry City",
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31249",
    "team_code": 9,
    "team": "Coventry City",
    "team_short": "COV",
    "shot_zone": "outside_box",
    "is_home": false,
    "shots": 1,
    "goals": 0,
    "us_xg": 0.0196,
    "kickoff_raw": "2026-10-19 19:00:00",
    "opponent_code": 6,
    "opponent": "Spurs",
    "built_at_utc": "2026-10-21T19:29:30Z"
  }
]
```


## `player_situation_season`

**Grain:** 1 row per understat player × season × situation  
**What:** Taker volume/quality by situation (player_code applied at serving)  
**Rows:** 1,755

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `player_id` | `String` | dimension |
| `player_name` | `String` | dimension |
| `situation` | `String` | dimension |
| `shots` | `UInt32` | metric/attr |
| `goals` | `UInt32` | metric/attr |
| `us_xg` | `Float64` | metric/attr |
| `primary_team_id` | `String` | dimension |
| `sample_last_action` | `String` | metric/attr |
| `us_xg_per_shot` | `Float64` | metric/attr |
| `built_at_utc` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2025-2026",
    "player_id": "8260",
    "player_name": "Erling Haaland",
    "situation": "OpenPlay",
    "shots": 104,
    "goals": 24,
    "us_xg": 23.0667,
    "primary_team_id": "88",
    "sample_last_action": "Cross",
    "us_xg_per_shot": 0.2218,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2025-2026",
    "player_id": "13222",
    "player_name": "Thiago",
    "situation": "OpenPlay",
    "shots": 67,
    "goals": 14,
    "us_xg": 16.0889,
    "primary_team_id": "244",
    "sample_last_action": "Rebound",
    "us_xg_per_shot": 0.2401,
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2025-2026",
    "player_id": "8865",
    "player_name": "Ollie Watkins",
    "situation": "OpenPlay",
    "shots": 74,
    "goals": 12,
    "us_xg": 15.8562,
    "primary_team_id": "71",
    "sample_last_action": "Pass",
    "us_xg_per_shot": 0.2143,
    "built_at_utc": "2026-10-21T19:29:30Z"
  }
]
```


## `player_create_situation_season`

**Grain:** 1 row per creator name × season × situation  
**What:** Assisted-shot xG by situation (player_code applied at serving)  
**Rows:** 1,336

### Headers

| Column | Dtype | Role |
|---|---|---|
| `season` | `String` | dimension |
| `player_name` | `String` | dimension |
| `situation` | `String` | dimension |
| `assisted_shots` | `UInt32` | metric/attr |
| `assisted_goals` | `UInt32` | metric/attr |
| `assisted_us_xg` | `Float64` | metric/attr |
| `player_id` | `String` | dimension |
| `built_at_utc` | `String` | metric/attr |

### Sample rows

```json
[
  {
    "season": "2025-2026",
    "player_name": "Bruno Fernandes",
    "situation": "OpenPlay",
    "assisted_shots": 88,
    "assisted_goals": 10,
    "assisted_us_xg": 11.8637,
    "player_id": "1228",
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Mathis Cherki",
    "situation": "OpenPlay",
    "assisted_shots": 45,
    "assisted_goals": 11,
    "assisted_us_xg": 9.0433,
    "player_id": "8094",
    "built_at_utc": "2026-10-21T19:29:30Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Jéremy Doku",
    "situation": "OpenPlay",
    "assisted_shots": 56,
    "assisted_goals": 5,
    "assisted_us_xg": 7.2875,
    "player_id": "8981",
    "built_at_utc": "2026-10-21T19:29:30Z"
  }
]
```

