# FPL Pulse Talk — decision log

Living record of **locked product and data decisions**. Update this file in the **same change** as the code or serving JSON that implements the decision. Newest entries at the top of the chronological list.

Related docs: [README](../README.md) · [dashboard](./dashboard_readme.md) · [FPL dictionary](./data_dictionary.md) · [Understat pipeline](./understat_pipeline.md) · [PL merge](./pl_merge.md) · [Understat plan](./understat_dataset_plan.md)

## How to add an entry

1. Add a row to **Locked now** if the choice is still in force (or replace the old row).
2. Add a dated block under **Chronology** (`YYYY-MM-DD`, newest first).
3. State the **choice**, **why**, and **where it lives** (path or page). Note drawbacks when the choice is a compromise.
4. Commit and push with the implementing files so a laptop loss does not drop the record.

## Locked now

| Topic | Choice |
|---|---|
| Merged site | Player pages read Premier League `master/pl_merge/player_match`. FPL/Opta and Understat measures remain separately labeled; never average or silently coalesce them. |
| Metric precedence | When FPL-Core has the same player metric, the site shows FPL-Core only. Hide duplicate US minutes/xG/xA/npxG/shots/key passes; retain Understat-only xGChain/xGBuildup, BCC/BCT/BCS/BCM (xG > 0.27), and Understat-native insight views. |
| Big chance (US) | Shots with `xg > 0.27`. **BCT** = taken (shooter); **BCS** = scored; **BCM** = missed (`BCT = BCS + BCM`); **BCC** = created (`player_assisted`, name→id). Match-level `us_*` → site `BCC`/`BCT`/`BCS`/`BCM`. Site **BCM** is Understat (not Opta `big_chances_missed`, kept as `BCM_opta`). Creativity = BCC; Threat = BCT/BCS/BCM. Per-90 uses Understat minutes. |
| Site dimensions | FPL owns player identity, team, position, price, GW, and default minutes. Understat player views use curated FPL `player_code` / names; Understat metrics carry `US` / `us_*` labels. |
| Team identity | Understat teams join FPL `team_code` via `data/understat/maps/team_map.csv` only (no fuzzy team match). |
| PL merge | Premier League-only identity maps + `master/pl_merge/player_match` in `pipeline/pl_merge/`. This is the player-match source for site serving. |
| Player map | Curated under `data/pl_merge/maps/player_map.csv`. Fuzzy is a proposal; overrides win. Do not join on season-scoped FPL `player_id`. |
| Insights → Understat | Same shell (`#insights-understat`). Match timing = shots × FPL GW. Attack tempo = season `attackSpeed` ribbons (`us_team_attack_speed.json`). Standalone `web/understat-shots.html` remains. |
| FPL treemap | Separate `#insights-fpl-treemap`. Club/player area follow Size / sort. Metric groups include Big chances (BCT · BCS · BCM). Tiles show the metric-pair lines **and** the selected Size / sort value when it is not already in the pair. BCC/BCT/BCS/BCM available under every metric’s sort list. No drawer. Shares `web/team-colors.js`. |
| Player performances | `#insights-player-performance`. Free X / Y / bubble / sort metrics (G, xG, A, xA, GI, xGI, DC, CS, xGOT, CC, npxG, Sh, SoT, TiB, BCC, BCT, BCS, BCM). Top 10–40 by sort metric. Exclude multi-search. Season / position / GW / Per 90 / 45+ kept. Axes auto-scale; bubble size stays on raw totals under Per 90. |
| Sidebar | Children of a nav parent are indented with a left guide rule (`.nav-kids`). Collapsed rail still hides them entirely. |
| Local preview | `scripts/serve.command` (double-click) or `.venv/bin/python serve.py --port N`. Port defaults to 8765; `serve.py` has no persistent port setting. |
| DefCon | `defcon` prefers upstream match-level `defensive_contributions`; when blank (2026-27 on) it derives CBIT for defenders, CBIT + recoveries for MID/FWD, and 0 for GK, using `coalesce(tackles, tackles_won)`. Derivation reproduces FPL gameweek totals exactly. |
| Branding | Mark is option-A mint cartoon vintage mic + white ECG pulse + teal ring (animated in sidebar). Same mark in chart-export footer, `web/assets/fpl-pulse-mark.svg`, and square `web/assets/fpl-pulse-logo.png` (favicon). X still links to `https://x.com/fpl_pulse_talk`. |
| Home hub | Match / Player / Team insight boards live on Home (not separate Insights nav pages). Legacy `#insights-players|matches|teams` hashes redirect to Home. |
| Team metrics (-A) | Teams table against metrics use short + `-A` (`G-A`, `xG-A`, `Sh-A`, `SoT-A`, `CC-A`, `BCC-A`). BCC/BCC-A = Opta team big chances for/conceded; CC = sum of player chances_created; CC-A = opponent CC. |
| Shot sides | `#insights-team-sides` uses Understat Y thirds (low=Right, mid=Center, high=Left) for shots for/against. Serving: `us_team_side_channels.json` (aggregates + per-shot `points` with shooter/assister). Table cells show `value (%)`; sort mode Value vs %. Dual pitch: vertical (attack ↑ / concede ↓), team dropdowns above each pitch, L/C/R band stats near centre (attack blue / defend red), circle size = Understat xG. Assister xA on a shot = that shot’s xG. |
| Finishing | Bubble fill = club colour. Per 90 (default on): X = Sh/90, bubble = xG/90; off: X = Sh, bubble = xG. Y = SoT% always. Axes auto-scale to cohort. |
| Fixture Proof | `#insights-fixture-proof`. Live PL table in GW window: Top 5 by G or xG; Bottom 5 by GC or xGC among the rest (disjoint). Chart metric npG+A/90 or npxG+xA/90. Top N by separate rank metric. Position multi-select. Optional sample filter: ≥45 mins/app and ≥30% of that team’s PL matches in the GW window. Dots: top green · rest open · bottom red; connector yellow. |
| GW Review | Top-level `#gw-review`. Season + GW filters. Four social cards (Snapshot, Attack, Defence, Points XI), each with ChartExport download. Snapshot KPI order: Goals → Team CS → 10+ pts Haul → Top haul → Best xGI (goals & team CS show Δ vs prior GW). Snapshot also pairs Points leaders \| compact Team of the Week pitch. Attack pairs (top 8): xGI\|Goals, CC\|BCC\|Assists, Over\|Under. Defence: DEF+GK\|DefCon (top 8). Points XI card keeps full pitch. PL-only; DGW rows summed. |
| Players table drawer | Clicking a name on Attackers / Defenders / GK opens a side drawer of that player’s gameweeks for the **currently visible** metric columns, plus Total and Per 90 footer rows. Points/CS are one figure per GW. |
| Metric controls | Metric-group chips are always visible; there is no redundant “More metrics” toggle. |
| Understat CSS | Scoped under `.us-shots`. Site-wide accent green (`#3ddc97`) lives in `web/styles.css`. |
| Refresh | `refresh.command` opens the menu: 1 dataset, 2 git push, 3 both. Dataset = FPL → Understat → PL merge/roster → both serving layers. Publish is `git add -A` + commit + push so Netlify redeploys. Non-tty runs (launchd) still fall through to dataset only. |
| Runtime / cloud | Keep data refresh local on the personal Mac. Cloud compute is optional only for unattended refresh while the Mac is off; Netlify remains the third-party static-site host. |
| Attackers npxG | FPL-Core only. Prefer shot-joined `np_xg`; else `xG − 0.79 × penalties_scored` (`PENALTY_XG` in `build_serving.py`). Does not fix SPxG. |
| Understat Top / Bottom 10 | Rank **selected season + selected metric** (and Per 90). Against = bottom 10 by that metric **conceded**. Changing metric resets the preset unless “All teams”. |
| 45+ mins (Understat) | Uses FPL/Opta Premier League minutes from the merged player-match table. |
| Player drawer | Situation + last-action mixes are **that player’s shots**. Against (conceded) is team-only and hidden on a player drawer. |
| Understat player playing time | Player per-90 and average minutes use FPL/Opta PL minutes/appearances from the merged table; shot metrics remain Understat. |
| Treemap tooltip | Column grid. First row: matches + avg mins/90. No “% of shown teams”. Do not repeat the selected metric in the volume row. |
| Asset cache | Bump `?v=` on `understat-shots.js/css`, `dual-range.js`, `chart-export.js`, `us_shot_treemap.json`, `us_team_timing.json`, and `us_team_attack_speed.json` when serving shape or UI changes. |
| Range filters | GW and price use one two-thumb slider (both ends movable). Price max/min follow live `meta.prices` (0.5 steps). |
| `now_cost` | Already £m. Do not divide by 10. |
| FPL points | Authoritative on `player_gw`. `player_match` can repeat GW points on DGW rows (`is_dgw`). |
| UI rollback | Keep the last two dashboard commits. Ask before going further back. |

