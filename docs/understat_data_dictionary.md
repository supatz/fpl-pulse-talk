# Understat masters — data dictionary (samples)

Generated `2026-09-07T08:14:07Z`.

FPL dimensions on the **site** come from FPL sources. These tables hold Understat metrics.
Team-facing derived tables are joined to FPL `team_code` via `data/understat/maps/team_map.csv`.
Player tables still key on Understat `player_id` until a curated `player_map` exists.

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
    "match_id": "31209",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-06 15:30:00",
    "home_team_id": "83",
    "away_team_id": "80",
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "home_short": "ARS",
    "away_short": "CHE",
    "home_goals": 2.0,
    "away_goals": 1.0,
    "home_xg": 2.8056,
    "away_xg": 0.4305,
    "forecast_w": 0.9066,
    "forecast_d": 0.0737,
    "forecast_l": 0.0197,
    "ingested_at_utc": "2026-09-07T08:13:42Z",
    "source": "understat.com"
  },
  {
    "match_id": "31208",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-06 13:00:00",
    "home_team_id": "72",
    "away_team_id": "89",
    "home_team": "Everton",
    "away_team": "Manchester United",
    "home_short": "EVE",
    "away_short": "MUN",
    "home_goals": 2.0,
    "away_goals": 2.0,
    "home_xg": 1.0563,
    "away_xg": 0.8722,
    "forecast_w": 0.3879,
    "forecast_d": 0.3237,
    "forecast_l": 0.2884,
    "ingested_at_utc": "2026-09-07T08:13:42Z",
    "source": "understat.com"
  },
  {
    "match_id": "31207",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-05 16:30:00",
    "home_team_id": "91",
    "away_team_id": "71",
    "home_team": "Hull",
    "away_team": "Aston Villa",
    "home_short": "HUL",
    "away_short": "AVL",
    "home_goals": 0.0,
    "away_goals": 0.0,
    "home_xg": 0.8124,
    "away_xg": 1.6353,
    "forecast_w": 0.1491,
    "forecast_d": 0.2595,
    "forecast_l": 0.5914,
    "ingested_at_utc": "2026-09-07T08:13:42Z",
    "source": "understat.com"
  }
]
```


## `shot`

**Grain:** 1 row per shot  
**What:** Atomic fact: situation, last_action, coords, zone, player  
**Rows:** 10,353

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
    "ingested_at_utc": "2026-09-07T08:13:24Z",
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
    "ingested_at_utc": "2026-09-07T08:13:24Z",
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
    "ingested_at_utc": "2026-09-07T08:13:24Z",
    "source": "understat.com"
  }
]
```


## `team_match_style`

**Grain:** 1 row per team per match  
**What:** PPDA, deep completions, match xG/xGA from team history  
**Rows:** 820

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
    "team_id": "80",
    "team_title": "Chelsea",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": false,
    "h_a": "a",
    "result": "l",
    "scored": 1.0,
    "conceded": 2.0,
    "xg": 0.4305,
    "xga": 2.8056,
    "npxg": 0.4305,
    "npxga": 2.8056,
    "npxgd": -2.375,
    "xpts": 0.1328,
    "deep": 5.0,
    "deep_allowed": 17.0,
    "ppda_att": 177.0,
    "ppda_def": 18.0,
    "ppda": 9.8333,
    "ppda_allowed_att": 187.0,
    "ppda_allowed_def": 21.0,
    "ppda_allowed": 8.9048,
    "wins_cum": 0.0,
    "draws_cum": 0.0,
    "losses_cum": 1.0,
    "pts_cum": 0.0,
    "match_id": "31209",
    "opponent_id": "83",
    "team_code": 8,
    "team": "Chelsea",
    "team_short": "CHE",
    "opponent_code": 3,
    "opponent": "Arsenal",
    "opponent_short": "ARS",
    "ingested_at_utc": "2026-09-07T08:13:47Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "83",
    "team_title": "Arsenal",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "h_a": "h",
    "result": "w",
    "scored": 2.0,
    "conceded": 1.0,
    "xg": 2.8056,
    "xga": 0.4305,
    "npxg": 2.8056,
    "npxga": 0.4305,
    "npxgd": 2.375,
    "xpts": 2.7935,
    "deep": 17.0,
    "deep_allowed": 5.0,
    "ppda_att": 187.0,
    "ppda_def": 21.0,
    "ppda": 8.9048,
    "ppda_allowed_att": 177.0,
    "ppda_allowed_def": 18.0,
    "ppda_allowed": 9.8333,
    "wins_cum": 1.0,
    "draws_cum": 0.0,
    "losses_cum": 0.0,
    "pts_cum": 3.0,
    "match_id": "31209",
    "opponent_id": "80",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "ingested_at_utc": "2026-09-07T08:13:47Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "72",
    "team_title": "Everton",
    "kickoff_raw": "2026-09-06 13:00:00",
    "is_home": true,
    "h_a": "h",
    "result": "d",
    "scored": 2.0,
    "conceded": 2.0,
    "xg": 1.0563,
    "xga": 0.8722,
    "npxg": 1.0563,
    "npxga": 0.8722,
    "npxgd": 0.1841,
    "xpts": 1.4874,
    "deep": 7.0,
    "deep_allowed": 7.0,
    "ppda_att": 305.0,
    "ppda_def": 23.0,
    "ppda": 13.2609,
    "ppda_allowed_att": 222.0,
    "ppda_allowed_def": 14.0,
    "ppda_allowed": 15.8571,
    "wins_cum": 0.0,
    "draws_cum": 1.0,
    "losses_cum": 0.0,
    "pts_cum": 1.0,
    "match_id": "31208",
    "opponent_id": "89",
    "team_code": 11,
    "team": "Everton",
    "team_short": "EVE",
    "opponent_code": 1,
    "opponent": "Man Utd",
    "opponent_short": "MUN",
    "ingested_at_utc": "2026-09-07T08:13:47Z",
    "source": "understat.com"
  }
]
```


## `team_context_season`

**Grain:** 1 row per team × season × context_family × context_value  
**What:** Season splits incl. attackSpeed (for + against)  
**Rows:** 1,299

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
    "ingested_at_utc": "2026-09-07T08:13:40Z",
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
    "ingested_at_utc": "2026-09-07T08:13:40Z",
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
    "ingested_at_utc": "2026-09-07T08:13:40Z",
    "source": "understat.com"
  }
]
```


