# FPL master datasets — data dictionary

Generated `2026-09-16T07:49:40Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **18,439**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 867 (4.7%) |  |
| `assists` | `Float64` | 947 (5.1%) |  |
| `total_shots` | `Float64` | 1,984 (10.8%) |  |
| `xg` | `Float64` | 2,225 (12.1%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,841 (10.0%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 1,984 (10.8%) |  |
| `successful_dribbles` | `String` | 3,069 (16.6%) |  |
| `big_chances_missed` | `String` | 3,397 (18.4%) |  |
| `touches_opposition_box` | `Float64` | 1,275 (6.9%) |  |
| `touches` | `Float64` | 790 (4.3%) |  |
| `accurate_passes` | `Float64` | 947 (5.1%) |  |
| `accurate_passes_percent` | `Float64` | 1,002 (5.4%) |  |
| `chances_created` | `Float64` | 943 (5.1%) |  |
| `final_third_passes` | `Float64` | 1,570 (8.5%) |  |
| `accurate_crosses` | `Float64` | 2,139 (11.6%) |  |
| `accurate_crosses_percent` | `Float64` | 2,174 (11.8%) |  |
| `accurate_long_balls` | `Float64` | 1,650 (8.9%) |  |
| `accurate_long_balls_percent` | `Float64` | 1,685 (9.1%) |  |
| `tackles_won` | `Float64` | 790 (4.3%) |  |
| `interceptions` | `Float64` | 790 (4.3%) |  |
| `recoveries` | `Float64` | 790 (4.3%) |  |
| `blocks` | `Float64` | 1,275 (6.9%) |  |
| `clearances` | `Float64` | 790 (4.3%) |  |
| `headed_clearances` | `Float64` | 2,602 (14.1%) |  |
| `dribbled_past` | `Float64` | 1,275 (6.9%) |  |
| `duels_won` | `Float64` | 1,217 (6.6%) |  |
| `duels_lost` | `Float64` | 1,252 (6.8%) |  |
| `ground_duels_won` | `Float64` | 1,113 (6.0%) |  |
| `ground_duels_won_percent` | `Float64` | 1,113 (6.0%) |  |
| `aerial_duels_won` | `Float64` | 939 (5.1%) |  |
| `aerial_duels_won_percent` | `Float64` | 1,720 (9.3%) |  |
| `was_fouled` | `Float64` | 2,066 (11.2%) |  |
| `fouls_committed` | `Float64` | 790 (4.3%) |  |
| `saves` | `Float64` | 2,912 (15.8%) |  |
| `goals_conceded` | `Float64` | 2,912 (15.8%) |  |
| `xgot_faced` | `String` | 3,285 (17.8%) |  |
| `goals_prevented` | `String` | 3,285 (17.8%) |  |
| `sweeper_actions` | `Float64` | 3,240 (17.6%) |  |
| `gk_accurate_passes` | `Float64` | 3,240 (17.6%) |  |
| `gk_accurate_long_balls` | `Float64` | 3,242 (17.6%) |  |
| `dispossessed` | `String` | 1,260 (6.8%) |  |
| `high_claim` | `Float64` | 3,240 (17.6%) |  |
| `saves_inside_box` | `Float64` | 3,240 (17.6%) |  |
| `offsides` | `String` | 3,397 (18.4%) |  |
| `successful_dribbles_percent` | `String` | 3,104 (16.8%) |  |
| `tackles_won_percent` | `String` | 3,104 (16.8%) |  |
| `xgot` | `Float64` | 2,691 (14.6%) |  |
| `tackles` | `String` | 3,069 (16.6%) |  |
| `start_min` | `Int64` | 837 (4.5%) |  |
| `finish_min` | `Int64` | 837 (4.5%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.7%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,543 (78.9%) |  |
| `distance_covered` | `String` | 14,543 (78.9%) |  |
| `walking_distance` | `String` | 15,779 (85.6%) |  |
| `running_distance` | `String` | 14,543 (78.9%) |  |
| `sprinting_distance` | `String` | 14,611 (79.2%) |  |
| `number_of_sprints` | `String` | 14,658 (79.5%) |  |
| `defensive_contributions` | `String` | 3,599 (19.5%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,410 (7.6%) |  |
| `away_team` | `Int64` | 1,808 (9.8%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.1%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.1%) |  |
| `is_home` | `Boolean` | 1,410 (7.6%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,387 (18.4%) | Opponent club code. |
| `team_goals_for` | `Float64` | 249 (1.4%) |  |
| `team_goals_against` | `Float64` | 249 (1.4%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 249 (1.4%) |  |
| `started` | `Boolean` | 4,939 (26.8%) |  |
| `formation` | `String` | 4,939 (26.8%) |  |
| `lineup_status` | `String` | 4,939 (26.8%) |  |
| `lineup_team_code` | `Int64` | 4,939 (26.8%) |  |
| `rating` | `Float64` | 5,862 (31.8%) |  |
| `yellow_cards` | `Float64` | 5,623 (30.5%) |  |
| `red_cards` | `Float64` | 5,623 (30.5%) |  |
| `np_xg` | `Float64` | 11,634 (63.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 11,634 (63.1%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 11,634 (63.1%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 11,634 (63.1%) |  |
| `own_goals` | `Float64` | 1,039 (5.6%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 18,439 (100.0%) |  |
| `fpl_points` | `Float64` | 1,039 (5.6%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (5.6%) |  |
| `bps` | `Float64` | 1,039 (5.6%) |  |
| `now_cost` | `Float64` | 1,039 (5.6%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (5.6%) |  |
| `form` | `Float64` | 1,039 (5.6%) |  |
| `penalties_order` | `String` | 16,631 (90.2%) |  |
| `direct_freekicks_order` | `String` | 16,551 (89.8%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 15,937 (86.4%) |  |
| `status` | `String` | 1,039 (5.6%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **32,561**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 21,076 (64.7%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (18.5%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 30,012 (92.2%) |  |
| `direct_freekicks_order` | `String` | 30,598 (94.0%) |  |
| `penalties_order` | `String` | 30,643 (94.1%) |  |
| `set_piece_threat` | `String` | 32,561 (100.0%) |  |
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
| `goals_for` | `Float64` | 757 (39.7%) |  |
| `goals_against` | `Float64` | 757 (39.7%) |  |
| `elo` | `Float64` | 983 (51.5%) |  |
| `possession` | `Float64` | 843 (44.2%) |  |
| `xg` | `Float64` | 844 (44.2%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 878 (46.0%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 872 (45.7%) |  |
| `xg_set_play` | `String` | 872 (45.7%) |  |
| `xgot` | `Float64` | 872 (45.7%) |  |
| `total_shots` | `String` | 837 (43.8%) |  |
| `shots_on_target` | `String` | 837 (43.8%) |  |
| `shots_inside_box` | `String` | 838 (43.9%) |  |
| `shots_outside_box` | `String` | 838 (43.9%) |  |
| `big_chances` | `String` | 838 (43.9%) |  |
| `big_chances_missed` | `String` | 838 (43.9%) |  |
| `touches_in_opposition_box` | `String` | 838 (43.9%) |  |
| `corners` | `String` | 837 (43.8%) |  |
| `accurate_passes` | `String` | 838 (43.9%) |  |
| `accurate_passes_pct` | `String` | 838 (43.9%) |  |
| `accurate_long_balls` | `String` | 838 (43.9%) |  |
| `accurate_long_balls_pct` | `String` | 838 (43.9%) |  |
| `accurate_crosses` | `String` | 838 (43.9%) |  |
| `accurate_crosses_pct` | `String` | 838 (43.9%) |  |
| `tackles_won` | `String` | 847 (44.4%) |  |
| `tackles_won_pct` | `String` | 998 (52.3%) |  |
| `interceptions` | `String` | 838 (43.9%) |  |
| `blocks` | `String` | 842 (44.1%) |  |
| `clearances` | `String` | 838 (43.9%) |  |
| `duels_won` | `String` | 842 (44.1%) |  |
| `aerial_duels_won` | `String` | 838 (43.9%) |  |
| `aerial_duels_won_pct` | `String` | 838 (43.9%) |  |
| `ground_duels_won` | `String` | 838 (43.9%) |  |
| `ground_duels_won_pct` | `String` | 839 (43.9%) |  |
| `fouls_committed` | `String` | 838 (43.9%) |  |
| `offsides` | `String` | 838 (43.9%) |  |
| `yellow_cards` | `String` | 840 (44.0%) |  |
| `red_cards` | `String` | 841 (44.1%) |  |
| `keeper_saves` | `String` | 838 (43.9%) |  |
| `successful_dribbles` | `String` | 838 (43.9%) |  |
| `successful_dribbles_pct` | `String` | 838 (43.9%) |  |
| `possession_against` | `String` | 843 (44.2%) |  |
| `xga` | `Float64` | 844 (44.2%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 878 (46.0%) |  |
| `xg_open_play_against` | `String` | 872 (45.7%) |  |
| `xg_set_play_against` | `String` | 872 (45.7%) |  |
| `xgot_against` | `String` | 872 (45.7%) |  |
| `shots_conceded` | `String` | 837 (43.8%) |  |
| `sot_conceded` | `String` | 837 (43.8%) |  |
| `shots_inside_box_against` | `String` | 838 (43.9%) |  |
| `shots_outside_box_against` | `String` | 838 (43.9%) |  |
| `big_chances_conceded` | `String` | 838 (43.9%) |  |
| `big_chances_missed_against` | `String` | 838 (43.9%) |  |
| `touches_in_opposition_box_against` | `String` | 838 (43.9%) |  |
| `corners_against` | `String` | 837 (43.8%) |  |
| `accurate_passes_against` | `String` | 838 (43.9%) |  |
| `accurate_passes_pct_against` | `String` | 838 (43.9%) |  |
| `accurate_long_balls_against` | `String` | 838 (43.9%) |  |
| `accurate_long_balls_pct_against` | `String` | 838 (43.9%) |  |
| `accurate_crosses_against` | `String` | 838 (43.9%) |  |
| `accurate_crosses_pct_against` | `String` | 838 (43.9%) |  |
| `tackles_won_against` | `String` | 847 (44.4%) |  |
| `tackles_won_pct_against` | `String` | 998 (52.3%) |  |
| `interceptions_against` | `String` | 838 (43.9%) |  |
| `blocks_against` | `String` | 842 (44.1%) |  |
| `clearances_against` | `String` | 838 (43.9%) |  |
| `duels_won_against` | `String` | 842 (44.1%) |  |
| `aerial_duels_won_against` | `String` | 838 (43.9%) |  |
| `aerial_duels_won_pct_against` | `String` | 838 (43.9%) |  |
| `ground_duels_won_against` | `String` | 838 (43.9%) |  |
| `ground_duels_won_pct_against` | `String` | 839 (43.9%) |  |
| `fouls_committed_against` | `String` | 838 (43.9%) |  |
| `offsides_against` | `String` | 838 (43.9%) |  |
| `yellow_cards_against` | `String` | 840 (44.0%) |  |
| `red_cards_against` | `String` | 841 (44.1%) |  |
| `keeper_saves_against` | `String` | 838 (43.9%) |  |
| `successful_dribbles_against` | `String` | 838 (43.9%) |  |
| `successful_dribbles_pct_against` | `String` | 838 (43.9%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 757 (39.7%) |  |
| `points` | `Int64` | 763 (40.0%) |  |
| `clean_sheet` | `Boolean` | 763 (40.0%) |  |
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

Rows: **345**. Columns: **12**.

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

