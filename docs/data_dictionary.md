# FPL master datasets — data dictionary

Generated `2026-08-24T08:05:56Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **16,701**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.4%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 391 (2.3%) |  |
| `assists` | `Float64` | 471 (2.8%) |  |
| `total_shots` | `Float64` | 921 (5.5%) |  |
| `xg` | `Float64` | 1,162 (7.0%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,060 (6.3%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 921 (5.5%) |  |
| `successful_dribbles` | `String` | 1,331 (8.0%) |  |
| `big_chances_missed` | `String` | 1,659 (9.9%) |  |
| `touches_opposition_box` | `Float64` | 799 (4.8%) |  |
| `touches` | `Float64` | 401 (2.4%) |  |
| `accurate_passes` | `Float64` | 471 (2.8%) |  |
| `accurate_passes_percent` | `Float64` | 513 (3.1%) |  |
| `chances_created` | `Float64` | 470 (2.8%) |  |
| `final_third_passes` | `Float64` | 917 (5.5%) |  |
| `accurate_crosses` | `Float64` | 981 (5.9%) |  |
| `accurate_crosses_percent` | `Float64` | 1,016 (6.1%) |  |
| `accurate_long_balls` | `Float64` | 755 (4.5%) |  |
| `accurate_long_balls_percent` | `Float64` | 790 (4.7%) |  |
| `tackles_won` | `Float64` | 401 (2.4%) |  |
| `interceptions` | `Float64` | 401 (2.4%) |  |
| `recoveries` | `Float64` | 401 (2.4%) |  |
| `blocks` | `Float64` | 799 (4.8%) |  |
| `clearances` | `Float64` | 401 (2.4%) |  |
| `headed_clearances` | `Float64` | 1,388 (8.3%) |  |
| `dribbled_past` | `Float64` | 799 (4.8%) |  |
| `duels_won` | `Float64` | 617 (3.7%) |  |
| `duels_lost` | `Float64` | 642 (3.8%) |  |
| `ground_duels_won` | `Float64` | 568 (3.4%) |  |
| `ground_duels_won_percent` | `Float64` | 568 (3.4%) |  |
| `aerial_duels_won` | `Float64` | 493 (3.0%) |  |
| `aerial_duels_won_percent` | `Float64` | 896 (5.4%) |  |
| `was_fouled` | `Float64` | 934 (5.6%) |  |
| `fouls_committed` | `Float64` | 401 (2.4%) |  |
| `saves` | `Float64` | 1,261 (7.6%) |  |
| `goals_conceded` | `Float64` | 1,261 (7.6%) |  |
| `xgot_faced` | `String` | 1,629 (9.8%) |  |
| `goals_prevented` | `String` | 1,629 (9.8%) |  |
| `sweeper_actions` | `Float64` | 1,589 (9.5%) |  |
| `gk_accurate_passes` | `Float64` | 1,589 (9.5%) |  |
| `gk_accurate_long_balls` | `Float64` | 1,591 (9.5%) |  |
| `dispossessed` | `String` | 784 (4.7%) |  |
| `high_claim` | `Float64` | 1,589 (9.5%) |  |
| `saves_inside_box` | `Float64` | 1,589 (9.5%) |  |
| `offsides` | `String` | 1,659 (9.9%) |  |
| `successful_dribbles_percent` | `String` | 1,366 (8.2%) |  |
| `tackles_won_percent` | `String` | 1,366 (8.2%) |  |
| `xgot` | `Float64` | 1,273 (7.6%) |  |
| `tackles` | `String` | 1,331 (8.0%) |  |
| `start_min` | `Int64` | 448 (2.7%) |  |
| `finish_min` | `Int64` | 448 (2.7%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.9%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,120 (84.5%) |  |
| `distance_covered` | `String` | 14,120 (84.5%) |  |
| `walking_distance` | `String` | 14,120 (84.5%) |  |
| `running_distance` | `String` | 14,120 (84.5%) |  |
| `sprinting_distance` | `String` | 14,120 (84.5%) |  |
| `number_of_sprints` | `String` | 14,120 (84.5%) |  |
| `defensive_contributions` | `String` | 1,861 (11.1%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,249 (7.5%) |  |
| `away_team` | `Int64` | 1,628 (9.7%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.5%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.5%) |  |
| `is_home` | `Boolean` | 1,249 (7.5%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,031 (18.1%) | Opponent club code. |
| `team_goals_for` | `Float64` | 207 (1.2%) |  |
| `team_goals_against` | `Float64` | 207 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 207 (1.2%) |  |
| `started` | `Boolean` | 3,201 (19.2%) |  |
| `formation` | `String` | 3,201 (19.2%) |  |
| `lineup_status` | `String` | 3,201 (19.2%) |  |
| `lineup_team_code` | `Int64` | 3,201 (19.2%) |  |
| `rating` | `Float64` | 4,124 (24.7%) |  |
| `yellow_cards` | `Float64` | 3,885 (23.3%) |  |
| `red_cards` | `Float64` | 3,885 (23.3%) |  |
| `np_xg` | `Float64` | 10,318 (61.8%) | Non-penalty xG aggregated from shots.situation. |
| `set_piece_xg` | `Float64` | 10,318 (61.8%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 10,318 (61.8%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 10,318 (61.8%) |  |
| `own_goals` | `Float64` | 1,039 (6.2%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 16,701 (100.0%) |  |
| `fpl_points` | `Float64` | 1,039 (6.2%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,039 (6.2%) |  |
| `bps` | `Float64` | 1,039 (6.2%) |  |
| `now_cost` | `Float64` | 1,039 (6.2%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,039 (6.2%) |  |
| `form` | `Float64` | 1,039 (6.2%) |  |
| `penalties_order` | `String` | 15,102 (90.4%) |  |
| `direct_freekicks_order` | `String` | 15,035 (90.0%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 14,517 (86.9%) |  |
| `status` | `String` | 1,039 (6.2%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **30,587**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 19,657 (64.3%) |  |
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
| `corners_and_indirect_freekicks_order` | `String` | 28,281 (92.5%) |  |
| `direct_freekicks_order` | `String` | 28,798 (94.2%) |  |
| `penalties_order` | `String` | 28,855 (94.3%) |  |
| `set_piece_threat` | `String` | 30,587 (100.0%) |  |
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
| `goals_for` | `Float64` | 759 (41.7%) |  |
| `goals_against` | `Float64` | 759 (41.7%) |  |
| `elo` | `Float64` | 928 (51.0%) |  |
| `possession` | `Float64` | 841 (46.2%) |  |
| `xg` | `Float64` | 842 (46.3%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 876 (48.1%) | Non-penalty xG aggregated from shots.situation. |
| `xg_open_play` | `String` | 870 (47.8%) |  |
| `xg_set_play` | `String` | 870 (47.8%) |  |
| `xgot` | `Float64` | 870 (47.8%) |  |
| `total_shots` | `String` | 835 (45.9%) |  |
| `shots_on_target` | `String` | 835 (45.9%) |  |
| `shots_inside_box` | `String` | 836 (45.9%) |  |
| `shots_outside_box` | `String` | 836 (45.9%) |  |
| `big_chances` | `String` | 836 (45.9%) |  |
| `big_chances_missed` | `String` | 836 (45.9%) |  |
| `touches_in_opposition_box` | `String` | 836 (45.9%) |  |
| `corners` | `String` | 835 (45.9%) |  |
| `accurate_passes` | `String` | 836 (45.9%) |  |
| `accurate_passes_pct` | `String` | 836 (45.9%) |  |
| `accurate_long_balls` | `String` | 836 (45.9%) |  |
| `accurate_long_balls_pct` | `String` | 836 (45.9%) |  |
| `accurate_crosses` | `String` | 836 (45.9%) |  |
| `accurate_crosses_pct` | `String` | 836 (45.9%) |  |
| `tackles_won` | `String` | 845 (46.4%) |  |
| `tackles_won_pct` | `String` | 909 (49.9%) |  |
| `interceptions` | `String` | 836 (45.9%) |  |
| `blocks` | `String` | 840 (46.2%) |  |
| `clearances` | `String` | 836 (45.9%) |  |
| `duels_won` | `String` | 840 (46.2%) |  |
| `aerial_duels_won` | `String` | 836 (45.9%) |  |
| `aerial_duels_won_pct` | `String` | 836 (45.9%) |  |
| `ground_duels_won` | `String` | 836 (45.9%) |  |
| `ground_duels_won_pct` | `String` | 837 (46.0%) |  |
| `fouls_committed` | `String` | 836 (45.9%) |  |
| `offsides` | `String` | 836 (45.9%) |  |
| `yellow_cards` | `String` | 838 (46.0%) |  |
| `red_cards` | `String` | 839 (46.1%) |  |
| `keeper_saves` | `String` | 836 (45.9%) |  |
| `successful_dribbles` | `String` | 836 (45.9%) |  |
| `successful_dribbles_pct` | `String` | 836 (45.9%) |  |
| `possession_against` | `String` | 841 (46.2%) |  |
| `xga` | `Float64` | 842 (46.3%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 876 (48.1%) |  |
| `xg_open_play_against` | `String` | 870 (47.8%) |  |
| `xg_set_play_against` | `String` | 870 (47.8%) |  |
| `xgot_against` | `String` | 870 (47.8%) |  |
| `shots_conceded` | `String` | 835 (45.9%) |  |
| `sot_conceded` | `String` | 835 (45.9%) |  |
| `shots_inside_box_against` | `String` | 836 (45.9%) |  |
| `shots_outside_box_against` | `String` | 836 (45.9%) |  |
| `big_chances_conceded` | `String` | 836 (45.9%) |  |
| `big_chances_missed_against` | `String` | 836 (45.9%) |  |
| `touches_in_opposition_box_against` | `String` | 836 (45.9%) |  |
| `corners_against` | `String` | 835 (45.9%) |  |
| `accurate_passes_against` | `String` | 836 (45.9%) |  |
| `accurate_passes_pct_against` | `String` | 836 (45.9%) |  |
| `accurate_long_balls_against` | `String` | 836 (45.9%) |  |
| `accurate_long_balls_pct_against` | `String` | 836 (45.9%) |  |
| `accurate_crosses_against` | `String` | 836 (45.9%) |  |
| `accurate_crosses_pct_against` | `String` | 836 (45.9%) |  |
| `tackles_won_against` | `String` | 845 (46.4%) |  |
| `tackles_won_pct_against` | `String` | 909 (49.9%) |  |
| `interceptions_against` | `String` | 836 (45.9%) |  |
| `blocks_against` | `String` | 840 (46.2%) |  |
| `clearances_against` | `String` | 836 (45.9%) |  |
| `duels_won_against` | `String` | 840 (46.2%) |  |
| `aerial_duels_won_against` | `String` | 836 (45.9%) |  |
| `aerial_duels_won_pct_against` | `String` | 836 (45.9%) |  |
| `ground_duels_won_against` | `String` | 836 (45.9%) |  |
| `ground_duels_won_pct_against` | `String` | 837 (46.0%) |  |
| `fouls_committed_against` | `String` | 836 (45.9%) |  |
| `offsides_against` | `String` | 836 (45.9%) |  |
| `yellow_cards_against` | `String` | 838 (46.0%) |  |
| `red_cards_against` | `String` | 839 (46.1%) |  |
| `keeper_saves_against` | `String` | 836 (45.9%) |  |
| `successful_dribbles_against` | `String` | 836 (45.9%) |  |
| `successful_dribbles_pct_against` | `String` | 836 (45.9%) |  |
| `kickoff_raw` | `String` | 44 (2.4%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.4%) |  |
| `result` | `String` | 759 (41.7%) |  |
| `points` | `Int64` | 759 (41.7%) |  |
| `clean_sheet` | `Boolean` | 759 (41.7%) |  |
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

Rows: **373**. Columns: **12**.

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