## Chronology

### 2026-10-27 — Snapshot embeds compact Team of the Week

**Choice:** Snapshot card pairs Points leaders with a compact pitch (formation visual only — same XI as the dedicated card). Full Team of the Week card remains for social download.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review paired leader tables

**Choice:** Attack restores Goals beside xGI; Chances | Assists; Over | Under. Defence keeps DEF+GK | DefCon. Each pair uses a bold vertical rule; every paired table shows top 8. Split tables fill their half-width.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review compact tables + pitch badges

**Choice:** GW Review tables use content-width layout (metrics pack beside the player column, spare space on the right). Tighter row padding. Pitch XI adds the same haul badges (⚽/🅰️/🛡️/🧱) under pts · ownership %.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review goals Δ + pitch ownership

**Choice:** Goals KPI meta stays “across the PL”; delta vs prior GW sits in the value as coloured `(▲+N)` / `(▼-N)`. Pitch XI shows `pts · selected_by_%` from `players_gw` (joined on `player_id` = match `pid`), not bonus.

**Where:** `web/gw-review.js`, docs.

### 2026-10-27 — GW Review snapshot KPI refresh

**Choice:** Top haul / best xGI show attribute badges (goals ⚽×N, assists 🅰️, CS 🛡️, DefCon pts 🧱). Goals KPI includes vs prior GW delta (green/red). Assists + CS-assets KPIs replaced by team clean-sheet count from `teams_gw.clean_sheet` (distinct teams). Hauls label = “10+ pts Haul”. Table Player header size matches player name.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review attack board + dynamic XI

