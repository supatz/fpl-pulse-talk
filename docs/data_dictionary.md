# FPL master datasets — data dictionary

Generated `2026-11-15T19:01:31Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **21,918**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,824 (8.3%) |  |
| `assists` | `Float64` | 1,903 (8.7%) |  |
| `total_shots` | `Float64` | 4,098 (18.7%) |  |
| `xg` | `Float64` | 4,339 (19.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 3,415 (15.6%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 4,098 (18.7%) |  |
| `successful_dribbles` | `String` | 6,548 (29.9%) |  |
| `big_chances_missed` | `String` | 6,876 (31.4%) |  |
| `touches_opposition_box` | `Float64` | 2,232 (10.2%) |  |
| `touches` | `Float64` | 1,570 (7.2%) |  |
| `accurate_passes` | `Float64` | 1,904 (8.7%) |  |
| `accurate_passes_percent` | `Float64` | 1,983 (9.0%) |  |
| `chances_created` | `Float64` | 1,890 (8.6%) |  |
| `final_third_passes` | `Float64` | 2,885 (13.2%) |  |
| `accurate_crosses` | `Float64` | 4,437 (20.2%) |  |
| `accurate_crosses_percent` | `Float64` | 4,472 (20.4%) |  |
| `accurate_long_balls` | `Float64` | 3,431 (15.7%) |  |
| `accurate_long_balls_percent` | `Float64` | 3,466 (15.8%) |  |
| `tackles_won` | `Float64` | 1,570 (7.2%) |  |
| `interceptions` | `Float64` | 1,570 (7.2%) |  |
| `recoveries` | `Float64` | 1,570 (7.2%) |  |
| `blocks` | `Float64` | 2,232 (10.2%) |  |
| `clearances` | `Float64` | 1,570 (7.2%) |  |
| `headed_clearances` | `Float64` | 5,056 (23.1%) |  |
| `dribbled_past` | `Float64` | 2,232 (10.2%) |  |
| `duels_won` | `Float64` | 2,441 (11.1%) |  |
| `duels_lost` | `Float64` | 2,483 (11.3%) |  |
| `ground_duels_won` | `Float64` | 2,238 (10.2%) |  |
| `ground_duels_won_percent` | `Float64` | 2,238 (10.2%) |  |
| `aerial_duels_won` | `Float64` | 1,858 (8.5%) |  |
| `aerial_duels_won_percent` | `Float64` | 3,424 (15.6%) |  |
| `was_fouled` | `Float64` | 4,351 (19.9%) |  |
| `fouls_committed` | `Float64` | 1,570 (7.2%) |  |
| `saves` | `Float64` | 6,214 (28.4%) |  |
| `goals_conceded` | `Float64` | 6,214 (28.4%) |  |
| `xgot_faced` | `String` | 6,594 (30.1%) |  |
| `goals_prevented` | `String` | 6,594 (30.1%) |  |
| `sweeper_actions` | `Float64` | 6,542 (29.8%) |  |
| `gk_accurate_passes` | `Float64` | 6,542 (29.8%) |  |
| `gk_accurate_long_balls` | `Float64` | 6,546 (29.9%) |  |
| `dispossessed` | `String` | 2,217 (10.1%) |  |
| `high_claim` | `Float64` | 6,542 (29.8%) |  |
| `saves_inside_box` | `Float64` | 6,542 (29.8%) |  |
| `offsides` | `String` | 6,876 (31.4%) |  |
| `successful_dribbles_percent` | `String` | 6,583 (30.0%) |  |
| `tackles_won_percent` | `String` | 6,583 (30.0%) |  |
| `xgot` | `Float64` | 5,548 (25.3%) |  |
| `tackles` | `String` | 6,548 (29.9%) |  |
| `start_min` | `Int64` | 1,617 (7.4%) |  |
| `finish_min` | `Int64` | 1,617 (7.4%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.4%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 16,087 (73.4%) |  |
| `distance_covered` | `String` | 16,087 (73.4%) |  |
| `walking_distance` | `String` | 19,163 (87.4%) |  |
| `running_distance` | `String` | 16,087 (73.4%) |  |
| `sprinting_distance` | `String` | 16,232 (74.1%) |  |
| `number_of_sprints` | `String` | 16,356 (74.6%) |  |
| `defensive_contributions` | `String` | 7,078 (32.3%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,791 (8.2%) |  |
| `away_team` | `Int64` | 2,134 (9.7%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.4%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.4%) |  |
| `is_home` | `Boolean` | 1,791 (8.2%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 4,094 (18.7%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.2%) |  |
| `team_goals_against` | `Float64` | 253 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.2%) |  |
| `started` | `Boolean` | 8,418 (38.4%) |  |
| `formation` | `String` | 8,418 (38.4%) |  |
| `lineup_status` | `String` | 8,418 (38.4%) |  |
| `lineup_team_code` | `Int64` | 8,418 (38.4%) |  |
| `rating` | `Float64` | 9,341 (42.6%) |  |
| `yellow_cards` | `Float64` | 9,102 (41.5%) |  |
| `red_cards` | `Float64` | 9,102 (41.5%) |  |
| `np_xg` | `Float64` | 14,310 (65.3%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 14,310 (65.3%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 14,310 (65.3%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 14,310 (65.3%) |  |
| `own_goals` | `Float64` | 1,041 (4.7%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 21,918 (100.0%) |  |
| `fpl_points` | `Float64` | 1,041 (4.7%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,041 (4.7%) |  |
| `bps` | `Float64` | 1,041 (4.7%) |  |
| `now_cost` | `Float64` | 1,041 (4.7%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,041 (4.7%) |  |
| `form` | `Float64` | 1,041 (4.7%) |  |
| `penalties_order` | `String` | 19,663 (89.7%) |  |
| `direct_freekicks_order` | `String` | 19,531 (89.1%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 18,727 (85.4%) |  |
| `status` | `String` | 1,041 (4.7%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **36,574**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 23,887 (65.3%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (16.4%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 33,471 (91.5%) |  |
| `direct_freekicks_order` | `String` | 34,205 (93.5%) |  |
| `penalties_order` | `String` | 34,281 (93.7%) |  |
| `set_piece_threat` | `String` | 36,574 (100.0%) |  |
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

Rows: **1,928**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 324 (16.8%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 607 (31.5%) |  |
| `goals_against` | `Float64` | 607 (31.5%) |  |
| `elo` | `Float64` | 1,002 (52.0%) |  |
| `possession` | `Float64` | 687 (35.6%) |  |
| `xg` | `Float64` | 688 (35.7%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 722 (37.4%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 716 (37.1%) |  |
| `xg_set_play` | `String` | 716 (37.1%) |  |
| `xgot` | `Float64` | 716 (37.1%) |  |
| `total_shots` | `String` | 681 (35.3%) |  |
| `shots_on_target` | `String` | 681 (35.3%) |  |
| `shots_inside_box` | `String` | 682 (35.4%) |  |
| `shots_outside_box` | `String` | 682 (35.4%) |  |
| `big_chances` | `String` | 682 (35.4%) |  |
| `big_chances_missed` | `String` | 682 (35.4%) |  |
| `touches_in_opposition_box` | `String` | 682 (35.4%) |  |
| `corners` | `String` | 681 (35.3%) |  |
| `accurate_passes` | `String` | 682 (35.4%) |  |
| `accurate_passes_pct` | `String` | 682 (35.4%) |  |
| `accurate_long_balls` | `String` | 682 (35.4%) |  |
| `accurate_long_balls_pct` | `String` | 682 (35.4%) |  |
| `accurate_crosses` | `String` | 682 (35.4%) |  |
| `accurate_crosses_pct` | `String` | 682 (35.4%) |  |
| `tackles_won` | `String` | 691 (35.8%) |  |
| `tackles_won_pct` | `String` | 1,017 (52.7%) |  |
| `interceptions` | `String` | 682 (35.4%) |  |
| `blocks` | `String` | 686 (35.6%) |  |
| `clearances` | `String` | 682 (35.4%) |  |
| `duels_won` | `String` | 686 (35.6%) |  |
| `aerial_duels_won` | `String` | 682 (35.4%) |  |
| `aerial_duels_won_pct` | `String` | 682 (35.4%) |  |
| `ground_duels_won` | `String` | 682 (35.4%) |  |
| `ground_duels_won_pct` | `String` | 683 (35.4%) |  |
| `fouls_committed` | `String` | 682 (35.4%) |  |
| `offsides` | `String` | 682 (35.4%) |  |
| `yellow_cards` | `String` | 684 (35.5%) |  |
| `red_cards` | `String` | 685 (35.5%) |  |
| `keeper_saves` | `String` | 682 (35.4%) |  |
| `successful_dribbles` | `String` | 682 (35.4%) |  |
| `successful_dribbles_pct` | `String` | 682 (35.4%) |  |
| `possession_against` | `String` | 687 (35.6%) |  |
| `xga` | `Float64` | 688 (35.7%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 722 (37.4%) |  |
| `xg_open_play_against` | `String` | 716 (37.1%) |  |
| `xg_set_play_against` | `String` | 716 (37.1%) |  |
| `xgot_against` | `String` | 716 (37.1%) |  |
| `shots_conceded` | `String` | 681 (35.3%) |  |
| `sot_conceded` | `String` | 681 (35.3%) |  |
| `shots_inside_box_against` | `String` | 682 (35.4%) |  |
| `shots_outside_box_against` | `String` | 682 (35.4%) |  |
| `big_chances_conceded` | `String` | 682 (35.4%) |  |
| `big_chances_missed_against` | `String` | 682 (35.4%) |  |
| `touches_in_opposition_box_against` | `String` | 682 (35.4%) |  |
| `corners_against` | `String` | 681 (35.3%) |  |
| `accurate_passes_against` | `String` | 682 (35.4%) |  |
| `accurate_passes_pct_against` | `String` | 682 (35.4%) |  |
| `accurate_long_balls_against` | `String` | 682 (35.4%) |  |
| `accurate_long_balls_pct_against` | `String` | 682 (35.4%) |  |
| `accurate_crosses_against` | `String` | 682 (35.4%) |  |
| `accurate_crosses_pct_against` | `String` | 682 (35.4%) |  |
| `tackles_won_against` | `String` | 691 (35.8%) |  |
| `tackles_won_pct_against` | `String` | 1,017 (52.7%) |  |
| `interceptions_against` | `String` | 682 (35.4%) |  |
| `blocks_against` | `String` | 686 (35.6%) |  |
| `clearances_against` | `String` | 682 (35.4%) |  |
| `duels_won_against` | `String` | 686 (35.6%) |  |
| `aerial_duels_won_against` | `String` | 682 (35.4%) |  |
| `aerial_duels_won_pct_against` | `String` | 682 (35.4%) |  |
| `ground_duels_won_against` | `String` | 682 (35.4%) |  |
| `ground_duels_won_pct_against` | `String` | 683 (35.4%) |  |
| `fouls_committed_against` | `String` | 682 (35.4%) |  |
| `offsides_against` | `String` | 682 (35.4%) |  |
| `yellow_cards_against` | `String` | 684 (35.5%) |  |
| `red_cards_against` | `String` | 685 (35.5%) |  |
| `keeper_saves_against` | `String` | 682 (35.4%) |  |
| `successful_dribbles_against` | `String` | 682 (35.4%) |  |
| `successful_dribbles_pct_against` | `String` | 682 (35.4%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 607 (31.5%) |  |
| `points` | `Int64` | 607 (31.5%) |  |
| `clean_sheet` | `Boolean` | 607 (31.5%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,832 (95.0%) |  |
| `weather_description` | `String` | 1,856 (96.3%) |  |
| `temperature_c` | `String` | 1,832 (95.0%) |  |
| `wind_speed` | `String` | 1,832 (95.0%) |  |
| `pitch_condition` | `String` | 1,832 (95.0%) |  |
| `is_local_derby` | `Boolean` | 1,054 (54.7%) |  |
| `is_neutral_ground` | `Boolean` | 1,054 (54.7%) |  |
| `lineup_status` | `String` | 1,054 (54.7%) |  |
| `strength` | `Float64` | 1,003 (52.0%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 1,003 (52.0%) |  |
| `strength_attack_away` | `Float64` | 1,003 (52.0%) |  |
| `strength_defence_home` | `Float64` | 1,003 (52.0%) |  |
| `strength_defence_away` | `Float64` | 1,003 (52.0%) |  |
| `home_shot_model_xg` | `Float64` | 1,168 (60.6%) |  |
| `away_shot_model_xg` | `Float64` | 1,168 (60.6%) |  |
| `incident_timing_coverage` | `String` | 1,168 (60.6%) |  |
| `unlocated_card_count` | `Int64` | 1,168 (60.6%) |  |
| `quarantined_incident_count` | `Int64` | 1,168 (60.6%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **283**. Columns: **12**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `kickoff_utc` | `String` | 1 (0.4%) |  |
| `home_team` | `Int64` | 0 (0.0%) |  |
| `away_team` | `Int64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

