# FPL master datasets — data dictionary

Generated `2026-11-02T08:42:40Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **21,294**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,654 (7.8%) |  |
| `assists` | `Float64` | 1,733 (8.1%) |  |
| `total_shots` | `Float64` | 3,721 (17.5%) |  |
| `xg` | `Float64` | 3,962 (18.6%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 3,126 (14.7%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 3,721 (17.5%) |  |
| `successful_dribbles` | `String` | 5,924 (27.8%) |  |
| `big_chances_missed` | `String` | 6,252 (29.4%) |  |
| `touches_opposition_box` | `Float64` | 2,062 (9.7%) |  |
| `touches` | `Float64` | 1,431 (6.7%) |  |
| `accurate_passes` | `Float64` | 1,734 (8.1%) |  |
| `accurate_passes_percent` | `Float64` | 1,805 (8.5%) |  |
| `chances_created` | `Float64` | 1,721 (8.1%) |  |
| `final_third_passes` | `Float64` | 2,645 (12.4%) |  |
| `accurate_crosses` | `Float64` | 4,027 (18.9%) |  |
| `accurate_crosses_percent` | `Float64` | 4,062 (19.1%) |  |
| `accurate_long_balls` | `Float64` | 3,105 (14.6%) |  |
| `accurate_long_balls_percent` | `Float64` | 3,140 (14.7%) |  |
| `tackles_won` | `Float64` | 1,431 (6.7%) |  |
| `interceptions` | `Float64` | 1,431 (6.7%) |  |
| `recoveries` | `Float64` | 1,431 (6.7%) |  |
| `blocks` | `Float64` | 2,062 (9.7%) |  |
| `clearances` | `Float64` | 1,431 (6.7%) |  |
| `headed_clearances` | `Float64` | 4,615 (21.7%) |  |
| `dribbled_past` | `Float64` | 2,062 (9.7%) |  |
| `duels_won` | `Float64` | 2,224 (10.4%) |  |
| `duels_lost` | `Float64` | 2,257 (10.6%) |  |
| `ground_duels_won` | `Float64` | 2,033 (9.5%) |  |
| `ground_duels_won_percent` | `Float64` | 2,033 (9.5%) |  |
| `aerial_duels_won` | `Float64` | 1,698 (8.0%) |  |
| `aerial_duels_won_percent` | `Float64` | 3,120 (14.7%) |  |
| `was_fouled` | `Float64` | 3,948 (18.5%) |  |
| `fouls_committed` | `Float64` | 1,431 (6.7%) |  |
| `saves` | `Float64` | 5,621 (26.4%) |  |
| `goals_conceded` | `Float64` | 5,621 (26.4%) |  |
| `xgot_faced` | `String` | 6,000 (28.2%) |  |
| `goals_prevented` | `String` | 6,000 (28.2%) |  |
| `sweeper_actions` | `Float64` | 5,949 (27.9%) |  |
| `gk_accurate_passes` | `Float64` | 5,949 (27.9%) |  |
| `gk_accurate_long_balls` | `Float64` | 5,953 (28.0%) |  |
| `dispossessed` | `String` | 2,047 (9.6%) |  |
| `high_claim` | `Float64` | 5,949 (27.9%) |  |
| `saves_inside_box` | `Float64` | 5,949 (27.9%) |  |
| `offsides` | `String` | 6,252 (29.4%) |  |
| `successful_dribbles_percent` | `String` | 5,959 (28.0%) |  |
| `tackles_won_percent` | `String` | 5,959 (28.0%) |  |
| `xgot` | `Float64` | 5,044 (23.7%) |  |
| `tackles` | `String` | 5,924 (27.8%) |  |
| `start_min` | `Int64` | 1,478 (6.9%) |  |
| `finish_min` | `Int64` | 1,478 (6.9%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.5%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 15,821 (74.3%) |  |
| `distance_covered` | `String` | 15,821 (74.3%) |  |
| `walking_distance` | `String` | 18,555 (87.1%) |  |
| `running_distance` | `String` | 15,821 (74.3%) |  |
| `sprinting_distance` | `String` | 15,950 (74.9%) |  |
| `number_of_sprints` | `String` | 16,062 (75.4%) |  |
| `defensive_contributions` | `String` | 6,454 (30.3%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,664 (7.8%) |  |
| `away_team` | `Int64` | 2,076 (9.7%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.5%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.5%) |  |
| `is_home` | `Boolean` | 1,664 (7.8%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,909 (18.4%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.2%) |  |
| `team_goals_against` | `Float64` | 253 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.2%) |  |
| `started` | `Boolean` | 7,794 (36.6%) |  |
| `formation` | `String` | 7,794 (36.6%) |  |
| `lineup_status` | `String` | 7,794 (36.6%) |  |
| `lineup_team_code` | `Int64` | 7,794 (36.6%) |  |
| `rating` | `Float64` | 8,717 (40.9%) |  |
| `yellow_cards` | `Float64` | 8,478 (39.8%) |  |
| `red_cards` | `Float64` | 8,478 (39.8%) |  |
| `np_xg` | `Float64` | 13,838 (65.0%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 13,838 (65.0%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 13,838 (65.0%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 13,838 (65.0%) |  |
| `own_goals` | `Float64` | 1,040 (4.9%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 21,294 (100.0%) |  |
| `fpl_points` | `Float64` | 1,040 (4.9%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,040 (4.9%) |  |
| `bps` | `Float64` | 1,040 (4.9%) |  |
| `now_cost` | `Float64` | 1,040 (4.9%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,040 (4.9%) |  |
| `form` | `Float64` | 1,040 (4.9%) |  |
| `penalties_order` | `String` | 19,122 (89.8%) |  |
| `direct_freekicks_order` | `String` | 19,008 (89.3%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 18,246 (85.7%) |  |
| `status` | `String` | 1,040 (4.9%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **35,902**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 23,411 (65.2%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (16.8%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 32,902 (91.6%) |  |
| `direct_freekicks_order` | `String` | 33,609 (93.6%) |  |
| `penalties_order` | `String` | 33,674 (93.8%) |  |
| `set_piece_threat` | `String` | 35,902 (100.0%) |  |
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
| `goals_for` | `Float64` | 638 (33.1%) |  |
| `goals_against` | `Float64` | 638 (33.1%) |  |
| `elo` | `Float64` | 1,002 (52.0%) |  |
| `possession` | `Float64` | 718 (37.2%) |  |
| `xg` | `Float64` | 719 (37.3%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 753 (39.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 747 (38.7%) |  |
| `xg_set_play` | `String` | 747 (38.7%) |  |
| `xgot` | `Float64` | 747 (38.7%) |  |
| `total_shots` | `String` | 712 (36.9%) |  |
| `shots_on_target` | `String` | 712 (36.9%) |  |
| `shots_inside_box` | `String` | 713 (37.0%) |  |
| `shots_outside_box` | `String` | 713 (37.0%) |  |
| `big_chances` | `String` | 713 (37.0%) |  |
| `big_chances_missed` | `String` | 713 (37.0%) |  |
| `touches_in_opposition_box` | `String` | 713 (37.0%) |  |
| `corners` | `String` | 712 (36.9%) |  |
| `accurate_passes` | `String` | 713 (37.0%) |  |
| `accurate_passes_pct` | `String` | 713 (37.0%) |  |
| `accurate_long_balls` | `String` | 713 (37.0%) |  |
| `accurate_long_balls_pct` | `String` | 713 (37.0%) |  |
| `accurate_crosses` | `String` | 713 (37.0%) |  |
| `accurate_crosses_pct` | `String` | 713 (37.0%) |  |
| `tackles_won` | `String` | 722 (37.4%) |  |
| `tackles_won_pct` | `String` | 1,017 (52.7%) |  |
| `interceptions` | `String` | 713 (37.0%) |  |
| `blocks` | `String` | 717 (37.2%) |  |
| `clearances` | `String` | 713 (37.0%) |  |
| `duels_won` | `String` | 717 (37.2%) |  |
| `aerial_duels_won` | `String` | 713 (37.0%) |  |
| `aerial_duels_won_pct` | `String` | 713 (37.0%) |  |
| `ground_duels_won` | `String` | 713 (37.0%) |  |
| `ground_duels_won_pct` | `String` | 714 (37.0%) |  |
| `fouls_committed` | `String` | 713 (37.0%) |  |
| `offsides` | `String` | 713 (37.0%) |  |
| `yellow_cards` | `String` | 715 (37.1%) |  |
| `red_cards` | `String` | 716 (37.1%) |  |
| `keeper_saves` | `String` | 713 (37.0%) |  |
| `successful_dribbles` | `String` | 713 (37.0%) |  |
| `successful_dribbles_pct` | `String` | 713 (37.0%) |  |
| `possession_against` | `String` | 718 (37.2%) |  |
| `xga` | `Float64` | 719 (37.3%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 753 (39.1%) |  |
| `xg_open_play_against` | `String` | 747 (38.7%) |  |
| `xg_set_play_against` | `String` | 747 (38.7%) |  |
| `xgot_against` | `String` | 747 (38.7%) |  |
| `shots_conceded` | `String` | 712 (36.9%) |  |
| `sot_conceded` | `String` | 712 (36.9%) |  |
| `shots_inside_box_against` | `String` | 713 (37.0%) |  |
| `shots_outside_box_against` | `String` | 713 (37.0%) |  |
| `big_chances_conceded` | `String` | 713 (37.0%) |  |
| `big_chances_missed_against` | `String` | 713 (37.0%) |  |
| `touches_in_opposition_box_against` | `String` | 713 (37.0%) |  |
| `corners_against` | `String` | 712 (36.9%) |  |
| `accurate_passes_against` | `String` | 713 (37.0%) |  |
| `accurate_passes_pct_against` | `String` | 713 (37.0%) |  |
| `accurate_long_balls_against` | `String` | 713 (37.0%) |  |
| `accurate_long_balls_pct_against` | `String` | 713 (37.0%) |  |
| `accurate_crosses_against` | `String` | 713 (37.0%) |  |
| `accurate_crosses_pct_against` | `String` | 713 (37.0%) |  |
| `tackles_won_against` | `String` | 722 (37.4%) |  |
| `tackles_won_pct_against` | `String` | 1,017 (52.7%) |  |
| `interceptions_against` | `String` | 713 (37.0%) |  |
| `blocks_against` | `String` | 717 (37.2%) |  |
| `clearances_against` | `String` | 713 (37.0%) |  |
| `duels_won_against` | `String` | 717 (37.2%) |  |
| `aerial_duels_won_against` | `String` | 713 (37.0%) |  |
| `aerial_duels_won_pct_against` | `String` | 713 (37.0%) |  |
| `ground_duels_won_against` | `String` | 713 (37.0%) |  |
| `ground_duels_won_pct_against` | `String` | 714 (37.0%) |  |
| `fouls_committed_against` | `String` | 713 (37.0%) |  |
| `offsides_against` | `String` | 713 (37.0%) |  |
| `yellow_cards_against` | `String` | 715 (37.1%) |  |
| `red_cards_against` | `String` | 716 (37.1%) |  |
| `keeper_saves_against` | `String` | 713 (37.0%) |  |
| `successful_dribbles_against` | `String` | 713 (37.0%) |  |
| `successful_dribbles_pct_against` | `String` | 713 (37.0%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 638 (33.1%) |  |
| `points` | `Int64` | 638 (33.1%) |  |
| `clean_sheet` | `Boolean` | 638 (33.1%) |  |
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

Rows: **294**. Columns: **12**.

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

