# FPL Pulse Talk

Static dashboard (`web/`) backed by a merged Premier League player-match table. FPL/Opta owns dimensions and default measures; Understat roster measures stay separately labeled `US` / `us_*`. Locked choices: [`docs/decision_log.md`](docs/decision_log.md). Doc index: [`docs/README.md`](docs/README.md).

## Datasets

| Dataset | Source | Powers |
|---|---|---|
| **FPL-Core** | Public [`olbauday/FPL-Core-Insights`](https://github.com/olbauday/FPL-Core-Insights) (cached under `.cache/FPL-Core-Insights/data/`) | Dimensions, FPL/Opta metrics, fixtures, teams |
| **Understat** | understat.com → `master/understat/` | `US …` metrics on player pages plus Insights → Understat |
| **PL merge** | FPL PL `player_match` left-joined to Understat roster via curated maps | Player pages and player insights. [`docs/pl_merge.md`](docs/pl_merge.md) |

The merge table keeps FPL `minutes` and adds `us_minutes`; the site never silently substitutes one for the other.
For overlapping player metrics, the UI displays FPL-Core. Understat-only xGChain/xGBuildup remain available. Insights also includes a separate FPL-Core player treemap.

## FPL-Core masters

Local **player-match**, **player-gw**, **team-match**, and **fixtures** masters. No GitHub login or token is used.

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
| **Manual trigger** | `./scripts/refresh.sh` (Terminal menu: dataset, git push, or both) |
| Finder | double-click `scripts/refresh.command` — menu: 1 dataset, 2 git push, 3 both (3 refreshes then publishes to Netlify) |
| Non-interactive | `./scripts/refresh.sh --dataset` |
| Scheduled (after install) | Monday and Thursday 08:00 **dataset only**, or `launchctl start com.fpl.masterdataset.refresh` |
| Ignore cache, rebuild all | `.venv/bin/python build.py --full` |
| Dashboard JSON only | `.venv/bin/python build.py --serving-only` |
| PL merge (maps + player-match parquet) | `.venv/bin/python build_pl_merge.py` |

`--refresh` is incremental: unchanged gameweek folders are reused. Source data is updated twice daily (07:30 and 17:30 UTC); twice a week is enough.

Change the clock by editing `scripts/install_schedule.sh` (`Hour` / `Minute`) and re-running it. Uninstall with `./scripts/uninstall_schedule.sh`.

Logs: `logs/pipeline.log`, `logs/refresh.log`, `logs/launchd.*.log`.

## Local vs cloud

The refresh pipeline runs locally on this Mac. No cloud compute is required for a personal project; double-click `scripts/refresh.command` and pick 1 for data only or 3 to refresh and push the result live. Netlify is only the third-party host for the generated static `web/` files.

Move refresh compute to a service such as GitHub Actions only if it must run while the Mac is off. That would execute on the provider's servers, not a “local cloud,” and requires storing any deployment credentials there.

## Outputs

```
master/player_match/season=…/competition=…/part.parquet
master/pl_merge/player_match/season=…/part.parquet
master/understat/roster/season=…/part.parquet
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
.venv/bin/python build_pl_merge.py
.venv/bin/python build_serving.py                    # merged player JSON + FPL team/fixture JSON
.venv/bin/python build_understat.py --serving-only   # mapped Understat JSON + player shot mixes
.venv/bin/python serve.py          # http://127.0.0.1:8765/ (or --port N; scripts/serve.command works from Finder)
```

Presentation edits never rebuild Parquet. Netlify publish directory is `web/` (JSON is copied to `web/data/`). See `docs/dashboard_readme.md`.

Attackers **npxG** is FPL-Core only: shot-joined non-penalty xG, or `xG − 0.79 × penalties_scored` when the shot `player_id` is blank.

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
