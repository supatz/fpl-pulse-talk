# FPL master datasets — data dictionary

Generated `2026-09-14T10:47:20Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **18,399**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 858 (4.7%) |  |
| `assists` | `Float64` | 938 (5.1%) |  |
| `total_shots` | `Float64` | 1,957 (10.6%) |  |
| `xg` | `Float64` | 2,198 (11.9%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,820 (9.9%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 1,957 (10.6%) |  |
| `successful_dribbles` | `String` | 3,029 (16.5%) |  |
| `big_chances_missed` | `String` | 3,357 (18.2%) |  |
| `touches_opposition_box` | `Float64` | 1,266 (6.9%) |  |
| `touches` | `Float64` | 783 (4.3%) |  |
| `accurate_passes` | `Float64` | 938 (5.1%) |  |
| `accurate_passes_percent` | `Float64` | 992 (5.4%) |  |
| `chances_created` | `Float64` | 934 (5.1%) |  |
| `final_third_passes` | `Float64` | 1,556 (8.5%) |  |
| `accurate_crosses` | `Float64` | 2,114 (11.5%) |  |
| `accurate_crosses_percent` | `Float64` | 2,149 (11.7%) |  |
| `accurate_long_balls` | `Float64` | 1,629 (8.9%) |  |
| `accurate_long_balls_percent` | `Float64` | 1,664 (9.0%) |  |
| `tackles_won` | `Float64` | 783 (4.3%) |  |
| `interceptions` | `Float64` | 783 (4.3%) |  |
| `recoveries` | `Float64` | 783 (4.3%) |  |
| `blocks` | `Float64` | 1,266 (6.9%) |  |
| `clearances` | `Float64` | 783 (4.3%) |  |
| `headed_clearances` | `Float64` | 2,575 (14.0%) |  |
| `dribbled_past` | `Float64` | 1,266 (6.9%) |  |
| `duels_won` | `Float64` | 1,208 (6.6%) |  |
| `duels_lost` | `Float64` | 1,241 (6.7%) |  |
| `ground_duels_won` | `Float64` | 1,104 (6.0%) |  |
| `ground_duels_won_percent` | `Float64` | 1,104 (6.0%) |  |
| `aerial_duels_won` | `Float64` | 931 (5.1%) |  |
| `aerial_duels_won_percent` | `Float64` | 1,702 (9.3%) |  |
| `was_fouled` | `Float64` | 2,043 (11.1%) |  |
| `fouls_committed` | `Float64` | 783 (4.3%) |  |
| `saves` | `Float64` | 2,874 (15.6%) |  |
| `goals_conceded` | `Float64` | 2,874 (15.6%) |  |
| `xgot_faced` | `String` | 3,247 (17.6%) |  |
| `goals_prevented` | `String` | 3,247 (17.6%) |  |
| `sweeper_actions` | `Float64` | 3,202 (17.4%) |  |
| `gk_accurate_passes` | `Float64` | 3,202 (17.4%) |  |
| `gk_accurate_long_balls` | `Float64` | 3,204 (17.4%) |  |
| `dispossessed` | `String` | 1,251 (6.8%) |  |
| `high_claim` | `Float64` | 3,202 (17.4%) |  |
| `saves_inside_box` | `Float64` | 3,202 (17.4%) |  |
| `offsides` | `String` | 3,357 (18.2%) |  |
| `successful_dribbles_percent` | `String` | 3,064 (16.7%) |  |
| `tackles_won_percent` | `String` | 3,064 (16.7%) |  |
| `xgot` | `Float64` | 2,658 (14.4%) |  |
| `tackles` | `String` | 3,029 (16.5%) |  |
| `start_min` | `Int64` | 830 (4.5%) |  |
| `finish_min` | `Int64` | 830 (4.5%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.7%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,536 (79.0%) |  |
| `distance_covered` | `String` | 14,536 (79.0%) |  |
| `walking_distance` | `String` | 15,739 (85.5%) |  |
| `running_distance` | `String` | 14,536 (79.0%) |  |
| `sprinting_distance` | `String` | 14,603 (79.4%) |  |
| `number_of_sprints` | `String` | 14,649 (79.6%) |  |
| `defensive_contributions` | `String` | 3,559 (19.3%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,410 (7.7%) |  |
| `away_team` | `Int64` | 1,808 (9.8%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.1%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.1%) |  |
| `is_home` | `Boolean` | 1,410 (7.7%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,387 (18.4%) | Opponent club code. |
| `team_goals_for` | `Float64` | 249 (1.4%) |  |
| `team_goals_against` | `Float64` | 249 (1.4%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 249 (1.4%) |  |
| `started` | `Boolean` | 4,899 (26.6%) |  |
| `formation` | `String` | 4,899 (26.6%) |  |
| `lineup_status` | `String` | 4,899 (26.6%) |  |
| `lineup_team_code` | `Int64` | 4,899 (26.6%) |  |
| `rating` | `Float64` | 5,822 (31.6%) |  |
| `yellow_cards` | `Float64` | 5,583 (30.3%) |  |
| `red_cards` | `Float64` | 5,583 (30.3%) |  |
| `np_xg` | `Float64` | 11,607 (63.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 11,607 (63.1%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 11,607 (63.1%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 11,607 (63.1%) |  |
| `own_goals` | `Float64` | 1,039 (5.6%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 18,399 (100.0%) |  |
| `fpl_points` | `Float64` | 1,039 (5.6%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (5.6%) |  |
| `bps` | `Float64` | 1,039 (5.6%) |  |
| `now_cost` | `Float64` | 1,039 (5.6%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (5.6%) |  |
| `form` | `Float64` | 1,039 (5.6%) |  |
| `penalties_order` | `String` | 16,594 (90.2%) |  |
| `direct_freekicks_order` | `String` | 16,518 (89.8%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 15,905 (86.4%) |  |
| `status` | `String` | 1,039 (5.6%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **32,560**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 21,081 (64.7%) |  |
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
| `corners_and_indirect_freekicks_order` | `String` | 30,011 (92.2%) |  |
| `direct_freekicks_order` | `String` | 30,597 (94.0%) |  |
| `penalties_order` | `String` | 30,642 (94.1%) |  |
| `set_piece_threat` | `String` | 32,560 (100.0%) |  |
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
| `goals_for` | `Float64` | 765 (40.1%) |  |
| `goals_against` | `Float64` | 765 (40.1%) |  |
| `elo` | `Float64` | 983 (51.5%) |  |
| `possession` | `Float64` | 845 (44.3%) |  |
| `xg` | `Float64` | 846 (44.3%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 880 (46.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 874 (45.8%) |  |
| `xg_set_play` | `String` | 874 (45.8%) |  |
| `xgot` | `Float64` | 874 (45.8%) |  |
| `total_shots` | `String` | 839 (43.9%) |  |
| `shots_on_target` | `String` | 839 (43.9%) |  |
| `shots_inside_box` | `String` | 840 (44.0%) |  |
| `shots_outside_box` | `String` | 840 (44.0%) |  |
| `big_chances` | `String` | 840 (44.0%) |  |
| `big_chances_missed` | `String` | 840 (44.0%) |  |
| `touches_in_opposition_box` | `String` | 840 (44.0%) |  |
| `corners` | `String` | 839 (43.9%) |  |
| `accurate_passes` | `String` | 840 (44.0%) |  |
| `accurate_passes_pct` | `String` | 840 (44.0%) |  |
| `accurate_long_balls` | `String` | 840 (44.0%) |  |
| `accurate_long_balls_pct` | `String` | 840 (44.0%) |  |
| `accurate_crosses` | `String` | 840 (44.0%) |  |
| `accurate_crosses_pct` | `String` | 840 (44.0%) |  |
| `tackles_won` | `String` | 849 (44.5%) |  |
| `tackles_won_pct` | `String` | 998 (52.3%) |  |
| `interceptions` | `String` | 840 (44.0%) |  |
| `blocks` | `String` | 844 (44.2%) |  |
| `clearances` | `String` | 840 (44.0%) |  |
| `duels_won` | `String` | 844 (44.2%) |  |
| `aerial_duels_won` | `String` | 840 (44.0%) |  |
| `aerial_duels_won_pct` | `String` | 840 (44.0%) |  |
| `ground_duels_won` | `String` | 840 (44.0%) |  |
| `ground_duels_won_pct` | `String` | 841 (44.1%) |  |
| `fouls_committed` | `String` | 840 (44.0%) |  |
| `offsides` | `String` | 840 (44.0%) |  |
| `yellow_cards` | `String` | 842 (44.1%) |  |
| `red_cards` | `String` | 843 (44.2%) |  |
| `keeper_saves` | `String` | 840 (44.0%) |  |
| `successful_dribbles` | `String` | 840 (44.0%) |  |
| `successful_dribbles_pct` | `String` | 840 (44.0%) |  |
| `possession_against` | `String` | 845 (44.3%) |  |
| `xga` | `Float64` | 846 (44.3%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 880 (46.1%) |  |
| `xg_open_play_against` | `String` | 874 (45.8%) |  |
| `xg_set_play_against` | `String` | 874 (45.8%) |  |
| `xgot_against` | `String` | 874 (45.8%) |  |
| `shots_conceded` | `String` | 839 (43.9%) |  |
| `sot_conceded` | `String` | 839 (43.9%) |  |
| `shots_inside_box_against` | `String` | 840 (44.0%) |  |
| `shots_outside_box_against` | `String` | 840 (44.0%) |  |
| `big_chances_conceded` | `String` | 840 (44.0%) |  |
| `big_chances_missed_against` | `String` | 840 (44.0%) |  |
| `touches_in_opposition_box_against` | `String` | 840 (44.0%) |  |
| `corners_against` | `String` | 839 (43.9%) |  |
| `accurate_passes_against` | `String` | 840 (44.0%) |  |
| `accurate_passes_pct_against` | `String` | 840 (44.0%) |  |
| `accurate_long_balls_against` | `String` | 840 (44.0%) |  |
| `accurate_long_balls_pct_against` | `String` | 840 (44.0%) |  |
| `accurate_crosses_against` | `String` | 840 (44.0%) |  |
| `accurate_crosses_pct_against` | `String` | 840 (44.0%) |  |
| `tackles_won_against` | `String` | 849 (44.5%) |  |
| `tackles_won_pct_against` | `String` | 998 (52.3%) |  |
| `interceptions_against` | `String` | 840 (44.0%) |  |
| `blocks_against` | `String` | 844 (44.2%) |  |
| `clearances_against` | `String` | 840 (44.0%) |  |
| `duels_won_against` | `String` | 844 (44.2%) |  |
| `aerial_duels_won_against` | `String` | 840 (44.0%) |  |
| `aerial_duels_won_pct_against` | `String` | 840 (44.0%) |  |
| `ground_duels_won_against` | `String` | 840 (44.0%) |  |
| `ground_duels_won_pct_against` | `String` | 841 (44.1%) |  |
| `fouls_committed_against` | `String` | 840 (44.0%) |  |
| `offsides_against` | `String` | 840 (44.0%) |  |
| `yellow_cards_against` | `String` | 842 (44.1%) |  |
| `red_cards_against` | `String` | 843 (44.2%) |  |
| `keeper_saves_against` | `String` | 840 (44.0%) |  |
| `successful_dribbles_against` | `String` | 840 (44.0%) |  |
| `successful_dribbles_pct_against` | `String` | 840 (44.0%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 765 (40.1%) |  |
| `points` | `Int64` | 765 (40.1%) |  |
| `clean_sheet` | `Boolean` | 765 (40.1%) |  |
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

Rows: **346**. Columns: **12**.

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

