# FPL Pulse Talk — dashboard

Static multi-file site. Presentation lives in `web/`. Data lives in `serving/*.json` (copied to `web/data/` for deploy).

**Decisions:** [`decision_log.md`](./decision_log.md).

## Datasets on the site

| Pages | JSON | Source |
|---|---|---|
| Home, Fixtures, Attackers, Defenders, GK, Teams, Insights Players / Matches / Teams | `players.json`, `players_matches.json`, `teams.json`, `meta.json`, … | FPL-Core |
| Insights → Understat (`#insights-understat`) | `us_shot_treemap.json`, `us_team_situation.json`, `us_player_situation.json` | Understat only |

Do not join FPL player minutes onto Understat tiles. There is no `player_map`.

## Local

```bash
.venv/bin/python build_serving.py              # FPL masters → JSON; does not rebuild Parquet
.venv/bin/python build_understat.py --serving-only
.venv/bin/python serve.py                      # http://127.0.0.1:8765/
```

Do **not** open `web/index.html` via `file://` — `fetch` of JSON is blocked in most browsers.

Hard-refresh after serving-shape changes. Understat JS/CSS/JSON use `?v=` cache busts (`web/index.html`, `DATA_URL` in `web/understat-shots.js`).

## Pages

| Route | Notes |
|---|---|
| `#home` | Jumps into the rest of the site |
| `#fixtures` | Current GW cards + ticker |
| `#attackers` / `#defenders` / `#gk` / `#teams` | FPL-Core tables. Attackers **npxG**: shot join, else `xG − 0.79 × penalties_scored` |
| `#insights-players` / `#insights-matches` / `#insights-teams` | FPL-Core insight boards |
| `#insights-understat` | Player treemap + situation / last-action / against. Player drawer = that player’s shot mix; Against is team-only |

Standalone Understat: `web/understat-shots.html`.

## What to edit for common tweaks

| Change | File | Cost |
|---|---|---|
| Rename a metric / tooltip / column order | `web/registry.js` | 🟢 |
| Look and feel (incl. global accent green) | `web/styles.css` | 🟢 |
| Table behaviour | `web/components.js` `makeTable` | 🟢 |
| New view wiring | `web/app.js` + a `VIEWS` entry | 🟢 |
| Understat explore UI | `web/understat-shots.js` / `.css` | 🟢 |
| New FPL precomputed field | `build_serving.py` | 🟠 |
| Understat player/team splits | `pipeline/understat/shot_treemap.py` then `--serving-only` | 🟠 |
| Rebuild Parquet masters | `build.py --refresh` / `build_understat.py --refresh` | 🔴 |

Filters and sort are stored in `localStorage` key `fplpulse.v1`.

Hover any italic **i** to see `page.section.element`. Click to copy. Names: [`element_registry.md`](./element_registry.md).
