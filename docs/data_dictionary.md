# FPL master datasets — data dictionary

Generated `2026-10-30T13:29:26Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **20,894**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,545 (7.4%) |  |
| `assists` | `Float64` | 1,624 (7.8%) |  |
| `total_shots` | `Float64` | 3,480 (16.7%) |  |
| `xg` | `Float64` | 3,721 (17.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 2,931 (14.0%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 3,480 (16.7%) |  |
| `successful_dribbles` | `String` | 5,524 (26.4%) |  |
| `big_chances_missed` | `String` | 5,852 (28.0%) |  |
| `touches_opposition_box` | `Float64` | 1,953 (9.3%) |  |
| `touches` | `Float64` | 1,342 (6.4%) |  |
| `accurate_passes` | `Float64` | 1,625 (7.8%) |  |
| `accurate_passes_percent` | `Float64` | 1,694 (8.1%) |  |
| `chances_created` | `Float64` | 1,613 (7.7%) |  |
| `final_third_passes` | `Float64` | 2,494 (11.9%) |  |
| `accurate_crosses` | `Float64` | 3,755 (18.0%) |  |
| `accurate_crosses_percent` | `Float64` | 3,790 (18.1%) |  |
| `accurate_long_balls` | `Float64` | 2,898 (13.9%) |  |
| `accurate_long_balls_percent` | `Float64` | 2,933 (14.0%) |  |
| `tackles_won` | `Float64` | 1,342 (6.4%) |  |
| `interceptions` | `Float64` | 1,342 (6.4%) |  |
| `recoveries` | `Float64` | 1,342 (6.4%) |  |
| `blocks` | `Float64` | 1,953 (9.3%) |  |
| `clearances` | `Float64` | 1,342 (6.4%) |  |
| `headed_clearances` | `Float64` | 4,349 (20.8%) |  |
| `dribbled_past` | `Float64` | 1,953 (9.3%) |  |
| `duels_won` | `Float64` | 2,090 (10.0%) |  |
| `duels_lost` | `Float64` | 2,119 (10.1%) |  |
| `ground_duels_won` | `Float64` | 1,910 (9.1%) |  |
| `ground_duels_won_percent` | `Float64` | 1,910 (9.1%) |  |
| `aerial_duels_won` | `Float64` | 1,593 (7.6%) |  |
| `aerial_duels_won_percent` | `Float64` | 2,935 (14.0%) |  |
| `was_fouled` | `Float64` | 3,689 (17.7%) |  |
| `fouls_committed` | `Float64` | 1,342 (6.4%) |  |
| `saves` | `Float64` | 5,241 (25.1%) |  |
| `goals_conceded` | `Float64` | 5,241 (25.1%) |  |
| `xgot_faced` | `String` | 5,619 (26.9%) |  |
| `goals_prevented` | `String` | 5,619 (26.9%) |  |
| `sweeper_actions` | `Float64` | 5,569 (26.7%) |  |
| `gk_accurate_passes` | `Float64` | 5,569 (26.7%) |  |
| `gk_accurate_long_balls` | `Float64` | 5,572 (26.7%) |  |
| `dispossessed` | `String` | 1,938 (9.3%) |  |
| `high_claim` | `Float64` | 5,569 (26.7%) |  |
| `saves_inside_box` | `Float64` | 5,569 (26.7%) |  |
| `offsides` | `String` | 5,852 (28.0%) |  |
| `successful_dribbles_percent` | `String` | 5,559 (26.6%) |  |
| `tackles_won_percent` | `String` | 5,559 (26.6%) |  |
| `xgot` | `Float64` | 4,706 (22.5%) |  |
| `tackles` | `String` | 5,524 (26.4%) |  |
| `start_min` | `Int64` | 1,389 (6.6%) |  |
| `finish_min` | `Int64` | 1,389 (6.6%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.5%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 15,700 (75.1%) |  |
| `distance_covered` | `String` | 15,700 (75.1%) |  |
| `walking_distance` | `String` | 18,155 (86.9%) |  |
| `running_distance` | `String` | 15,700 (75.1%) |  |
| `sprinting_distance` | `String` | 15,817 (75.7%) |  |
| `number_of_sprints` | `String` | 15,917 (76.2%) |  |
| `defensive_contributions` | `String` | 6,054 (29.0%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,664 (8.0%) |  |
| `away_team` | `Int64` | 2,076 (9.9%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.6%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.6%) |  |
| `is_home` | `Boolean` | 1,664 (8.0%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,909 (18.7%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.2%) |  |
| `team_goals_against` | `Float64` | 253 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.2%) |  |
| `started` | `Boolean` | 7,394 (35.4%) |  |
| `formation` | `String` | 7,394 (35.4%) |  |
| `lineup_status` | `String` | 7,394 (35.4%) |  |
| `lineup_team_code` | `Int64` | 7,394 (35.4%) |  |
| `rating` | `Float64` | 8,317 (39.8%) |  |
| `yellow_cards` | `Float64` | 8,078 (38.7%) |  |
| `red_cards` | `Float64` | 8,078 (38.7%) |  |
| `np_xg` | `Float64` | 13,566 (64.9%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 13,566 (64.9%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 13,566 (64.9%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 13,566 (64.9%) |  |
| `own_goals` | `Float64` | 1,243 (5.9%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 20,894 (100.0%) |  |
| `fpl_points` | `Float64` | 1,243 (5.9%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,243 (5.9%) |  |
| `bps` | `Float64` | 1,243 (5.9%) |  |
| `now_cost` | `Float64` | 1,243 (5.9%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,243 (5.9%) |  |
| `form` | `Float64` | 1,243 (5.9%) |  |
| `penalties_order` | `String` | 18,797 (90.0%) |  |
| `direct_freekicks_order` | `String` | 18,694 (89.5%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 17,964 (86.0%) |  |
| `status` | `String` | 1,243 (5.9%) |  |
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

Rows: **1,927**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 323 (16.8%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 655 (34.0%) |  |
| `goals_against` | `Float64` | 655 (34.0%) |  |
| `elo` | `Float64` | 1,001 (51.9%) |  |
| `possession` | `Float64` | 737 (38.2%) |  |
| `xg` | `Float64` | 738 (38.3%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 772 (40.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 766 (39.8%) |  |
| `xg_set_play` | `String` | 766 (39.8%) |  |
| `xgot` | `Float64` | 766 (39.8%) |  |
| `total_shots` | `String` | 731 (37.9%) |  |
| `shots_on_target` | `String` | 731 (37.9%) |  |
| `shots_inside_box` | `String` | 732 (38.0%) |  |
| `shots_outside_box` | `String` | 732 (38.0%) |  |
| `big_chances` | `String` | 732 (38.0%) |  |
| `big_chances_missed` | `String` | 732 (38.0%) |  |
| `touches_in_opposition_box` | `String` | 732 (38.0%) |  |
| `corners` | `String` | 731 (37.9%) |  |
| `accurate_passes` | `String` | 732 (38.0%) |  |
| `accurate_passes_pct` | `String` | 732 (38.0%) |  |
| `accurate_long_balls` | `String` | 732 (38.0%) |  |
| `accurate_long_balls_pct` | `String` | 732 (38.0%) |  |
| `accurate_crosses` | `String` | 732 (38.0%) |  |
| `accurate_crosses_pct` | `String` | 732 (38.0%) |  |
| `tackles_won` | `String` | 741 (38.5%) |  |
| `tackles_won_pct` | `String` | 1,016 (52.7%) |  |
| `interceptions` | `String` | 732 (38.0%) |  |
| `blocks` | `String` | 736 (38.2%) |  |
| `clearances` | `String` | 732 (38.0%) |  |
| `duels_won` | `String` | 736 (38.2%) |  |
| `aerial_duels_won` | `String` | 732 (38.0%) |  |
| `aerial_duels_won_pct` | `String` | 732 (38.0%) |  |
| `ground_duels_won` | `String` | 732 (38.0%) |  |
| `ground_duels_won_pct` | `String` | 733 (38.0%) |  |
| `fouls_committed` | `String` | 732 (38.0%) |  |
| `offsides` | `String` | 732 (38.0%) |  |
| `yellow_cards` | `String` | 734 (38.1%) |  |
| `red_cards` | `String` | 735 (38.1%) |  |
| `keeper_saves` | `String` | 732 (38.0%) |  |
| `successful_dribbles` | `String` | 732 (38.0%) |  |
| `successful_dribbles_pct` | `String` | 732 (38.0%) |  |
| `possession_against` | `String` | 737 (38.2%) |  |
| `xga` | `Float64` | 738 (38.3%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 772 (40.1%) |  |
| `xg_open_play_against` | `String` | 766 (39.8%) |  |
| `xg_set_play_against` | `String` | 766 (39.8%) |  |
| `xgot_against` | `String` | 766 (39.8%) |  |
| `shots_conceded` | `String` | 731 (37.9%) |  |
| `sot_conceded` | `String` | 731 (37.9%) |  |
| `shots_inside_box_against` | `String` | 732 (38.0%) |  |
| `shots_outside_box_against` | `String` | 732 (38.0%) |  |
| `big_chances_conceded` | `String` | 732 (38.0%) |  |
| `big_chances_missed_against` | `String` | 732 (38.0%) |  |
| `touches_in_opposition_box_against` | `String` | 732 (38.0%) |  |
| `corners_against` | `String` | 731 (37.9%) |  |
| `accurate_passes_against` | `String` | 732 (38.0%) |  |
| `accurate_passes_pct_against` | `String` | 732 (38.0%) |  |
| `accurate_long_balls_against` | `String` | 732 (38.0%) |  |
| `accurate_long_balls_pct_against` | `String` | 732 (38.0%) |  |
| `accurate_crosses_against` | `String` | 732 (38.0%) |  |
| `accurate_crosses_pct_against` | `String` | 732 (38.0%) |  |
| `tackles_won_against` | `String` | 741 (38.5%) |  |
| `tackles_won_pct_against` | `String` | 1,016 (52.7%) |  |
| `interceptions_against` | `String` | 732 (38.0%) |  |
| `blocks_against` | `String` | 736 (38.2%) |  |
| `clearances_against` | `String` | 732 (38.0%) |  |
| `duels_won_against` | `String` | 736 (38.2%) |  |
| `aerial_duels_won_against` | `String` | 732 (38.0%) |  |
| `aerial_duels_won_pct_against` | `String` | 732 (38.0%) |  |
| `ground_duels_won_against` | `String` | 732 (38.0%) |  |
| `ground_duels_won_pct_against` | `String` | 733 (38.0%) |  |
| `fouls_committed_against` | `String` | 732 (38.0%) |  |
| `offsides_against` | `String` | 732 (38.0%) |  |
| `yellow_cards_against` | `String` | 734 (38.1%) |  |
| `red_cards_against` | `String` | 735 (38.1%) |  |
| `keeper_saves_against` | `String` | 732 (38.0%) |  |
| `successful_dribbles_against` | `String` | 732 (38.0%) |  |
| `successful_dribbles_pct_against` | `String` | 732 (38.0%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 655 (34.0%) |  |
| `points` | `Int64` | 657 (34.1%) |  |
| `clean_sheet` | `Boolean` | 657 (34.1%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,831 (95.0%) |  |
| `weather_description` | `String` | 1,855 (96.3%) |  |
| `temperature_c` | `String` | 1,831 (95.0%) |  |
| `wind_speed` | `String` | 1,831 (95.0%) |  |
| `pitch_condition` | `String` | 1,831 (95.0%) |  |
| `is_local_derby` | `Boolean` | 1,053 (54.6%) |  |
| `is_neutral_ground` | `Boolean` | 1,053 (54.6%) |  |
| `lineup_status` | `String` | 1,053 (54.6%) |  |
| `strength` | `Float64` | 1,002 (52.0%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 1,002 (52.0%) |  |
| `strength_attack_away` | `Float64` | 1,002 (52.0%) |  |
| `strength_defence_home` | `Float64` | 1,002 (52.0%) |  |
| `strength_defence_away` | `Float64` | 1,002 (52.0%) |  |
| `home_shot_model_xg` | `Float64` | 1,167 (60.6%) |  |
| `away_shot_model_xg` | `Float64` | 1,167 (60.6%) |  |
| `incident_timing_coverage` | `String` | 1,167 (60.6%) |  |
| `unlocated_card_count` | `Int64` | 1,167 (60.6%) |  |
| `quarantined_incident_count` | `Int64` | 1,167 (60.6%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **304**. Columns: **12**.

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