## `league_player`

**Grain:** 1 row per player per season  
**What:** Understat season totals (xg_chain, etc.)  
**Rows:** 924

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
    "ingested_at_utc": "2026-09-07T08:13:41Z",
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
    "ingested_at_utc": "2026-09-07T08:13:41Z",
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
    "ingested_at_utc": "2026-09-07T08:13:41Z",
    "source": "understat.com"
  }
]
```


## `team_situation_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xg created (for)  
**Rows:** 2,206

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
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "situation": "OpenPlay",
    "is_home": true,
    "shots": 13,
    "goals": 2,
    "us_xg": 1.7384,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "us_xg_per_shot": 0.1337,
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "situation": "SetPiece",
    "is_home": true,
    "shots": 3,
    "goals": 0,
    "us_xg": 1.131,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "us_xg_per_shot": 0.377,
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 8,
    "team": "Chelsea",
    "team_short": "CHE",
    "situation": "DirectFreekick",
    "is_home": false,
    "shots": 1,
    "goals": 0,
    "us_xg": 0.0323,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 3,
    "opponent": "Arsenal",
    "opponent_short": "ARS",
    "us_xg_per_shot": 0.0323,
    "built_at_utc": "2026-09-07T08:14:07Z"
  }
]
```


## `team_situation_against_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xga faced (against)  
**Rows:** 2,206

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
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "situation": "DirectFreekick",
    "is_home": true,
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0323,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "us_xga_per_shot": 0.0323,
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "situation": "FromCorner",
    "is_home": true,
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0127,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "us_xga_per_shot": 0.0127,
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "situation": "OpenPlay",
    "is_home": true,
    "shots_faced": 10,
    "goals_against": 0,
    "us_xga": 0.3488,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "us_xga_per_shot": 0.0349,
    "built_at_utc": "2026-09-07T08:14:07Z"
  }
]
```


## `team_situation_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling for-metrics over last 5/10/15 matches  
**Rows:** 12,300

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
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "DirectFreekick",
    "shots": 2,
    "goals": 0,
    "us_xg": 0.1284,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xg_per_shot": 0.0642
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "FromCorner",
    "shots": 7,
    "goals": 0,
    "us_xg": 0.5559,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xg_per_shot": 0.0794
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "OpenPlay",
    "shots": 31,
    "goals": 6,
    "us_xg": 4.4328,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xg_per_shot": 0.143
  }
]
```


## `team_situation_against_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling against-metrics over last 5/10/15 matches  
**Rows:** 12,300

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
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "DirectFreekick",
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0323,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xga_per_shot": 0.0323
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "FromCorner",
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0127,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xga_per_shot": 0.0127
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "kickoff_raw": "2026-09-06 15:30:00",
    "is_home": true,
    "opponent_code": 8,
    "opponent": "Chelsea",
    "opponent_short": "CHE",
    "situation": "OpenPlay",
    "shots_faced": 21,
    "goals_against": 0,
    "us_xga": 1.1891,
    "window": 5,
    "built_at_utc": "2026-09-07T08:14:07Z",
    "us_xga_per_shot": 0.0566
  }
]
```


## `team_zone_match`

**Grain:** 1 row per team × match × shot_zone  
**What:** Box / six-yard / outside-box  
**Rows:** 2,237

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
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "shot_zone": "outside_box",
    "is_home": true,
    "shots": 3,
    "goals": 1,
    "us_xg": 0.1009,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "shot_zone": "penalty_area",
    "is_home": true,
    "shots": 10,
    "goals": 1,
    "us_xg": 2.0449,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31209",
    "team_code": 3,
    "team": "Arsenal",
    "team_short": "ARS",
    "shot_zone": "six_yard",
    "is_home": true,
    "shots": 3,
    "goals": 0,
    "us_xg": 0.7236,
    "kickoff_raw": "2026-09-06 15:30:00",
    "opponent_code": 8,
    "opponent": "Chelsea",
    "built_at_utc": "2026-09-07T08:14:07Z"
  }
]
```


## `player_situation_season`

**Grain:** 1 row per understat player × season × situation  
**What:** Taker volume/quality by situation (player_code map TBD)  
**Rows:** 1,535

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
    "built_at_utc": "2026-09-07T08:14:07Z"
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
    "built_at_utc": "2026-09-07T08:14:07Z"
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
    "built_at_utc": "2026-09-07T08:14:07Z"
  }
]
```


## `player_create_situation_season`

**Grain:** 1 row per creator name × season × situation  
**What:** Assisted-shot xG by situation (player_code map TBD)  
**Rows:** 1,181

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
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Mathis Cherki",
    "situation": "OpenPlay",
    "assisted_shots": 45,
    "assisted_goals": 11,
    "assisted_us_xg": 9.0433,
    "player_id": "8094",
    "built_at_utc": "2026-09-07T08:14:07Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Jéremy Doku",
    "situation": "OpenPlay",
    "assisted_shots": 56,
    "assisted_goals": 5,
    "assisted_us_xg": 7.2875,
    "player_id": "8981",
    "built_at_utc": "2026-09-07T08:14:07Z"
  }
]
```

