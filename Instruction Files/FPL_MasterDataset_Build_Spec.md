# FPL‑Core‑Insights → Master Datasets — Build Spec (Handover to Cursor)

**Purpose of this document.** Everything a coding agent (Cursor) needs to turn the public
`olbauday/FPL-Core-Insights` repo into two clean, local **master datasets** —
**player‑match** and **team‑match** — stored in a fast, efficient format, ready for an
HTML dashboard to be built on top later. It captures the repo structure, exact schemas,
join keys, data quirks, target dataset designs, storage format, pipeline architecture, and
acceptance criteria.

> Written from hands‑on inspection of the repo. Treat the **repo's current state as
> authoritative** — it is actively maintained and schemas can drift, so validate every run
> (see §5 and §9). Do not fabricate fields that aren't there (see §6 gotchas).

---

## 0. TL;DR — what to build

**Scope = extract everything, filter later.** Ingest **all competitions** (Premier League, domestic
cups, European competitions, curtain‑raisers, and **pre‑season friendlies**) and **all gameweeks
including GW0**, keeping a `competition` column on every row. The dashboard filters to what a view
needs (default views can still show PL only). Only exclude **duplicates and invalid/erroneous
rows** — never drop a whole competition at ingest. This means we never have to rebuild the masters
to answer a new question.

1. A Python pipeline that **shallow‑clones the public repo** (no auth), discovers seasons,
   competitions and gameweeks dynamically, validates schemas, and builds:
   - **`player_match`** — one row per player per match (Opta/football layer).
   - **`player_gw`** — one row per player per gameweek (FPL fantasy layer: points, price, ownership).
   - **`team_match`** — one row per team per match (two rows per fixture).
   - **`fixtures`** — upcoming (unplayed) matches for scheduling/ticker.
2. Store the canonical masters as **partitioned Parquet** (columnar, typed, compressed).
3. Emit a small **serving layer (JSON)** derived from the masters for the browser dashboard,
   plus a **manifest** (provenance/drift detection) and a **data dictionary**.
4. Make it **idempotent, incremental, and drift‑resilient**.

**Why two player tables (match vs gw):** football stats are per *match*; FPL points are per
*gameweek*. In a Double Gameweek a player has 2 matches but 1 FPL points figure. Keeping them
in separate tables (joined on `season, gw, player_id`) avoids double‑counting and keeps both
grains clean. A convenience join is described in §6.

---

## 1. Data source

- **Repo:** `https://github.com/olbauday/FPL-Core-Insights` — public, open data. Clone with a
  plain unauthenticated shallow clone: `git clone --depth 1 <url>`. **Do not use any personal
  or enterprise GitHub account/token.** Attribute the source.
- **Refresh cadence at source:** updated twice daily (07:30 and 17:30 UTC). A **weekly or
  on‑demand** pull is plenty for analysis; the pull is the *only* step that touches the network.
- **Combines three sources:** official FPL API data, manually‑curated Opta‑like match stats,
  and ClubElo ratings (Elo often not yet populated — treat as missing).
- **Drift warning:** files, columns, IDs, join relationships, metric definitions, competition
  coverage and directory structure **may change mid‑season**. The pipeline must detect and
  surface drift rather than silently coerce.

---

## 2. Repository layout

```
data/
  2024-2025/ | 2025-2026/ | 2026-2027/          # one dir per season (discover, don't hardcode)
    players.csv  playerstats.csv  teams.csv  gameweek_summaries.csv  team_history.csv
    By Gameweek/GW1 … GW38/                       # COMBINED — may contain multiple competitions
    By Tournament/
      Premier League/GW1 … GW38/                  # canonical PL-only slice (USE THIS for FPL)
      Champions League/ | EFL Cup/ | Europa League/ | Conference League/
```

Each **GW folder** (under either `By Gameweek` or `By Tournament/<comp>`) contains:

```
matches.csv  fixtures.csv  playermatchstats.csv  player_gameweek_stats.csv
players.csv  playerstats.csv  teams.csv  shots.csv  lineups.csv  incidents.csv
average_positions.csv  match_enrichment.csv  player_match_enrichment.csv
momentum.csv  xg_by_minute.csv
```

### ⚠️ Ingest source & de‑duplication rule (read carefully)
`By Gameweek/GW{n}/` is the **union/projection of every competition** for that gameweek, while
`By Tournament/<competition>/GW{n}/` holds each competition **exactly once**. The same match
therefore appears in **both** trees → the duplicate trap.