**Choice:** Attack card: xGI full-width, then Chances created (CC + US BCC) left of Assists; Goals removed from this card. Bold rules between metric blocks. Team of the week picks the max-points valid formation (1 GK, DEF 3–5, MID 2–5, FWD 1–3, always 11) from that GW’s top scorers by position.

**Why:** Creation board fits the attack story better than goals next to xGI; XI should flex with who actually hauled.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review layout polish + pitch XI

**Choice:** Snapshot KPIs use a 3-column grid with separate label/value/meta nodes (fixes merged text). Points leaders show Bonus, not BPS. Team of the week on a pitch (no bench). Light emoji on section labels for social posts.

**Why:** Linear left-column cards wasted space and labels collided with values; pitch XI matches the playing-11 share format.

**Where:** `web/{gw-review.js,styles.css,index.html}`, docs.

### 2026-10-27 — GW Review social snapshot page

**Choice:** New shell nav page `#gw-review` for a single-GW FPL glimpse. Four downloadable cards: Snapshot (KPIs + points leaders), Attack (xGI/G/A + over/under), Defence (pts/CS/DefCon), Points XI (by pts). Built for X/Twitter via existing ChartExport caption + brand strip.

**Why:** Weekly posting needs ready-made, segmented images rather than one overloaded graphic. Ownership omitted until serving includes it.

**Where:** `web/{gw-review,app,index,styles}.{js,html,css}`, docs.

### 2026-10-27 — Fixture Proof GW + sample filter

**Choice:** GW dual-range (like other insights). Checkbox (default on): keep players with ≥45 mins per appearance and apps ≥30% of their team’s finished PL matches in the GW window.

**Where:** `web/{fixture-proof.js,index.html}`.

### 2026-10-27 — Fixture Proof rank metric + position multi-select

**Choice:** Position is multi-select (MID / ATT / DEF+GK). Top N selection uses a separate “Top N by” filter (default xG/90), independent of the chart display metric (npG+A or npxG+xA /90).

**Where:** `web/{fixture-proof,index,styles}.{js,html,css}`.

