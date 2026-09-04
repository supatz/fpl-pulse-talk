import { FDR_URL, INSIGHT_WINDOWS, VIEWS } from "./registry.js";
import {
  aggregatePlayers,
  aggregateTeamRows,
  computeInsights,
  computeMatchInsights,
  computeTeamInsights,
  decorateNames,
  initTooltip,
  lastGwSlice,
  loadState,
  makeMultiSelect,
  makeTable,
  matchFilterOptions,
  renderCards,
  renderFixtureCards,
  renderInsightList,
  renderMatchBoard,
  renderTicker,
  saveState,
} from "./components.js";

const DATA = {};
const FILES = ["meta.json", "players_matches.json", "fixtures.json", "teams_gw.json"];
const PAGES = [
  "home",
  "fixtures",
  "attackers",
  "defenders",
  "gk",
  "insights-players",
  "insights-matches",
  "insights-teams",
  "insights-understat",
  "teams",
  "chips",
  "data",
];
const INSIGHT_PAGES = ["insights-players", "insights-matches", "insights-teams", "insights-understat"];

async function loadData() {
  const results = await Promise.all(
    FILES.map(async (name) => {
      const res = await fetch(`./data/${name}`, { cache: "no-store" });
      if (!res.ok) throw new Error(`Could not load ${name} (${res.status})`);
      return [name.replace(".json", ""), await res.json()];
    })
  );
  results.forEach(([k, v]) => {
    DATA[k] = v;
  });
}

const PAGE_TITLES = {
  home: "Home",
  fixtures: "Fixtures",
  attackers: "Attackers",
  defenders: "Defenders",
  gk: "Goalkeepers",
  "insights-players": "Insights · Players",
  "insights-matches": "Insights · Matches",
  "insights-teams": "Insights · Teams",
  "insights-understat": "Insights · Understat",
  teams: "Teams",
  chips: "Chips",
  data: "Data",
};

function showPage(id) {
  id = String(id || "").replace(/^#/, "");
  if (id === "insights") id = "insights-players";
  const hasPage = Boolean(document.getElementById(`page-${id}`));
  const page = hasPage ? id : "home";
  document.querySelectorAll("main > .page").forEach((p) => {
    p.hidden = p.id !== `page-${page}`;
  });
  document.querySelectorAll("[data-page]").forEach((a) => {
    const isPlayers = ["attackers", "defenders", "gk"].includes(page);
    const isInsights = INSIGHT_PAGES.includes(page);
    a.classList.toggle(
      "active",
      a.dataset.page === page || (isPlayers && a.dataset.page === "players") || (isInsights && a.dataset.page === "insights")
    );
  });
  const title = document.getElementById("topbar-title");
  if (title) title.textContent = PAGE_TITLES[page] || page;
  document.querySelectorAll(".nav-block").forEach((block) => {
    const g = block.dataset.group;
    const open =
      (g === "players" && ["attackers", "defenders", "gk"].includes(page)) ||
      (g === "insights" && INSIGHT_PAGES.includes(page));
    block.classList.toggle("is-open", open);
  });
  const app = document.getElementById("app");
  const scrim = document.getElementById("nav-scrim");
  if (app && window.matchMedia("(max-width: 860px)").matches) {
    app.classList.remove("is-open");
    if (scrim) scrim.hidden = true;
  }
  if (location.hash !== `#${page}`) history.replaceState(null, "", `#${page}`);
  if (page === "insights-understat") {
    requestAnimationFrame(() => {
      try {
        window.initUnderstatShots?.();
      } catch (err) {
        const status = document.getElementById("us-status");
        if (status) status.textContent = `Understat view failed to start: ${err.message}`;
      }
    });
  }
}

function wireShell() {
  const app = document.getElementById("app");
  const scrim = document.getElementById("nav-scrim");
  if (!app) return;
  app.classList.toggle("is-collapsed", localStorage.getItem("fplpulse.nav") === "1");
  document.getElementById("sidebar-collapse")?.addEventListener("click", () => {
    app.classList.toggle("is-collapsed");
    localStorage.setItem("fplpulse.nav", app.classList.contains("is-collapsed") ? "1" : "0");
  });
  document.getElementById("sidebar-open")?.addEventListener("click", () => {
    app.classList.add("is-open");
    if (scrim) scrim.hidden = false;
  });
  scrim?.addEventListener("click", () => {
    app.classList.remove("is-open");
    scrim.hidden = true;
  });
  document.querySelectorAll(".nav-parent").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      btn.closest(".nav-block")?.classList.toggle("is-open");
    });
  });
}

