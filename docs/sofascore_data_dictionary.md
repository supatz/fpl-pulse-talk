# SofaScore data dictionary

Generated `2026-11-15T19:37:10Z`. Parallel to Understat; never coalesced.

| Table | Grain | Notes | Rows |
|---|---|---|---|
| `event` | 1 row per Premier League fixture | SofaScore event_id, kickoff, teams, score | 761 |

**event columns:** `event_id`, `ss_season_id`, `season`, `kickoff_ts`, `kickoff_utc`, `kick_date`, `is_result`, `home_team_id`, `away_team_id`, `home_team`, `away_team`, `home_short`, `away_short`, `home_goals`, `away_goals`, `round`, `has_xg`, `ingested_at_utc`, `source`
| `shot` | 1 row per shot | Native situation, shotType, coords 0–100, xg/xgot, zones | 12289 |

**shot columns:** `shot_id`, `event_id`, `season`, `minute`, `time_seconds`, `is_home`, `team_id`, `opponent_id`, `player_id`, `player_name`, `situation`, `shot_type`, `body_part`, `goal_type`, `xg`, `xgot`, `x`, `y`, `x01`, `y01`, `shot_zone`, `side`, `is_goal`, `is_sot` …
| `player_match` | 1 row per player × event from lineups | Native bigChancesCreated/Missed, expectedAssists | 19189 |

**player_match columns:** `event_id`, `season`, `team_id`, `is_home`, `player_id`, `player_name`, `position`, `minutes`, `expected_goals`, `expected_assists`, `big_chances_created`, `big_chances_missed`, `big_chances_scored`, `key_passes`, `total_shots`, `rating`, `ingested_at_utc`, `source`

Site player chips `BCC_sf` / `BCM_sf` / `SiB_sf` left-join this `player_match` + shot zone onto FPL `player_code`. Null when unmapped. No BCS/BCT from SofaScore. Unmapped players remain on SofaScore treemap. Fill `data/sofascore/review/player_mapping_worksheet.csv`.