### 2026-10-27 — Fixture Proof insight page

**Choice:** New Insights page comparing each player’s selected per-90 metric vs current-season top 5 / rest / bottom 5 opponents. Top 5 ranked by G or xG; bottom 5 by GC or xGC among remaining clubs. npG = G − PenG. Dumbbell: green / open / red dots, yellow connector. Top N by overall rate with exclude + pin.

**Where:** `web/{fixture-proof,app,index,styles}.{js,html,css}`, `docs/{decision_log,dashboard_readme}.md`.

### 2026-10-22 — Finishing Per 90 checkbox

**Choice:** Finishing gains a Per 90 filter (default on). On: X = Sh/90, bubble = xG/90. Off: X = Sh, bubble = xG. SoT% unchanged.

**Where:** `web/{finishing.js,index.html}`.

### 2026-10-22 — Pitch tip shooter/assist + finishing xG/90 bubble

**Choice:** Pitch tip shows shooter + xG and assister + xA (xA = shot xG when assisted) in a 2-col grid. Finishing bubble size = xG/90; tip adds G/xG in a 2-col grid.

**Where:** `pipeline/understat/side_channels.py`, `web/{finishing,team-sides,styles}.{js,css}`, serving `us_team_side_channels.json`.

### 2026-10-22 — Finishing autoscale + pitch label colours

**Choice:** Finishing scatter axes auto-scale to the filtered cohort (padded extent, not fixed 0–floor). Pitch compare stats sit near midfield; attack labels/circles blue, defend red.

**Where:** `web/{finishing,team-sides}.js`.

### 2026-10-22 — Team sides vertical pitch + value/% sort

**Choice:** Rotate pitch compare to vertical (attack ↑, concede ↓); place each team dropdown above its pitch; show `value (%)` on L/C/R bands (attack gold / concede red). Table cells show value (%); “Sort columns by” toggles value vs % for L/C/R headers.

**Where:** `web/{team-sides,index,styles}.{js,html,css}`, `docs/decision_log.md`.

### 2026-10-21 — Team sides pitch compare + finishing label/tooltip polish

**Choice:** Extend `us_team_side_channels.json` with per-shot `points` for pitch viz. Team sides table sorts on L/C/R and L-A/C-A/R-A click. Dual pitch UI under the table (two team dropdowns): green pitch with goals, L/C/R bands, attack (gold) at right / concede (red) at left, circle size by xG or equal. Finishing keeps club colours (documented in status); collision-aware short labels + cursor-following tooltip.

**Why:** User asked for sortable side columns, visual pitch compare, and readable finishing labels/tooltip; xGOT unavailable on Understat shots so size filter is xG/equal.

**Where:** `pipeline/understat/side_channels.py`, `web/{team-sides,finishing,index,styles}.{js,html,css}`, `docs/dashboard_readme.md`.

**Drawbacks:** Pitch size cannot offer true xGOT; against points duplicate each shot under the defending team.

### 2026-10-21 — Home hub, team -A metrics, finishing + shot sides

**Choice:** Move Match / Player / Team insight boards onto Home; remove those Insights nav links. Fix empty boards when persisted GW/filters don’t match the season. Teams table adds for/against metrics with `-A` suffix + GW drawer (opponent). Player drawer shows opponent. FPL treemap gains Per 90 + 45+ mins. New Insights: Finishing (SoT% vs Sh/90) and Team shot sides (L/C/R for & against). Chances-created side zones deferred pending coordinate proxy confirmation.

**Where:** `web/{index,app,components,registry,player-drawer,team-drawer,fpl-treemap,finishing,team-sides}.js`, `build_serving.py`, `pipeline/understat/{zones,side_channels,serve}.py`.

### 2026-10-15 — Brand mark: mint mic + pulse (option A)

**Choice:** Replace the green center dot with a cartoon vintage broadcast mic (mint fill, dark outlines, grille, U-yoke, base). Keep the teal ring and white ECG pulse (pulse draws behind the mic). Use that mark everywhere: sidebar SVG, chart PNG footer, favicon, and `web/assets/fpl-pulse-logo.png`.

**Why:** User locked concept A from the logo options (mic from stadium-mic refs, doodle style, brand green retained).