function wireNav() {
  document.querySelectorAll("[data-page]").forEach((el) => {
    el.addEventListener("click", (e) => {
      const page = el.dataset.page;
      if (!page || page === "players" || page === "insights") return;
      e.preventDefault();
      e.stopPropagation();
      showPage(page);
    });
  });
  window.addEventListener("hashchange", () => showPage(location.hash.replace("#", "")));
}

function metaCtx() {
  const meta = DATA.meta || {};
  return {
    meta,
    seasons: meta.seasons || [meta.analysis_season, meta.current_season].filter(Boolean),
    competitions: meta.competitions || [],
    roster: new Set(meta.roster_codes || []),
    prices: meta.prices || {},
  };
}

function renderHome() {
  const { meta } = metaCtx();
  const line = document.getElementById("home-meta");
  if (line) {
    line.textContent = [
      meta.built_at_utc ? `Snapshot ${meta.built_at_utc}` : null,
      meta.current_season ? `Season ${meta.current_season}` : null,
      meta.upcoming_gw != null ? `Live GW ${meta.upcoming_gw}` : null,
    ]
      .filter(Boolean)
      .join(" · ");
  }
  renderCards("home-jumps", [
    { name: "home.jump.fixtures", href: "#fixtures", kicker: "Next", title: "Fixtures", value: meta.upcoming_gw != null ? `GW ${meta.upcoming_gw}` : "—", meta: "One gameweek of cards" },
    { name: "home.jump.attackers", href: "#attackers", kicker: "Players", title: "Attackers", value: "MID + FWD", meta: "xGI and creation" },
    { name: "home.jump.defenders", href: "#defenders", kicker: "Players", title: "Defenders", value: "DEF", meta: "CS + DefCon/90" },
    { name: "home.jump.gk", href: "#gk", kicker: "Players", title: "Goalkeepers", value: "GK", meta: "xG prevented" },
    { name: "home.jump.insights", href: "#insights-players", kicker: "Watch", title: "Insights", value: "Players · Matches · Teams", meta: "Compact lists + match boards" },
    { name: "home.jump.teams", href: "#teams", kicker: "Clubs", title: "Teams", value: "Last N GW", meta: "Home / away split" },
  ]);
}

function renderFixtures() {
  const fx = DATA.fixtures || {};
  const { meta } = metaCtx();
  const host = document.getElementById("fixtures-cards");
  const bar = document.getElementById("fixtures-comp-host");
  const persisted = loadState("fixtures");
  const state = { competitions: persisted.competitions || ["Premier League"] };
  if (bar && !bar.dataset.ready) {
    const comps = ["Premier League", ...(meta.competitions || [])].filter((v, i, a) => a.indexOf(v) === i);
    const ms = makeMultiSelect({
      name: "fixtures.filter.competition",
      label: "Competition",
      tip: "Default is Premier League. Multi-select.",
      options: comps.map((c) => ({ value: c, label: c })),
      selected: state.competitions,
      onChange: (v) => {
        state.competitions = v;
        saveState("fixtures", state);
        paint();
      },
    });
    bar.innerHTML = "";
    bar.appendChild(ms.el);
    bar.dataset.ready = "1";
    decorateNames(bar);
  }
  function paint() {
    const upcoming = (fx.upcoming || []).filter((f) => !state.competitions.length || state.competitions.includes(f.competition));
    renderFixtureCards(host, upcoming, { competition: "all" });
  }
  paint();
  renderTicker("fixtures-ticker", fx.ticker);
  const link = document.getElementById("fdr-link");
  if (link) link.href = fx.fdr_url || FDR_URL;
}

function renderPlayerView(key) {
  const cfg = VIEWS[key];
  const { meta, seasons, competitions, roster, prices } = metaCtx();
  makeTable({
    el: `${key}-root`,
    view: key,
    columns: cfg.columns,
    extraColumns: cfg.extraColumns,
    metricGroups: cfg.metricGroups,
    defaultSort: cfg.defaultSort,
    defaultDir: cfg.defaultDir,
    per90Keys: cfg.per90Keys,
    always90Keys: cfg.always90Keys,
    minMinsDefault: cfg.minMinsDefault,
    positionFilter: cfg.positionFilter,
    positions: cfg.positions,
    competitions,
    seasons,
    season: meta.analysis_season,
    roster,
    rows: (state) =>
      aggregatePlayers(DATA.players_matches, { ...state, positions: cfg.positions }, { prices }),
  });
}

function renderTeams() {
  const cfg = VIEWS.teams;
  const { meta, seasons, competitions } = metaCtx();
  makeTable({
    ...cfg,
    el: "teams-root",
    view: "teams",
    competitions,
    seasons,
    season: meta.analysis_season,
    rows: (state) => aggregateTeamRows(DATA.teams_gw, state),
  });
}

