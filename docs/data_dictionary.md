# FPL master datasets — data dictionary

Generated `2026-10-20T12:37:38Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **20,074**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,325 (6.6%) |  |
| `assists` | `Float64` | 1,404 (7.0%) |  |
| `total_shots` | `Float64` | 2,988 (14.9%) |  |
| `xg` | `Float64` | 3,229 (16.1%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 2,576 (12.8%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 2,988 (14.9%) |  |
| `successful_dribbles` | `String` | 4,704 (23.4%) |  |
| `big_chances_missed` | `String` | 5,032 (25.1%) |  |
| `touches_opposition_box` | `Float64` | 1,733 (8.6%) |  |
| `touches` | `Float64` | 1,164 (5.8%) |  |
| `accurate_passes` | `Float64` | 1,405 (7.0%) |  |
| `accurate_passes_percent` | `Float64` | 1,470 (7.3%) |  |
| `chances_created` | `Float64` | 1,396 (7.0%) |  |
| `final_third_passes` | `Float64` | 2,193 (10.9%) |  |
| `accurate_crosses` | `Float64` | 3,207 (16.0%) |  |
| `accurate_crosses_percent` | `Float64` | 3,242 (16.2%) |  |
| `accurate_long_balls` | `Float64` | 2,478 (12.3%) |  |
| `accurate_long_balls_percent` | `Float64` | 2,513 (12.5%) |  |
| `tackles_won` | `Float64` | 1,164 (5.8%) |  |
| `interceptions` | `Float64` | 1,164 (5.8%) |  |
| `recoveries` | `Float64` | 1,164 (5.8%) |  |
| `blocks` | `Float64` | 1,733 (8.6%) |  |
| `clearances` | `Float64` | 1,164 (5.8%) |  |
| `headed_clearances` | `Float64` | 3,756 (18.7%) |  |
| `dribbled_past` | `Float64` | 1,733 (8.6%) |  |
| `duels_won` | `Float64` | 1,806 (9.0%) |  |
| `duels_lost` | `Float64` | 1,835 (9.1%) |  |
| `ground_duels_won` | `Float64` | 1,658 (8.3%) |  |
| `ground_duels_won_percent` | `Float64` | 1,658 (8.3%) |  |
| `aerial_duels_won` | `Float64` | 1,380 (6.9%) |  |
| `aerial_duels_won_percent` | `Float64` | 2,523 (12.6%) |  |
| `was_fouled` | `Float64` | 3,169 (15.8%) |  |
| `fouls_committed` | `Float64` | 1,164 (5.8%) |  |
| `saves` | `Float64` | 4,463 (22.2%) |  |
| `goals_conceded` | `Float64` | 4,463 (22.2%) |  |
| `xgot_faced` | `String` | 4,840 (24.1%) |  |
| `goals_prevented` | `String` | 4,840 (24.1%) |  |
| `sweeper_actions` | `Float64` | 4,791 (23.9%) |  |
| `gk_accurate_passes` | `Float64` | 4,791 (23.9%) |  |
| `gk_accurate_long_balls` | `Float64` | 4,793 (23.9%) |  |
| `dispossessed` | `String` | 1,718 (8.6%) |  |
| `high_claim` | `Float64` | 4,791 (23.9%) |  |
| `saves_inside_box` | `Float64` | 4,791 (23.9%) |  |
| `offsides` | `String` | 5,032 (25.1%) |  |
| `successful_dribbles_percent` | `String` | 4,739 (23.6%) |  |
| `tackles_won_percent` | `String` | 4,739 (23.6%) |  |
| `xgot` | `Float64` | 4,025 (20.1%) |  |
| `tackles` | `String` | 4,704 (23.4%) |  |
| `start_min` | `Int64` | 1,211 (6.0%) |  |
| `finish_min` | `Int64` | 1,211 (6.0%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.6%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 15,245 (75.9%) |  |
| `distance_covered` | `String` | 15,245 (75.9%) |  |
| `walking_distance` | `String` | 17,367 (86.5%) |  |
| `running_distance` | `String` | 15,245 (75.9%) |  |
| `sprinting_distance` | `String` | 15,344 (76.4%) |  |
| `number_of_sprints` | `String` | 15,429 (76.9%) |  |
| `defensive_contributions` | `String` | 5,234 (26.1%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,552 (7.7%) |  |
| `away_team` | `Int64` | 1,992 (9.9%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.7%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.7%) |  |
| `is_home` | `Boolean` | 1,552 (7.7%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,713 (18.5%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.3%) |  |
| `team_goals_against` | `Float64` | 253 (1.3%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.3%) |  |
| `started` | `Boolean` | 6,574 (32.7%) |  |
| `formation` | `String` | 6,574 (32.7%) |  |
| `lineup_status` | `String` | 6,574 (32.7%) |  |
| `lineup_team_code` | `Int64` | 6,574 (32.7%) |  |
| `rating` | `Float64` | 7,497 (37.3%) |  |
| `yellow_cards` | `Float64` | 7,258 (36.2%) |  |
| `red_cards` | `Float64` | 7,258 (36.2%) |  |
| `np_xg` | `Float64` | 12,891 (64.2%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 12,891 (64.2%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 12,891 (64.2%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 12,891 (64.2%) |  |
| `own_goals` | `Float64` | 1,040 (5.2%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 20,074 (100.0%) |  |
| `fpl_points` | `Float64` | 1,040 (5.2%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,040 (5.2%) |  |
| `bps` | `Float64` | 1,040 (5.2%) |  |
| `now_cost` | `Float64` | 1,040 (5.2%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,040 (5.2%) |  |
| `form` | `Float64` | 1,040 (5.2%) |  |
| `penalties_order` | `String` | 18,061 (90.0%) |  |
| `direct_freekicks_order` | `String` | 17,964 (89.5%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 17,269 (86.0%) |  |
| `status` | `String` | 1,040 (5.2%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **34,563**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 22,463 (65.0%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (17.4%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 31,749 (91.9%) |  |
| `direct_freekicks_order` | `String` | 32,406 (93.8%) |  |
| `penalties_order` | `String` | 32,459 (93.9%) |  |
| `set_piece_threat` | `String` | 34,563 (100.0%) |  |
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
| `goals_for` | `Float64` | 692 (36.0%) |  |
| `goals_against` | `Float64` | 692 (36.0%) |  |
| `elo` | `Float64` | 996 (51.8%) |  |
| `possession` | `Float64` | 774 (40.3%) |  |
| `xg` | `Float64` | 775 (40.3%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 809 (42.1%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 803 (41.8%) |  |
| `xg_set_play` | `String` | 803 (41.8%) |  |
| `xgot` | `Float64` | 803 (41.8%) |  |
| `total_shots` | `String` | 768 (40.0%) |  |
| `shots_on_target` | `String` | 768 (40.0%) |  |
| `shots_inside_box` | `String` | 769 (40.0%) |  |
| `shots_outside_box` | `String` | 769 (40.0%) |  |
| `big_chances` | `String` | 769 (40.0%) |  |
| `big_chances_missed` | `String` | 769 (40.0%) |  |
| `touches_in_opposition_box` | `String` | 769 (40.0%) |  |
| `corners` | `String` | 768 (40.0%) |  |
| `accurate_passes` | `String` | 769 (40.0%) |  |
| `accurate_passes_pct` | `String` | 769 (40.0%) |  |
| `accurate_long_balls` | `String` | 769 (40.0%) |  |
| `accurate_long_balls_pct` | `String` | 769 (40.0%) |  |
| `accurate_crosses` | `String` | 769 (40.0%) |  |
| `accurate_crosses_pct` | `String` | 769 (40.0%) |  |
| `tackles_won` | `String` | 778 (40.5%) |  |
| `tackles_won_pct` | `String` | 1,011 (52.6%) |  |
| `interceptions` | `String` | 769 (40.0%) |  |
| `blocks` | `String` | 773 (40.2%) |  |
| `clearances` | `String` | 769 (40.0%) |  |
| `duels_won` | `String` | 773 (40.2%) |  |
| `aerial_duels_won` | `String` | 769 (40.0%) |  |
| `aerial_duels_won_pct` | `String` | 769 (40.0%) |  |
| `ground_duels_won` | `String` | 769 (40.0%) |  |
| `ground_duels_won_pct` | `String` | 770 (40.1%) |  |
| `fouls_committed` | `String` | 769 (40.0%) |  |
| `offsides` | `String` | 769 (40.0%) |  |
| `yellow_cards` | `String` | 771 (40.1%) |  |
| `red_cards` | `String` | 772 (40.2%) |  |
| `keeper_saves` | `String` | 769 (40.0%) |  |
| `successful_dribbles` | `String` | 769 (40.0%) |  |
| `successful_dribbles_pct` | `String` | 769 (40.0%) |  |
| `possession_against` | `String` | 774 (40.3%) |  |
| `xga` | `Float64` | 775 (40.3%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 809 (42.1%) |  |
| `xg_open_play_against` | `String` | 803 (41.8%) |  |
| `xg_set_play_against` | `String` | 803 (41.8%) |  |
| `xgot_against` | `String` | 803 (41.8%) |  |
| `shots_conceded` | `String` | 768 (40.0%) |  |
| `sot_conceded` | `String` | 768 (40.0%) |  |
| `shots_inside_box_against` | `String` | 769 (40.0%) |  |
| `shots_outside_box_against` | `String` | 769 (40.0%) |  |
| `big_chances_conceded` | `String` | 769 (40.0%) |  |
| `big_chances_missed_against` | `String` | 769 (40.0%) |  |
| `touches_in_opposition_box_against` | `String` | 769 (40.0%) |  |
| `corners_against` | `String` | 768 (40.0%) |  |
| `accurate_passes_against` | `String` | 769 (40.0%) |  |
| `accurate_passes_pct_against` | `String` | 769 (40.0%) |  |
| `accurate_long_balls_against` | `String` | 769 (40.0%) |  |
| `accurate_long_balls_pct_against` | `String` | 769 (40.0%) |  |
| `accurate_crosses_against` | `String` | 769 (40.0%) |  |
| `accurate_crosses_pct_against` | `String` | 769 (40.0%) |  |
| `tackles_won_against` | `String` | 778 (40.5%) |  |
| `tackles_won_pct_against` | `String` | 1,011 (52.6%) |  |
| `interceptions_against` | `String` | 769 (40.0%) |  |
| `blocks_against` | `String` | 773 (40.2%) |  |
| `clearances_against` | `String` | 769 (40.0%) |  |
| `duels_won_against` | `String` | 773 (40.2%) |  |
| `aerial_duels_won_against` | `String` | 769 (40.0%) |  |
| `aerial_duels_won_pct_against` | `String` | 769 (40.0%) |  |
| `ground_duels_won_against` | `String` | 769 (40.0%) |  |
| `ground_duels_won_pct_against` | `String` | 770 (40.1%) |  |
| `fouls_committed_against` | `String` | 769 (40.0%) |  |
| `offsides_against` | `String` | 769 (40.0%) |  |
| `yellow_cards_against` | `String` | 771 (40.1%) |  |
| `red_cards_against` | `String` | 772 (40.2%) |  |
| `keeper_saves_against` | `String` | 769 (40.0%) |  |
| `successful_dribbles_against` | `String` | 769 (40.0%) |  |
| `successful_dribbles_pct_against` | `String` | 769 (40.0%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 692 (36.0%) |  |
| `points` | `Int64` | 692 (36.0%) |  |
| `clean_sheet` | `Boolean` | 692 (36.0%) |  |
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

Rows: **317**. Columns: **12**.

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

