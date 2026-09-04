# FPL Pulse Talk — decision log

Living record of **locked product and data decisions**. Update this file in the **same change** as the code or serving JSON that implements the decision. Newest entries at the top of the chronological list.

Related docs: [README](../README.md) · [dashboard](./dashboard_readme.md) · [FPL dictionary](./data_dictionary.md) · [Understat pipeline](./understat_pipeline.md) · [Understat plan](./understat_dataset_plan.md)

## How to add an entry

1. Add a row to **Locked now** if the choice is still in force (or replace the old row).
2. Add a dated block under **Chronology** (`YYYY-MM-DD`, newest first).
3. State the **choice**, **why**, and **where it lives** (path or page). Note drawbacks when the choice is a compromise.
4. Commit and push with the implementing files so a laptop loss does not drop the record.

## Locked now

| Topic | Choice |
|---|---|
| Two datasets | **FPL-Core** and **Understat** stay separate. Do not join player minutes or mix metrics across them on Attackers / other FPL pages. |
| Site dimensions | FPL owns player, team, price, minutes on FPL pages. Understat pages use Understat ids and `league_player.time` until a curated `player_map` exists. |
| Team identity | Understat teams join FPL `team_code` via `data/understat/maps/team_map.csv` only (no fuzzy team match). |
| Player map | **Not built.** No FPL ↔ Understat player join. |
| Insights → Understat | Same shell as other Insights pages (`#insights-understat`). Standalone `web/understat-shots.html` remains. |
| Understat CSS | Scoped under `.us-shots`. Site-wide accent green (`#3ddc97`) lives in `web/styles.css`. |
| Refresh | `scripts/refresh.sh` / schedule: FPL dataset then Understat. D3 is vendored at `web/vendor/d3.min.js`. |
| Attackers npxG | FPL-Core only. Prefer shot-joined `np_xg`; else `xG − 0.79 × penalties_scored` (`PENALTY_XG` in `build_serving.py`). Does not fix SPxG. |
| Understat Top / Bottom 10 | Rank **selected season + selected metric** (and Per 90). Against = bottom 10 by that metric **conceded**. Changing metric resets the preset unless “All teams”. |
| 45+ mins (Understat) | Filter on Understat `league_player.time` as minutes. Not FPL minutes. |
| Player drawer | Situation + last-action mixes are **that player’s shots**. Against (conceded) is team-only and hidden on a player drawer. |
| Understat player playing time | `matches` = Understat `games` when present, else unique shot `match_id`s. `avg mins/90` = `minutes / matches` (average minutes per appearance). |
| Treemap tooltip | Column grid. First row: matches + avg mins/90. No “% of shown teams”. Do not repeat the selected metric in the volume row. |
| Asset cache | Bump `?v=` on `understat-shots.js/css` and `us_shot_treemap.json` when serving shape or UI changes. |
| `now_cost` | Already £m. Do not divide by 10. |
| FPL points | Authoritative on `player_gw`. `player_match` can repeat GW points on DGW rows (`is_dgw`). |
| UI rollback | Keep the last two dashboard commits. Ask before going further back. |

## Chronology

### 2026-09-05 — Player drawer mixes + readable tooltip

**Choice:** Ship per-player `by_situation` / `by_last_action_group` in `us_shot_treemap.json`. The drawer and tooltip resolve the player from serving data (id, then name), not the slim treemap leaf. Tooltip is a labeled column grid; cache-bust JSON (`?v=10`).

**Why:** Clicking a player showed the team mix (or empty mixes after the JS switch) and blank matches, because player splits were missing or the browser kept an old JSON.

**Where:** `pipeline/understat/shot_treemap.py`, `web/understat-shots.js`, `web/understat-shots.css`.

### 2026-09-04 — Understat explore in Insights

**Choice:** Wire Understat into `#insights-understat` like Players / Matches / Teams. Scope Understat CSS. Raise Insights submenu `max-height` so Understat is not hidden under Collapse. Vendor D3. Run Understat on the same Mon/Thu refresh as FPL.

**Why:** One site, two sources; Understat styles must not leak. Nav must show every Insights link.

**Where:** `web/index.html`, `web/app.js`, `web/styles.css`, `scripts/refresh.sh`, `web/vendor/d3.min.js`.

### 2026-09-04 — Attackers npxG fallback (FPL-Core)

**Choice:** If shot `np_xg` is null and match `xG` exists, serving uses `xG − 0.79 × penalties_scored`. Shot-joined rows stay as-is.

**Why:** Many 2026–27 FPL-Core shots have a blank `player_id`, so the shot join misses (e.g. B.Fernandes GW2). User accepted a typical penalty xG of 0.79.

**Drawbacks:** 0.79 is typical, not the actual penalty xG. Missed pens with a blank shot id can inflate npxG. SPxG is unchanged.

**Where:** `build_serving.py` (`PENALTY_XG`), Attackers column `npxG` in `web/registry.js`.

### 2026-09-04 — Understat ranking, 45+ mins, treemap type

**Choice:** Top/Bottom 10 follow the selected metric (Against = conceded). 45+ mins uses Understat minutes only. Team treemap labels bold; player labels Helvetica Neue / weight 500.

**Where:** `web/understat-shots.js`, `web/understat-shots.css`.

### 2026-08 — Site + FPL-Core pipeline (already shipped)

**Choice:** Static Netlify site (`web/`). Masters from public `olbauday/FPL-Core-Insights`. Ingest every competition; filter in the UI. Serving JSON copied to `web/data/`. Presentation edits do not rebuild Parquet.

**Where:** `build.py`, `build_serving.py`, `web/`, `docs/data_dictionary.md`.