**Rule: ingest from `By Tournament/<competition>/` ONLY, iterating every competition subfolder and
every `GW{n}` folder (including `GW0`). Do NOT read `By Gameweek` — it would duplicate everything.**
Set `competition` from the tournament folder name. A match belongs to exactly one competition, so
across tournament folders there is no overlap.
- *Optional safety net:* after building, reconcile against `By Gameweek` by `match_id` and add any
  **orphan** matches missing from `By Tournament` (dedupe on `match_id`). In practice there should
  be none.

**Competitions vary by season — discover them, don't hardcode.** Observed examples:
- `2025-2026`: Premier League, Champions League, Europa League, Conference League, EFL Cup
- `2026-2027`: Premier League, EFL Cup, Community Shield, UEFA Super Cup, **Friendlies**

**Pre‑season / curtain‑raisers = `GW0`.** Friendlies, Community Shield and UEFA Super Cup sit under
`.../GW0/`. Include them (tagged by competition); note friendly coverage is spotty and often
**team‑level only** (player detail tables may be sparse/absent — keep nulls, don't assume files
exist).

**Coverage is uneven for non‑PL competitions.** Only the PL has complete detail every GW; other
competitions have `GW{n}` folders only for gameweeks they actually played, and some detail tables
(shots/incidents/etc.) may be missing for a given match. **Check file existence per folder**;
absence ⇒ null, not zero.

**Gameweek** = the **folder number** (`GW0`…`GW38`), cross‑checked against `matches.gameweek`. For
non‑PL competitions the `GW{n}` is the FPL gameweek the fixture is mapped to (so cups/Europe align
to the FPL calendar), not a competition round number.

---

## 3. Source file grain & the columns that matter

Grain = "what one row represents". Verified column names below.

### `players.csv` — player identity (dimension)
Grain: one row per player (in that season).
`player_code` (**STABLE across seasons — use for cross‑season identity**), `player_id`
(**season‑specific — reassigned each season**), `first_name`, `second_name`, `web_name`
(display), `team_code` (stable club code → join to `teams.code`), `position`
(Goalkeeper/Defender/Midfielder/Forward).

### `teams.csv` — team dimension
`code` (**stable club code**), `id` (**season‑specific 1..20 — do not confuse with code**),
`name`, `short_name`, `strength`, `strength_overall_home/away`, `strength_attack_home/away`,
`strength_defence_home/away` (1–5; some 0/blank → missing), `pulse_id`, `elo` (often blank),
`fotmob_name`.

### `playermatchstats.csv` — **PLAYER × MATCH (the backbone of `player_match`)**
Grain: one row per player per match. `player_id` (season‑scoped), `match_id`.
Football/Opta metrics:
`minutes_played, goals, assists, total_shots, xg, xa, shots_on_target, successful_dribbles,
big_chances_missed, touches_opposition_box, touches, accurate_passes, accurate_passes_percent,
chances_created, final_third_passes, accurate_crosses(_percent), accurate_long_balls(_percent),
tackles_won, interceptions, recoveries, blocks, clearances, headed_clearances, dribbled_past,
duels_won, duels_lost, ground_duels_won(_percent), aerial_duels_won(_percent), was_fouled,
fouls_committed, saves, goals_conceded, xgot_faced, goals_prevented, sweeper_actions,
gk_accurate_passes, gk_accurate_long_balls, dispossessed, high_claim, saves_inside_box,
offsides, successful_dribbles_percent, tackles_won_percent, xgot, tackles, start_min,
finish_min, team_goals_conceded, penalties_scored, penalties_missed, defensive_contributions`.

### `player_match_enrichment.csv` — PLAYER × MATCH (extra)
`player_id, match_id, player_name, rating, possession_lost, attacking_shots_blocked,
total_passes, total_long_balls, total_crosses, total_dribbles, ground_duels_lost,
aerial_duels_lost, yellow_cards, red_cards, goalkeeper_punches`.

