# FPL master datasets — data dictionary

Generated `2026-10-12T08:27:06Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **19,494**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,158 (5.9%) |  |
| `assists` | `Float64` | 1,237 (6.3%) |  |
| `total_shots` | `Float64` | 2,621 (13.4%) |  |
| `xg` | `Float64` | 2,862 (14.7%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 2,313 (11.9%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 2,621 (13.4%) |  |
| `successful_dribbles` | `String` | 4,124 (21.2%) |  |
| `big_chances_missed` | `String` | 4,452 (22.8%) |  |
| `touches_opposition_box` | `Float64` | 1,566 (8.0%) |  |
| `touches` | `Float64` | 1,027 (5.3%) |  |
| `accurate_passes` | `Float64` | 1,238 (6.4%) |  |
| `accurate_passes_percent` | `Float64` | 1,299 (6.7%) |  |
| `chances_created` | `Float64` | 1,230 (6.3%) |  |
| `final_third_passes` | `Float64` | 1,976 (10.1%) |  |
| `accurate_crosses` | `Float64` | 2,833 (14.5%) |  |
| `accurate_crosses_percent` | `Float64` | 2,868 (14.7%) |  |
| `accurate_long_balls` | `Float64` | 2,187 (11.2%) |  |
| `accurate_long_balls_percent` | `Float64` | 2,222 (11.4%) |  |
| `tackles_won` | `Float64` | 1,027 (5.3%) |  |
| `interceptions` | `Float64` | 1,027 (5.3%) |  |
| `recoveries` | `Float64` | 1,027 (5.3%) |  |
| `blocks` | `Float64` | 1,566 (8.0%) |  |
| `clearances` | `Float64` | 1,027 (5.3%) |  |
| `headed_clearances` | `Float64` | 3,334 (17.1%) |  |
| `dribbled_past` | `Float64` | 1,566 (8.0%) |  |
| `duels_won` | `Float64` | 1,586 (8.1%) |  |
| `duels_lost` | `Float64` | 1,616 (8.3%) |  |
| `ground_duels_won` | `Float64` | 1,455 (7.5%) |  |
| `ground_duels_won_percent` | `Float64` | 1,455 (7.5%) |  |
| `aerial_duels_won` | `Float64` | 1,217 (6.2%) |  |
| `aerial_duels_won_percent` | `Float64` | 2,231 (11.4%) |  |
| `was_fouled` | `Float64` | 2,777 (14.2%) |  |
| `fouls_committed` | `Float64` | 1,027 (5.3%) |  |
| `saves` | `Float64` | 3,913 (20.1%) |  |
| `goals_conceded` | `Float64` | 3,913 (20.1%) |  |
| `xgot_faced` | `String` | 4,287 (22.0%) |  |
| `goals_prevented` | `String` | 4,287 (22.0%) |  |
| `sweeper_actions` | `Float64` | 4,241 (21.8%) |  |
| `gk_accurate_passes` | `Float64` | 4,241 (21.8%) |  |
| `gk_accurate_long_balls` | `Float64` | 4,243 (21.8%) |  |
| `dispossessed` | `String` | 1,551 (8.0%) |  |
| `high_claim` | `Float64` | 4,241 (21.8%) |  |
| `saves_inside_box` | `Float64` | 4,241 (21.8%) |  |
| `offsides` | `String` | 4,452 (22.8%) |  |
| `successful_dribbles_percent` | `String` | 4,159 (21.3%) |  |
| `tackles_won_percent` | `String` | 4,159 (21.3%) |  |
| `xgot` | `Float64` | 3,541 (18.2%) |  |
| `tackles` | `String` | 4,124 (21.2%) |  |
| `start_min` | `Int64` | 1,074 (5.5%) |  |
| `finish_min` | `Int64` | 1,074 (5.5%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.6%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 15,015 (77.0%) |  |
| `distance_covered` | `String` | 15,015 (77.0%) |  |
| `walking_distance` | `String` | 16,834 (86.4%) |  |
| `running_distance` | `String` | 15,015 (77.0%) |  |
| `sprinting_distance` | `String` | 15,099 (77.5%) |  |
| `number_of_sprints` | `String` | 15,168 (77.8%) |  |
| `defensive_contributions` | `String` | 4,654 (23.9%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,474 (7.6%) |  |
| `away_team` | `Int64` | 1,887 (9.7%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.8%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.8%) |  |
| `is_home` | `Boolean` | 1,474 (7.6%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,530 (18.1%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.3%) |  |
| `team_goals_against` | `Float64` | 253 (1.3%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.3%) |  |
| `started` | `Boolean` | 5,994 (30.7%) |  |
| `formation` | `String` | 5,994 (30.7%) |  |
| `lineup_status` | `String` | 5,994 (30.7%) |  |
| `lineup_team_code` | `Int64` | 5,994 (30.7%) |  |
| `rating` | `Float64` | 6,917 (35.5%) |  |
| `yellow_cards` | `Float64` | 6,678 (34.3%) |  |
| `red_cards` | `Float64` | 6,678 (34.3%) |  |
| `np_xg` | `Float64` | 12,430 (63.8%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 12,430 (63.8%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 12,430 (63.8%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 12,430 (63.8%) |  |
| `own_goals` | `Float64` | 1,040 (5.3%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 19,494 (100.0%) |  |
| `fpl_points` | `Float64` | 1,040 (5.3%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,040 (5.3%) |  |
| `bps` | `Float64` | 1,040 (5.3%) |  |
| `now_cost` | `Float64` | 1,040 (5.3%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,040 (5.3%) |  |
| `form` | `Float64` | 1,040 (5.3%) |  |
| `penalties_order` | `String` | 17,567 (90.1%) |  |
| `direct_freekicks_order` | `String` | 17,489 (89.7%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 16,812 (86.2%) |  |
| `status` | `String` | 1,040 (5.3%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **33,895**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 21,999 (64.9%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (17.7%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 31,193 (92.0%) |  |
| `direct_freekicks_order` | `String` | 31,829 (93.9%) |  |
| `penalties_order` | `String` | 31,870 (94.0%) |  |
| `set_piece_threat` | `String` | 33,895 (100.0%) |  |
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
| `goals_for` | `Float64` | 723 (37.6%) |  |
| `goals_against` | `Float64` | 723 (37.6%) |  |
| `elo` | `Float64` | 996 (51.8%) |  |
| `possession` | `Float64` | 803 (41.8%) |  |
| `xg` | `Float64` | 804 (41.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 838 (43.6%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 832 (43.3%) |  |
| `xg_set_play` | `String` | 832 (43.3%) |  |
| `xgot` | `Float64` | 832 (43.3%) |  |
| `total_shots` | `String` | 797 (41.5%) |  |
| `shots_on_target` | `String` | 797 (41.5%) |  |
| `shots_inside_box` | `String` | 798 (41.5%) |  |
| `shots_outside_box` | `String` | 798 (41.5%) |  |
| `big_chances` | `String` | 798 (41.5%) |  |
| `big_chances_missed` | `String` | 798 (41.5%) |  |
| `touches_in_opposition_box` | `String` | 798 (41.5%) |  |
| `corners` | `String` | 797 (41.5%) |  |
| `accurate_passes` | `String` | 798 (41.5%) |  |
| `accurate_passes_pct` | `String` | 798 (41.5%) |  |
| `accurate_long_balls` | `String` | 798 (41.5%) |  |
| `accurate_long_balls_pct` | `String` | 798 (41.5%) |  |
| `accurate_crosses` | `String` | 798 (41.5%) |  |
| `accurate_crosses_pct` | `String` | 798 (41.5%) |  |
| `tackles_won` | `String` | 807 (42.0%) |  |
| `tackles_won_pct` | `String` | 1,011 (52.6%) |  |
| `interceptions` | `String` | 798 (41.5%) |  |
| `blocks` | `String` | 802 (41.7%) |  |
| `clearances` | `String` | 798 (41.5%) |  |
| `duels_won` | `String` | 802 (41.7%) |  |
| `aerial_duels_won` | `String` | 798 (41.5%) |  |
| `aerial_duels_won_pct` | `String` | 798 (41.5%) |  |
| `ground_duels_won` | `String` | 798 (41.5%) |  |
| `ground_duels_won_pct` | `String` | 799 (41.6%) |  |
| `fouls_committed` | `String` | 798 (41.5%) |  |
| `offsides` | `String` | 798 (41.5%) |  |
| `yellow_cards` | `String` | 800 (41.6%) |  |
| `red_cards` | `String` | 801 (41.7%) |  |
| `keeper_saves` | `String` | 798 (41.5%) |  |
| `successful_dribbles` | `String` | 798 (41.5%) |  |
| `successful_dribbles_pct` | `String` | 798 (41.5%) |  |
| `possession_against` | `String` | 803 (41.8%) |  |
| `xga` | `Float64` | 804 (41.8%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 838 (43.6%) |  |
| `xg_open_play_against` | `String` | 832 (43.3%) |  |
| `xg_set_play_against` | `String` | 832 (43.3%) |  |
| `xgot_against` | `String` | 832 (43.3%) |  |
| `shots_conceded` | `String` | 797 (41.5%) |  |
| `sot_conceded` | `String` | 797 (41.5%) |  |
| `shots_inside_box_against` | `String` | 798 (41.5%) |  |
| `shots_outside_box_against` | `String` | 798 (41.5%) |  |
| `big_chances_conceded` | `String` | 798 (41.5%) |  |
| `big_chances_missed_against` | `String` | 798 (41.5%) |  |
| `touches_in_opposition_box_against` | `String` | 798 (41.5%) |  |
| `corners_against` | `String` | 797 (41.5%) |  |
| `accurate_passes_against` | `String` | 798 (41.5%) |  |
| `accurate_passes_pct_against` | `String` | 798 (41.5%) |  |
| `accurate_long_balls_against` | `String` | 798 (41.5%) |  |
| `accurate_long_balls_pct_against` | `String` | 798 (41.5%) |  |
| `accurate_crosses_against` | `String` | 798 (41.5%) |  |
| `accurate_crosses_pct_against` | `String` | 798 (41.5%) |  |
| `tackles_won_against` | `String` | 807 (42.0%) |  |
| `tackles_won_pct_against` | `String` | 1,011 (52.6%) |  |
| `interceptions_against` | `String` | 798 (41.5%) |  |
| `blocks_against` | `String` | 802 (41.7%) |  |
| `clearances_against` | `String` | 798 (41.5%) |  |
| `duels_won_against` | `String` | 802 (41.7%) |  |
| `aerial_duels_won_against` | `String` | 798 (41.5%) |  |
| `aerial_duels_won_pct_against` | `String` | 798 (41.5%) |  |
| `ground_duels_won_against` | `String` | 798 (41.5%) |  |
| `ground_duels_won_pct_against` | `String` | 799 (41.6%) |  |
| `fouls_committed_against` | `String` | 798 (41.5%) |  |
| `offsides_against` | `String` | 798 (41.5%) |  |
| `yellow_cards_against` | `String` | 800 (41.6%) |  |
| `red_cards_against` | `String` | 801 (41.7%) |  |
| `keeper_saves_against` | `String` | 798 (41.5%) |  |
| `successful_dribbles_against` | `String` | 798 (41.5%) |  |
| `successful_dribbles_pct_against` | `String` | 798 (41.5%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 723 (37.6%) |  |
| `points` | `Int64` | 723 (37.6%) |  |
| `clean_sheet` | `Boolean` | 723 (37.6%) |  |
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

Rows: **328**. Columns: **12**.

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