**Where:** `web/index.html`, `web/styles.css`, `web/chart-export.js`, `web/assets/fpl-pulse-mark.svg`, `web/assets/fpl-pulse-logo.png`.

### 2026-10-15 — Chart download caption header

**Choice:** PNG downloads for Understat, FPL treemap, and Player performances get a compact top banner: plain-English title, small metric glossary (`G = Goals · …`), and short filter meta (season / GW). Footer brand strip unchanged.

**Why:** Shared images need a quick read of what the chart shows without opening the site.

**Where:** `web/chart-export.js`, caption builders in `web/{fpl-treemap,player-performance,understat-shots}.js`.

### 2026-10-15 — Insight chart PNG download with brand strip

**Choice:** Add a small “Download chart” control under Understat, FPL treemap, and Player performances. Export is PNG of the visible chart plus a short footer stripe: pulse mark, “FPL PULSE TALK”, X mark, `@fpl_pulse_talk`.

**Where:** `web/chart-export.js`, page hosts in `web/index.html` / `understat-shots.html`, bind in the three chart scripts.

### 2026-10-15 — Dual-thumb GW/price ranges + dynamic cost ceiling

**Choice:** Replace paired From/To range inputs with one two-thumb slider (both ends movable) for GW and price filters site-wide. Price bounds come from live `meta.prices` (0.5 steps); migrate the old £15.0 hard max so Haaland (£15.6) stays visible.

**Where:** `web/dual-range.js`, `web/components.js`, `web/understat-shots.js`, `web/fpl-treemap.js`, `web/player-performance.js`, `web/styles.css`, `web/index.html`.

### 2026-10-15 — Understat BCS / BCM split + player performance axes

**Choice:** Split taken big chances into **BCS** (goal) and **BCM** (non-goal). Site `BCM` is now Understat-derived; Opta `big_chances_missed` serves as `BCM_opta` only. Add BCC/BCT/BCS/BCM to Player performances X/Y/bubble (and sort list). Treemap Big chances group shows BCT · BCS · BCM.

**Why:** Conversion of the same xG>0.27 chances needs scored vs missed, not only taken.

**Where:** `pipeline/pl_merge/merge.py`, `build_serving.py`, `web/registry.js`, `web/player-performance.js`, `web/fpl-treemap.js`.

### 2026-10-15 — Understat BCC / BCT + treemap sort on tiles

**Choice:** Derive match-level big chances from Understat shots (`xg > 0.27`): BCT for the shooter, BCC for `player_assisted`. Join onto `pl_merge/player_match`. Expose as `BCC` / `BCT` on Attackers / Defenders / GK (Creativity / Threat). FPL treemap adds Big chances metric group, BCC/BCT in every Size / sort list, and prints the selected sort metric on tiles.

**Why:** FPL publishes BCM but not player-level big chances created; Understat shot xG is the available definition. Tiles previously hid non-primary sort metrics (e.g. SoT).

**Where:** `pipeline/pl_merge/merge.py`, `build_serving.py`, `web/registry.js`, `web/components.js`, `web/fpl-treemap.js`, `web/index.html`.

**Drawbacks:** Assister id is name-matched within season; unmapped names drop BCC. Threshold is locked at 0.27 (strict >).

### 2026-10-13 — Player performances free axes

**Choice:** Drop Attack / Defence / Finishing tabs. User picks X, Y, bubble size and sort metric from a shared list (G, xG, A, xA, GI, xGI, DC, CS, xGOT, CC, npxG, Sh, SoT, TiB); top-N includes 10 and 15; typeable multi-exclude; axes auto-scale independently. Tooltip shows short names for the four selected metrics plus apps / mins / mins/app. Lede lists Goal threat / Creativity / Defence combinations.

**Why:** Pre-set scatters were too narrow; free axes cover threat, creativity and defence on one page.

**Where:** `web/player-performance.js`, `web/index.html`, `web/styles.css`.

**Drawbacks:** No parity line (axes are independent). Bubble size stays on raw totals under Per 90.

### 2026-09-30 — Player GW drawer, performance tabs, pulse mark