### `player_gameweek_stats.csv` — **PLAYER × GAMEWEEK (the FPL fantasy layer → `player_gw`)**
Grain: one row per player per GW, **discrete** (this GW only), FPL‑API derived (PL‑only).
`id` (= season `player_id`), `gw`, `web_name`, `status`, `news`, `now_cost` (price snapshot at
deadline), `selected_by_percent`, `form`, `event_points`, `total_points` (**this GW's points**),
`bonus`, `bps`, `points_per_game`, `ep_next/ep_this`, `transfers_in/out_event`,
`corners_and_indirect_freekicks_order`, `direct_freekicks_order`, `penalties_order`,
`set_piece_threat`, `minutes`, `goals_scored`, `assists`, `clean_sheets`, `goals_conceded`,
`own_goals`, `penalties_saved/missed`, `yellow_cards`, `red_cards`, `saves`, `starts`,
`expected_goals`, `expected_assists`, `expected_goal_involvements`, `expected_goals_conceded`
(FPL‑API xG family — *distinct from Opta `xg` above*), `influence`, `creativity`, `threat`,
`ict_index`, `tackles`, `clearances_blocks_interceptions`, `recoveries`, `defensive_contribution`.

### `playerstats.csv` — CUMULATIVE season snapshot (⚠️ not per‑GW)
Same columns as `player_gameweek_stats` but values are **cumulative season totals**. **Do not use
as gameweek observations.** Useful only for an end‑of‑season snapshot or current price/ownership.

### `matches.csv` — **MATCH (team‑level, both teams in one row → `team_match`)**
Grain: one row per match. `gameweek, kickoff_time, home_team, away_team` (**team CODES**, float),
`home_team_elo, away_team_elo`, `home_score, away_score`, `finished`, `match_id` (string, e.g.
`26-27-prem-arsenal-vs-coventry-city`), `match_url`, `fotmob_id`, `tournament`, and paired
`home_*/away_*` metrics: `possession, expected_goals_xg, total_shots, shots_on_target,
big_chances, big_chances_missed, accurate_passes(_pct), fouls_committed, corners, xg_open_play,
xg_set_play, non_penalty_xg, xg_on_target_xgot, shots_off_target, blocked_shots, hit_woodwork,
shots_inside_box, shots_outside_box, passes, own_half, opposition_half, accurate_long_balls(_pct),
accurate_crosses(_pct), throws, touches_in_opposition_box, offsides, yellow_cards, red_cards,
tackles_won(_pct), interceptions, blocks, clearances, keeper_saves, duels_won,
ground_duels_won(_pct), aerial_duels_won(_pct), successful_dribbles(_pct)`, `stats_processed`,
`player_stats_processed`.

### `fixtures.csv` — same schema as `matches.csv` but INCLUDES unplayed
`finished=False` rows have null stats. Source for **upcoming fixtures / ticker**. Some future GW
rows can have **NaN team codes** (schedule not finalised) — guard/skip these.

### `shots.csv` — SHOT events
`match_id, shot_index, minute, added_time, is_home, player_id, player_name, outcome, situation,
body_part, xg, xgot, start_x, start_y, goal_mouth_y, goal_mouth_z, goal_mouth_location`.
Enables shot maps, set‑piece vs open‑play xG, penalty splits (via `situation`).

### `lineups.csv` — confirmed lineups (per player per match)
`match_id, team_side, team_code, player_id, player_name, position, jersey_number, is_starting,
formation, lineup_status`. Use for **confirmed starts** and formation context.

### `incidents.csv` — canonical events
`match_id, incident_index, incident_type, minute, added_time, team_side, player_id,
secondary_player_id, assist_player_id, card_type, goal_type, home_score, away_score, text`.
Use for canonical goals/assists, cards, subs, minute‑of‑involvement.

### `average_positions.csv` — `match_id, team_side, player_id, x, y` (avg position).
### `match_enrichment.csv` — match context + shot‑model xG + data‑quality flags
`match_id, travel_distance_km, weather_description, temperature_c, wind_speed, pitch_condition,
is_local_derby, is_neutral_ground, lineup_status, home_shot_model_xg, away_shot_model_xg,
incident_timing_coverage, unlocated_card_count, quarantined_incident_count`.

---

## 4. Join keys & referential integrity (do this exactly)

| Need | Key | Notes |
|---|---|---|
| Cross‑season player identity | **`player_code`** | `player_id` is reassigned each season — never join across seasons on it. |
| Within‑season player joins | `player_id` | Consistent within a season/season folder. |
| Player ↔ match football stats | `player_id + match_id` | From `playermatchstats`, `player_match_enrichment`, `lineups`, `shots`, `average_positions`. |
| Player ↔ FPL fantasy (GW) | `player_id + gw` | From `player_gameweek_stats` (`id` = player_id). |
| Match ↔ teams | `home_team` / `away_team` = **team CODE** → `teams.code` | Not `teams.id`. |
| Player ↔ team/position | `players.player_id` (+ `team_code`, `position`) | Dimension join. |
| Gameweek | folder `GW{n}` (authoritative) + `matches.gameweek` | Cross‑check. |
| Match dedupe | ingest PL only from `By Tournament/Premier League` | See §2. |

**After every join, log:** input row count, output row count, unmatched keys, duplicate keys.
Investigate unmatched (transfers, new signings, missing lineups) — do not silently drop.

---

## 5. Data quirks / gotchas (encode as validation rules)

1. **`now_cost` is price in £m as a decimal** (e.g. `7.0`), NOT tenths. Don't divide by 10.
2. **Missing means unknown, not zero.** Never `fillna(0)` on measures (xg, xa, minutes, elo,
   goals_prevented, etc.). Preserve nulls.
3. **Pre‑season / new‑season snapshots**: at the very start of a season `playerstats` /
   `player_gameweek_stats` can be a snapshot with **0 minutes played**. Don't treat as real
   performance — check `minutes`/`starts` before using.
4. **"Big chances created" is NOT available at player level.** Only `matches.home/away_big_chances`
   (team level) and `playermatchstats.big_chances_missed` exist. **Do not invent BCC.** Use
   `chances_created` (key passes), `xa`, `touches_opposition_box` as creation proxies.
5. **Three different xG lineages — keep provenance, don't mix:** Opta `playermatchstats.xg`,
   shot‑model `match_enrichment.*_shot_model_xg`, and FPL‑API `player_gameweek_stats.expected_goals`.
6. **Elo & some `strength_*` fields are blank/0** → treat as missing.
7. **Promoted clubs have no prior‑season PL history** → expect nulls on cross‑season joins.
8. **Extract all competitions; tag, don't drop.** Keep every competition (incl. friendlies/GW0)
   with a `competition` column. The dashboard filters/segments as needed. **Never blend
   competitions into the same rolling metric silently** — a "last‑5" must state whether it's PL‑only
   or all‑comps; default dashboard views should filter to PL, but the *data* keeps everything.
9. **`fixtures.csv` future rows may have NaN team codes** — skip/guard.
10. **Double/Blank Gameweeks:** a team/player can have 0 or 2 matches in a GW. This is exactly why
    `player_match` (per match) and `player_gw` (per GW) are separate. Carry `gw_match_count`.

---

## 6. Target dataset — `player_match` (primary player table)

**Grain:** one row per `(season, competition, gw, match_id, player_id)` — **all competitions
included** (PL, cups, Europe, friendlies/GW0), each tagged by `competition`. No competition is
dropped at ingest; filtering happens in the dashboard.

**Column plan (target ← source):**

*Identity / context*
- `season` ← folder
- `competition` ← folder (`'Premier League'` default) / `matches.tournament`
- `gw` ← folder, cross‑checked with `matches.gameweek`
- `match_id` ← `matches.match_id`
- `kickoff_utc` ← `matches.kickoff_time` (normalise to UTC ISO)
- `player_id` ← `playermatchstats.player_id`
- `player_code` ← join `players` on `player_id` (stable cross‑season id)
- `web_name`, `position` ← `players`
- `team_code`, `opponent_code` ← derive from `matches` (which side the player's team is)
- `is_home` (bool), `venue` ('H'/'A')
- `team_goals_for`, `team_goals_against`, `result` ('W'/'D'/'L') ← `matches` scores
- `started` (bool), `formation`, `lineup_status` ← `lineups`

*Playing time*
- `minutes` ← `playermatchstats.minutes_played`; `start_min`, `finish_min`

*Attacking / shooting*
- `goals`, `assists`, `penalties_scored`, `penalties_missed`
- `total_shots`, `shots_on_target`, `xg`, `xgot`, `big_chances_missed`
- `touches_opposition_box`, `successful_dribbles`

*Creation / passing*
- `xa`, `chances_created` (key passes), `final_third_passes`,
  `accurate_crosses`(+`_percent`), `accurate_passes`(+`_percent`), `accurate_long_balls`(+`_percent`)

*Defending*
- `tackles`, `tackles_won`, `interceptions`, `clearances`, `headed_clearances`, `blocks`,
  `recoveries`, `defensive_contributions`, `dribbled_past`, `duels_won`, `duels_lost`,
  `ground_duels_won`(+`_percent`), `aerial_duels_won`(+`_percent`), `dispossessed`, `was_fouled`,
  `fouls_committed`

*Goalkeeping*
- `saves`, `saves_inside_box`, `goals_conceded`, `xgot_faced`, `goals_prevented`
  (= xG prevented via saves), `high_claim`, `sweeper_actions`, `gk_accurate_passes`

*Discipline*
- `yellow_cards`, `red_cards`, `offsides`, `own_goals` (own_goals from `incidents`/`player_gw`)

*Enrichment*
- `rating` ← `player_match_enrichment`
- shots‑derived per player‑match (aggregate `shots.csv` by `match_id+player_id`): `np_xg`
  (non‑penalty xG), `set_piece_xg`, `open_play_xg`, `penalty_shots` (from `situation`/`body_part`)

*FPL fantasy (attached from `player_gw` on `season+gw+player_id`; see DGW note)*
- `fpl_points`, `bonus`, `bps`, `now_cost`, `selected_by_percent`, `form`,
  `penalties_order`, `direct_freekicks_order`, `corners_and_indirect_freekicks_order`, `status`
- `is_dgw` (bool), `gw_match_count`, `gw_match_index` (1 of N in the GW)

**DGW handling (important):** FPL points are per **gameweek**, not per match. Attach GW‑level FPL
fields onto the match rows for convenience but set `is_dgw=true` / `gw_match_count=2` so the
dashboard never sums a player's GW points twice. The **authoritative FPL series lives in
`player_gw`**; `player_match` is authoritative for *football* stats.

*Provenance (every table):* `source_commit` (git SHA), `ingested_at_utc`, `source_files` list.

### Companion table — `player_gw` (FPL fantasy per GW)
Grain: `(season, gw, player_id)`. All of `player_gameweek_stats` you care about
(`total_points, event_points, bonus, bps, minutes, starts, goals_scored, assists, clean_sheets,
goals_conceded, saves, now_cost, selected_by_percent, expected_goals/assists/goal_involvements,
influence, creativity, threat, ict_index, defensive_contribution, *_order, set_piece_threat,
status, news`) + `player_code`, `team_code`, `position`, provenance. This is the clean layer for
rolling FPL form, price/ownership trends, and per‑90 (with minute thresholds).

> **`player_gw` is Premier‑League‑only by nature** — FPL points only accrue in the PL. Note that
> `player_gameweek_stats.csv` is an FPL‑API snapshot **replicated inside every competition's GW
> folder** for that gameweek, so building `player_gw` from `By Tournament/*` would duplicate it.
> **Source `player_gw` from `By Tournament/Premier League` only, or dedupe on
> `(season, gw, player_id)`.** (This is the one place the "read all tournament folders" rule needs a
> guard — the football tables in `playermatchstats` are genuinely per‑competition and do not
> duplicate.)

---

## 7. Target dataset — `team_match`

**Grain:** one row per `(season, competition, gw, match_id, team_code)` → **two rows per match**
(unpivot `matches.csv` home/away).

**Columns (target ← `matches.home_*/away_*` for the team's side):**
- context: `season, competition, gw, match_id, kickoff_utc, team_code, opponent_code, is_home,
  finished`
- result: `goals_for` (`*_score`), `goals_against`, `result`, `points` (3/1/0), `clean_sheet` (bool)
- attack: `xg`, `np_xg` (`non_penalty_xg`), `xg_open_play`, `xg_set_play`, `xgot`
  (`xg_on_target_xgot`), `total_shots`, `shots_on_target`, `shots_inside_box`,
  `shots_outside_box`, `big_chances`, `big_chances_missed`, `touches_in_opposition_box`, `corners`
- defence (mirror = opponent's attack): `xga`, `shots_conceded`, `sot_conceded`,
  `big_chances_conceded`, `keeper_saves`
- control/other: `possession`, `accurate_passes`(+`pct`), `accurate_long_balls`(+`pct`),
  `accurate_crosses`(+`pct`), `tackles_won`(+`pct`), `interceptions`, `blocks`, `clearances`,
  `duels_won`, `aerial/ground_duels_won`(+`pct`), `fouls_committed`, `offsides`,
  `yellow_cards`, `red_cards`
- strength/context: `elo` (`*_team_elo` if present), team `strength_*` snapshot from `teams.csv`,
  and match_enrichment (`is_local_derby`, `weather_description`, `temperature_c`, `pitch_condition`)
- provenance columns as above.

This grain makes rolling team attack/defence (last‑N GW), home/away splits, and opponent‑adjusted
context trivial for the dashboard.

---

## 8. Storage format & layout (fast + efficient for the dashboard)

**Canonical masters → Apache Parquet** (columnar, typed, compressed — Zstd or Snappy). Rationale:
small on disk, preserves nulls and dtypes, very fast partial/column reads with pandas / polars /
DuckDB, ideal for incremental analysis.

**Partition by season then competition** (so a PL‑only dashboard read touches only PL files, while
all‑competition analysis is still one directory away — cheap either way):
```
master/
  player_match/ season=2025-2026/competition=Premier League/part.parquet
                season=2025-2026/competition=Champions League/part.parquet
                season=2026-2027/competition=Friendlies/part.parquet   # GW0 pre-season
                …                                                       # every competition
  player_gw/    season=2025-2026/part.parquet          # FPL fantasy is PL-only by nature
  team_match/   season=2025-2026/competition=Premier League/part.parquet  … (all comps)
  fixtures/     season=2026-2027/part.parquet
manifest.json            # provenance + drift detection (see below)
docs/data_dictionary.md  # generated column dictionary
```
Partitioning by `competition` is what makes "extract all, filter later" cheap: the dashboard's
default PL view reads only the `competition=Premier League` partitions; an all‑comps view reads the
rest without any rebuild.

**Serving layer for the HTML dashboard.** Browsers cannot read Parquet natively without a heavy
WASM engine, so add a **build step** that turns the masters into small, ready‑to‑render artefacts:

- **Recommended (simplest, fastest to load):** `build_serving.py` reads the Parquet masters and
  emits **compact pre‑aggregated JSON** (e.g. rolling 5/10/15‑GW player windows, current‑GW
  fixtures + ticker, team aggregates). The dashboard either embeds this JSON in a single
  self‑contained HTML or `fetch`es a handful of small `.json` files. Instant render, no DB in the
  browser. (This mirrors a working pattern already used in this project.)
- **Optional (flexible in‑browser querying):** ship the Parquet files + **DuckDB‑WASM** and let
  the dashboard run SQL client‑side. More powerful/ad‑hoc, but heavier initial load and more
  complexity. Document as an advanced mode, not the default.

Keep the serving JSON **small**: only the columns/rows a view needs, rounded sensibly. The masters
stay full‑fidelity in Parquet.

**`manifest.json` (provenance & drift):** `built_at_utc`, `source_commit` (git SHA), `seasons`,
`competitions`, per‑table `row_counts`, `null_rate` summary, and a **`schema_hash`** per source
file so a changed upstream schema is detected and flagged rather than silently ingested.

---

## 9. Pipeline architecture

Stages (each a pure, testable function):
1. **fetch** — shallow clone to a temp dir; capture the commit SHA. (Only network step.)
2. **discover** — enumerate seasons, **every `By Tournament/<competition>` folder**, and every
   `GW{n}` (incl. `GW0`) from disk. **Never hardcode** the season/competition list or GW count.
3. **validate schema** — assert required columns exist per source file; if columns are
   missing/renamed, **fail loudly with a diff** and write the drift to the manifest. Do not coerce.
   Handle **missing detail tables** gracefully for sparsely‑covered competitions (null, don't fail).
4. **build** — construct `player_match`, `player_gw`, `team_match`, `fixtures` across **all
   competitions**, each row tagged with `competition`. Source only from `By Tournament/*`.
5. **quality checks** — row counts vs expectation, null‑rate report, duplicate‑key check,
   referential integrity (every `player_id`/`team_code` resolves), sanity ranges (0≤minutes≤120,
   xg≥0, price in plausible band, etc.).
6. **write** — Parquet with **atomic writes** (write temp then move); update `manifest.json` and
   `docs/data_dictionary.md`.
7. **serving** — derive the dashboard JSON.

**Idempotent & incremental:** compare per‑file hashes / commit SHA to reprocess only changed
seasons/GWs; support a `--full` rebuild. Re‑runs on unchanged input produce byte‑identical output.

**Suggested tech:** Python + **polars** (or pandas) + **pyarrow** (Parquet); **DuckDB** optional
for SQL transforms/quality checks. Prefer polars/DuckDB for speed on the per‑match tables.

---

## 10. Best‑practices checklist (enforce)

- [ ] Explicit target schemas & dtypes; validate (e.g. `pandera`, or manual asserts).
- [ ] **Missing = null**; never `fillna(0)` on measures.
- [ ] Ingest **all competitions from `By Tournament/*`** (incl. GW0 friendlies); **never read
      `By Gameweek`** (duplicate source). Tag every row with `competition`.
- [ ] Cross‑season identity on `player_code`; within‑season on `player_id`; teams on `code`.
- [ ] Keep **provenance** columns (`source_commit`, `ingested_at_utc`, `source_files`).
- [ ] Document & flag **DGW/BGW** (`is_dgw`, `gw_match_count`).
- [ ] Do **not** invent "big chances created" (unavailable) — use CC/xA/TiB proxies.
- [ ] Per‑90 / ratios computed at the **analysis/serving** layer with a **minimum‑minutes
      threshold** — don't destroy raw counts in the master.
- [ ] Atomic, deterministic, idempotent writes; incremental by default, `--full` available.
- [ ] Log join diagnostics (in/out/unmatched/dupes) every run.
- [ ] `manifest.json` with `schema_hash` per source file to detect drift.
- [ ] Unit tests on transforms + a few **golden‑row** tests (known player/match values).

---

## 11. Deliverables & acceptance criteria (for Cursor)

**Repo structure to produce:**
```
/pipeline/            # fetch, validate, build, quality, serving modules
/master/              # partitioned Parquet (player_match, player_gw, team_match, fixtures)
/serving/             # small JSON artefacts for the dashboard
/docs/data_dictionary.md
manifest.json
README.md             # how to run
```

**CLI:**
- `python build.py --refresh`        # clone + validate + build masters + serving
- `python build.py --serving-only`   # rebuild only the dashboard JSON from existing Parquet
- `python build.py --full`           # ignore incremental cache, rebuild everything

**Acceptance criteria:**
1. Masters build for all seasons present; schema validation passes or drift is reported.
2. **No duplicate rows** at each declared grain; referential integrity holds.
3. **All competitions present** (PL, cups, Europe, friendlies/GW0), each tagged with `competition`,
   and **not** double‑counted (sourced from `By Tournament/*`, never `By Gameweek`).
4. Nulls preserved (spot‑check: promoted‑club cross‑season joins, pre‑season 0‑minute snapshots,
   friendlies with team‑level‑only data).
5. `manifest.json` records commit SHA, row counts, null summary, schema hashes.
6. These **sample queries** return sensible results:
   - Top 20 players by rolling last‑5‑GW `xg + xa` (min ~60 mins/appearance), **filtered
     `competition='Premier League'`**, from `player_match`.
   - The same but **all competitions** (no competition filter) — proving nothing was dropped and
     cup/European minutes are included.
   - A team's last‑10‑GW `xg` for / `xga` against, home vs away, PL‑filtered, from `team_match`.
   - A player's FPL points, price and ownership trajectory over the season from `player_gw`.
   - Pre‑season (`gw=0`, `competition='Friendlies'`) minutes per player exist where the source
     published them.
   - Upcoming gameweek fixtures with each team's opponent and home/away from `fixtures`.
7. Serving JSON loads in the dashboard with no network calls (embedded) or a few small fetches.

---

## 12. Notes the dashboard layer will rely on (so design the masters for them)

- Rolling windows (last 5/10/15 GW) per player and per team — cheap if grain is per match/GW.
- Average **minutes per appearance** is the right "is this a regular?" filter (window‑independent),
  so keep `minutes` and an appearance count queryable.
- Fixture difficulty / predicted xG uses team rolling `xg`/`xga` + home/away + opponent strength —
  all available from `team_match` + `teams` strength (note Elo may be blank).
- Set‑piece & penalty responsibility come from `*_order` fields (`player_gw`) and `shots.situation`.

---

*Source: `olbauday/FPL-Core-Insights` (public). This spec reflects the repo as inspected; validate
against the live schema on first run and update the data dictionary from the manifest.*
