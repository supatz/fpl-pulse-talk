# FPL master datasets — data dictionary

Generated `2026-10-28T07:24:35Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **20,691**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,500 (7.2%) |  |
| `assists` | `Float64` | 1,579 (7.6%) |  |
| `total_shots` | `Float64` | 3,359 (16.2%) |  |
| `xg` | `Float64` | 3,600 (17.4%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 2,854 (13.8%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 3,359 (16.2%) |  |
| `successful_dribbles` | `String` | 5,321 (25.7%) |  |
| `big_chances_missed` | `String` | 5,649 (27.3%) |  |
| `touches_opposition_box` | `Float64` | 1,908 (9.2%) |  |
| `touches` | `Float64` | 1,308 (6.3%) |  |
| `accurate_passes` | `Float64` | 1,580 (7.6%) |  |
| `accurate_passes_percent` | `Float64` | 1,649 (8.0%) |  |
| `chances_created` | `Float64` | 1,568 (7.6%) |  |
| `final_third_passes` | `Float64` | 2,432 (11.8%) |  |
| `accurate_crosses` | `Float64` | 3,615 (17.5%) |  |
| `accurate_crosses_percent` | `Float64` | 3,650 (17.6%) |  |
| `accurate_long_balls` | `Float64` | 2,808 (13.6%) |  |
| `accurate_long_balls_percent` | `Float64` | 2,843 (13.7%) |  |
| `tackles_won` | `Float64` | 1,308 (6.3%) |  |
| `interceptions` | `Float64` | 1,308 (6.3%) |  |
| `recoveries` | `Float64` | 1,308 (6.3%) |  |
| `blocks` | `Float64` | 1,908 (9.2%) |  |
| `clearances` | `Float64` | 1,308 (6.3%) |  |
| `headed_clearances` | `Float64` | 4,206 (20.3%) |  |
| `dribbled_past` | `Float64` | 1,908 (9.2%) |  |
| `duels_won` | `Float64` | 2,027 (9.8%) |  |
| `duels_lost` | `Float64` | 2,058 (9.9%) |  |
| `ground_duels_won` | `Float64` | 1,860 (9.0%) |  |
| `ground_duels_won_percent` | `Float64` | 1,860 (9.0%) |  |
| `aerial_duels_won` | `Float64` | 1,550 (7.5%) |  |
| `aerial_duels_won_percent` | `Float64` | 2,835 (13.7%) |  |
| `was_fouled` | `Float64` | 3,566 (17.2%) |  |
| `fouls_committed` | `Float64` | 1,308 (6.3%) |  |
| `saves` | `Float64` | 5,049 (24.4%) |  |
| `goals_conceded` | `Float64` | 5,049 (24.4%) |  |
| `xgot_faced` | `String` | 5,427 (26.2%) |  |
| `goals_prevented` | `String` | 5,427 (26.2%) |  |
| `sweeper_actions` | `Float64` | 5,377 (26.0%) |  |
| `gk_accurate_passes` | `Float64` | 5,377 (26.0%) |  |
| `gk_accurate_long_balls` | `Float64` | 5,380 (26.0%) |  |
| `dispossessed` | `String` | 1,893 (9.1%) |  |
| `high_claim` | `Float64` | 5,377 (26.0%) |  |
| `saves_inside_box` | `Float64` | 5,377 (26.0%) |  |
| `offsides` | `String` | 5,649 (27.3%) |  |
| `successful_dribbles_percent` | `String` | 5,356 (25.9%) |  |
| `tackles_won_percent` | `String` | 5,356 (25.9%) |  |
| `xgot` | `Float64` | 4,542 (22.0%) |  |
| `tackles` | `String` | 5,321 (25.7%) |  |
| `start_min` | `Int64` | 1,355 (6.5%) |  |
| `finish_min` | `Int64` | 1,355 (6.5%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.5%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 15,497 (74.9%) |  |
| `distance_covered` | `String` | 15,497 (74.9%) |  |
| `walking_distance` | `String` | 17,952 (86.8%) |  |
| `running_distance` | `String` | 15,497 (74.9%) |  |
| `sprinting_distance` | `String` | 15,614 (75.5%) |  |
| `number_of_sprints` | `String` | 15,714 (75.9%) |  |
| `defensive_contributions` | `String` | 5,851 (28.3%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,649 (8.0%) |  |
| `away_team` | `Int64` | 2,076 (10.0%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.6%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.6%) |  |
| `is_home` | `Boolean` | 1,649 (8.0%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,894 (18.8%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.2%) |  |
| `team_goals_against` | `Float64` | 253 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.2%) |  |
| `started` | `Boolean` | 7,191 (34.8%) |  |
| `formation` | `String` | 7,191 (34.8%) |  |
| `lineup_status` | `String` | 7,191 (34.8%) |  |
| `lineup_team_code` | `Int64` | 7,191 (34.8%) |  |
| `rating` | `Float64` | 8,114 (39.2%) |  |
| `yellow_cards` | `Float64` | 7,875 (38.1%) |  |
| `red_cards` | `Float64` | 7,875 (38.1%) |  |
| `np_xg` | `Float64` | 13,363 (64.6%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 13,363 (64.6%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 13,363 (64.6%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 13,363 (64.6%) |  |
| `own_goals` | `Float64` | 1,040 (5.0%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 20,691 (100.0%) |  |
| `fpl_points` | `Float64` | 1,040 (5.0%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,040 (5.0%) |  |
| `bps` | `Float64` | 1,040 (5.0%) |  |
| `now_cost` | `Float64` | 1,040 (5.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,040 (5.0%) |  |
| `form` | `Float64` | 1,040 (5.0%) |  |
| `penalties_order` | `String` | 18,594 (89.9%) |  |
| `direct_freekicks_order` | `String` | 18,491 (89.4%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 17,761 (85.8%) |  |
| `status` | `String` | 1,040 (5.0%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **35,232**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 22,929 (65.1%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (17.1%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 32,325 (91.7%) |  |
| `direct_freekicks_order` | `String` | 33,007 (93.7%) |  |
| `penalties_order` | `String` | 33,066 (93.9%) |  |
| `set_piece_threat` | `String` | 35,232 (100.0%) |  |
| `minutes` | `Float64` | 0 (0.0%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals_scored` | `Float64` | 0 (0.0%) |  |
| `assists` | `Float64` | 0 (0.0%) |  |
| `clean_sheets` | `Float64` | 0 (0.0%) |  |
| `goals_conceded` | `Float64` | 0 (0.0%) |  |
| `own_goals` | `Float64` | 0 (0.0%) |  |
| `penalties_saved` | `Float64` | 0 (0.0%) |  |
| `penalties_missed` | `Float64` | 0 (0.0%) |  |
| `yellow_cards` | `Float64` | 0 (0.0%) |  |
| `red_cards` | `Float64` | 0 (0.0%) |  |
| `saves` | `Float64` | 0 (0.0%) |  |
| `starts` | `Float64` | 0 (0.0%) |  |
| `expected_goals` | `Float64` | 0 (0.0%) | FPL-API xG family on player_gw. Do not mix with Opta xg. |
| `expected_assists` | `Float64` | 0 (0.0%) |  |
| `expected_goal_involvements` | `Float64` | 0 (0.0%) |  |
| `expected_goals_conceded` | `Float64` | 0 (0.0%) |  |
| `influence` | `Float64` | 0 (0.0%) |  |
| `creativity` | `Float64` | 0 (0.0%) |  |
| `threat` | `Float64` | 0 (0.0%) |  |
| `ict_index` | `Float64` | 0 (0.0%) |  |
| `tackles` | `Float64` | 0 (0.0%) |  |
| `clearances_blocks_interceptions` | `Float64` | 0 (0.0%) |  |
| `recoveries` | `Float64` | 0 (0.0%) |  |
| `defensive_contribution` | `Float64` | 0 (0.0%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `position` | `String` | 0 (0.0%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `team_match`

Rows: **1,922**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 322 (16.8%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 662 (34.4%) |  |
| `goals_against` | `Float64` | 662 (34.4%) |  |
| `elo` | `Float64` | 996 (51.8%) |  |
| `possession` | `Float64` | 743 (38.7%) |  |
| `xg` | `Float64` | 744 (38.7%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 778 (40.5%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 772 (40.2%) |  |
| `xg_set_play` | `String` | 772 (40.2%) |  |
| `xgot` | `Float64` | 772 (40.2%) |  |
| `total_shots` | `String` | 737 (38.3%) |  |
| `shots_on_target` | `String` | 737 (38.3%) |  |
| `shots_inside_box` | `String` | 738 (38.4%) |  |
| `shots_outside_box` | `String` | 738 (38.4%) |  |
| `big_chances` | `String` | 738 (38.4%) |  |
| `big_chances_missed` | `String` | 738 (38.4%) |  |
| `touches_in_opposition_box` | `String` | 738 (38.4%) |  |
| `corners` | `String` | 737 (38.3%) |  |
| `accurate_passes` | `String` | 738 (38.4%) |  |
| `accurate_passes_pct` | `String` | 738 (38.4%) |  |
| `accurate_long_balls` | `String` | 738 (38.4%) |  |
| `accurate_long_balls_pct` | `String` | 738 (38.4%) |  |
| `accurate_crosses` | `String` | 738 (38.4%) |  |
| `accurate_crosses_pct` | `String` | 738 (38.4%) |  |
| `tackles_won` | `String` | 747 (38.9%) |  |
| `tackles_won_pct` | `String` | 1,011 (52.6%) |  |
| `interceptions` | `String` | 738 (38.4%) |  |
| `blocks` | `String` | 742 (38.6%) |  |
| `clearances` | `String` | 738 (38.4%) |  |
| `duels_won` | `String` | 742 (38.6%) |  |
| `aerial_duels_won` | `String` | 738 (38.4%) |  |
| `aerial_duels_won_pct` | `String` | 738 (38.4%) |  |
| `ground_duels_won` | `String` | 738 (38.4%) |  |
| `ground_duels_won_pct` | `String` | 739 (38.4%) |  |
| `fouls_committed` | `String` | 738 (38.4%) |  |
| `offsides` | `String` | 738 (38.4%) |  |
| `yellow_cards` | `String` | 740 (38.5%) |  |
| `red_cards` | `String` | 741 (38.6%) |  |
| `keeper_saves` | `String` | 738 (38.4%) |  |
| `successful_dribbles` | `String` | 738 (38.4%) |  |
| `successful_dribbles_pct` | `String` | 738 (38.4%) |  |
| `possession_against` | `String` | 743 (38.7%) |  |
| `xga` | `Float64` | 744 (38.7%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 778 (40.5%) |  |
| `xg_open_play_against` | `String` | 772 (40.2%) |  |
| `xg_set_play_against` | `String` | 772 (40.2%) |  |
| `xgot_against` | `String` | 772 (40.2%) |  |
| `shots_conceded` | `String` | 737 (38.3%) |  |
| `sot_conceded` | `String` | 737 (38.3%) |  |
| `shots_inside_box_against` | `String` | 738 (38.4%) |  |
| `shots_outside_box_against` | `String` | 738 (38.4%) |  |
| `big_chances_conceded` | `String` | 738 (38.4%) |  |
| `big_chances_missed_against` | `String` | 738 (38.4%) |  |
| `touches_in_opposition_box_against` | `String` | 738 (38.4%) |  |
| `corners_against` | `String` | 737 (38.3%) |  |
| `accurate_passes_against` | `String` | 738 (38.4%) |  |
| `accurate_passes_pct_against` | `String` | 738 (38.4%) |  |
| `accurate_long_balls_against` | `String` | 738 (38.4%) |  |
| `accurate_long_balls_pct_against` | `String` | 738 (38.4%) |  |
| `accurate_crosses_against` | `String` | 738 (38.4%) |  |
| `accurate_crosses_pct_against` | `String` | 738 (38.4%) |  |
| `tackles_won_against` | `String` | 747 (38.9%) |  |
| `tackles_won_pct_against` | `String` | 1,011 (52.6%) |  |
| `interceptions_against` | `String` | 738 (38.4%) |  |
| `blocks_against` | `String` | 742 (38.6%) |  |
| `clearances_against` | `String` | 738 (38.4%) |  |
| `duels_won_against` | `String` | 742 (38.6%) |  |
| `aerial_duels_won_against` | `String` | 738 (38.4%) |  |
| `aerial_duels_won_pct_against` | `String` | 738 (38.4%) |  |
| `ground_duels_won_against` | `String` | 738 (38.4%) |  |
| `ground_duels_won_pct_against` | `String` | 739 (38.4%) |  |
| `fouls_committed_against` | `String` | 738 (38.4%) |  |
| `offsides_against` | `String` | 738 (38.4%) |  |
| `yellow_cards_against` | `String` | 740 (38.5%) |  |
| `red_cards_against` | `String` | 741 (38.6%) |  |
| `keeper_saves_against` | `String` | 738 (38.4%) |  |
| `successful_dribbles_against` | `String` | 738 (38.4%) |  |
| `successful_dribbles_pct_against` | `String` | 738 (38.4%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 662 (34.4%) |  |
| `points` | `Int64` | 663 (34.5%) |  |
| `clean_sheet` | `Boolean` | 663 (34.5%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,826 (95.0%) |  |
| `weather_description` | `String` | 1,850 (96.3%) |  |
| `temperature_c` | `String` | 1,826 (95.0%) |  |
| `wind_speed` | `String` | 1,826 (95.0%) |  |
| `pitch_condition` | `String` | 1,826 (95.0%) |  |
| `is_local_derby` | `Boolean` | 1,048 (54.5%) |  |
| `is_neutral_ground` | `Boolean` | 1,048 (54.5%) |  |
| `lineup_status` | `String` | 1,048 (54.5%) |  |
| `strength` | `Float64` | 997 (51.9%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 997 (51.9%) |  |
| `strength_attack_away` | `Float64` | 997 (51.9%) |  |
| `strength_defence_home` | `Float64` | 997 (51.9%) |  |
| `strength_defence_away` | `Float64` | 997 (51.9%) |  |
| `home_shot_model_xg` | `Float64` | 1,162 (60.5%) |  |
| `away_shot_model_xg` | `Float64` | 1,162 (60.5%) |  |
| `incident_timing_coverage` | `String` | 1,162 (60.5%) |  |
| `unlocated_card_count` | `Int64` | 1,162 (60.5%) |  |
| `quarantined_incident_count` | `Int64` | 1,162 (60.5%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **307**. Columns: **12**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `kickoff_utc` | `String` | 1 (0.3%) |  |
| `home_team` | `Int64` | 0 (0.0%) |  |
| `away_team` | `Int64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

