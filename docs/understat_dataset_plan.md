# Understat dataset plan — EPL (use-case driven)

**Status:** **built** for the team + player shot explore (2026-09). This file is the original design; current locks are in [`decision_log.md`](./decision_log.md).

**Depends on:** [understat_api_endpoints.md](./understat_api_endpoints.md)  
**Site pattern:** parquet masters → compact serving JSON (`build_understat.py`)

**Shipped vs still open**

| Item | Status |
|---|---|
| Team map → FPL `team_code` | Shipped (`data/understat/maps/team_map.csv`) |
| Shot fact + situation / last-action / against | Shipped |
| Insights → Understat treemap + matrices | Shipped |
| Per-player situation / last-action in `us_shot_treemap.json` | Shipped |
| Curated `player_map` (FPL `player_code`) | **Not built** — serving player JSON still uses Understat ids |
| Match join to FPL `match_id` | Planned; not required for the explore page |

### Locked decisions

| Decision | Choice |
|---|---|
| Seasons (v1) | Understat `2025` + `2026` → FPL `2025-2026` + `2026-2027` |
| Pilot | **Team** situation / style first |
| Identity on the site | **FPL owns all dimensions** (player, position, team, price, etc.). Understat supplies **metrics only** for gaps not already covered (situation, lastAction, shot coords/zones, attack speed, PPDA/deep, xGChain/xGBuildup, …). Serving JSON is keyed by FPL `team_code` / `player_code`, never by Understat ids. |

### Architecture: separate Understat masters → join → serving (not in-place merge)

Understat does **not** overwrite or widen your existing Opta/FPL masters (`player_match`, `team_match`, …) as the source of truth. Those stay as they are.

```
master/player_match, team_match, …     ← FPL/Opta (unchanged)
master/understat/*                     ← new, Understat-only grain + understat ids
master/understat/id_map_*              ← explicit join tables we maintain
        │
        ▼  join at serving / insight build time
serving/us_team_situation.json         ← keyed by FPL team_code (+ season, window, …)
```

**What “merged” looks like for the site**

- Team pilot row example: `{ team_code: 14, season, window: "5", situation: "FromCorner", us_xg, us_shots, … }`  
  Dimensions (`team_code`, name, short) come from FPL; metrics (`us_*`) come from Understat after join.
- We do **not** invent a fake 1:1 between Understat shot rows and Opta `player_match` rows in v1. Situation/zone/attack-speed products are Understat-native aggregates attached to FPL entities.

**Join keys (honest accuracy)**

| Entity | How we map | Accuracy |
|---|---|---|
| **Team** | Curated table: Understat title/`team_id` → FPL `team_code` (20 EPL clubs). Hand-maintained / reviewed — **not** fuzzy matching. | Exact for EPL |
| **Match** | After team map: same `kickoff` (±tolerance) + home/away `team_code` → your `match_id` | High for PL; quarantine mismatches |
| **Player** | Curated + assisted match (normalized name + team + season). Fuzzy only as a *proposal* step; rows ship only when confirmed / high confidence. | Imperfect; team pilot does not need it |

So: yes, Understat is built **separately**, then attached via **explicit map tables**. Fuzzy logic may help *suggest* player links; it is not the authority that silently merges data into FPL rows.

This plan is scoped to what you said you want from Understat:

1. Team chance/shot creation by **situation** (strengths / weaknesses over time)  
2. **Who** creates / takes shots by situation (player picks)  
3. **lastAction** as supporting threat context (set-piece vs open-play patterns)  
4. **Shot coordinates / zones** (box penetration)  
5. **Attack speed** (transition / directness style)  
6. Plus earlier targets: **xGChain / xGBuildup / PPDA**

---

## Metric reality check (important)