**Choice:** Player names on Attackers / Defenders / GK open a drawer of gameweek rows for the visible metrics, with Total and Per 90 at the foot. Player performances splits into Attack / Defence / Finishing. Sidebar logo is replaced by a beating pulse.

**Why:** GW detail belongs on the player row, not a separate page. Defence and finishing need their own scatters without cloning the filter bar. The pulse is the brand mark.

**Where:** `web/player-drawer.js`, `web/components.js`, `web/player-performance.js`, `web/index.html`, `web/styles.css`.

### 2026-09-20 — Position filters on both FPL insight charts

**Choice:** Add All / MID / ATT / DEF + GK filters to the FPL treemap and Player performances. DEF deliberately includes goalkeepers.

**Why:** The same metric has a different interpretation and useful comparison set by position; combining GK with DEF preserves a compact three-role filter.

**Where:** `web/index.html`, `web/fpl-treemap.js`, `web/player-performance.js`.

**Drawbacks:** On attacking metrics, DEF + GK can contain fewer than the requested number because players with both actual and expected values at zero are excluded.

### 2026-09-20 — Refresh menu restored on the Finder button

**Choice:** `refresh.command` runs `refresh.sh` with no flags again, so double-clicking shows the 1 dataset / 2 git push / 3 both menu. This reverses the 2026-09-15 prompt-free choice. Publish keeps `git add -A`.

**Why:** Publishing to Netlify is part of the routine, and reaching it only through Terminal was the wrong trade. One button that asks beats two buttons or a silent push.

**Where:** `scripts/refresh.command`, `scripts/refresh.sh` (unchanged; already handled all three modes).

**Drawbacks:** The refresh button is no longer one click — it always asks first. `git add -A` on publish commits every uncommitted change in the folder, including in-progress code edits; the commit-message prompt is the only gate.

### 2026-09-20 — Player performances top-N and volume tooltip

**Choice:** Default the scatter to the top 20 by the actual measure, with a Players filter for 30 and 40. Always show SoT and CC in the tooltip, independent of which metric sizes the bubble.

**Why:** Fifteen was too tight once bubbles and names were in play; 20 is readable, 30/40 are opt-in. Volume belongs in the hover even when it is not the bubble measure.

**Where:** `web/player-performance.js`, `web/index.html`.

**Drawbacks:** Top 40 still crowds names; hover remains the reliable read for overlapping labels.

### 2026-09-20 — Nav indentation and scatter bubbles

**Choice:** Indent `.nav-kids` behind a left guide rule so Players and Insights children read as sub-pages. Drop CC vs xA from Player performances. Size each bubble by volume — `SoT` on goals, `CC` on assists — using a sqrt scale so area, not radius, carries the value, and keep bubbles on raw totals even under Per 90. Keep both axes on one zero-based scale.

**Why:** The flat nav gave no visual hierarchy. CC vs xA compared a raw count against an assist-weighted model, which made the parity line meaningless. Volume bubbles say whether an overperformer is doing it on high or low chance volume. Axes fitted to their own range were tried and rejected: starting away from zero made the plot hard to read.

**Where:** `web/styles.css`, `web/player-performance.js`, `web/index.html`.

**Drawbacks:** A zero-based shared scale still crowds tight clusters — per-90 assists bunch near the origin because xA per 90 is small. Bubbles staying on totals under Per 90 mixes a rate position with a volume size, which the status line spells out.

### 2026-09-19 — Player performances scatter and a serve launcher

**Choice:** Add `#insights-player-performance`: an FPL-Core actual-vs-expected scatter with a metric dropdown (G vs xG, A vs xA, CC vs xA), season and GW range, Per 90 and 45+ mins-per-appearance checkboxes, capped at the top 15 by the actual measure. Add `scripts/serve.command` so the local preview can be started without a terminal.

**Why:** Over/under performance is the question the scatter answers directly, and the top-15 cap plus the minutes filter keep it readable — without the filter, per-90 leaderboards fill with cameo appearances. The launcher exists because the preview server only lives as long as the shell that started it.

**Where:** `web/player-performance.js`, `web/index.html`, `web/app.js`, `web/styles.css`, `scripts/serve.command`.

**Drawbacks:** CC vs xA compares chance volume with an assist-weighted model, so the parity line is a reference rather than a like-for-like benchmark. The top-15 cap hides the long tail, and label anti-overlap is greedy, so dense clusters can still push a name off its ideal slot.