function asList(v, fallback) {
  if (Array.isArray(v) && v.length) return v;
  if (v && v !== "all") return [v];
  return fallback;
}

function insightBaseState(key, extra = {}) {
  const { meta, seasons, competitions, roster } = metaCtx();
  const persisted = loadState(key);
  return {
    seasons: asList(persisted.seasons || persisted.season, [meta.analysis_season].filter(Boolean)),
    competitions: asList(persisted.competitions || persisted.competition, ["Premier League"]),
    venues: asList(persisted.venues || persisted.venue, ["H", "A"]),
    window: persisted.window || 5,
    currentOnly: true,
    roster,
    seasonsAll: seasons,
    competitionsAll: ["Premier League", ...competitions.filter((c) => c !== "Premier League")],
    ...extra,
    ...Object.fromEntries(Object.entries(persisted).filter(([k]) => ["gws", "matches", "gwFrom", "gwTo"].includes(k))),
  };
}

function mountGlobalInsightFilters(host, namePrefix, state, extras, render) {
  host.className = "insight-filters";
  host.dataset.name = `${namePrefix}.controls`;
  host.innerHTML = "";
  const seasonMs = makeMultiSelect({
    name: `${namePrefix}.filter.season`,
    label: "Season",
    tip: "Season year. Multi-select.",
    options: state.seasonsAll.map((s) => ({ value: s, label: s })),
    selected: state.seasons,
    onChange: (v) => {
      state.seasons = v;
      render();
    },
  });
  const compMs = makeMultiSelect({
    name: `${namePrefix}.filter.competition`,
    label: "Competition",
    tip: "Competition / tournament. Multi-select.",
    options: state.competitionsAll.map((c) => ({ value: c, label: c })),
    selected: state.competitions,
    onChange: (v) => {
      state.competitions = v;
      render();
    },
  });
  const venueMs = makeMultiSelect({
    name: `${namePrefix}.filter.venue`,
    label: "Venue",
    tip: "Home / away. Multi-select.",
    options: [
      { value: "H", label: "Home" },
      { value: "A", label: "Away" },
    ],
    selected: state.venues,
    onChange: (v) => {
      state.venues = v;
      render();
    },
  });
  host.append(seasonMs.el, compMs.el, venueMs.el, ...extras);
  decorateNames(host);
}

function renderInsightsPlayers() {
  const { prices } = metaCtx();
  const host = document.getElementById("insights-players-controls");
  if (!host) return;
  const state = insightBaseState("insights-players");
  const idx = Math.max(0, INSIGHT_WINDOWS.indexOf(state.window));
  const win = document.createElement("label");
  win.className = "ctrl";
  win.dataset.name = "insights.players.filter.window";
  win.dataset.tip = "Last N gameweeks, capped at 10.";
  win.innerHTML = `<span class="ctrl-copy"><span data-window-label>Last ${state.window} GW</span>
    <input type="range" min="0" max="${INSIGHT_WINDOWS.length - 1}" value="${idx}" /></span>`;
  win.querySelector("input").addEventListener("input", (e) => {
    state.window = INSIGHT_WINDOWS[Number(e.target.value)] || 5;
    win.querySelector("[data-window-label]").textContent = `Last ${state.window} GW`;
    paint();
  });
  const paint = () => {
    saveState("insights-players", state);
    const ins = computeInsights(DATA.players_matches, { ...state, positions: ["Forward", "Midfielder"] }, { prices });
    renderInsightList("insights-topxgi", ins.top_xgi);
    renderInsightList("insights-rising", ins.rising);
    renderInsightList("insights-finishing", ins.finishing);
    renderInsightList("insights-quiet", ins.quiet);
  };
  mountGlobalInsightFilters(host, "insights.players", state, [win], paint);
  paint();
}

