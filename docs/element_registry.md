# Element registry

The italic **i** appears only when you hover a named label (not on changing values). Click to copy.

| Name | What it is |
|---|---|
| `nav.*` | Sidebar and page links |
| `nav.collapse` / `nav.topbar` | Collapse control and workspace bar |
| `nav.insights.players` / `.matches` / `.teams` / `.understat` / `.sofascore` / `.sofascore_sides` / `.fpl_treemap` / `.player_performance` / `.team_performance` | Insights subpages |
| `home.title` / `home.meta` / `home.jumps` | Home |
| `fixtures.title` / `fixtures.gwlabel` / `fixtures.controls` | Fixtures heading and GW note |
| `fixtures.filter.competition` | Fixtures competition (multi-select) |
| `fixtures.cards` | Current-GW match cards (no per-card `i`) |
| `fixtures.ticker` | Next-6-GW ticker |
| `{view}.title` | Attackers / Defenders / GK / Teams heading |
| `{view}.controls` | Filter cluster |
| `{view}.filter.season` | Season year (multi-select) |
| `{view}.filter.competition` | Competition / tournament (multi-select) |
| `{view}.filter.venue` | Home / away (multi-select) |
| `{view}.filter.range` | Exact GW from–to |
| `{view}.filter.position` | Attackers MID/FWD (multi-select) |
| `{view}.filter.players` | Player picker (multi-select) |
| `{view}.filter.mins` | Min minutes / appearance |
| `{view}.filter.cost` | FPL price range (£m) |
| `{view}.filter.search` | Search |
| `{view}.filter.per90` | Per-90 toggle |
| `{view}.filter.detail` | Always-visible metric-group buttons |
| `{view}.table` / `{view}.grid` / `{view}.showing` | Table chrome |
| `players.drawer` / `players.drawer.body` | Gameweek drawer opened from a player name |
| `{view}.col.{metric}` | A column header |
| `insights.players.*` / `insights.matches.*` / `insights.teams.*` | Insight filters and titles |
| `insights.matches.board` / `insights.matches.grid` | Match insight containers |
| `insights.understat.title` | Understat page heading |
| `insights.sofascore.title` / `insights.sofascore_sides.title` | SofaScore explore headings |
| `shots.*` | Understat explore chrome (views, filters, chart) |
| `ss.shots.*` / `ss.team_sides.*` | SofaScore explore chrome |
| `shots.drawer` | Player/team shot-mix drawer |
| `us-tip` / `.tip` | Treemap hover (moved to `document.body` for positioning) |
| `insights.fpl_treemap.title` | FPL player treemap heading |
| `fpl_treemap.controls.metric` / `.sort` / `.extra` / `.gw` / `.teams` | FPL treemap metric, tile-size, extra metrics, gameweek, and team filters |
| `fpl_treemap.status` / `.chart` | FPL treemap status and visualization |
| `insights.team_performance.title` / `team_performance.controls.*` / `.chart` | Team performances scatter |