| Your question | Best Understat source | Caveat |
|---|---|---|
| Situation (OpenPlay, FromCorner, SetPiece, Penalty, DirectFreekick) | **Shot rows** (`situation`) | Atomic; can roll over time by match |
| Who shoots / who assists that chance | Shot: `player_id`, `player_assisted` | “Creator” ≈ assisted-by name; not a full key-pass event feed |
| lastAction (Pass, Cross, Rebound, …) | Shot: `lastAction` | Supportive label on the shot, not a separate chance event |
| Inside box / 6-yard / outside box | Derive from shot `X`,`Y` **or** season `team.get_context_data → shotZone` | Coord-derived = over-time; context shotZone = season aggregate only |
| Attack speed (Fast / Normal / Slow / Standard) | **`team.get_context_data` only** | **Not on shot rows.** Season for/against totals only — no match-by-match series from the public API |
| PPDA / deep completions | `league.get_team_data` → `history[]` | Per match, but history rows lack `match_id` — join on date + home/away |
| xGChain / xGBuildup | Match roster / player match lines | Not on shots |

**Attack speed reading:** your interpretation is directionally right. Understat’s Fast/Normal/Slow/Standard describes how quickly the possession progressed before the shot (more direct / transition-like vs slower build-up). It is **not** a pure “counter-attack” flag, but it is the right lever for “do they score from quick transitions?” — just only as a **season profile**, unless Understat later exposes it per shot.

**“Chances created”:** Understat does not emit a separate chance event stream. For situation-aware creation, use:

- **Taker** = shooter on the shot  
- **Creator** = `player_assisted` when present  
- Volume / quality = `shots`, `xG`, goals (`result == "Goal"`)

---

## Design principle

Build **one atomic shot fact table**, then derive team/player situation and zone analytics from it.  
Pull **team context** only for what shots cannot provide (attack speed, and optional season checksums).  
Pull **team match history** for PPDA / deep / match xG.  
Pull **match roster** for xGChain / xGBuildup (and clean player–match minutes).

```
                    ┌─────────────────────┐
  league fixtures → │ understat_match     │
                    └─────────┬───────────┘
                              │ match_id
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
 understat_shot      understat_roster     team_match_style
 (situation,         (xGChain,            (PPDA, deep,
  lastAction, X,Y,    xGBuildup,           xG, xGA)
  player, xG)         minutes)
         │
         ├─► agg team × situation × match / rolling
         ├─► agg player × situation (taker + creator)
         └─► zone from coordinates

  team_context_season ──► attack_speed (+ optional shotZone checksum)
```

---

## Tables to create (v1)

Season partition: `season=YYYY-YYYY` (map Understat `"2024"` → `2024-2025`).  
League: EPL only. Namespace all metrics (`us_` or keep under `master/understat/`).

### A. Foundations (ingest raw → normalize)

#### 1. `understat_match`

**Source:** `league.get_match_data(season)`  
**Grain:** one row per EPL fixture  

Key cols: `match_id`, `kickoff_utc`, `is_result`, `home_team_id`, `away_team_id`, `home_team`, `away_team`, `home_goals`, `away_goals`, `home_xg`, `away_xg`, `forecast_w/d/l`, `season`.

#### 2. `understat_shot`  ★ primary fact

**Source:** `match.get_shot_data` for each finished EPL `match_id`  
**Grain:** one row per shot  

| Column | Role for your use cases |
|---|---|
| `shot_id`, `match_id`, `minute`, `date` | time / join |
| `season`, `team_id`, `opponent_id`, `is_home` | team strength/weakness |
| `player_id`, `player_name` | who takes the shot |
| `player_assisted` | who creates (when known) |
| `situation` | OpenPlay / FromCorner / SetPiece / Penalty / DirectFreekick |
| `last_action` | Pass, Cross, Rebound, … |
| `x`, `y` | pitch coords (0–1) |
| `shot_zone` | **derived** at ingest: `six_yard` / `penalty_area` / `outside_box` (see below) |
| `shot_type` | LeftFoot / RightFoot / Head / … |
| `result` | Goal / SavedShot / MissedShots / BlockedShot / ShotOnPost / … |
| `xg` | shot quality |

**Zone derivation (align with Understat’s `shotZone` labels):**

Understat pitch: higher `X` ≈ closer to the opponent goal (attacking toward X=1). Approximate bins used on their site:

- `six_yard` — very close to goal (high X, central Y)  
- `penalty_area` — inside box but outside six-yard  
- `outside_box` — otherwise  

