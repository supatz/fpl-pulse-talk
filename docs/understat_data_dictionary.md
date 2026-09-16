# Understat masters — data dictionary (samples)

Generated `2026-09-16T07:50:10Z`.

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
    "match_id": "31219",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-14 19:00:00",
    "home_team_id": "245",
    "away_team_id": "86",
    "home_team": "Leeds",
    "away_team": "Newcastle United",
    "home_short": "LED",
    "away_short": "NEW",
    "home_goals": 4.0,
    "away_goals": 1.0,
    "home_xg": 2.2902,
    "away_xg": 0.7932,
    "forecast_w": 0.7751,
    "forecast_d": 0.1682,
    "forecast_l": 0.0567,
    "ingested_at_utc": "2026-09-16T07:49:58Z",
    "source": "understat.com"
  },
  {
    "match_id": "31218",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-13 15:30:00",
    "home_team_id": "89",
    "away_team_id": "88",
    "home_team": "Manchester United",
    "away_team": "Manchester City",
    "home_short": "MUN",
    "away_short": "MCI",
    "home_goals": 0.0,
    "away_goals": 1.0,
    "home_xg": 0.9434,
    "away_xg": 1.1407,
    "forecast_w": 0.2657,
    "forecast_d": 0.3273,
    "forecast_l": 0.407,
    "ingested_at_utc": "2026-09-16T07:49:58Z",
    "source": "understat.com"
  },
  {
    "match_id": "31217",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-13 13:00:00",
    "home_team_id": "294",
    "away_team_id": "220",
    "home_team": "Coventry",
    "away_team": "Brighton",
    "home_short": "COV",
    "away_short": "BRI",
    "home_goals": 0.0,
    "away_goals": 5.0,
    "home_xg": 1.0481,
    "away_xg": 2.7652,
    "forecast_w": 0.0726,
    "forecast_d": 0.1427,
    "forecast_l": 0.7847,
    "ingested_at_utc": "2026-09-16T07:49:58Z",
    "source": "understat.com"
  }
]
```


## `shot`

**Grain:** 1 row per shot  
**What:** Atomic fact: situation, last_action, coords, zone, player  
**Rows:** 10,612

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
    "ingested_at_utc": "2026-09-16T07:49:44Z",
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
    "ingested_at_utc": "2026-09-16T07:49:44Z",
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
    "ingested_at_utc": "2026-09-16T07:49:44Z",
    "source": "understat.com"
  }
]
```


## `team_match_style`

