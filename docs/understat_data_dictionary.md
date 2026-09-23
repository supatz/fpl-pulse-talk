# Understat masters — data dictionary (samples)

Generated `2026-09-23T17:50:01Z`.

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
    "match_id": "31229",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-20 15:30:00",
    "home_team_id": "228",
    "away_team_id": "89",
    "home_team": "Fulham",
    "away_team": "Manchester United",
    "home_short": "FLH",
    "away_short": "MUN",
    "home_goals": 1.0,
    "away_goals": 1.0,
    "home_xg": 1.7172,
    "away_xg": 2.1245,
    "forecast_w": 0.2919,
    "forecast_d": 0.2282,
    "forecast_l": 0.4799,
    "ingested_at_utc": "2026-09-23T17:49:56Z",
    "source": "understat.com"
  },
  {
    "match_id": "31222",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-20 13:00:00",
    "home_team_id": "88",
    "away_team_id": "77",
    "home_team": "Manchester City",
    "away_team": "Sunderland",
    "home_short": "MCI",
    "away_short": "SUN",
    "home_goals": 5.0,
    "away_goals": 3.0,
    "home_xg": 2.6686,
    "away_xg": 3.1066,
    "forecast_w": 0.3014,
    "forecast_d": 0.2268,
    "forecast_l": 0.4718,
    "ingested_at_utc": "2026-09-23T17:49:56Z",
    "source": "understat.com"
  },
  {
    "match_id": "31225",
    "understat_season": "2026",
    "season": "2026-2027",
    "league": "EPL",
    "is_result": true,
    "kickoff_raw": "2026-09-20 13:00:00",
    "home_team_id": "245",
    "away_team_id": "78",
    "home_team": "Leeds",
    "away_team": "Crystal Palace",
    "home_short": "LED",
    "away_short": "CRY",
    "home_goals": 0.0,
    "away_goals": 0.0,
    "home_xg": 1.0855,
    "away_xg": 1.1291,
    "forecast_w": 0.3359,
    "forecast_d": 0.3093,
    "forecast_l": 0.3548,
    "ingested_at_utc": "2026-09-23T17:49:56Z",
    "source": "understat.com"
  }
]
```


## `shot`

**Grain:** 1 row per shot  
**What:** Atomic fact: situation, last_action, coords, zone, player  
**Rows:** 10,922

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
    "ingested_at_utc": "2026-09-23T17:49:31Z",
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
    "ingested_at_utc": "2026-09-23T17:49:31Z",
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
    "ingested_at_utc": "2026-09-23T17:49:31Z",
    "source": "understat.com"
  }
]
```


## `team_match_style`

