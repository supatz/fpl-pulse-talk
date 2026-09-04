# FPL master datasets — data dictionary

Generated `2026-09-04T18:22:21Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **17,403**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.4%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 579 (3.3%) |  |
| `assists` | `Float64` | 659 (3.8%) |  |
| `total_shots` | `Float64` | 1,341 (7.7%) |  |
| `xg` | `Float64` | 1,582 (9.1%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,366 (7.8%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 1,341 (7.7%) |  |
| `successful_dribbles` | `String` | 2,033 (11.7%) |  |
| `big_chances_missed` | `String` | 2,361 (13.6%) |  |
| `touches_opposition_box` | `Float64` | 987 (5.7%) |  |
| `touches` | `Float64` | 554 (3.2%) |  |
| `accurate_passes` | `Float64` | 659 (3.8%) |  |
| `accurate_passes_percent` | `Float64` | 707 (4.1%) |  |
| `chances_created` | `Float64` | 657 (3.8%) |  |
| `final_third_passes` | `Float64` | 1,182 (6.8%) |  |
| `accurate_crosses` | `Float64` | 1,441 (8.3%) |  |
| `accurate_crosses_percent` | `Float64` | 1,476 (8.5%) |  |
| `accurate_long_balls` | `Float64` | 1,109 (6.4%) |  |
| `accurate_long_balls_percent` | `Float64` | 1,144 (6.6%) |  |
| `tackles_won` | `Float64` | 554 (3.2%) |  |
| `interceptions` | `Float64` | 554 (3.2%) |  |
| `recoveries` | `Float64` | 554 (3.2%) |  |
| `blocks` | `Float64` | 987 (5.7%) |  |
| `clearances` | `Float64` | 554 (3.2%) |  |
| `headed_clearances` | `Float64` | 1,879 (10.8%) |  |
| `dribbled_past` | `Float64` | 987 (5.7%) |  |
| `duels_won` | `Float64` | 868 (5.0%) |  |
| `duels_lost` | `Float64` | 884 (5.1%) |  |
| `ground_duels_won` | `Float64` | 782 (4.5%) |  |
| `ground_duels_won_percent` | `Float64` | 782 (4.5%) |  |
| `aerial_duels_won` | `Float64` | 671 (3.9%) |  |
| `aerial_duels_won_percent` | `Float64` | 1,236 (7.1%) |  |
| `was_fouled` | `Float64` | 1,400 (8.0%) |  |
| `fouls_committed` | `Float64` | 554 (3.2%) |  |
| `saves` | `Float64` | 1,928 (11.1%) |  |
| `goals_conceded` | `Float64` | 1,928 (11.1%) |  |
| `xgot_faced` | `String` | 2,298 (13.2%) |  |
| `goals_prevented` | `String` | 2,298 (13.2%) |  |
| `sweeper_actions` | `Float64` | 2,256 (13.0%) |  |
| `gk_accurate_passes` | `Float64` | 2,256 (13.0%) |  |
| `gk_accurate_long_balls` | `Float64` | 2,258 (13.0%) |  |
| `dispossessed` | `String` | 972 (5.6%) |  |
| `high_claim` | `Float64` | 2,256 (13.0%) |  |
| `saves_inside_box` | `Float64` | 2,256 (13.0%) |  |
| `offsides` | `String` | 2,361 (13.6%) |  |
| `successful_dribbles_percent` | `String` | 2,068 (11.9%) |  |
| `tackles_won_percent` | `String` | 2,068 (11.9%) |  |
| `xgot` | `Float64` | 1,838 (10.6%) |  |
| `tackles` | `String` | 2,033 (11.7%) |  |
| `start_min` | `Int64` | 601 (3.5%) |  |
| `finish_min` | `Int64` | 601 (3.5%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.8%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,200 (81.6%) |  |
| `distance_covered` | `String` | 14,200 (81.6%) |  |
| `walking_distance` | `String` | 14,822 (85.2%) |  |
| `running_distance` | `String` | 14,200 (81.6%) |  |
| `sprinting_distance` | `String` | 14,235 (81.8%) |  |
| `number_of_sprints` | `String` | 14,257 (81.9%) |  |
| `defensive_contributions` | `String` | 2,563 (14.7%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,327 (7.6%) |  |
| `away_team` | `Int64` | 1,725 (9.9%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.3%) |  |
| `is_home` | `Boolean` | 1,327 (7.6%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,221 (18.5%) | Opponent club code. |
| `team_goals_for` | `Float64` | 249 (1.4%) |  |
| `team_goals_against` | `Float64` | 249 (1.4%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 249 (1.4%) |  |
| `started` | `Boolean` | 3,903 (22.4%) |  |
| `formation` | `String` | 3,903 (22.4%) |  |
| `lineup_status` | `String` | 3,903 (22.4%) |  |
| `lineup_team_code` | `Int64` | 3,903 (22.4%) |  |
| `rating` | `Float64` | 4,826 (27.7%) |  |
| `yellow_cards` | `Float64` | 4,587 (26.4%) |  |
| `red_cards` | `Float64` | 4,587 (26.4%) |  |
| `np_xg` | `Float64` | 10,857 (62.4%) | Non-penalty xG from shots (situation != penalty). Serving may fill gaps with xG − 0.79 × penalties_scored. |
| `set_piece_xg` | `Float64` | 10,857 (62.4%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 10,857 (62.4%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 10,857 (62.4%) |  |
| `own_goals` | `Float64` | 1,039 (6.0%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 17,403 (100.0%) |  |
| `fpl_points` | `Float64` | 1,039 (6.0%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (6.0%) |  |
| `bps` | `Float64` | 1,039 (6.0%) |  |
| `now_cost` | `Float64` | 1,039 (6.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (6.0%) |  |
| `form` | `Float64` | 1,039 (6.0%) |  |
| `penalties_order` | `String` | 15,717 (90.3%) |  |
| `direct_freekicks_order` | `String` | 15,653 (89.9%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 15,090 (86.7%) |  |
| `status` | `String` | 1,039 (6.0%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **31,246**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 20,147 (64.5%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (19.3%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 28,859 (92.4%) |  |
| `direct_freekicks_order` | `String` | 29,401 (94.1%) |  |
| `penalties_order` | `String` | 29,450 (94.3%) |  |
| `set_piece_threat` | `String` | 31,246 (100.0%) |  |
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
| `goals_for` | `Float64` | 815 (42.7%) |  |
| `goals_against` | `Float64` | 815 (42.7%) |  |
| `elo` | `Float64` | 983 (51.5%) |  |
| `possession` | `Float64` | 895 (46.9%) |  |
| `xg` | `Float64` | 896 (46.9%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 930 (48.7%) | Non-penalty xG from shots (situation != penalty). Serving may fill gaps with xG − 0.79 × penalties_scored. |
| `xg_open_play` | `String` | 924 (48.4%) |  |
| `xg_set_play` | `String` | 924 (48.4%) |  |
| `xgot` | `Float64` | 924 (48.4%) |  |
| `total_shots` | `String` | 889 (46.6%) |  |
| `shots_on_target` | `String` | 889 (46.6%) |  |
| `shots_inside_box` | `String` | 890 (46.6%) |  |
| `shots_outside_box` | `String` | 890 (46.6%) |  |
| `big_chances` | `String` | 890 (46.6%) |  |
| `big_chances_missed` | `String` | 890 (46.6%) |  |
| `touches_in_opposition_box` | `String` | 890 (46.6%) |  |
| `corners` | `String` | 889 (46.6%) |  |
| `accurate_passes` | `String` | 890 (46.6%) |  |
| `accurate_passes_pct` | `String` | 890 (46.6%) |  |
| `accurate_long_balls` | `String` | 890 (46.6%) |  |
| `accurate_long_balls_pct` | `String` | 890 (46.6%) |  |
| `accurate_crosses` | `String` | 890 (46.6%) |  |
| `accurate_crosses_pct` | `String` | 890 (46.6%) |  |
| `tackles_won` | `String` | 899 (47.1%) |  |
| `tackles_won_pct` | `String` | 998 (52.3%) |  |
| `interceptions` | `String` | 890 (46.6%) |  |
| `blocks` | `String` | 894 (46.8%) |  |
| `clearances` | `String` | 890 (46.6%) |  |
| `duels_won` | `String` | 894 (46.8%) |  |
| `aerial_duels_won` | `String` | 890 (46.6%) |  |
| `aerial_duels_won_pct` | `String` | 890 (46.6%) |  |
| `ground_duels_won` | `String` | 890 (46.6%) |  |
| `ground_duels_won_pct` | `String` | 891 (46.7%) |  |
| `fouls_committed` | `String` | 890 (46.6%) |  |
| `offsides` | `String` | 890 (46.6%) |  |
| `yellow_cards` | `String` | 892 (46.7%) |  |
| `red_cards` | `String` | 893 (46.8%) |  |
| `keeper_saves` | `String` | 890 (46.6%) |  |
| `successful_dribbles` | `String` | 890 (46.6%) |  |
| `successful_dribbles_pct` | `String` | 890 (46.6%) |  |
| `possession_against` | `String` | 895 (46.9%) |  |
| `xga` | `Float64` | 896 (46.9%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 930 (48.7%) |  |
| `xg_open_play_against` | `String` | 924 (48.4%) |  |
| `xg_set_play_against` | `String` | 924 (48.4%) |  |
| `xgot_against` | `String` | 924 (48.4%) |  |
| `shots_conceded` | `String` | 889 (46.6%) |  |
| `sot_conceded` | `String` | 889 (46.6%) |  |
| `shots_inside_box_against` | `String` | 890 (46.6%) |  |
| `shots_outside_box_against` | `String` | 890 (46.6%) |  |
| `big_chances_conceded` | `String` | 890 (46.6%) |  |
| `big_chances_missed_against` | `String` | 890 (46.6%) |  |
| `touches_in_opposition_box_against` | `String` | 890 (46.6%) |  |
| `corners_against` | `String` | 889 (46.6%) |  |
| `accurate_passes_against` | `String` | 890 (46.6%) |  |
| `accurate_passes_pct_against` | `String` | 890 (46.6%) |  |
| `accurate_long_balls_against` | `String` | 890 (46.6%) |  |
| `accurate_long_balls_pct_against` | `String` | 890 (46.6%) |  |
| `accurate_crosses_against` | `String` | 890 (46.6%) |  |
| `accurate_crosses_pct_against` | `String` | 890 (46.6%) |  |
| `tackles_won_against` | `String` | 899 (47.1%) |  |
| `tackles_won_pct_against` | `String` | 998 (52.3%) |  |
| `interceptions_against` | `String` | 890 (46.6%) |  |
| `blocks_against` | `String` | 894 (46.8%) |  |
| `clearances_against` | `String` | 890 (46.6%) |  |
| `duels_won_against` | `String` | 894 (46.8%) |  |
| `aerial_duels_won_against` | `String` | 890 (46.6%) |  |
| `aerial_duels_won_pct_against` | `String` | 890 (46.6%) |  |
| `ground_duels_won_against` | `String` | 890 (46.6%) |  |
| `ground_duels_won_pct_against` | `String` | 891 (46.7%) |  |
| `fouls_committed_against` | `String` | 890 (46.6%) |  |
| `offsides_against` | `String` | 890 (46.6%) |  |
| `yellow_cards_against` | `String` | 892 (46.7%) |  |
| `red_cards_against` | `String` | 893 (46.8%) |  |
| `keeper_saves_against` | `String` | 890 (46.6%) |  |
| `successful_dribbles_against` | `String` | 890 (46.6%) |  |
| `successful_dribbles_pct_against` | `String` | 890 (46.6%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 815 (42.7%) |  |
| `points` | `Int64` | 815 (42.7%) |  |
| `clean_sheet` | `Boolean` | 815 (42.7%) |  |
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

Rows: **367**. Columns: **12**.

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