**Grain:** 1 row per team per match  
**What:** PPDA, deep completions, match xG/xGA from team history  
**Rows:** 840

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
    "team_id": "86",
    "team_title": "Newcastle United",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": false,
    "h_a": "a",
    "result": "l",
    "scored": 1.0,
    "conceded": 4.0,
    "xg": 0.7932,
    "xga": 2.2902,
    "npxg": 0.7932,
    "npxga": 2.2902,
    "npxgd": -1.497,
    "xpts": 0.3383,
    "deep": 5.0,
    "deep_allowed": 9.0,
    "ppda_att": 265.0,
    "ppda_def": 26.0,
    "ppda": 10.1923,
    "ppda_allowed_att": 228.0,
    "ppda_allowed_def": 25.0,
    "ppda_allowed": 9.12,
    "wins_cum": 0.0,
    "draws_cum": 0.0,
    "losses_cum": 1.0,
    "pts_cum": 0.0,
    "match_id": "31219",
    "opponent_id": "245",
    "team_code": 4,
    "team": "Newcastle",
    "team_short": "NEW",
    "opponent_code": 2,
    "opponent": "Leeds",
    "opponent_short": "LEE",
    "ingested_at_utc": "2026-09-16T07:49:59Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "245",
    "team_title": "Leeds",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "h_a": "h",
    "result": "w",
    "scored": 4.0,
    "conceded": 1.0,
    "xg": 2.2902,
    "xga": 0.7932,
    "npxg": 2.2902,
    "npxga": 0.7932,
    "npxgd": 1.497,
    "xpts": 2.4935,
    "deep": 9.0,
    "deep_allowed": 5.0,
    "ppda_att": 228.0,
    "ppda_def": 25.0,
    "ppda": 9.12,
    "ppda_allowed_att": 265.0,
    "ppda_allowed_def": 26.0,
    "ppda_allowed": 10.1923,
    "wins_cum": 1.0,
    "draws_cum": 0.0,
    "losses_cum": 0.0,
    "pts_cum": 3.0,
    "match_id": "31219",
    "opponent_id": "86",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "ingested_at_utc": "2026-09-16T07:49:59Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "88",
    "team_title": "Manchester City",
    "kickoff_raw": "2026-09-13 15:30:00",
    "is_home": false,
    "h_a": "a",
    "result": "w",
    "scored": 1.0,
    "conceded": 0.0,
    "xg": 1.1407,
    "xga": 0.9434,
    "npxg": 1.1407,
    "npxga": 0.9434,
    "npxgd": 0.1973,
    "xpts": 1.5483,
    "deep": 2.0,
    "deep_allowed": 12.0,
    "ppda_att": 220.0,
    "ppda_def": 18.0,
    "ppda": 12.2222,
    "ppda_allowed_att": 239.0,
    "ppda_allowed_def": 37.0,
    "ppda_allowed": 6.4595,
    "wins_cum": 1.0,
    "draws_cum": 0.0,
    "losses_cum": 0.0,
    "pts_cum": 3.0,
    "match_id": "31218",
    "opponent_id": "89",
    "team_code": 43,
    "team": "Man City",
    "team_short": "MCI",
    "opponent_code": 1,
    "opponent": "Man Utd",
    "opponent_short": "MUN",
    "ingested_at_utc": "2026-09-16T07:49:59Z",
    "source": "understat.com"
  }
]
```


## `team_context_season`

**Grain:** 1 row per team × season × context_family × context_value  
**What:** Season splits incl. attackSpeed (for + against)  
**Rows:** 1,314

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
    "ingested_at_utc": "2026-09-16T07:49:56Z",
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
    "ingested_at_utc": "2026-09-16T07:49:56Z",
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
    "ingested_at_utc": "2026-09-16T07:49:56Z",
    "source": "understat.com"
  }
]
```


## `league_player`

