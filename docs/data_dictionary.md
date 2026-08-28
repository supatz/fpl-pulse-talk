# FPL master datasets — data dictionary

Generated `2026-08-28T15:32:10Z`.

Source: public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights).

Missing values are null, never filled with zero. `player_id` is season-scoped;
`player_code` and `team_code` are stable. FPL points live on `player_gw`;
`player_match` is the football grain.

## `player_match`

Rows: **17,001**. Columns: **114**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `minutes` | `Float64` | 62 (0.4%) | Minutes played (Opta/match layer). Missing is unknown, not zero. |
| `goals` | `Float64` | 470 (2.8%) |  |
| `assists` | `Float64` | 550 (3.2%) |  |
| `total_shots` | `Float64` | 1,085 (6.4%) |  |
| `xg` | `Float64` | 1,326 (7.8%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `xa` | `Float64` | 1,172 (6.9%) | Opta expected assists. |
| `shots_on_target` | `Float64` | 1,085 (6.4%) |  |
| `successful_dribbles` | `String` | 1,631 (9.6%) |  |
| `big_chances_missed` | `String` | 1,959 (11.5%) |  |
| `touches_opposition_box` | `Float64` | 878 (5.2%) |  |
| `touches` | `Float64` | 466 (2.7%) |  |
| `accurate_passes` | `Float64` | 550 (3.2%) |  |
| `accurate_passes_percent` | `Float64` | 596 (3.5%) |  |
| `chances_created` | `Float64` | 549 (3.2%) |  |
| `final_third_passes` | `Float64` | 1,028 (6.0%) |  |
| `accurate_crosses` | `Float64` | 1,180 (6.9%) |  |
| `accurate_crosses_percent` | `Float64` | 1,215 (7.1%) |  |
| `accurate_long_balls` | `Float64` | 893 (5.3%) |  |
| `accurate_long_balls_percent` | `Float64` | 928 (5.5%) |  |
| `tackles_won` | `Float64` | 466 (2.7%) |  |
| `interceptions` | `Float64` | 466 (2.7%) |  |
| `recoveries` | `Float64` | 466 (2.7%) |  |
| `blocks` | `Float64` | 878 (5.2%) |  |
| `clearances` | `Float64` | 466 (2.7%) |  |
| `headed_clearances` | `Float64` | 1,606 (9.4%) |  |
| `dribbled_past` | `Float64` | 878 (5.2%) |  |
| `duels_won` | `Float64` | 719 (4.2%) |  |
| `duels_lost` | `Float64` | 749 (4.4%) |  |
| `ground_duels_won` | `Float64` | 656 (3.9%) |  |
| `ground_duels_won_percent` | `Float64` | 656 (3.9%) |  |
| `aerial_duels_won` | `Float64` | 569 (3.3%) |  |
| `aerial_duels_won_percent` | `Float64` | 1,053 (6.2%) |  |
| `was_fouled` | `Float64` | 1,128 (6.6%) |  |
| `fouls_committed` | `Float64` | 466 (2.7%) |  |
| `saves` | `Float64` | 1,547 (9.1%) |  |
| `goals_conceded` | `Float64` | 1,547 (9.1%) |  |
| `xgot_faced` | `String` | 1,915 (11.3%) |  |
| `goals_prevented` | `String` | 1,915 (11.3%) |  |
| `sweeper_actions` | `Float64` | 1,875 (11.0%) |  |
| `gk_accurate_passes` | `Float64` | 1,875 (11.0%) |  |
| `gk_accurate_long_balls` | `Float64` | 1,877 (11.0%) |  |
| `dispossessed` | `String` | 863 (5.1%) |  |
| `high_claim` | `Float64` | 1,875 (11.0%) |  |
| `saves_inside_box` | `Float64` | 1,875 (11.0%) |  |
| `offsides` | `String` | 1,959 (11.5%) |  |
| `successful_dribbles_percent` | `String` | 1,666 (9.8%) |  |
| `tackles_won_percent` | `String` | 1,666 (9.8%) |  |
| `xgot` | `Float64` | 1,500 (8.8%) |  |
| `tackles` | `String` | 1,631 (9.6%) |  |
| `start_min` | `Int64` | 513 (3.0%) |  |
| `finish_min` | `Int64` | 513 (3.0%) |  |
| `team_goals_conceded` | `Int64` | 314 (1.8%) |  |
| `penalties_scored` | `Float64` | 46 (0.3%) |  |
| `penalties_missed` | `Int64` | 21 (0.1%) |  |
| `top_speed` | `String` | 14,420 (84.8%) |  |
| `distance_covered` | `String` | 14,420 (84.8%) |  |
| `walking_distance` | `String` | 14,420 (84.8%) |  |
| `running_distance` | `String` | 14,420 (84.8%) |  |
| `sprinting_distance` | `String` | 14,420 (84.8%) |  |
| `number_of_sprints` | `String` | 14,420 (84.8%) |  |
| `defensive_contributions` | `String` | 2,161 (12.7%) |  |
| `player_code` | `Int64` | 0 (0.0%) | Stable cross-season player identity. |
| `web_name` | `String` | 0 (0.0%) |  |
| `position` | `String` | 0 (0.0%) |  |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `home_team` | `Int64` | 1,326 (7.8%) |  |
| `away_team` | `Int64` | 1,724 (10.1%) |  |
| `home_score` | `Float64` | 0 (0.0%) |  |
| `away_score` | `Float64` | 0 (0.0%) |  |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `kickoff_raw` | `String` | 749 (4.4%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `match_gw` | `Int64` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 749 (4.4%) |  |
| `is_home` | `Boolean` | 1,326 (7.8%) | True if the row's team/player is the home side. |
| `opponent_code` | `Int64` | 3,204 (18.8%) | Opponent club code. |
| `team_goals_for` | `Float64` | 210 (1.2%) |  |
| `team_goals_against` | `Float64` | 210 (1.2%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `result` | `String` | 210 (1.2%) |  |
| `started` | `Boolean` | 3,501 (20.6%) |  |
| `formation` | `String` | 3,501 (20.6%) |  |
| `lineup_status` | `String` | 3,501 (20.6%) |  |
| `lineup_team_code` | `Int64` | 3,501 (20.6%) |  |
| `rating` | `Float64` | 4,424 (26.0%) |  |
| `yellow_cards` | `Float64` | 4,185 (24.6%) |  |
| `red_cards` | `Float64` | 4,185 (24.6%) |  |
| `np_xg` | `Float64` | 10,587 (62.3%) | Non-penalty xG aggregated from shots.situation. |
| `set_piece_xg` | `Float64` | 10,587 (62.3%) | Shot-model xG on set-piece situations. |
| `open_play_xg` | `Float64` | 10,587 (62.3%) | Shot-model xG on open-play situations. |
| `penalty_shots` | `UInt32` | 10,587 (62.3%) |  |
| `own_goals` | `Float64` | 1,252 (7.4%) |  |
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `corners` | `String` | 17,001 (100.0%) |  |
| `fpl_points` | `Float64` | 1,252 (7.4%) | FPL gameweek points attached for convenience. Authoritative series is player_gw. Do not sum on DGW rows. |
| `bonus` | `Float64` | 1,252 (7.4%) |  |
| `bps` | `Float64` | 1,252 (7.4%) |  |
| `now_cost` | `Float64` | 1,252 (7.4%) | FPL price in £m as a decimal (e.g. 7.0). Do not divide by 10. |
| `selected_by_percent` | `Float64` | 1,252 (7.4%) |  |
| `form` | `Float64` | 1,252 (7.4%) |  |
| `penalties_order` | `String` | 15,387 (90.5%) |  |
| `direct_freekicks_order` | `String` | 15,326 (90.1%) |  |
| `corners_and_indirect_freekicks_order` | `String` | 14,800 (87.1%) |  |
| `status` | `String` | 1,252 (7.4%) |  |
| `gw_match_index` | `Int64` | 0 (0.0%) | 1-based index of this match within the player's GW. |
| `gw_match_count` | `UInt32` | 0 (0.0%) | Player-match rows for this player in the GW (all competitions). |
| `is_dgw` | `Boolean` | 0 (0.0%) | True when the player has 2+ Premier League matches in this GW. |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `player_gw`

Rows: **30,594**. Columns: **52**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `player_id` | `Int64` | 0 (0.0%) | Season-scoped FPL player id. Do not join across seasons. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `web_name` | `String` | 0 (0.0%) |  |
| `status` | `String` | 0 (0.0%) |  |
| `news` | `String` | 19,658 (64.3%) |  |
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
| `corners_and_indirect_freekicks_order` | `String` | 28,286 (92.5%) |  |
| `direct_freekicks_order` | `String` | 28,805 (94.2%) |  |
| `penalties_order` | `String` | 28,862 (94.3%) |  |
| `set_piece_threat` | `String` | 30,594 (100.0%) |  |
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

Rows: **1,879**. Columns: **115**.

| Column | Dtype | Nulls | Notes |
|---|---|---:|---|
| `season` | `String` | 0 (0.0%) | Season folder name (YYYY-YYYY). |
| `competition` | `String` | 0 (0.0%) | Tournament folder name. Dashboard filters; ingest keeps every competition. |
| `gw` | `Int64` | 0 (0.0%) | FPL gameweek from the GW folder number (includes 0 for pre-season). |
| `match_id` | `String` | 0 (0.0%) | Stable match identifier from the source repo. |
| `team_code` | `Int64` | 0 (0.0%) | Stable club code (teams.code), not season id. |
| `opponent_code` | `Int64` | 291 (15.5%) | Opponent club code. |
| `is_home` | `Boolean` | 0 (0.0%) | True if the row's team/player is the home side. |
| `finished` | `Boolean` | 0 (0.0%) |  |
| `goals_for` | `Float64` | 805 (42.8%) |  |
| `goals_against` | `Float64` | 805 (42.8%) |  |
| `elo` | `Float64` | 971 (51.7%) |  |
| `possession` | `Float64` | 885 (47.1%) |  |
| `xg` | `Float64` | 886 (47.2%) | Opta/match-layer expected goals. Distinct from FPL expected_goals and shot-model xG. |
| `np_xg` | `Float64` | 920 (49.0%) | Non-penalty xG aggregated from shots.situation. |
| `xg_open_play` | `String` | 914 (48.6%) |  |
| `xg_set_play` | `String` | 914 (48.6%) |  |
| `xgot` | `Float64` | 914 (48.6%) |  |
| `total_shots` | `String` | 879 (46.8%) |  |
| `shots_on_target` | `String` | 879 (46.8%) |  |
| `shots_inside_box` | `String` | 880 (46.8%) |  |
| `shots_outside_box` | `String` | 880 (46.8%) |  |
| `big_chances` | `String` | 880 (46.8%) |  |
| `big_chances_missed` | `String` | 880 (46.8%) |  |
| `touches_in_opposition_box` | `String` | 880 (46.8%) |  |
| `corners` | `String` | 879 (46.8%) |  |
| `accurate_passes` | `String` | 880 (46.8%) |  |
| `accurate_passes_pct` | `String` | 880 (46.8%) |  |
| `accurate_long_balls` | `String` | 880 (46.8%) |  |
| `accurate_long_balls_pct` | `String` | 880 (46.8%) |  |
| `accurate_crosses` | `String` | 880 (46.8%) |  |
| `accurate_crosses_pct` | `String` | 880 (46.8%) |  |
| `tackles_won` | `String` | 889 (47.3%) |  |
| `tackles_won_pct` | `String` | 968 (51.5%) |  |
| `interceptions` | `String` | 880 (46.8%) |  |
| `blocks` | `String` | 884 (47.0%) |  |
| `clearances` | `String` | 880 (46.8%) |  |
| `duels_won` | `String` | 884 (47.0%) |  |
| `aerial_duels_won` | `String` | 880 (46.8%) |  |
| `aerial_duels_won_pct` | `String` | 880 (46.8%) |  |
| `ground_duels_won` | `String` | 880 (46.8%) |  |
| `ground_duels_won_pct` | `String` | 881 (46.9%) |  |
| `fouls_committed` | `String` | 880 (46.8%) |  |
| `offsides` | `String` | 880 (46.8%) |  |
| `yellow_cards` | `String` | 882 (46.9%) |  |
| `red_cards` | `String` | 883 (47.0%) |  |
| `keeper_saves` | `String` | 880 (46.8%) |  |
| `successful_dribbles` | `String` | 880 (46.8%) |  |
| `successful_dribbles_pct` | `String` | 880 (46.8%) |  |
| `possession_against` | `String` | 885 (47.1%) |  |
| `xga` | `Float64` | 886 (47.2%) | Expected goals against (opponent xG) on team_match. |
| `np_xg_against` | `String` | 920 (49.0%) |  |
| `xg_open_play_against` | `String` | 914 (48.6%) |  |
| `xg_set_play_against` | `String` | 914 (48.6%) |  |
| `xgot_against` | `String` | 914 (48.6%) |  |
| `shots_conceded` | `String` | 879 (46.8%) |  |
| `sot_conceded` | `String` | 879 (46.8%) |  |
| `shots_inside_box_against` | `String` | 880 (46.8%) |  |
| `shots_outside_box_against` | `String` | 880 (46.8%) |  |
| `big_chances_conceded` | `String` | 880 (46.8%) |  |
| `big_chances_missed_against` | `String` | 880 (46.8%) |  |
| `touches_in_opposition_box_against` | `String` | 880 (46.8%) |  |
| `corners_against` | `String` | 879 (46.8%) |  |
| `accurate_passes_against` | `String` | 880 (46.8%) |  |
| `accurate_passes_pct_against` | `String` | 880 (46.8%) |  |
| `accurate_long_balls_against` | `String` | 880 (46.8%) |  |
| `accurate_long_balls_pct_against` | `String` | 880 (46.8%) |  |
| `accurate_crosses_against` | `String` | 880 (46.8%) |  |
| `accurate_crosses_pct_against` | `String` | 880 (46.8%) |  |
| `tackles_won_against` | `String` | 889 (47.3%) |  |
| `tackles_won_pct_against` | `String` | 968 (51.5%) |  |
| `interceptions_against` | `String` | 880 (46.8%) |  |
| `blocks_against` | `String` | 884 (47.0%) |  |
| `clearances_against` | `String` | 880 (46.8%) |  |
| `duels_won_against` | `String` | 884 (47.0%) |  |
| `aerial_duels_won_against` | `String` | 880 (46.8%) |  |
| `aerial_duels_won_pct_against` | `String` | 880 (46.8%) |  |
| `ground_duels_won_against` | `String` | 880 (46.8%) |  |
| `ground_duels_won_pct_against` | `String` | 881 (46.9%) |  |
| `fouls_committed_against` | `String` | 880 (46.8%) |  |
| `offsides_against` | `String` | 880 (46.8%) |  |
| `yellow_cards_against` | `String` | 882 (46.9%) |  |
| `red_cards_against` | `String` | 883 (47.0%) |  |
| `keeper_saves_against` | `String` | 880 (46.8%) |  |
| `successful_dribbles_against` | `String` | 880 (46.8%) |  |
| `successful_dribbles_pct_against` | `String` | 880 (46.8%) |  |
| `kickoff_raw` | `String` | 44 (2.3%) |  |
| `tournament` | `String` | 0 (0.0%) |  |
| `kickoff_utc` | `String` | 44 (2.3%) |  |
| `result` | `String` | 805 (42.8%) |  |
| `points` | `Int64` | 805 (42.8%) |  |
| `clean_sheet` | `Boolean` | 805 (42.8%) |  |
| `venue` | `String` | 0 (0.0%) | H or A. |
| `travel_distance_km` | `String` | 1,783 (94.9%) |  |
| `weather_description` | `String` | 1,807 (96.2%) |  |
| `temperature_c` | `String` | 1,783 (94.9%) |  |
| `wind_speed` | `String` | 1,783 (94.9%) |  |
| `pitch_condition` | `String` | 1,783 (94.9%) |  |
| `is_local_derby` | `Boolean` | 1,005 (53.5%) |  |
| `is_neutral_ground` | `Boolean` | 1,005 (53.5%) |  |
| `lineup_status` | `String` | 1,005 (53.5%) |  |
| `strength` | `Float64` | 954 (50.8%) |  |
| `strength_overall_home` | `Float64` | 0 (0.0%) |  |
| `strength_overall_away` | `Float64` | 0 (0.0%) |  |
| `strength_attack_home` | `Float64` | 954 (50.8%) |  |
| `strength_attack_away` | `Float64` | 954 (50.8%) |  |
| `strength_defence_home` | `Float64` | 954 (50.8%) |  |
| `strength_defence_away` | `Float64` | 954 (50.8%) |  |
| `home_shot_model_xg` | `Float64` | 1,119 (59.6%) |  |
| `away_shot_model_xg` | `Float64` | 1,119 (59.6%) |  |
| `incident_timing_coverage` | `String` | 1,119 (59.6%) |  |
| `unlocated_card_count` | `Int64` | 1,119 (59.6%) |  |
| `quarantined_incident_count` | `Int64` | 1,119 (59.6%) |  |
| `source_commit` | `String` | 0 (0.0%) | Git SHA of olbauday/FPL-Core-Insights at ingest. |
| `ingested_at_utc` | `String` | 0 (0.0%) | UTC timestamp of this pipeline run. |
| `source_files` | `String` | 0 (0.0%) | Source files contributing to the row (truncated list). |

## `fixtures`

Rows: **377**. Columns: **12**.

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