Calibrate cutoffs once against `team.get_context_data → shotZone` season totals (checksum), then freeze the function in code.

#### 3. `understat_team_match_style`

**Source:** flatten `league.get_team_data` → `history[]`, join to `understat_match` on `date` + side  
**Grain:** team × match  

Cols: `match_id`, `team_id`, `is_home`, `xg`, `xga`, `npxg`, `npxga`, `ppda_att`, `ppda_def`, `ppda` (att/def), `deep`, `deep_allowed`, `xpts`, `scored`, `conceded`, `result`.

Powers: press intensity (PPDA), penetration proxy (deep), match xG trend — complementary to situation tables.

#### 4. `understat_roster`

**Source:** `match.get_roster_data`  
**Grain:** player × match appearance  

Cols: `match_id`, `roster_id`, `player_id`, `team_id`, `minutes`, `goals`, `assists`, `shots`, `xg`, `xa`, `xg_chain`, `xg_buildup`, cards, positions.

Powers: xGChain / xGBuildup for FPL player cards; also a clean minutes denominator.

#### 5. `understat_team_context_season`

**Source:** flatten `team.get_context_data`  
**Grain:** team × season × `context_family` × `context_value`  

Families to keep for v1: `attackSpeed`, `situation` (checksum), `shotZone` (checksum).  
Optional later: `formation`, `gameState`, `timing`.

This is the **only** home for attack-speed style until a per-shot field exists.

#### 6. `understat_id_map` (pipeline join only — not a site concept)

Understat and FPL use different id systems. The site never needs to know Understat ids. The pipeline needs a join table so Understat metrics can be attached to the FPL entities you already show.

| Map | From (Understat) | To (FPL / this repo) | Hard? |
|---|---|---|---|
| team | `team_id` / title | `team_code` | Easy (20 clubs) |
| match | `match_id` | your `match_id` | Medium (kickoff + home/away) |
| player | `player_id` | `player_code` | Harder (names, transfers, spelling) |

**Rule:** masters may keep understat ids internally. Anything written to `serving/` for the site must resolve to FPL keys. Unmapped player rows stay in parquet for debugging and are omitted (or rolled into team-only stats) until mapped — the team pilot can ship on the team map alone.

---

### B. Derived analytics (built from shots — your scenarios)

These are what the site/insights layer should query. Recompute from `understat_shot`; do not scrape them.

#### 1. Team situation — strength / weakness over time

**Table:** `us_team_situation_match`  
**Grain:** `team_id × match_id × situation`

Metrics (for and optionally against by flipping team):

- `shots`, `goals`, `xg`, `xg_per_shot`  
- share of team’s match xG in that situation  

**Rolling:** `us_team_situation_rolling` with windows **5 / 10 / 15** matches (same spirit as `build_serving.py` `WINDOWS`).

**Example answers:**

- “Arsenal’s share of xG from FromCorner over last 10”  
- “Opponent xG conceded from OpenPlay last 5” (defensive weakness)

#### 2. Player situation — who to pick

**Tables:**

- `us_player_situation_season` — taker: `player_id × situation`  
- `us_player_create_situation_season` — creator: aggregate where `player_assisted` matches player name/id (resolve name → id via season player list)

Metrics: `shots` / `assisted_shots`, `goals`, `xg`, `xa`-proxy (sum xG on assisted shots), minutes from roster for rates.

**Example answers:**

- “Haaland open-play xG per 90”  
- “Which Arsenal players generate the most assisted-shot xG from corners?”

#### 3. lastAction as support

Keep on the shot fact; optional rollup:

- `us_team_last_action_season` / player variant — top lastActions for Goals and for xG, optionally filtered by `situation=FromCorner|SetPiece`

**Example:** “Arsenal goals with lastAction in {Cross, Aerial, Rebound} on FromCorner”

#### 4. Shot zones / box penetration

On every shot: derived `shot_zone`. Then:

- `us_team_zone_match` / rolling — share of shots & xG from `penalty_area` + `six_yard` vs `outside_box`  
- Same for **against** (opponent shots) → “easy to penetrate?”

**Example:** “% of shots faced inside the six-yard box last 10”

#### 5. Attack speed (season profile)

