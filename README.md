# FPL master datasets

Local **player-match**, **player-gw**, **team-match**, and **fixtures** masters built from the public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights) repo. No GitHub login or token is used.

The pipeline extracts **every competition** (Premier League, cups, Europe, Community Shield, Super Cup, friendlies / GW0) and tags each row with `competition`. The dashboard can filter later. `By Gameweek/` is never read, so matches are not double-counted.

## One-time setup

```bash
cd "/Users/supatil/Documents/Claude/Projects/FPL Data Cursor"
/opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Enable the Monday / Thursday schedule (08:00 local time):

```bash
./scripts/install_schedule.sh
```

## How to refresh

| When | Command |
|---|---|
| **Manual trigger** | `./scripts/refresh.sh` (in Terminal it asks: dataset, git push, or both) |
| Same, via Python | `.venv/bin/python build.py --refresh` |
| Finder | double-click `scripts/refresh.command` (same menu) |
| Scheduled (after install) | Monday and Thursday 08:00 **dataset only**, or `launchctl start com.fpl.masterdataset.refresh` |
| Ignore cache, rebuild all | `.venv/bin/python build.py --full` |
| Dashboard JSON only | `.venv/bin/python build.py --serving-only` |

`--refresh` is incremental: unchanged gameweek folders are reused. Source data is updated twice daily (07:30 and 17:30 UTC); twice a week is enough.

Change the clock by editing `scripts/install_schedule.sh` (`Hour` / `Minute`) and re-running it. Uninstall with `./scripts/uninstall_schedule.sh`.

Logs: `logs/pipeline.log`, `logs/refresh.log`, `logs/launchd.*.log`.

## Outputs

```
master/player_match/season=…/competition=…/part.parquet
master/player_gw/season=…/part.parquet
master/team_match/season=…/competition=…/part.parquet
master/fixtures/season=…/part.parquet
serving/*.json
manifest.json
docs/data_dictionary.md
```

`player_id` is season-scoped. Use `player_code` across seasons. Team joins use `team_code` (`teams.code`), not `teams.id`. `now_cost` is already in £m (do not divide by 10). Missing stats stay null.

FPL points are per gameweek. On a Double Gameweek, `player_match` repeats the GW points on each match row and sets `is_dgw` / `gw_match_count` so they are not summed twice. The clean FPL series is `player_gw` (Premier League only).

Seasons without a `By Tournament/` tree (currently `2024-2025`) are skipped and recorded in `manifest.json`.

## Dashboard

Static site in `web/`. After masters exist:

```bash
.venv/bin/python build_serving.py
.venv/bin/python serve.py          # http://127.0.0.1:8765/
```

Presentation edits never rebuild Parquet. Netlify publish directory is `web/` (JSON is copied to `web/data/`). See `docs/dashboard_readme.md`.

### Roll back the last UI versions

```bash
git log --oneline -5
git checkout c98e1a5 -- web          # previous snapshot (material sidebar)
git checkout HEAD -- web             # undo a checkout, if needed
```

Keep the last two dashboard commits. Ask before going further back.

## Tests

```bash
.venv/bin/python -m pytest -q
```
