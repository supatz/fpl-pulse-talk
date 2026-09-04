# Understat pipeline (EPL)

Separate Understat masters joined to FPL `team_code` at serving time. Raw API JSON is cached under `.cache/understat/` so iteration does not re-scrape.

## Commands

```bash
# Full ingest (uses shot cache) + derive + serving + dictionary
.venv/bin/python build_understat.py

# Scheduled / manual refresh: re-pull fixture indexes + new match shots only
./scripts/refresh_understat.sh
# or: make understat-refresh

# Rebuild analytics/serving/dictionary only (no network)
.venv/bin/python build_understat.py --derive-only

# Force re-fetch everything from understat.com
.venv/bin/python build_understat.py --force
```

`./scripts/refresh.sh` / `refresh.command` now run FPL then Understat on the dataset path (including the Mon/Thu schedule). Use `./scripts/refresh_understat.sh` to refresh Understat alone.

## Layout

| Path | Role |
|---|---|
| `data/understat/maps/team_map.csv` | Curated Understat team_id → FPL `team_code` |
| `.cache/understat/**/*.json` | Reusable raw responses |
| `master/understat/match/` | Fixture index |
| `master/understat/shot/` | Atomic shot fact (+ situation, last_action, zone) |
| `master/understat/team_match_style/` | PPDA / deep / match xG per team-match |
| `master/understat/team_context_season/` | Season context incl. attackSpeed |
| `master/understat/league_player/` | Season player totals (xg_chain, …) |
| `master/understat/team_situation_*` | For / against / rolling situation |
| `master/understat/player_*_situation_*` | Player taker/creator by situation |
| `serving/us_team_situation.json` | Team pilot (FPL team_code keys) |
| `serving/us_player_situation.json` | Player samples (understat ids until map) |
| `docs/understat_data_dictionary.md` | Headers + grain + sample rows |

Reusable modules: `pipeline/understat/` (`client`, `cache`, `ingest`, `derive`, `serve`, `zones`, `maps`, `dictionary`, `last_action_groups`, `shot_treemap`).

## Shot treemap explore page (standalone)

```bash
.venv/bin/python build_understat.py --derive-only   # refreshes serving JSON
.venv/bin/python serve.py                           # http://127.0.0.1:8765/
# site: http://127.0.0.1:8765/index.html#insights-understat
# standalone: http://127.0.0.1:8765/understat-shots.html
```

Page: Insights → Understat (`web/index.html#insights-understat`) plus standalone `web/understat-shots.html`. Data: `serving/us_shot_treemap.json` (mirrored to `web/data/`).