From `understat_team_context_season` where `context_family=attackSpeed`:

- for / against: shots, goals, xG by Fast/Normal/Slow/Standard  
- shares and goals−xG finishing luck

**Example:** “Does this team’s Fast-attack xG share sit above league average?”  
Do **not** promise match-level attack-speed trends in v1.

#### 6. PPDA / deep / chains (style pack)

From `understat_team_match_style` + roster:

- team rolling PPDA, deep, deep_allowed  
- player season `xg_chain`, `xg_buildup` per 90  

Complements situation story (“high press + corner threat”, etc.).

---

## Serving layer (site)

Mirror existing flow: masters stay wide; `serving/` gets small JSON views, e.g.:

| Serving file | Powers |
|---|---|
| `us_team_situation.json` | Team page: situation mix + rolling sparkline |
| `us_player_situation.json` | Player page: OP vs set-piece xG, creator vs taker |
| `us_team_style.json` | PPDA, deep, attack-speed season profile |
| `us_shots_sample.json` or per-match on demand | Shot maps (coords) — consider lazy/per-match if payload is large |

Keep Understat metrics clearly labeled (`us_xg`, …) next to Opta/FPL fields.

---

## Use case → table cheat sheet

| Scenario | Read from |
|---|---|
| Team creates chances from which situation, over time | `us_team_situation_match` / rolling |
| Opponent weakness by situation | same, `against` or opponent filter |
| Who takes shots by situation | `us_player_situation_*` |
| Who creates (assisted) by situation | `us_player_create_situation_*` |
| Arsenal set-piece threat / Haaland open-play | situation + optional lastAction filter on shots |
| Where shots come from (box / 6-yard) | `shot_zone` on shots → zone aggs |
| Counter / transition style | `attackSpeed` in team context season |
| Press + penetration | PPDA / deep on team_match_style |
| Involvement without the final shot | roster `xg_chain` / `xg_buildup` |

---

## Build order (next steps)

### Step 0 — Scope (locked)
- Seasons: Understat **`2025` + `2026`** (FPL 2025-2026 + 2026-2027).  
- Pilot: team situation / style.  
- Rate limit: cache raw JSON under `.cache/understat/`; sleep between match shot pulls.

### Step 1 — Index + maps
1. Ingest `understat_match` + league player/team lists.  
2. Seed `team_id → team_code` map (20 clubs) — enough to ship the team pilot.  
3. Draft `player_id → player_code` in parallel (needed before player pages); quarantine low-confidence rows so serving never shows orphan Understat-only players.

### Step 2 — Shot backbone
1. For each finished match: `get_shot_data` → `understat_shot` with typed numerics + derived `shot_zone`.  
2. Validate: sum of shot xG ≈ match `home_xg`/`away_xg`; zone counts ≈ context `shotZone` for a sample team-season.

### Step 3 — Style + chains
1. Flatten team history → `understat_team_match_style` (join match ids).  
2. Roster → `understat_roster` for xGChain/xGBuildup.  
3. Flatten `get_context_data` → `understat_team_context_season` (at least `attackSpeed`).

### Step 4 — Derived analytics
1. Team situation match + rolling (5/10/15).  
2. Player situation (taker) + creator rollup.  
3. Zone rolling for/against.

### Step 5 — Serving + one pilot UI slice
1. Emit 1–2 serving JSON files.  
2. Pilot: one team page block (“chance sources”) + one player block (“open-play vs set-piece xG”).

### Step 6 — Only then expand
- More seasons, formation/gameState context, denser shot maps, stricter player mapping.

---

## What not to build in v1

- Full career player shot dumps for every historical season (start with selected seasons via **match** shots — EPL-complete and consistent).  
- Treating attack speed as a per-match time series.  
- Merging Understat xG into existing Opta `xg` columns.  
- Relying on `player.get_shot_data` as the season build path (harder to bound to EPL fixtures; use match endpoint instead).

---

## Next implementation ticket

Decisions above are locked. First build: **cache + `understat_match` + `understat_shot` for seasons 2025 and 2026**, with zone derivation, xG checksums, and `team_id → team_code` map so team-pilot serving can speak FPL team codes.
