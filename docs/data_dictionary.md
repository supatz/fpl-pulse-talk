# FPL master datasets — data dictionary

Generated `2026-09-07T08:13:19Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **17,761**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 680 (3.8%) |  |
| `assists` | `Float64` | 760 (4.3%) |  |
| `total_shots` | `Float64` | 1,569 (8.8%) |  |
| `xg` | `Float64` | 1,810 (10.2%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,544 (8.7%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 1,569 (8.8%) |  |
| `successful_dribbles` | `String` | 2,391 (13.5%) |  |
| `big_chances_missed` | `String` | 2,719 (15.3%) |  |
| `touches_opposition_box` | `Float64` | 1,088 (6.1%) |  |
| `touches` | `Float64` | 637 (3.6%) |  |
| `accurate_passes` | `Float64` | 760 (4.3%) |  |
| `accurate_passes_percent` | `Float64` | 812 (4.6%) |  |
| `chances_created` | `Float64` | 757 (4.3%) |  |
| `final_third_passes` | `Float64` | 1,324 (7.5%) |  |
| `accurate_crosses` | `Float64` | 1,688 (9.5%) |  |
| `accurate_crosses_percent` | `Float64` | 1,723 (9.7%) |  |
| `accurate_long_balls` | `Float64` | 1,294 (7.3%) |  |
| `accurate_long_balls_percent` | `Float64` | 1,329 (7.5%) |  |
| `tackles_won` | `Float64` | 637 (3.6%) |  |
| `interceptions` | `Float64` | 637 (3.6%) |  |
| `recoveries` | `Float64` | 637 (3.6%) |  |
| `blocks` | `Float64` | 1,088 (6.1%) |  |
| `clearances` | `Float64` | 637 (3.6%) |  |
| `headed_clearances` | `Float64` | 2,126 (12.0%) |  |
| `dribbled_past` | `Float64` | 1,088 (6.1%) |  |
| `duels_won` | `Float64` | 989 (5.6%) |  |
| `duels_lost` | `Float64` | 1,013 (5.7%) |  |
| `ground_duels_won` | `Float64` | 897 (5.1%) |  |
| `ground_duels_won_percent` | `Float64` | 897 (5.1%) |  |
| `aerial_duels_won` | `Float64` | 766 (4.3%) |  |
| `aerial_duels_won_percent` | `Float64` | 1,403 (7.9%) |  |
| `was_fouled` | `Float64` | 1,626 (9.2%) |  |
| `fouls_committed` | `Float64` | 637 (3.6%) |  |
| `saves` | `Float64` | 2,268 (12.8%) |  |
| `goals_conceded` | `Float64` | 2,268 (12.8%) |  |
| `xgot_faced` | `String` | 2,639 (14.9%) |  |
| `goals_prevented` | `String` | 2,639 (14.9%) |  |
| `sweeper_actions` | `Float64` | 2,596 (14.6%) |  |
| `gk_accurate_passes` | `Float64` | 2,596 (14.6%) |  |
| `gk_accurate_long_balls` | `Float64` | 2,598 (14.6%) |  |
| `dispossessed` | `String` | 1,073 (6.0%) |  |
| `high_claim` | `Float64` | 2,596 (14.6%) |  |
| `saves_inside_box` | `Float64` | 2,596 (14.6%) |  |
| `offsides` | `String` | 2,719 (15.3%) |  |
| `successful_dribbles_percent` | `String` | 2,426 (13.7%) |  |
| `tackles_won_percent` | `String` | 2,426 (13.7%) |  |
| `xgot` | `Float64` | 2,145 (12.1%) |  |
| `tackles` | `String` | 2,391 (13.5%) |  |
| `start_min` | `Int64` | 684 (3.9%) |  |
| `finish_min` | `Int64` | 684 (3.9%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.8%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,283 (80.4%) |  |
| `distance_covered` | `String` | 14,283 (80.4%) |  |
| `walking_distance` | `String` | 15,180 (85.5%) |  |
| `running_distance` | `String` | 14,283 (80.4%) |  |
| `sprinting_distance` | `String` | 14,331 (80.7%) |  |
| `number_of_sprints` | `String` | 14,366 (80.9%) |  |
| `defensive_contributions` | `String` | 2,921 (16.4%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,327 (7.5%) |  |
| `away_team` | `Int64` | 1,725 (9.7%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.2%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.2%) |  |
| `is_home` | `Boolean` | 1,327 (7.5%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,221 (18.1%) | Opponent club code. |
| `team_goals_for` | `Float64` | 249 (1.4%) |  |
| `team_goals_against` | `Float64` | 249 (1.4%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 249 (1.4%) |  |
| `started` | `Boolean` | 4,261 (24.0%) |  |
| `formation` | `String` | 4,261 (24.0%) |  |
| `lineup_status` | `String` | 4,261 (24.0%) |  |
| `lineup_team_code` | `Int64` | 4,261 (24.0%) |  |
| `rating` | `Float64` | 5,184 (29.2%) |  |
| `yellow_cards` | `Float64` | 4,945 (27.8%) |  |
| `red_cards` | `Float64` | 4,945 (27.8%) |  |
| `np_xg` | `Float64` | 11,100 (62.5%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 11,100 (62.5%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 11,100 (62.5%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 11,100 (62.5%) |  |
| `own_goals` | `Float64` | 1,039 (5.8%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 17,761 (100.0%) |  |
| `fpl_points` | `Float64` | 1,039 (5.8%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (5.8%) |  |
| `bps` | `Float64` | 1,039 (5.8%) |  |
| `now_cost` | `Float64` | 1,039 (5.8%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (5.8%) |  |
| `form` | `Float64` | 1,039 (5.8%) |  |
| `penalties_order` | `String` | 16,033 (90.3%) |  |
| `direct_freekicks_order` | `String` | 15,964 (89.9%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 15,377 (86.6%) |  |
| `status` | `String` | 1,039 (5.8%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **31,900**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 20,622 (64.6%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (18.9%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 29,428 (92.3%) |  |
| `direct_freekicks_order` | `String` | 29,998 (94.0%) |  |
| `penalties_order` | `String` | 30,044 (94.2%) |  |
| `set_piece_threat` | `String` | 31,900 (100.0%) |  |
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

Rows: **1,909**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 321 (16.8%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 795 (41.6%) |  |
| `goals_against` | `Float64` | 795 (41.6%) |  |
| `elo` | `Float64` | 983 (51.5%) |  |
| `possession` | `Float64` | 877 (45.9%) |  |
| `xg` | `Float64` | 878 (46.0%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 912 (47.8%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 906 (47.5%) |  |
| `xg_set_play` | `String` | 906 (47.5%) |  |
| `xgot` | `Float64` | 906 (47.5%) |  |
| `total_shots` | `String` | 871 (45.6%) |  |
| `shots_on_target` | `String` | 871 (45.6%) |  |
| `shots_inside_box` | `String` | 872 (45.7%) |  |
| `shots_outside_box` | `String` | 872 (45.7%) |  |
| `big_chances` | `String` | 872 (45.7%) |  |
| `big_chances_missed` | `String` | 872 (45.7%) |  |
| `touches_in_opposition_box` | `String` | 872 (45.7%) |  |
| `corners` | `String` | 871 (45.6%) |  |
| `accurate_passes` | `String` | 872 (45.7%) |  |
| `accurate_passes_pct` | `String` | 872 (45.7%) |  |
| `accurate_long_balls` | `String` | 872 (45.7%) |  |
| `accurate_long_balls_pct` | `String` | 872 (45.7%) |  |
| `accurate_crosses` | `String` | 872 (45.7%) |  |
| `accurate_crosses_pct` | `String` | 872 (45.7%) |  |
| `tackles_won` | `String` | 881 (46.1%) |  |
| `tackles_won_pct` | `String` | 998 (52.3%) |  |
| `interceptions` | `String` | 872 (45.7%) |  |
| `blocks` | `String` | 876 (45.9%) |  |
| `clearances` | `String` | 872 (45.7%) |  |
| `duels_won` | `String` | 876 (45.9%) |  |
| `aerial_duels_won` | `String` | 872 (45.7%) |  |
| `aerial_duels_won_pct` | `String` | 872 (45.7%) |  |
| `ground_duels_won` | `String` | 872 (45.7%) |  |
| `ground_duels_won_pct` | `String` | 873 (45.7%) |  |
| `fouls_committed` | `String` | 872 (45.7%) |  |
| `offsides` | `String` | 872 (45.7%) |  |
| `yellow_cards` | `String` | 874 (45.8%) |  |
| `red_cards` | `String` | 875 (45.8%) |  |
| `keeper_saves` | `String` | 872 (45.7%) |  |
| `successful_dribbles` | `String` | 872 (45.7%) |  |
| `successful_dribbles_pct` | `String` | 872 (45.7%) |  |
| `possession_against` | `String` | 877 (45.9%) |  |
| `xga` | `Float64` | 878 (46.0%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 912 (47.8%) |  |
| `xg_open_play_against` | `String` | 906 (47.5%) |  |
| `xg_set_play_against` | `String` | 906 (47.5%) |  |
| `xgot_against` | `String` | 906 (47.5%) |  |
| `shots_conceded` | `String` | 871 (45.6%) |  |
| `sot_conceded` | `String` | 871 (45.6%) |  |
| `shots_inside_box_against` | `String` | 872 (45.7%) |  |
| `shots_outside_box_against` | `String` | 872 (45.7%) |  |
| `big_chances_conceded` | `String` | 872 (45.7%) |  |
| `big_chances_missed_against` | `String` | 872 (45.7%) |  |
| `touches_in_opposition_box_against` | `String` | 872 (45.7%) |  |
| `corners_against` | `String` | 871 (45.6%) |  |
| `accurate_passes_against` | `String` | 872 (45.7%) |  |
| `accurate_passes_pct_against` | `String` | 872 (45.7%) |  |
| `accurate_long_balls_against` | `String` | 872 (45.7%) |  |
| `accurate_long_balls_pct_against` | `String` | 872 (45.7%) |  |
| `accurate_crosses_against` | `String` | 872 (45.7%) |  |
| `accurate_crosses_pct_against` | `String` | 872 (45.7%) |  |
| `tackles_won_against` | `String` | 881 (46.1%) |  |
| `tackles_won_pct_against` | `String` | 998 (52.3%) |  |
| `interceptions_against` | `String` | 872 (45.7%) |  |
| `blocks_against` | `String` | 876 (45.9%) |  |
| `clearances_against` | `String` | 872 (45.7%) |  |
| `duels_won_against` | `String` | 876 (45.9%) |  |
| `aerial_duels_won_against` | `String` | 872 (45.7%) |  |
| `aerial_duels_won_pct_against` | `String` | 872 (45.7%) |  |
| `ground_duels_won_against` | `String` | 872 (45.7%) |  |
| `ground_duels_won_pct_against` | `String` | 873 (45.7%) |  |
| `fouls_committed_against` | `String` | 872 (45.7%) |  |
| `offsides_against` | `String` | 872 (45.7%) |  |
| `yellow_cards_against` | `String` | 874 (45.8%) |  |
| `red_cards_against` | `String` | 875 (45.8%) |  |
| `keeper_saves_against` | `String` | 872 (45.7%) |  |
| `successful_dribbles_against` | `String` | 872 (45.7%) |  |
| `successful_dribbles_pct_against` | `String` | 872 (45.7%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 795 (41.6%) |  |
| `points` | `Int64` | 795 (41.6%) |  |
| `clean_sheet` | `Boolean` | 795 (41.6%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,813 (95.0%) |  |
| `weather_description` | `String` | 1,837 (96.2%) |  |
| `temperature_c` | `String` | 1,813 (95.0%) |  |
| `wind_speed` | `String` | 1,813 (95.0%) |  |
| `pitch_condition` | `String` | 1,813 (95.0%) |  |
| `is_local_derby` | `Boolean` | 1,035 (54.2%) |  |
| `is_neutral_ground` | `Boolean` | 1,035 (54.2%) |  |
| `lineup_status` | `String` | 1,035 (54.2%) |  |
| `strength` | `Float64` | 984 (51.5%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 984 (51.5%) |  |
| `strength_attack_away` | `Float64` | 984 (51.5%) |  |
| `strength_defence_home` | `Float64` | 984 (51.5%) |  |
| `strength_defence_away` | `Float64` | 984 (51.5%) |  |
| `home_shot_model_xg` | `Float64` | 1,149 (60.2%) |  |
| `away_shot_model_xg` | `Float64` | 1,149 (60.2%) |  |
| `incident_timing_coverage` | `String` | 1,149 (60.2%) |  |
| `unlocated_card_count` | `Int64` | 1,149 (60.2%) |  |
| `quarantined_incident_count` | `Int64` | 1,149 (60.2%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **357**. Columns: **12**.

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