**Grain:** 1 row per team per match  
**What:** PPDA, deep completions, match xG/xGA from team history  
**Rows:** 860

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
    "team_id": "89",
    "team_title": "Manchester United",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "h_a": "a",
    "result": "d",
    "scored": 1.0,
    "conceded": 1.0,
    "xg": 2.1245,
    "xga": 1.7172,
    "npxg": 2.1245,
    "npxga": 1.7172,
    "npxgd": 0.4073,
    "xpts": 1.6679,
    "deep": 15.0,
    "deep_allowed": 5.0,
    "ppda_att": 281.0,
    "ppda_def": 14.0,
    "ppda": 20.0714,
    "ppda_allowed_att": 281.0,
    "ppda_allowed_def": 18.0,
    "ppda_allowed": 15.6111,
    "wins_cum": 0.0,
    "draws_cum": 1.0,
    "losses_cum": 0.0,
    "pts_cum": 1.0,
    "match_id": "31229",
    "opponent_id": "228",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "ingested_at_utc": "2026-09-23T17:49:46Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "228",
    "team_title": "Fulham",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": true,
    "h_a": "h",
    "result": "d",
    "scored": 1.0,
    "conceded": 1.0,
    "xg": 1.7172,
    "xga": 2.1245,
    "npxg": 1.7172,
    "npxga": 2.1245,
    "npxgd": -0.4073,
    "xpts": 1.1039,
    "deep": 5.0,
    "deep_allowed": 15.0,
    "ppda_att": 281.0,
    "ppda_def": 18.0,
    "ppda": 15.6111,
    "ppda_allowed_att": 281.0,
    "ppda_allowed_def": 14.0,
    "ppda_allowed": 20.0714,
    "wins_cum": 0.0,
    "draws_cum": 1.0,
    "losses_cum": 0.0,
    "pts_cum": 1.0,
    "match_id": "31229",
    "opponent_id": "89",
    "team_code": 54,
    "team": "Fulham",
    "team_short": "FUL",
    "opponent_code": 1,
    "opponent": "Man Utd",
    "opponent_short": "MUN",
    "ingested_at_utc": "2026-09-23T17:49:46Z",
    "source": "understat.com"
  },
  {
    "understat_season": "2026",
    "season": "2026-2027",
    "team_id": "73",
    "team_title": "Bournemouth",
    "kickoff_raw": "2026-09-20 13:00:00",
    "is_home": true,
    "h_a": "h",
    "result": "l",
    "scored": 0.0,
    "conceded": 1.0,
    "xg": 0.9447,
    "xga": 1.2912,
    "npxg": 0.9447,
    "npxga": 1.2912,
    "npxgd": -0.3465,
    "xpts": 1.0417,
    "deep": 8.0,
    "deep_allowed": 8.0,
    "ppda_att": 237.0,
    "ppda_def": 21.0,
    "ppda": 11.2857,
    "ppda_allowed_att": 174.0,
    "ppda_allowed_def": 18.0,
    "ppda_allowed": 9.6667,
    "wins_cum": 0.0,
    "draws_cum": 0.0,
    "losses_cum": 1.0,
    "pts_cum": 0.0,
    "match_id": "31228",
    "opponent_id": "87",
    "team_code": 91,
    "team": "Bournemouth",
    "team_short": "BOU",
    "opponent_code": 14,
    "opponent": "Liverpool",
    "opponent_short": "LIV",
    "ingested_at_utc": "2026-09-23T17:49:46Z",
    "source": "understat.com"
  }
]
```


## `team_context_season`

**Grain:** 1 row per team × season × context_family × context_value  
**What:** Season splits incl. attackSpeed (for + against)  
**Rows:** 1,327

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
    "ingested_at_utc": "2026-09-23T17:49:42Z",
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
    "ingested_at_utc": "2026-09-23T17:49:42Z",
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
    "ingested_at_utc": "2026-09-23T17:49:42Z",
    "source": "understat.com"
  }
]
```


## `league_player`

**Grain:** 1 row per player per season  
**What:** Understat season totals (xg_chain, etc.)  
**Rows:** 958

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
    "ingested_at_utc": "2026-09-23T17:49:43Z",
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
    "ingested_at_utc": "2026-09-23T17:49:43Z",
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
    "ingested_at_utc": "2026-09-23T17:49:43Z",
    "source": "understat.com"
  }
]
```


## `roster`

**Grain:** 1 row per player × finished match  
**What:** Understat match roster used by the PL merge  
**Rows:** 13,028

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
    "ingested_at_utc": "2026-09-23T17:49:56Z",
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
    "ingested_at_utc": "2026-09-23T17:49:56Z",
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
    "ingested_at_utc": "2026-09-23T17:49:56Z",
    "source": "understat.com"
  }
]
```


## `team_situation_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xg created (for)  
**Rows:** 2,313

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
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "situation": "FromCorner",
    "is_home": false,
    "shots": 11,
    "goals": 0,
    "us_xg": 0.3543,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "us_xg_per_shot": 0.0322,
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "situation": "OpenPlay",
    "is_home": false,
    "shots": 18,
    "goals": 1,
    "us_xg": 1.7862,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "us_xg_per_shot": 0.0992,
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "situation": "SetPiece",
    "is_home": false,
    "shots": 1,
    "goals": 0,
    "us_xg": 0.0448,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "us_xg_per_shot": 0.0448,
    "built_at_utc": "2026-09-23T17:50:00Z"
  }
]
```


## `team_situation_against_match`

**Grain:** 1 row per team × match × situation  
**What:** Shots/goals/us_xga faced (against)  
**Rows:** 2,313

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
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "situation": "OpenPlay",
    "is_home": false,
    "shots_faced": 12,
    "goals_against": 0,
    "us_xga": 1.7172,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "us_xga_per_shot": 0.1431,
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 54,
    "team": "Fulham",
    "team_short": "FUL",
    "situation": "FromCorner",
    "is_home": true,
    "shots_faced": 11,
    "goals_against": 0,
    "us_xga": 0.3543,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 1,
    "opponent": "Man Utd",
    "opponent_short": "MUN",
    "us_xga_per_shot": 0.0322,
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 54,
    "team": "Fulham",
    "team_short": "FUL",
    "situation": "OpenPlay",
    "is_home": true,
    "shots_faced": 18,
    "goals_against": 1,
    "us_xga": 1.7862,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 1,
    "opponent": "Man Utd",
    "opponent_short": "MUN",
    "us_xga_per_shot": 0.0992,
    "built_at_utc": "2026-09-23T17:50:00Z"
  }
]
```