**Grain:** 1 row per player per season  
**What:** Understat season totals (xg_chain, etc.)  
**Rows:** 943

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
    "ingested_at_utc": "2026-09-16T07:49:58Z",
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
    "ingested_at_utc": "2026-09-16T07:49:58Z",
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
    "ingested_at_utc": "2026-09-16T07:49:58Z",
    "source": "understat.com"
  }
]
```


## `team_situation_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xg created (for)  
**Rows:** 2,260

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
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "situation": "FromCorner",
    "is_home": true,
    "shots": 1,
    "goals": 0,
    "us_xg": 0.0211,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "us_xg_per_shot": 0.0211,
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "situation": "OpenPlay",
    "is_home": true,
    "shots": 14,
    "goals": 3,
    "us_xg": 2.2691,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "us_xg_per_shot": 0.1621,
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 4,
    "team": "Newcastle",
    "team_short": "NEW",
    "situation": "OpenPlay",
    "is_home": false,
    "shots": 8,
    "goals": 1,
    "us_xg": 0.7967,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 2,
    "opponent": "Leeds",
    "opponent_short": "LEE",
    "us_xg_per_shot": 0.0996,
    "built_at_utc": "2026-09-16T07:50:10Z"
  }
]
```


## `team_situation_against_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xga faced (against)  
**Rows:** 2,260

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
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "situation": "OpenPlay",
    "is_home": true,
    "shots_faced": 8,
    "goals_against": 1,
    "us_xga": 0.7967,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "us_xga_per_shot": 0.0996,
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 4,
    "team": "Newcastle",
    "team_short": "NEW",
    "situation": "FromCorner",
    "is_home": false,
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0211,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 2,
    "opponent": "Leeds",
    "opponent_short": "LEE",
    "us_xga_per_shot": 0.0211,
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 4,
    "team": "Newcastle",
    "team_short": "NEW",
    "situation": "OpenPlay",
    "is_home": false,
    "shots_faced": 14,
    "goals_against": 3,
    "us_xga": 2.2691,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 2,
    "opponent": "Leeds",
    "opponent_short": "LEE",
    "us_xga_per_shot": 0.1621,
    "built_at_utc": "2026-09-16T07:50:10Z"
  }
]
```


## `team_situation_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling for-metrics over last 5/10/15 matches  
**Rows:** 12,600

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
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "DirectFreekick",
    "shots": 3,
    "goals": 1,
    "us_xg": 0.1582,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xg_per_shot": 0.0527
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "FromCorner",
    "shots": 7,
    "goals": 1,
    "us_xg": 1.9228,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xg_per_shot": 0.2747
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "OpenPlay",
    "shots": 38,
    "goals": 4,
    "us_xg": 4.8948,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xg_per_shot": 0.1288
  }
]
```


## `team_situation_against_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling against-metrics over last 5/10/15 matches  
**Rows:** 12,600

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
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "DirectFreekick",
    "shots_faced": 1,
    "goals_against": 0,
    "us_xga": 0.0736,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xga_per_shot": 0.0736
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "FromCorner",
    "shots_faced": 7,
    "goals_against": 1,
    "us_xga": 0.633,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xga_per_shot": 0.0904
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "kickoff_raw": "2026-09-14 19:00:00",
    "is_home": true,
    "opponent_code": 4,
    "opponent": "Newcastle",
    "opponent_short": "NEW",
    "situation": "OpenPlay",
    "shots_faced": 46,
    "goals_against": 2,
    "us_xga": 3.8968,
    "window": 5,
    "built_at_utc": "2026-09-16T07:50:10Z",
    "us_xga_per_shot": 0.0847
  }
]
```


## `team_zone_match`

**Grain:** 1 row per team × match × shot_zone  
**What:** Box / six-yard / outside-box  
**Rows:** 2,293

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
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "shot_zone": "outside_box",
    "is_home": true,
    "shots": 5,
    "goals": 0,
    "us_xg": 0.2074,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "shot_zone": "penalty_area",
    "is_home": true,
    "shots": 8,
    "goals": 3,
    "us_xg": 1.2183,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31219",
    "team_code": 2,
    "team": "Leeds",
    "team_short": "LEE",
    "shot_zone": "six_yard",
    "is_home": true,
    "shots": 2,
    "goals": 0,
    "us_xg": 0.8645,
    "kickoff_raw": "2026-09-14 19:00:00",
    "opponent_code": 4,
    "opponent": "Newcastle",
    "built_at_utc": "2026-09-16T07:50:10Z"
  }
]
```


## `player_situation_season`

**Grain:** 1 row per understat player × season × situation  
**What:** Taker volume/quality by situation (player_code map TBD)  
**Rows:** 1,589

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
    "built_at_utc": "2026-09-16T07:50:10Z"
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
    "built_at_utc": "2026-09-16T07:50:10Z"
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
    "built_at_utc": "2026-09-16T07:50:10Z"
  }
]
```


## `player_create_situation_season`

**Grain:** 1 row per creator name × season × situation  
**What:** Assisted-shot xG by situation (player_code map TBD)  
**Rows:** 1,219

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
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Mathis Cherki",
    "situation": "OpenPlay",
    "assisted_shots": 45,
    "assisted_goals": 11,
    "assisted_us_xg": 9.0433,
    "player_id": "8094",
    "built_at_utc": "2026-09-16T07:50:10Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Jéremy Doku",
    "situation": "OpenPlay",
    "assisted_shots": 56,
    "assisted_goals": 5,
    "assisted_us_xg": 7.2875,
    "player_id": "8981",
    "built_at_utc": "2026-09-16T07:50:10Z"
  }
]
```