function renderInsightsMatches() {
  const host = document.getElementById("insights-matches-controls");
  if (!host) return;
  const { meta } = metaCtx();
  const state = insightBaseState("insights-matches", {
    seasons: [meta.current_season || meta.analysis_season].filter(Boolean),
    competitions: ["Premier League"],
    gws: [],
    matches: [],
  });
  let gwMs;
  let matchMs;
  const paint = () => {
    saveState("insights-matches", state);
    const opts = matchFilterOptions(DATA.teams_gw, state);
    const last = lastGwSlice(
      (DATA.teams_gw || []).filter((r) => r.finished && r.season === (meta.current_season || meta.analysis_season) && r.competition === "Premier League"),
      1
    );
    if (!state.gws.length && last.to != null) state.gws = [last.to];
    gwMs?.setOptions(
      opts.gws.map((g) => ({ value: String(g), label: `GW ${g}` })),
      (state.gws || []).map(String)
    );
    if (matchMs) {
      matchMs.setOptions(opts.matches, state.matches);
    }
    const gws = (state.gws || []).map(Number).filter(Boolean);
    const bundles = computeMatchInsights(DATA.players_matches, DATA.teams_gw, { ...state, gws });
    const headline = gws.length === 1 ? `Gameweek ${gws[0]} — finished Premier League matches.` : `Selected gameweeks: ${gws.join(", ") || "all"}.`;
    renderMatchBoard("insights-matches-board", bundles, { headline });
  };
  gwMs = makeMultiSelect({
    name: "insights.matches.filter.gw",
    label: "Gameweek",
    tip: "Choose one or more finished gameweeks.",
    options: [],
    selected: [],
    onChange: (v) => {
      state.gws = v.map(Number);
      state.matches = [];
      paint();
    },
  });
  matchMs = makeMultiSelect({
    name: "insights.matches.filter.match",
    label: "Match",
    tip: "Leave on All to see every match in the selected GWs.",
    options: [],
    selected: [],
    searchable: true,
    onChange: (v) => {
      state.matches = v;
      paint();
    },
  });
  mountGlobalInsightFilters(host, "insights.matches", state, [gwMs.el, matchMs.el], paint);
  paint();
}

function renderInsightsTeams() {
  const host = document.getElementById("insights-teams-controls");
  if (!host) return;
  const state = insightBaseState("insights-teams");
  const idx = Math.max(0, INSIGHT_WINDOWS.indexOf(state.window));
  const win = document.createElement("label");
  win.className = "ctrl";
  win.dataset.name = "insights.teams.filter.window";
  win.dataset.tip = "Last N gameweeks, capped at 10.";
  win.innerHTML = `<span class="ctrl-copy"><span data-window-label>Last ${state.window} GW</span>
    <input type="range" min="0" max="${INSIGHT_WINDOWS.length - 1}" value="${idx}" /></span>`;
  win.querySelector("input").addEventListener("input", (e) => {
    state.window = INSIGHT_WINDOWS[Number(e.target.value)] || 5;
    win.querySelector("[data-window-label]").textContent = `Last ${state.window} GW`;
    paint();
  });
  const paint = () => {
    saveState("insights-teams", state);
    const scoped = (DATA.teams_gw || []).filter(
      (r) =>
        r.finished &&
        (!state.seasons.length || state.seasons.includes(r.season)) &&
        (!state.competitions.length || state.competitions.includes(r.competition))
    );
    const winSlice = lastGwSlice(scoped, state.window);
    const ins = computeTeamInsights(DATA.teams_gw, { ...state, gwFrom: winSlice.from, gwTo: winSlice.to });
    renderInsightList("insights-team-attack", ins.attack);
    renderInsightList("insights-team-defend", ins.defend);
    renderInsightList("insights-team-over", ins.over);
    renderInsightList("insights-team-leak", ins.leak);
  };
  mountGlobalInsightFilters(host, "insights.teams", state, [win], paint);
  paint();
}

function renderData() {
  const { meta } = metaCtx();
  const box = document.getElementById("data-notes");
  if (box) box.innerHTML = (meta.notes || []).map((n) => `<li>${n}</li>`).join("");
  const facts = document.getElementById("data-facts");
  if (facts) {
    facts.innerHTML = [
      ["Source", meta.source],
      ["Built", meta.built_at_utc],
      ["Schema", meta.schema_version],
      ["Current season", meta.current_season],
      ["Current squad", meta.counts?.roster],
    ]
      .map(([k, v]) => `<div><dt>${k}</dt><dd>${v ?? "—"}</dd></div>`)
      .join("");
  }
}

function bootError(err) {
  const banner = document.getElementById("boot-error");
  if (!banner) return;
  banner.hidden = false;
  banner.textContent = `${err.message}. Serve via python serve.py so ./data/*.json can load.`;
}

async function main() {
  initTooltip();
  wireShell();
  wireNav();
  decorateNames(document);
  try {
    await loadData();
  } catch (err) {
    bootError(err);
    showPage("home");
    return;
  }
  renderHome();
  renderFixtures();
  renderPlayerView("attackers");
  renderPlayerView("defenders");
  renderPlayerView("gk");
  renderInsightsPlayers();
  renderInsightsMatches();
  renderInsightsTeams();
  renderTeams();
  renderData();
  showPage(location.hash.replace("#", "") || "home");
}

main();
