# Premier League FPL × Understat merge

Reusable identity layer and **Premier League player-match** table used by the live site serving build. FPL still owns player, team, GW, price, and Opta minutes. Understat metrics are attached as `us_*`. Do not blend minutes or xG.

Locked choices: [`decision_log.md`](./decision_log.md).

## Command

```bash
# Ingest Understat match roster (cached) + write maps + merged parquet
.venv/bin/python build_pl_merge.py
# or: make pl-merge

# Reuse existing master/understat/roster parquet
.venv/bin/python build_pl_merge.py --skip-roster

# Maps + review CSVs only
.venv/bin/python build_pl_merge.py --maps-only

# Re-fetch roster JSON
.venv/bin/python build_pl_merge.py --force-roster
```

First roster ingest hits understat.com once per finished EPL match (same cache as shots: `.cache/understat/match/<id>/roster.json`). Later runs revisit all finished matches but reuse cached JSON, so only newly finished matches hit the network.

## Layout

| Path | Role |
|---|---|
| `pipeline/pl_merge/` | Matcher + merge |
| `data/pl_merge/maps/match_map.csv` | Understat `match_id` → FPL `match_id` + `gw` |
| `data/pl_merge/maps/player_map.csv` | Understat `player_id` → FPL `player_code` |
| `data/pl_merge/maps/player_overrides.csv` | Your locked player pairs (always win) |
| `data/pl_merge/maps/match_overrides.csv` | Your locked match pairs (always win) |
| `data/pl_merge/review/` | Ambiguous / unmatched queues |
| `master/understat/roster/` | Understat player × match appearances |
| `master/pl_merge/player_match/` | FPL PL `player_match` + `us_*` columns; source for player site serving |

## Join keys

1. **Team** — existing [`data/understat/maps/team_map.csv`](../data/understat/maps/team_map.csv) (not fuzzy).
2. **Match** — season + kickoff calendar date + home/away `team_code`. Unique pair within ±1 day if the date is split by timezone. Remaining fixtures go to `review/match_unmatched.csv`.
3. **Player** — Understat `player_id` → FPL `player_code` (never season-scoped `player_id`). Auto-accept only unique exact / last+initial / RapidFuzz ≥ 95 on the same club. Everything else is review.
4. **Player-match** — left join on FPL `(match_id, player_code)`. Unmapped or unused Understat appearances leave `us_*` null.

## After a transfer window

1. Double-click `scripts/refresh.command` and choose 1 (recommended), or refresh FPL + Understat masters.
2. Run `build_pl_merge.py` if running commands individually (roster cache fills new matches only).
3. Open `data/pl_merge/review/player_unmatched_understat.csv` and `player_ambiguous.csv`.
4. Append accepted pairs to `player_overrides.csv` as `understat_player_id,player_code,reason`.
5. Re-run. Overrides persist; only new ids need review.

## Review files (your input)

| File | What to do |
|---|---|
| `review/player_ambiguous.csv` | Pick the correct `player_code`; add a row to `player_overrides.csv` |
| `review/player_unmatched_understat.csv` | Name/loan/spelling; override or leave unmapped |
| `review/player_unmatched_fpl.csv` | FPL PL minutes with no Understat id (often unused / data lag) |
| `review/match_unmatched.csv` | Add `match_overrides.csv` if the fixture exists on both sides |

This first run: **0 unmatched matches**, **0 ambiguous players**, **0 unmatched PL-minute players**. Five nickname/spelling pairs are locked in `player_overrides.csv` (Yarmoliuk, Pino, Igor Julio, Ouattara, Chema Andrés). Re-check those if a second player with the same surname arrives.

## Site connection

`build_serving.py` requires this merged table for `players_matches.json`. The player tables expose Understat roster metrics under the **Understat** metric group with `US` labels. US per-90 metrics use `us_minutes`; FPL/Opta rates use FPL `minutes`.

Understat shot serving also applies `player_map.csv` and uses FPL player names/codes and FPL/Opta Premier League minutes. Original Understat ids and names remain in JSON for traceability.
