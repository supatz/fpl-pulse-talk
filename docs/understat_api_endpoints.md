# Understat API — endpoint exploration (EPL)

**Status:** exploration only — no ingest pipeline yet.  
**Library:** [`collinb9/understatAPI`](https://github.com/collinb9/understatAPI) (`pip install understatapi`, docs: [collinb9.github.io/understatAPI](https://collinb9.github.io/understatAPI/))  
**Scope for now:** Premier League only (`league="EPL"`). Other leagues (La Liga, Bundesliga, Serie A, Ligue 1, RFPL) exist in the same API and can be expanded later.  
**Sampled against:** EPL season `2024` (2024/25), live understat.com responses via understatAPI 0.7.x.

Understat is an unofficial scrape wrapper around understat.com pages. It is **not** an official API. Treat rate limits gently, cache raw pulls, and expect occasional schema drift.

---

## How this relates to FPL Pulse / this repo

Your current masters (`player_match`, `player_gw`, `team_match`, `fixtures`) and serving JSON (`players_matches.json`, `teams_gw.json`, …) already carry Opta/FPL xG-style fields. Understat adds a **second, shot-model-native** xG stack that is especially strong for:

| Gap vs current masters | Understat strength |
|---|---|
| Shot-level detail (coords, situation, body part, assist, last action) | `player.get_shot_data`, `match.get_shot_data` |
| Team style contexts (formation / game state / timing / PPDA / deep completions) | `team.get_context_data`, team match history |
| Stable understat player/team/match IDs for deep links | all endpoints |
| Non-penalty xG / xGChain / xGBuildup consistently | league + team + player + roster |

**Do not mix** Understat xG with FPL `expected_goals` or Opta `xg` without labeling the source. Same rule you already use in `docs/data_dictionary.md`.

Suggested storage pattern (mirrors this repo):

```
master/understat/
  league_player/season=YYYY/part.parquet
  league_match/season=YYYY/part.parquet
  team_match_history/season=YYYY/part.parquet   # from league.get_team_data history
  team_context/season=YYYY/part.parquet         # long form from get_context_data
  player_match/…                                # optional denser grain
  player_shot/…
  match_shot/…
  match_roster/…
  match_info/…
serving/  → compact JSON for the site (same spirit as players_matches.json)
```

Season key note: Understat uses the **start year** as a string (`"2024"` = 2024/25). Map to your `YYYY-YYYY` season folders at ingest.

---

## Client surface

```python
from understatapi import UnderstatClient

with UnderstatClient() as understat:
    understat.league(league="EPL")           # name
    understat.team(team="Manchester_United") # underscore name
    understat.player(player="1250")          # understat player id (str)
    understat.match(match="26602")           # understat match id (str)
```

| Endpoint | Understat page | ID style |
|---|---|---|
| `league` | `/league/<league>/<season>` | `EPL` |
| `team` | `/team/<team>/<season>` | `Manchester_United` (spaces → `_`) |
| `player` | `/player/<player_id>` | numeric string, stable across seasons |
| `match` | `/match/<match_id>` | numeric string |

Many numeric fields arrive as **strings** (e.g. `"29"`). Cast at ingest.

---

## 1. League endpoint — `understat.league("EPL")`

Webpage analog: season league table + player list + fixture list.

### 1.1 `get_player_data(season)`

**What it captures:** One row per player who appeared in the EPL that season — season totals (the league player table).

**Grain:** `(season, understat_player_id)`  
**Return:** `list[dict]`  
**EPL 2024 sample size:** ~562 players

| Field | Meaning |
|---|---|
| `id` | Understat player id |
| `player_name` | Display name |
| `team_title` | Club display name (can be multi-club string if transferred) |
| `position` | Coarse role string, e.g. `F M`, `F M S` (not FPL GKP/DEF/MID/FWD) |
| `games` | Appearances |
| `time` | Minutes |
| `goals`, `assists` | Counting stats |
| `shots`, `key_passes` | Volume |
| `yellow_cards`, `red_cards` | Discipline |
| `xG`, `xA` | Season expected goals / assists |
| `npg`, `npxG` | Non-penalty goals / xG |
| `xGChain`, `xGBuildup` | Possession-chain involvement metrics |

**Site use:** Season leaderboards, “understat xG vs goals”, cheap player index for joining to shot/match pulls.  
**Overlap:** Similar spirit to aggregating `player_match`, but Understat-native and lighter to refresh.

### 1.2 `get_team_data(season)`

**What it captures:** All 20 clubs for the season, each with a **per-match history** of team advanced stats (the data behind the league team table / progressive chart).

**Grain:** outer key = understat `team_id` → `{ id, title, history[] }` where each history row is one match.  
**Return:** `dict[team_id, team_blob]`

Team blob:

| Field | Meaning |
|---|---|
| `id` | Understat team id |
| `title` | Club name |
| `history` | List of match rows (length 38 for a completed season) |

Each `history[]` row:

| Field | Meaning |
|---|---|
| `date` | Kickoff datetime |
| `h_a` | `h` / `a` |
| `result` | `w` / `d` / `l` |
| `scored`, `missed` | Goals for / against |
| `xG`, `xGA`, `npxG`, `npxGA`, `npxGD` | Expected goals for/against (+ non-penalty) |
| `xpts` | Expected points |
| `wins`, `draws`, `loses`, `pts` | **Cumulative** table state after this match |
| `deep`, `deep_allowed` | Deep completions for / against |
| `ppda`, `ppda_allowed` | `{ att, def }` passes allowed per defensive action |

**Site use:** Team form, xG trendlines, PPDA / deep-completion style profiles — denser than your current `teams_gw` xG alone.  
**Note:** History rows do **not** include opponent name or match id; join via `league.get_match_data` on datetime + home/away.

### 1.3 `get_match_data(season)`

**What it captures:** Full EPL fixture list for the season (results + upcoming), with team objects, score, xG, and win/draw/loss forecast.

**Grain:** one row per fixture  
**Return:** `list[dict]`  
**EPL 2024:** 380 matches

| Field | Meaning |
|---|---|
| `id` | Understat match id |
| `isResult` | Played or not |
| `datetime` | Kickoff |
| `h`, `a` | `{ id, title, short_title }` |
| `goals` | `{ h, a }` (strings when played) |
| `xG` | `{ h, a }` |
| `forecast` | `{ w, d, l }` model probabilities (home win / draw / home loss) |

**Site use:** Fixture calendar, pre-match forecast chips, canonical understat `match_id` for deeper match pulls. Closest Understat analog to your `fixtures` master.

---

## 2. Team endpoint — `understat.team("Manchester_United")`

Webpage analog: club season page.

Team names use underscores (`Manchester_United`, `Nottingham_Forest`). Discover titles from `league.get_team_data` / `get_match_data`.

### 2.1 `get_player_data(season)`

**What it captures:** Season totals for players on that club (same field set as league player table, filtered to the squad).

**Grain:** `(season, team, understat_player_id)`  
**Fields:** same as §1.1

**Site use:** Club squad pages. Prefer **league** player pull as the season-wide source of truth; use team endpoint when you only need one club.

### 2.2 `get_match_data(season)`

**What it captures:** That club’s 38 fixtures with side, result, xG, and forecast (team-centric view of the league fixture list).

**Grain:** `(season, team, match_id)`  
**Extra vs league matches:** `side` (`h`/`a`), `result` (`w`/`d`/`l`)

**Site use:** Team schedule + results. Good companion to §1.2 history (this has opponent + match id; history has PPDA/deep/xpts).

### 2.3 `get_context_data(season)`

**What it captures:** Season-aggregated shot/xG splits for the team **and against**, sliced by context. This is Understat’s distinctive team “style” panel.

**Grain:** `(season, team, context_family, context_value)` after flattening  
**Return:** `dict` with top-level families:

| Family | Example keys | Typical metrics |
|---|---|---|
| `situation` | OpenPlay, FromCorner, SetPiece, Penalty, DirectFreekick | shots, goals, xG + `against` |
| `formation` | `4-2-3-1`, `3-4-2-1`, … | + `time` (minutes in that shape) |
| `gameState` | Goal diff 0, +1, -1, > +1, < -1 | + `time` |
| `timing` | 1-15, 16-30, …, 76+ | shots/goals/xG (+ against) |
| `shotZone` | shotSixYardBox, shotPenaltyArea, shotOboxTotal, ownGoals | same |
| `attackSpeed` | Fast, Normal, Slow, Standard | same |
| `result` | Goal, SavedShot, MissedShots, BlockedShot, ShotOnPost | same |

Each leaf is roughly `{ shots, goals, xG, against: { shots, goals, xG } }` (formation/gameState also include `time` / `stat`).

**Site use:** “How does this team create xG?” / set-piece vs open-play / formation minutes — content your Opta team_match table does not structure the same way.

---

## 3. Player endpoint — `understat.player("<id>")`

Webpage analog: player page. **No season argument** — methods return career history (filter to EPL / season at ingest).

Discover ids from `league.get_player_data`.

### 3.1 `get_match_data()`

**What it captures:** Per-match line for every league appearance in the player’s Understat career.

**Grain:** `(understat_player_id, match_id)`  
**Sample (Salah):** hundreds of rows across seasons

| Field | Meaning |
|---|---|
| `id` | Match id |
| `roster_id` | Appearance id (links to match roster) |
| `season` | Start year |
| `date` | Match date |
| `h_team`, `a_team`, `h_goals`, `a_goals` | Fixture context |
| `position` | Match position code (e.g. `AMR`, `FWR`) |
| `time` | Minutes |
| `goals`, `assists`, `shots`, `key_passes` | Match counting stats |
| `xG`, `xA`, `npg`, `npxG`, `xGChain`, `xGBuildup` | Match expected metrics |

**Site use:** Player form / xG over matches — natural join target next to your `player_match` (different provider; join on date+team or a future mapping table).

### 3.2 `get_shot_data()`

**What it captures:** Every shot the player has taken in tracked league matches (career).

**Grain:** one row per shot (`id` = shot id)  
**Sample (Salah):** ~1.3k shots

| Field | Meaning |
|---|---|
| `id` | Shot id |
| `player_id`, `player` | Shooter |
| `match_id`, `season`, `date`, `minute` | When |
| `h_a` | Home/away for the shooter |
| `X`, `Y` | Pitch coordinates (0–1 scale) |
| `xG` | Shot quality |
| `result` | Goal / SavedShot / MissedShots / BlockedShot / ShotOnPost / OwnGoal / … |
| `situation` | OpenPlay, FromCorner, SetPiece, Penalty, DirectFreekick |
| `shotType` | LeftFoot, RightFoot, Head, OtherBodyPart |
| `player_assisted` | Assist name (nullable) |
| `lastAction` | Preceding action label (Pass, Cross, …) |
| `h_team`, `a_team`, `h_goals`, `a_goals` | Match context |

**Site use:** Shot maps, npxG rebuilds, set-piece vs open-play player profiles. Highest-value unique Understat asset for the site.

### 3.3 `get_season_data()`

**What it captures:** Career breakdowns nested by season (and sometimes by subcategory).

**Return shape:**

```
{
  "season":    [ { season, team, games, goals, xG, ... }, ... ],  # list
  "position":  { "2024": { "FWR": {...}, "Sub": {...} }, ... },
  "situation": { "2024": { "OpenPlay": {...}, ... }, ... },
  "shotZones": { "2024": { "shotPenaltyArea": {...}, ... }, ... },
  "shotTypes": { "2024": { "LeftFoot": {...}, ... }, ... }
}
```

`season[]` rows include `team`, minutes (`time`), cards (`yellow`/`red`), and the usual xG family. Nested dicts break the same season into position / situation / zone / body-part slices.

**Site use:** Pre-aggregated career charts without recomputing from shots. For EPL-only DB, filter `season` rows / years carefully (player careers span clubs/leagues; situation splits are not always league-tagged).

---

## 4. Match endpoint — `understat.match("<id>")`

Webpage analog: single match centre. Ids from `league.get_match_data` / team match data.

### 4.1 `get_shot_data()`

**What it captures:** All shots in the match, split home/away.

**Return:** `{ "h": [shot, ...], "a": [shot, ...] }`  
**Shot fields:** same schema as §3.2

**Site use:** Match shot map, xG timeline (by `minute`). Prefer this over player shots when building match pages.

### 4.2 `get_roster_data()`

**What it captures:** Both squads’ player-match lines (starters + subs), keyed by `roster_id`.

**Return:** `{ "h": { roster_id: player_row, ... }, "a": { ... } }`

| Field | Meaning |
|---|---|
| `id` | Roster / appearance id |
| `player_id`, `player` | Understat player |
| `team_id` | Understat team |
| `position`, `positionOrder` | Role + sort order |
| `time` | Minutes |
| `goals`, `own_goals`, `assists`, `shots`, `key_passes` | Counting |
| `xG`, `xA`, `xGChain`, `xGBuildup` | Expected |
| `yellow_card`, `red_card` | Cards |
| `roster_in`, `roster_out` | Sub on/off roster ids (`"0"` if none) |
| `h_a` | Side |

**Site use:** Match lineups + per-player understat line. Best bridge from match → player id for that game.

### 4.3 `get_match_info()`

**What it captures:** Match header / summary block (scores, xG, shots, deep, PPDA, forecast, league metadata).

| Field | Meaning |
|---|---|
| `id`, `fid` | Understat id + secondary fixture id |
| `league`, `league_id`, `season` | Competition context (`EPL`, `1`, `2024`) |
| `team_h`, `team_a`, `h`, `a` | Names + understat team ids |
| `date` | Kickoff |
| `h_goals`, `a_goals`, `h_xg`, `a_xg` | Scoreline + xG |
| `h_w`, `h_d`, `h_l` | Forecast probabilities |
| `h_shot`, `a_shot`, `h_shotOnTarget`, `a_shotOnTarget` | Shot volumes |
| `h_deep`, `a_deep`, `h_ppda`, `a_ppda` | Style summary |
| `isData` | Whether detailed data is present |

**Site use:** Match header cards; lighter than pulling full shot lists when you only need the summary.

---

## Entity map (join keys)

| Entity | Understat key | Notes for FPL Pulse |
|---|---|---|
| League | `EPL` | Fixed for v1 |
| Season | `"2024"` | Map ↔ `2024-2025` |
| Team | `id` + `title` / underscore slug | Need mapping ↔ `team_code` |
| Player | `id` (stable) | Need mapping ↔ `player_code` (name+team+fuzzy) |
| Match | `id` | Need mapping ↔ your `match_id` (kickoff + home/away) |
| Shot | `id` | Understat-only |
| Roster line | `roster_id` / roster `id` | Links player ↔ match |

Until a mapping table exists, keep Understat as a **parallel master** keyed by understat ids; join into serving JSON only where mapping confidence is high.

---

## Recommended build order (when we leave exploration)

1. **League fixtures + players** (`get_match_data`, `get_player_data`) — index tables.  
2. **Team history + context** (`get_team_data` history, `get_context_data`) — team analytics.  
3. **Match roster + shots + info** for completed EPL matches — match centre grain.  
4. **Player shots / player matches** selectively (current season first; career backfill later).  
5. **ID mapping** to `player_code` / `team_code` / FPL `match_id`.  
6. **Serving JSON** compact projections for the site (short keys like existing `players_matches.json` if payload size matters).

---

## Caveats

- Unofficial scraper; be polite (session reuse via context manager, cache, incremental by season).  
- Strings vs numbers mixed in payloads — normalize in the pipeline.  
- `team_title` / multi-club seasons and player `get_season_data` can span non-EPL clubs — filter explicitly.  
- Understat position codes ≠ FPL positions.  
- xG definitions differ from Opta and FPL; always namespace columns (`understat_xg`, etc.).  
- `fpl-pulse-talk` GitHub tree was not readable from this environment (404/private); storage guidance above follows **this** repo’s parquet masters + `web/data` serving pattern, which matches the dashboard already in `web/`.

---

## Quick method checklist

| Endpoint | Method | Season arg? | Primary grain |
|---|---|---|---|
| league | `get_player_data` | yes | player-season |
| league | `get_team_data` | yes | team → match history |
| league | `get_match_data` | yes | fixture |
| team | `get_player_data` | yes | player-season (club) |
| team | `get_match_data` | yes | team-fixture |
| team | `get_context_data` | yes | team-season context slices |
| player | `get_match_data` | no (career) | player-match |
| player | `get_shot_data` | no (career) | shot |
| player | `get_season_data` | no (career) | player-season (+ slices) |
| match | `get_shot_data` | no | match shots h/a |
| match | `get_roster_data` | no | match roster lines |
| match | `get_match_info` | no | match summary |

Next step when you’re ready: pick seasons (e.g. current + last complete) and sketch the parquet schemas / mapping approach before writing ingest code.
