# SofaScore pipeline (Premier League)

Parallel to Understat. Does **not** write Understat caches, PL-merge maps, or `us_*` serving JSON. Site labels are **SofaScore** / `SS` / `*_sf`. Never average or fill from Understat or Opta.

Decisions: [`decision_log.md`](./decision_log.md). Dictionary stub: [`sofascore_data_dictionary.md`](./sofascore_data_dictionary.md).

## Commands

```bash
.venv/bin/python build_sofascore.py --refresh
.venv/bin/python build_sofascore.py --ingest-only --refresh
.venv/bin/python build_sofascore.py --serving-only
.venv/bin/python build_sofascore.py --maps-only   # identity maps + mapping worksheet; no live API
.venv/bin/python build_sofascore.py --force   # bypass JSON caches
```

After filling `player_code` on the mapping worksheet, run `--maps-only` then `.venv/bin/python build_serving.py` so `BCC_sf` / `BCM_sf` attach.

`scripts/refresh.sh` runs SofaScore **after** FPL serving. If SofaScore fails, FPL + Understat serving still complete.

Python `urllib` against `api.sofascore.com` / `www.sofascore.com/api` often returns **403**. Ingest reuses `.cache/sofascore` (and keeps existing masters). A browser session on sofascore.com can populate that cache. Season ids: 2025-2026 = `76986`, 2026-2027 = `96668`.

## Layout

| Path | Role |
|---|---|
| `data/sofascore/maps/team_map.csv` | SofaScore `team_id` → FPL `team_code` (hand-maintained; name fill for new clubs) |
| `data/sofascore/maps/match_map.csv` | `event_id` → FPL `match_id` + `gw` (kickoff ±1 day + home/away codes) |
| `data/sofascore/maps/player_map.csv` | `player_id` → FPL `player_code` |
| `data/sofascore/maps/*_overrides.csv` | Manual wins |
| `data/sofascore/review/` | Unmapped / ambiguous queues |
| `data/sofascore/review/player_mapping_worksheet.csv` | One row per unmapped/ambiguous SofaScore player: SS / FPL / Understat ids. Fill `player_code` then `--maps-only` |
| `.cache/sofascore/` | Raw unofficial `api.sofascore.com` JSON |
| `master/sofascore/event|shot|player_match/` | Parquet partitions |
| `serving/ss_shot_treemap.json` | Insights → SofaScore treemap / situation |
| `serving/ss_team_timing.json` | Match clock |
| `serving/ss_team_side_channels.json` | SofaScore sides |

## Pages

| Route | Data | Notes |
|---|---|---|
| `#insights-sofascore` | `ss_shot_treemap.json`, `ss_team_timing.json` | Treemap, situation, against (situation only), timing. No last-action / tempo. |
| `#insights-sofascore-sides` | `ss_team_side_channels.json` | Table + dual pitch. Spider remains Opta. |

Player tables: optional group **SofaScore only** (`BCC_sf`, `BCM_sf`, `SiB_sf`). Values are native SofaScore lineup big chances after `player_code` map. Null only when that player is still unmapped — never filled with 0. Unmapped shooters still appear on SofaScore treemap (SofaScore name; minutes from lineups). No `BCS_sf` / `BCT_sf` (SofaScore does not publish scored or taken).

## Identity and honesty

- Big chances on SofaScore views are native `bigChancesCreated` / `bigChancesMissed`. Not rebuilt from xG > 0.27. Unfinished postponed listings are not match-mapped when a finished twin exists.
- Situation labels stay SofaScore (`regular`, `assisted`, `fast-break`, `corner`, `set-piece`, `free-kick`, `throw-in-set-piece`, `penalty`).
- Shot xG is SofaScore; player per-90 minutes prefer FPL/Opta PL minutes after `player_code` map, else SofaScore lineup minutes so unmapped players are not dropped.
- Pitch: SofaScore `x` is % from the attacked goal; serving uses `x' = 1 − x/100` so attack plots toward the top. High Y = Left.
