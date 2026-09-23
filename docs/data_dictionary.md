# FPL master datasets — data dictionary

Generated `2026-09-23T17:49:28Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **19,135**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.3%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 1,063 (5.6%) |  |
| `assists` | `Float64` | 1,142 (6.0%) |  |
| `total_shots` | `Float64` | 2,393 (12.5%) |  |
| `xg` | `Float64` | 2,634 (13.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 2,141 (11.2%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 2,393 (12.5%) |  |
| `successful_dribbles` | `String` | 3,765 (19.7%) |  |
| `big_chances_missed` | `String` | 4,093 (21.4%) |  |
| `touches_opposition_box` | `Float64` | 1,471 (7.7%) |  |
| `touches` | `Float64` | 950 (5.0%) |  |
| `accurate_passes` | `Float64` | 1,143 (6.0%) |  |
| `accurate_passes_percent` | `Float64` | 1,202 (6.3%) |  |
| `chances_created` | `Float64` | 1,136 (5.9%) |  |
| `final_third_passes` | `Float64` | 1,837 (9.6%) |  |
| `accurate_crosses` | `Float64` | 2,597 (13.6%) |  |
| `accurate_crosses_percent` | `Float64` | 2,632 (13.8%) |  |
| `accurate_long_balls` | `Float64` | 2,006 (10.5%) |  |
| `accurate_long_balls_percent` | `Float64` | 2,041 (10.7%) |  |
| `tackles_won` | `Float64` | 950 (5.0%) |  |
| `interceptions` | `Float64` | 950 (5.0%) |  |
| `recoveries` | `Float64` | 950 (5.0%) |  |
| `blocks` | `Float64` | 1,471 (7.7%) |  |
| `clearances` | `Float64` | 950 (5.0%) |  |
| `headed_clearances` | `Float64` | 3,081 (16.1%) |  |
| `dribbled_past` | `Float64` | 1,471 (7.7%) |  |
| `duels_won` | `Float64` | 1,462 (7.6%) |  |
| `duels_lost` | `Float64` | 1,498 (7.8%) |  |
| `ground_duels_won` | `Float64` | 1,343 (7.0%) |  |
| `ground_duels_won_percent` | `Float64` | 1,343 (7.0%) |  |
| `aerial_duels_won` | `Float64` | 1,129 (5.9%) |  |
| `aerial_duels_won_percent` | `Float64` | 2,068 (10.8%) |  |
| `was_fouled` | `Float64` | 2,540 (13.3%) |  |
| `fouls_committed` | `Float64` | 950 (5.0%) |  |
| `saves` | `Float64` | 3,572 (18.7%) |  |
| `goals_conceded` | `Float64` | 3,572 (18.7%) |  |
| `xgot_faced` | `String` | 3,946 (20.6%) |  |
| `goals_prevented` | `String` | 3,946 (20.6%) |  |
| `sweeper_actions` | `Float64` | 3,900 (20.4%) |  |
| `gk_accurate_passes` | `Float64` | 3,900 (20.4%) |  |
| `gk_accurate_long_balls` | `Float64` | 3,902 (20.4%) |  |
| `dispossessed` | `String` | 1,456 (7.6%) |  |
| `high_claim` | `Float64` | 3,900 (20.4%) |  |
| `saves_inside_box` | `Float64` | 3,900 (20.4%) |  |
| `offsides` | `String` | 4,093 (21.4%) |  |
| `successful_dribbles_percent` | `String` | 3,800 (19.9%) |  |
| `tackles_won_percent` | `String` | 3,800 (19.9%) |  |
| `xgot` | `Float64` | 3,252 (17.0%) |  |
| `tackles` | `String` | 3,765 (19.7%) |  |
| `start_min` | `Int64` | 997 (5.2%) |  |
| `finish_min` | `Int64` | 997 (5.2%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.6%) |  |
| `penalties_scored` | `Float64` | 46 (0.2%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,938 (78.1%) |  |
| `distance_covered` | `String` | 14,938 (78.1%) |  |
| `walking_distance` | `String` | 16,475 (86.1%) |  |
| `running_distance` | `String` | 14,938 (78.1%) |  |
| `sprinting_distance` | `String` | 15,017 (78.5%) |  |
| `number_of_sprints` | `String` | 15,076 (78.8%) |  |
| `defensive_contributions` | `String` | 4,295 (22.4%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,474 (7.7%) |  |
| `away_team` | `Int64` | 1,887 (9.9%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (3.9%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (3.9%) |  |
| `is_home` | `Boolean` | 1,474 (7.7%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,530 (18.4%) | Opponent club code. |
| `team_goals_for` | `Float64` | 253 (1.3%) |  |
| `team_goals_against` | `Float64` | 253 (1.3%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 253 (1.3%) |  |
| `started` | `Boolean` | 5,635 (29.4%) |  |
| `formation` | `String` | 5,635 (29.4%) |  |
| `lineup_status` | `String` | 5,635 (29.4%) |  |
| `lineup_team_code` | `Int64` | 5,635 (29.4%) |  |
| `rating` | `Float64` | 6,558 (34.3%) |  |
| `yellow_cards` | `Float64` | 6,319 (33.0%) |  |
| `red_cards` | `Float64` | 6,319 (33.0%) |  |
| `np_xg` | `Float64` | 12,186 (63.7%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `set_piece_xg` | `Float64` | 12,186 (63.7%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 12,186 (63.7%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 12,186 (63.7%) |  |
| `own_goals` | `Float64` | 1,040 (5.4%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 19,135 (100.0%) |  |
| `fpl_points` | `Float64` | 1,040 (5.4%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,040 (5.4%) |  |
| `bps` | `Float64` | 1,040 (5.4%) |  |
| `now_cost` | `Float64` | 1,040 (5.4%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,040 (5.4%) |  |
| `form` | `Float64` | 1,040 (5.4%) |  |
| `penalties_order` | `String` | 17,240 (90.1%) |  |
| `direct_freekicks_order` | `String` | 17,166 (89.7%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 16,513 (86.3%) |  |
| `status` | `String` | 1,040 (5.4%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **33,228**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 21,542 (64.8%) |  |
| `now_cost` | `Float64` | 0 (0.0%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 0 (0.0%) |  |
| `form` | `Float64` | 0 (0.0%) |  |
| `event_points` | `Int64` | 0 (0.0%) |  |
| `total_points` | `Int64` | 0 (0.0%) |  |
| `bonus` | `Float64` | 0 (0.0%) |  |
| `bps` | `Float64` | 0 (0.0%) |  |
| `points_per_game` | `String` | 6,016 (18.1%) |  |
| `ep_next` | `Float64` | 1 (0.0%) |  |
| `ep_this` | `Float64` | 0 (0.0%) |  |
| `transfers_in_event` | `Int64` | 0 (0.0%) |  |
| `transfers_out_event` | `Int64` | 0 (0.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 30,598 (92.1%) |  |
| `direct_freekicks_order` | `String` | 31,206 (93.9%) |  |
| `penalties_order` | `String` | 31,249 (94.0%) |  |
| `set_piece_threat` | `String` | 33,228 (100.0%) |  |
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
| `goals_for` | `Float64` | 741 (38.6%) |  |
| `goals_against` | `Float64` | 741 (38.6%) |  |
| `elo` | `Float64` | 996 (51.8%) |  |
| `possession` | `Float64` | 821 (42.7%) |  |
| `xg` | `Float64` | 822 (42.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 856 (44.5%) | Non-penalty xG from FPL-Core shots (situation != penalty) joined on match_id + player_id. Serving fills gaps with xG − 0.79 × penalties_scored when the shot join is null. |
| `xg_open_play` | `String` | 850 (44.2%) |  |
| `xg_set_play` | `String` | 850 (44.2%) |  |
| `xgot` | `Float64` | 850 (44.2%) |  |
| `total_shots` | `String` | 815 (42.4%) |  |
| `shots_on_target` | `String` | 815 (42.4%) |  |
| `shots_inside_box` | `String` | 816 (42.5%) |  |
| `shots_outside_box` | `String` | 816 (42.5%) |  |
| `big_chances` | `String` | 816 (42.5%) |  |
| `big_chances_missed` | `String` | 816 (42.5%) |  |
| `touches_in_opposition_box` | `String` | 816 (42.5%) |  |
| `corners` | `String` | 815 (42.4%) |  |
| `accurate_passes` | `String` | 816 (42.5%) |  |
| `accurate_passes_pct` | `String` | 816 (42.5%) |  |
| `accurate_long_balls` | `String` | 816 (42.5%) |  |
| `accurate_long_balls_pct` | `String` | 816 (42.5%) |  |
| `accurate_crosses` | `String` | 816 (42.5%) |  |
| `accurate_crosses_pct` | `String` | 816 (42.5%) |  |
| `tackles_won` | `String` | 825 (42.9%) |  |
| `tackles_won_pct` | `String` | 1,011 (52.6%) |  |
| `interceptions` | `String` | 816 (42.5%) |  |
| `blocks` | `String` | 820 (42.7%) |  |
| `clearances` | `String` | 816 (42.5%) |  |
| `duels_won` | `String` | 820 (42.7%) |  |
| `aerial_duels_won` | `String` | 816 (42.5%) |  |
| `aerial_duels_won_pct` | `String` | 816 (42.5%) |  |
| `ground_duels_won` | `String` | 816 (42.5%) |  |
| `ground_duels_won_pct` | `String` | 817 (42.5%) |  |
| `fouls_committed` | `String` | 816 (42.5%) |  |
| `offsides` | `String` | 816 (42.5%) |  |
| `yellow_cards` | `String` | 818 (42.6%) |  |
| `red_cards` | `String` | 819 (42.6%) |  |
| `keeper_saves` | `String` | 816 (42.5%) |  |
| `successful_dribbles` | `String` | 816 (42.5%) |  |
| `successful_dribbles_pct` | `String` | 816 (42.5%) |  |
| `possession_against` | `String` | 821 (42.7%) |  |
| `xga` | `Float64` | 822 (42.8%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 856 (44.5%) |  |
| `xg_open_play_against` | `String` | 850 (44.2%) |  |
| `xg_set_play_against` | `String` | 850 (44.2%) |  |
| `xgot_against` | `String` | 850 (44.2%) |  |
| `shots_conceded` | `String` | 815 (42.4%) |  |
| `sot_conceded` | `String` | 815 (42.4%) |  |
| `shots_inside_box_against` | `String` | 816 (42.5%) |  |
| `shots_outside_box_against` | `String` | 816 (42.5%) |  |
| `big_chances_conceded` | `String` | 816 (42.5%) |  |
| `big_chances_missed_against` | `String` | 816 (42.5%) |  |
| `touches_in_opposition_box_against` | `String` | 816 (42.5%) |  |
| `corners_against` | `String` | 815 (42.4%) |  |
| `accurate_passes_against` | `String` | 816 (42.5%) |  |
| `accurate_passes_pct_against` | `String` | 816 (42.5%) |  |
| `accurate_long_balls_against` | `String` | 816 (42.5%) |  |
| `accurate_long_balls_pct_against` | `String` | 816 (42.5%) |  |
| `accurate_crosses_against` | `String` | 816 (42.5%) |  |
| `accurate_crosses_pct_against` | `String` | 816 (42.5%) |  |
| `tackles_won_against` | `String` | 825 (42.9%) |  |
| `tackles_won_pct_against` | `String` | 1,011 (52.6%) |  |
| `interceptions_against` | `String` | 816 (42.5%) |  |
| `blocks_against` | `String` | 820 (42.7%) |  |
| `clearances_against` | `String` | 816 (42.5%) |  |
| `duels_won_against` | `String` | 820 (42.7%) |  |
| `aerial_duels_won_against` | `String` | 816 (42.5%) |  |
| `aerial_duels_won_pct_against` | `String` | 816 (42.5%) |  |
| `ground_duels_won_against` | `String` | 816 (42.5%) |  |
| `ground_duels_won_pct_against` | `String` | 817 (42.5%) |  |
| `fouls_committed_against` | `String` | 816 (42.5%) |  |
| `offsides_against` | `String` | 816 (42.5%) |  |
| `yellow_cards_against` | `String` | 818 (42.6%) |  |
| `red_cards_against` | `String` | 819 (42.6%) |  |
| `keeper_saves_against` | `String` | 816 (42.5%) |  |
| `successful_dribbles_against` | `String` | 816 (42.5%) |  |
| `successful_dribbles_pct_against` | `String` | 816 (42.5%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 741 (38.6%) |  |
| `points` | `Int64` | 741 (38.6%) |  |
| `clean_sheet` | `Boolean` | 741 (38.6%) |  |
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

Rows: **337**. Columns: **12**.

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