## `team_situation_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling for-metrics over last 5/10/15 matches  
**Rows:** 12,900

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
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "DirectFreekick",
    "shots": 3,
    "goals": 0,
    "us_xg": 0.1237,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xg_per_shot": 0.0412
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "FromCorner",
    "shots": 21,
    "goals": 0,
    "us_xg": 0.8621,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xg_per_shot": 0.0411
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "OpenPlay",
    "shots": 86,
    "goals": 6,
    "us_xg": 9.0233,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xg_per_shot": 0.1049
  }
]
```


## `team_situation_against_rolling`

**Grain:** 1 row per team × match × situation × window  
**What:** Rolling against-metrics over last 5/10/15 matches  
**Rows:** 12,900

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
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "DirectFreekick",
    "shots_faced": 0,
    "goals_against": 0,
    "us_xga": 0.0,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xga_per_shot": null
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "FromCorner",
    "shots_faced": 7,
    "goals_against": 1,
    "us_xga": 1.2485,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xga_per_shot": 0.1784
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "kickoff_raw": "2026-09-20 15:30:00",
    "is_home": false,
    "opponent_code": 54,
    "opponent": "Fulham",
    "opponent_short": "FUL",
    "situation": "OpenPlay",
    "shots_faced": 40,
    "goals_against": 5,
    "us_xga": 5.2617,
    "window": 5,
    "built_at_utc": "2026-09-23T17:50:00Z",
    "us_xga_per_shot": 0.1315
  }
]
```


## `team_zone_match`

**Grain:** 1 row per team × match × shot_zone  
**What:** Box / six-yard / outside-box  
**Rows:** 2,348

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
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "shot_zone": "outside_box",
    "is_home": false,
    "shots": 12,
    "goals": 1,
    "us_xg": 0.3088,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "shot_zone": "own_goal",
    "is_home": false,
    "shots": 1,
    "goals": 0,
    "us_xg": 0.0,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2026-2027",
    "match_id": "31229",
    "team_code": 1,
    "team": "Man Utd",
    "team_short": "MUN",
    "shot_zone": "penalty_area",
    "is_home": false,
    "shots": 14,
    "goals": 0,
    "us_xg": 1.6635,
    "kickoff_raw": "2026-09-20 15:30:00",
    "opponent_code": 54,
    "opponent": "Fulham",
    "built_at_utc": "2026-09-23T17:50:00Z"
  }
]
```


## `player_situation_season`

**Grain:** 1 row per understat player × season × situation  
**What:** Taker volume/quality by situation (player_code applied at serving)  
**Rows:** 1,658

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
    "built_at_utc": "2026-09-23T17:50:00Z"
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
    "built_at_utc": "2026-09-23T17:50:00Z"
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
    "built_at_utc": "2026-09-23T17:50:00Z"
  }
]
```


## `player_create_situation_season`

**Grain:** 1 row per creator name × season × situation  
**What:** Assisted-shot xG by situation (player_code applied at serving)  
**Rows:** 1,265

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
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Mathis Cherki",
    "situation": "OpenPlay",
    "assisted_shots": 45,
    "assisted_goals": 11,
    "assisted_us_xg": 9.0433,
    "player_id": "8094",
    "built_at_utc": "2026-09-23T17:50:00Z"
  },
  {
    "season": "2025-2026",
    "player_name": "Jéremy Doku",
    "situation": "OpenPlay",
    "assisted_shots": 56,
    "assisted_goals": 5,
    "assisted_us_xg": 7.2875,
    "player_id": "8981",
    "built_at_utc": "2026-09-23T17:50:00Z"
  }
]
```