### 2026-09-19 — FPL treemap is one nested map, not a card grid

**Choice:** Render the FPL treemap as a single nested treemap in one SVG, matching `#insights-understat`: clubs are leaves of an outer treemap sized by their total of the Size / sort measure, and each club's players are laid out by a second treemap inside that block under a 42px header band.

**Why:** The CSS grid of fixed-height club cards gave every team identical area regardless of output, so the page read as equal boxes rather than a treemap.

**Where:** `web/fpl-treemap.js` (`drawTreemap`, `drawTile`), `web/index.html` (`#fpl-map-chart`), `web/styles.css`.

**Drawbacks:** Club blocks must share one fixed-height canvas (`min(74vh, 860px)`), so All teams squeezes smaller clubs and drops some tile labels; the card grid could scroll instead.

### 2026-09-19 — FPL Goals treemap labels

**Choice:** Goals tiles and team headers show only G and xG. SoT and npxG remain available in Size / sort and in the tooltip.

**Why:** Four numbers crowded the tiles and headers; G vs xG is the comparison that belongs on the map.

**Where:** `web/fpl-treemap.js`, `web/index.html`.

**Drawbacks:** SoT and npxG are no longer visible without hovering.

### 2026-09-19 — FPL treemap sort and team controls

**Choice:** Add Top 10, All teams, and individual team pills. Add a dynamic Size / sort selector limited to the active metric group. Goals exposes G, SoT, xG, and npxG; the other groups expose their two displayed measures. Use medium-bold player names.

**Why:** Users need to control both the clubs shown and which related measure determines tile area/ranking without switching the metric context.

**Where:** `web/index.html`, `web/fpl-treemap.js`, `web/styles.css`.

**Drawbacks:** Team ranking changes when Size / sort changes, and cards remain capped at six positive players so labels stay readable.

### 2026-09-19 — DefCon derivation and shared treemap palette

**Choice:** Derive `defcon` from components when upstream leaves match-level `defensive_contributions` blank: 0 for goalkeepers, clearances + blocks + interceptions + tackles for defenders, plus recoveries for MID/FWD, with `tackles` falling back to `tackles_won`. Move the club pastel palette into `web/team-colors.js` so both treemaps use identical colours.

**Why:** FPL-Core stopped populating per-match `defensive_contributions` in 2026-27 (the column exists but is empty), so DC was blank on the site for the current season. The derivation matches FPL's own gameweek `defensive_contribution` exactly for all 1,236 played 2026-27 player-gameweeks, and reaches 99.4% exact agreement in 2025-26.

**Where:** `_defcon_expr` in `build_serving.py`, `web/team-colors.js`, `web/fpl-treemap.js`, `web/understat-shots.js`.

**Drawbacks:** DC now mixes a reported and a derived measure across seasons. Rows with no defensive components at all stay null rather than 0, so matches with missing upstream stats are excluded rather than counted as zero.

### 2026-09-19 — FPL metric precedence, branding, and FPL treemap

**Choice:** Prefer FPL-Core whenever a player metric overlaps Understat. Keep only Understat-only xGChain/xGBuildup in player table extras. Add a separate team-grouped FPL treemap with primary/secondary pairs G/SoT, A/CC, xGI/xG, and DC/CS; no Understat drawer. Remove the More metrics gate and show group chips directly. Add the supplied logo and X profile link.

**Why:** One visible value per common metric keeps site comparisons consistent; source-specific Understat concepts remain available without duplicating xG/minutes. The FPL treemap gives a source-consistent visual counterpart to Understat analysis.

**Where:** `web/{index,styles,app,components,registry,fpl-treemap}.js`, `web/assets/fpl-pulse-logo.png`.

**Drawbacks:** Player tables no longer expose side-by-side provider comparisons for overlapping metrics, though both remain in merged parquet/serving JSON. Treemaps show the top six positive players per team so labels remain readable.

### 2026-09-19 — Site switched to the Premier League merge

**Choice:** Player pages now read `master/pl_merge/player_match`; Understat player serving resolves curated FPL `player_code` / names and uses FPL/Opta PL minutes. Understat roster metrics remain separately labeled `US …` / `us_*`, with US per-90 values divided by `us_minutes`. Team and fixture dimensions remain FPL-owned.

