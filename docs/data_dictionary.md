# FPL master datasets — data dictionary

Generated `2026-08-22T08:04:19Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **16,428**. Columns: **125**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.4%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 318 (1.9%) |  |
| `assists` | `Float64` | 398 (2.4%) |  |
| `total_shots` | `Float64` | 745 (4.5%) |  |
| `xg` | `Float64` | 986 (6.0%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 924 (5.6%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 745 (4.5%) |  |
| `successful_dribbles` | `String` | 1,058 (6.4%) |  |
| `big_chances_missed` | `String` | 1,386 (8.4%) |  |
| `touches_opposition_box` | `Float64` | 726 (4.4%) |  |
| `touches` | `Float64` | 342 (2.1%) |  |
| `accurate_passes` | `Float64` | 398 (2.4%) |  |
| `accurate_passes_percent` | `Float64` | 436 (2.7%) |  |
| `chances_created` | `Float64` | 397 (2.4%) |  |
| `final_third_passes` | `Float64` | 814 (5.0%) |  |
| `accurate_crosses` | `Float64` | 800 (4.9%) |  |
| `accurate_crosses_percent` | `Float64` | 835 (5.1%) |  |
| `accurate_long_balls` | `Float64` | 615 (3.7%) |  |
| `accurate_long_balls_percent` | `Float64` | 650 (4.0%) |  |
| `tackles_won` | `Float64` | 342 (2.1%) |  |
| `interceptions` | `Float64` | 342 (2.1%) |  |
| `recoveries` | `Float64` | 342 (2.1%) |  |
| `blocks` | `Float64` | 726 (4.4%) |  |
| `clearances` | `Float64` | 342 (2.1%) |  |
| `headed_clearances` | `Float64` | 1,199 (7.3%) |  |
| `dribbled_past` | `Float64` | 726 (4.4%) |  |
| `duels_won` | `Float64` | 529 (3.2%) |  |
| `duels_lost` | `Float64` | 546 (3.3%) |  |
| `ground_duels_won` | `Float64` | 480 (2.9%) |  |
| `ground_duels_won_percent` | `Float64` | 480 (2.9%) |  |
| `aerial_duels_won` | `Float64` | 424 (2.6%) |  |
| `aerial_duels_won_percent` | `Float64` | 767 (4.7%) |  |
| `was_fouled` | `Float64` | 756 (4.6%) |  |
| `fouls_committed` | `Float64` | 342 (2.1%) |  |
| `saves` | `Float64` | 1,002 (6.1%) |  |
| `goals_conceded` | `Float64` | 1,002 (6.1%) |  |
| `xgot_faced` | `String` | 1,369 (8.3%) |  |
| `goals_prevented` | `String` | 1,369 (8.3%) |  |
| `sweeper_actions` | `Float64` | 1,330 (8.1%) |  |
| `gk_accurate_passes` | `Float64` | 1,330 (8.1%) |  |
| `gk_accurate_long_balls` | `Float64` | 1,332 (8.1%) |  |
| `dispossessed` | `String` | 711 (4.3%) |  |
| `high_claim` | `Float64` | 1,330 (8.1%) |  |
| `saves_inside_box` | `Float64` | 1,330 (8.1%) |  |
| `offsides` | `String` | 1,386 (8.4%) |  |
| `successful_dribbles_percent` | `String` | 1,093 (6.7%) |  |
| `tackles_won_percent` | `String` | 1,093 (6.7%) |  |
| `xgot` | `Float64` | 1,046 (6.4%) |  |
| `tackles` | `String` | 1,058 (6.4%) |  |
| `start_min` | `Int64` | 389 (2.4%) |  |
| `finish_min` | `Int64` | 389 (2.4%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.9%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 13,847 (84.3%) |  |
| `distance_covered` | `String` | 13,847 (84.3%) |  |
| `walking_distance` | `String` | 13,847 (84.3%) |  |
| `running_distance` | `String` | 13,847 (84.3%) |  |
| `sprinting_distance` | `String` | 13,847 (84.3%) |  |
| `number_of_sprints` | `String` | 13,847 (84.3%) |  |
| `defensive_contributions` | `String` | 1,588 (9.7%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,249 (7.6%) |  |
| `away_team` | `Int64` | 1,628 (9.9%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.6%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.6%) |  |
| `is_home` | `Boolean` | 1,249 (7.6%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,031 (18.5%) | Opponent club code. |
| `team_goals_for` | `Float64` | 207 (1.3%) |  |
| `team_goals_against` | `Float64` | 207 (1.3%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 207 (1.3%) |  |
| `started` | `Boolean` | 2,928 (17.8%) |  |
| `formation` | `String` | 2,928 (17.8%) |  |
| `lineup_status` | `String` | 2,928 (17.8%) |  |
| `lineup_team_code` | `Int64` | 2,928 (17.8%) |  |
| `rating` | `Float64` | 3,851 (23.4%) |  |
| `yellow_cards` | `Float64` | 3,612 (22.0%) |  |
| `red_cards` | `Float64` | 3,612 (22.0%) |  |
| `np_xg` | `Float64` | 10,133 (61.7%) | Non-penalty xG aggregated from shots.situation. |
| `set_piece_xg` | `Float64` | 10,133 (61.7%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 10,133 (61.7%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 10,133 (61.7%) |  |
| `own_goals` | `Float64` | 1,039 (6.3%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 16,428 (100.0%) |  |
| `fpl_points_right` | `Int64` | 1,039 (6.3%) |  |
| `bonus_right` | `Float64` | 1,039 (6.3%) |  |
| `bps_right` | `Float64` | 1,039 (6.3%) |  |
| `now_cost_right` | `Float64` | 1,039 (6.3%) |  |
| `selected_by_percent_right` | `Float64` | 1,039 (6.3%) |  |
| `form_right` | `Float64` | 1,039 (6.3%) |  |
| `penalties_order_right` | `String` | 14,860 (90.5%) |  |
| `direct_freekicks_order_right` | `String` | 14,799 (90.1%) |  |
| `corners_and_indirect_freekicks_order_right` | `String` | 14,290 (87.0%) |  |
| `status_right` | `String` | 1,039 (6.3%) |  |
| `gw_match_count_right` | `UInt32` | 0 (0.0%) |  |
| `fpl_points` | `Float64` | 1,039 (6.3%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (6.3%) |  |
| `bps` | `Float64` | 1,039 (6.3%) |  |
| `now_cost` | `Float64` | 1,039 (6.3%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (6.3%) |  |
| `form` | `Float64` | 1,039 (6.3%) |  |
| `penalties_order` | `String` | 14,860 (90.5%) |  |
| `direct_freekicks_order` | `String` | 14,799 (90.1%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 14,290 (87.0%) |  |
| `status` | `String` | 1,039 (6.3%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **30,578**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 19,651 (64.3%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (19.7%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 28,272 (92.5%) |  |
| `direct_freekicks_order` | `String` | 28,791 (94.2%) |  |
| `penalties_order` | `String` | 28,846 (94.3%) |  |
| `set_piece_threat` | `String` | 30,578 (100.0%) |  |
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

Rows: **1,820**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 244 (13.4%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 775 (42.6%) |  |
| `goals_against` | `Float64` | 775 (42.6%) |  |
| `elo` | `Float64` | 928 (51.0%) |  |
| `possession` | `Float64` | 855 (47.0%) |  |
| `xg` | `Float64` | 856 (47.0%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 890 (48.9%) | Non-penalty xG aggregated from shots.situation. |
| `xg_open_play` | `String` | 884 (48.6%) |  |
| `xg_set_play` | `String` | 884 (48.6%) |  |
| `xgot` | `Float64` | 884 (48.6%) |  |
| `total_shots` | `String` | 849 (46.6%) |  |
| `shots_on_target` | `String` | 849 (46.6%) |  |
| `shots_inside_box` | `String` | 850 (46.7%) |  |
| `shots_outside_box` | `String` | 850 (46.7%) |  |
| `big_chances` | `String` | 850 (46.7%) |  |
| `big_chances_missed` | `String` | 850 (46.7%) |  |
| `touches_in_opposition_box` | `String` | 850 (46.7%) |  |
| `corners` | `String` | 849 (46.6%) |  |
| `accurate_passes` | `String` | 850 (46.7%) |  |
| `accurate_passes_pct` | `String` | 850 (46.7%) |  |
| `accurate_long_balls` | `String` | 850 (46.7%) |  |
| `accurate_long_balls_pct` | `String` | 850 (46.7%) |  |
| `accurate_crosses` | `String` | 850 (46.7%) |  |
| `accurate_crosses_pct` | `String` | 850 (46.7%) |  |
| `tackles_won` | `String` | 859 (47.2%) |  |
| `tackles_won_pct` | `String` | 909 (49.9%) |  |
| `interceptions` | `String` | 850 (46.7%) |  |
| `blocks` | `String` | 854 (46.9%) |  |
| `clearances` | `String` | 850 (46.7%) |  |
| `duels_won` | `String` | 854 (46.9%) |  |
| `aerial_duels_won` | `String` | 850 (46.7%) |  |
| `aerial_duels_won_pct` | `String` | 850 (46.7%) |  |
| `ground_duels_won` | `String` | 850 (46.7%) |  |
| `ground_duels_won_pct` | `String` | 851 (46.8%) |  |
| `fouls_committed` | `String` | 850 (46.7%) |  |
| `offsides` | `String` | 850 (46.7%) |  |
| `yellow_cards` | `String` | 852 (46.8%) |  |
| `red_cards` | `String` | 853 (46.9%) |  |
| `keeper_saves` | `String` | 850 (46.7%) |  |
| `successful_dribbles` | `String` | 850 (46.7%) |  |
| `successful_dribbles_pct` | `String` | 850 (46.7%) |  |
| `possession_against` | `String` | 855 (47.0%) |  |
| `xga` | `Float64` | 856 (47.0%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 890 (48.9%) |  |
| `xg_open_play_against` | `String` | 884 (48.6%) |  |
| `xg_set_play_against` | `String` | 884 (48.6%) |  |
| `xgot_against` | `String` | 884 (48.6%) |  |
| `shots_conceded` | `String` | 849 (46.6%) |  |
| `sot_conceded` | `String` | 849 (46.6%) |  |
| `shots_inside_box_against` | `String` | 850 (46.7%) |  |
| `shots_outside_box_against` | `String` | 850 (46.7%) |  |
| `big_chances_conceded` | `String` | 850 (46.7%) |  |
| `big_chances_missed_against` | `String` | 850 (46.7%) |  |
| `touches_in_opposition_box_against` | `String` | 850 (46.7%) |  |
| `corners_against` | `String` | 849 (46.6%) |  |
| `accurate_passes_against` | `String` | 850 (46.7%) |  |
| `accurate_passes_pct_against` | `String` | 850 (46.7%) |  |
| `accurate_long_balls_against` | `String` | 850 (46.7%) |  |
| `accurate_long_balls_pct_against` | `String` | 850 (46.7%) |  |
| `accurate_crosses_against` | `String` | 850 (46.7%) |  |
| `accurate_crosses_pct_against` | `String` | 850 (46.7%) |  |
| `tackles_won_against` | `String` | 859 (47.2%) |  |
| `tackles_won_pct_against` | `String` | 909 (49.9%) |  |
| `interceptions_against` | `String` | 850 (46.7%) |  |
| `blocks_against` | `String` | 854 (46.9%) |  |
| `clearances_against` | `String` | 850 (46.7%) |  |
| `duels_won_against` | `String` | 854 (46.9%) |  |
| `aerial_duels_won_against` | `String` | 850 (46.7%) |  |
| `aerial_duels_won_pct_against` | `String` | 850 (46.7%) |  |
| `ground_duels_won_against` | `String` | 850 (46.7%) |  |
| `ground_duels_won_pct_against` | `String` | 851 (46.8%) |  |
| `fouls_committed_against` | `String` | 850 (46.7%) |  |
| `offsides_against` | `String` | 850 (46.7%) |  |
| `yellow_cards_against` | `String` | 852 (46.8%) |  |
| `red_cards_against` | `String` | 853 (46.9%) |  |
| `keeper_saves_against` | `String` | 850 (46.7%) |  |
| `successful_dribbles_against` | `String` | 850 (46.7%) |  |
| `successful_dribbles_pct_against` | `String` | 850 (46.7%) |  |
| `kickoff_raw` | `String` | 44 (2.4%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.4%) |  |
| `result` | `String` | 775 (42.6%) |  |
| `points` | `Int64` | 775 (42.6%) |  |
| `clean_sheet` | `Boolean` | 775 (42.6%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,724 (94.7%) |  |
| `weather_description` | `String` | 1,748 (96.0%) |  |
| `temperature_c` | `String` | 1,724 (94.7%) |  |
| `wind_speed` | `String` | 1,724 (94.7%) |  |
| `pitch_condition` | `String` | 1,724 (94.7%) |  |
| `is_local_derby` | `Boolean` | 946 (52.0%) |  |
| `is_neutral_ground` | `Boolean` | 946 (52.0%) |  |
| `lineup_status` | `String` | 946 (52.0%) |  |
| `strength` | `Float64` | 895 (49.2%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 895 (49.2%) |  |
| `strength_attack_away` | `Float64` | 895 (49.2%) |  |
| `strength_defence_home` | `Float64` | 895 (49.2%) |  |
| `strength_defence_away` | `Float64` | 895 (49.2%) |  |
| `home_shot_model_xg` | `Float64` | 1,060 (58.2%) |  |
| `away_shot_model_xg` | `Float64` | 1,060 (58.2%) |  |
| `incident_timing_coverage` | `String` | 1,060 (58.2%) |  |
| `unlocated_card_count` | `Int64` | 1,060 (58.2%) |  |
| `quarantined_incident_count` | `Int64` | 1,060 (58.2%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **381**. Columns: **12**.

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

