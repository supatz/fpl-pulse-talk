# FPL Pulse Talk — dashboard

Static multi-file site. Presentation lives in `web/`. Data lives in `serving/*.json` (copied to `web/data/` for deploy).

**Decisions:** [`decision_log.md`](./decision_log.md).

## Datasets on the site

| Pages | JSON | Source |
|---|---|---|
| Home, Fixtures, Teams | `fixtures.json`, `teams_gw.json`, `meta.json`, … | FPL-Core (Premier League only on site) |
| Attackers, Defenders, GK, Insights Players / Matches | `players_matches.json` | PL merge: FPL-Core metrics plus Understat-only xGChain/xGBuildup |
| Insights → FPL treemap (`#insights-fpl-treemap`), Player performances (`#insights-player-performance`) | `players_matches.json` | FPL-Core player-match only |
| Insights → Understat (`#insights-understat`) | `us_shot_treemap.json`, `us_team_situation.json`, `us_player_situation.json` | Understat metrics with FPL team/player identity |

When the same metric exists in both providers, the site displays FPL-Core. Duplicate US minutes/xG/xA/npxG/shots/key passes remain in parquet/JSON for audit but are hidden. Understat-only xGChain/xGBuildup stay available.

## Local

```bash
.venv/bin/python build_pl_merge.py              # maps + merged PL player-match
.venv/bin/python build_serving.py               # merged player table → JSON
.venv/bin/python build_understat.py --serving-only
.venv/bin/python serve.py                      # http://127.0.0.1:8765/
.venv/bin/python serve.py --port 8770          # any other port
```

Or double-click `scripts/serve.command` (optional port argument); it keeps serving until the Terminal window is closed. The server has no persistent port setting — without `--port` it always comes back on 8765.

To refresh data and put it live, double-click `scripts/refresh.command` and choose 3 (refresh, then commit and push for Netlify). Choose 1 for data only, 2 to publish without refreshing.

Do **not** open `web/index.html` via `file://` — `fetch` of JSON is blocked in most browsers.

Hard-refresh after serving-shape changes. Understat JS/CSS/JSON use `?v=` cache busts (`web/index.html`, `DATA_URL` in `web/understat-shots.js`).

## Pages

| Route | Notes |
|---|---|
| `#home` | Jumps into the rest of the site |
| `#fixtures` | Current GW cards + ticker |
| `#attackers` / `#defenders` / `#gk` | Merged PL player-match. Click a player name for a gameweek drawer of the visible metrics (Total + Per 90). Metric-group buttons stay visible; Understat-only adds xGChain/xGBuildup |
| `#teams` | FPL-Core team-match |
| `#insights-players` / `#insights-matches` | Merged player-match; `#insights-teams` remains FPL team-match |
| `#insights-understat` | Player treemap + situation / last-action / against. Player drawer = that player’s shot mix; Against is team-only |
| `#home` | Match Insights, Player Insights, and Team Insights boards (moved from former Insights nav pages) |
| `#insights-fpl-treemap` | Nested player treemap: Top 10 / All / custom teams; All / MID / ATT / DEF + GK; Per 90 + 45+ mins. Size / sort includes BCC/BCT; Big chances metric group. Tiles show metric-pair lines plus the selected Size / sort value. Top six positive players per team; tooltip only, no drawer. Club colours from `web/team-colors.js` |
| `#insights-player-performance` | Free X / Y / bubble / sort (incl. GC, xGC, BCC…); sort asc/desc; top 10–40; kit-colour bubbles sized to the on-chart pool; optional trend line; exclude / season / position / GW / Per 90 / 45+. GC/xGC filled in serving from FPL player_gw (outfield Opta match GC is blank). |
| `#insights-finishing` | SoT% vs shots/90 scatter (top N by total shots). Bubble = xG/90, colour = club; 2-col tooltip (incl. G/xG). |
| `#insights-team-sides` | Table cells `value (%)`; sort by value or %. Dual vertical pitches (attack ↑ / concede ↓) with dropdowns above each, L/C/R band stats, six-yard boxes, circles sized by xG; centre Opta spider (xG/CC/BCC/SoT/xG-A/CC-A/BC-A/SoT-A) with ChartExport on table, spider, and pitches. Data: `us_team_side_channels.json` + `teams_gw.json`. |
| `#insights-fixture-proof` | Dumbbell: npG+A/90 or npxG+xA/90 vs live-season top 5 · rest · bottom 5. Top N by separate rank metric (xG/xGI/…). Position multi-select; exclude/add players. |
| `#gw-review` | Single-GW FPL social snapshot. Season + GW select. Four cards (Snapshot / Attack / Defence / Points XI pitch) each with Download for X. Attack pairs top-8 tables (xGI\|Goals, CC\|Assists). Defence: DEF+GK\|DefCon. Pitch XI: pts + ownership % + haul badges. Formation dynamic (DEF 3–5, MID 2–5, FWD 1–3). |
| `#teams` | Club table with `-A` against metrics; click team → GW drawer with opponent |

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
| FPL player treemap | `web/fpl-treemap.js` (uses existing `players_matches.json`) | 🟢 |
| Player performances scatter | `web/player-performance.js` (uses existing `players_matches.json`) | 🟢 |
| Understat player/team splits | `pipeline/understat/shot_treemap.py` then `--serving-only` | 🟠 |
| Rebuild Parquet masters | `build.py --refresh` / `build_understat.py --refresh` | 🔴 |

Filters and sort are stored in `localStorage` key `fplpulse.v1`.

Hover any italic **i** to see `page.section.element`. Click to copy. Names: [`element_registry.md`](./element_registry.md).