**Why:** One reusable player-match connection gives the site stable identities and both providers’ measures without pretending their models or minutes are interchangeable.

**Where:** `build_serving.py`, `pipeline/understat/{serve,shot_treemap}.py`, `web/{registry,components}.js`, serving JSON.

**Refresh:** Finder `scripts/refresh.command` now runs FPL → Understat → PL merge/roster → FPL and Understat serving automatically. Local execution is the default; cloud is optional.

**Drawbacks:** The merged player feed is Premier League only, so cup/European competition choices disappear from player pages. Both providers’ similarly named measures remain visible and must be selected deliberately.

### 2026-09-19 — Premier League FPL × Understat merge (off-site)

**Choice:** Build reusable PL identity maps and a player-match merge in a separate folder. Ingest Understat match roster. Match join = date + home/away `team_code` (±1 day unique fallback). Player join = `player_id` → `player_code` with unique exact / last+initial / fuzzy ≥ 95 on the same club; review the rest. FPL minutes/xG stay FPL; Understat metrics are `us_*`. Live site unchanged.

**Why:** One PL table for future site work without silently mixing models or GW labels. Roster is required for player-match grain (shots miss non-shooters). Transfer-window re-run is maps + overrides, not a new matcher.

**Where:** `pipeline/pl_merge/`, `build_pl_merge.py`, `data/pl_merge/`, `master/pl_merge/player_match/`, `master/understat/roster/`, `docs/pl_merge.md`.

**Drawbacks:** First roster ingest is per finished EPL match. Name collisions and timezone date splits need a human review CSV. Two xG/minutes series remain on the row by design.

### 2026-09-07 — Attack tempo ribbons

**Choice:** Ship Understat `attackSpeed` as Attack tempo ribbons (Fast → Standard → Normal → Slow) under Insights → Understat. Same metrics as timing. Season-only (no GW slider) — not on shot rows. Serving: `us_team_attack_speed.json`.

**Why:** Best public lever for transition vs build-up style; GW grain does not exist in the Understat API.

**Where:** `pipeline/understat/team_attack_speed.py`, `web/understat-shots.{js,css,html}`, `web/index.html`.

### 2026-09-07 — Timing GW slider + shot grain

**Choice:** Match timing is rebuilt from Understat **shots** (minute bins) joined to FPL Premier League `team_match` gameweeks. UI From/To dual slider filters GW range; shares recompute for the window. Removed column-peak (cyan) marks — sort by bucket instead. Season `team_context_season` timing remains in master but is not the serving source for this view.

**Why:** Season context has no GW filter; shot minutes do. Dual slider matches Attackers/Teams.

**Where:** `pipeline/understat/team_timing.py`, `serving/us_team_timing.json`, `web/understat-shots.{js,css,html}`, `web/index.html`.

### 2026-09-07 — Match timing fill + column peaks

**Choice:** Timing cell fill encodes **deviation from uniform** (~16.7%/bucket), not raw share. Gold = peak interval by share (row). Sky-blue outline = peak team by absolute value (column). Sort by season total or any clock bucket (dropdown + clickable headers).

**Why:** Full-season shares cluster near 1/6 so share-as-fill looked flat. Diverging fill shows front-/back-loading; separate colours keep row vs column peaks readable.

**Where:** `web/understat-shots.js`, `web/understat-shots.css`, sort options in `web/index.html` / `web/understat-shots.html`.

### 2026-09-07 — Match timing (clock ribbons)

**Choice:** Ship Understat `context_family=timing` as match-clock ribbons under Insights → Understat → Match timing. Metric filter uses short labels G / xG / Sh / ShC / GC / xGC. Cell fill = share of that team’s season total; label shows absolute value + %. League row averages shares across shown teams. Serving: `us_team_timing.json`.

**Why:** Timing is already in master but was not on the site; a true 90-minute axis beats a generic heatmap for “when it happens.”

**Where:** `pipeline/understat/team_timing.py`, `pipeline/understat/serve.py`, `web/understat-shots.{html,css,js}`, `web/index.html`, `serving/us_team_timing.json`.

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
