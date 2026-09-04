/* Understat shot explore — treemap + linked matrix views */
const DATA_URL = "./data/us_shot_treemap.json";
const TOP_N = 5;
const TOP_TEAMS = 10;
const HEADER_H = 42;
const MIN_FONT = 5;

/** Soft pastel palette from design swatch (16). */
const PALETTE = [
  "#fff699",
  "#fee8c3",
  "#ffcfa1",
  "#fbaea6",
  "#e9ed98",
  "#b6eea7",
  "#a6f5d8",
  "#b7e7f3",
  "#a1c4fc",
  "#d5bcfe",
  "#ffbdfb",
  "#feb9cc",
  "#bcaea1",
  "#d2c09a",
  "#dddddd",
  "#66747f",
];

/** Soft categorical palette for mix slices — higher contrast pastels. */
const SLICE_COLORS = [
  "#6ea0f0",
  "#3dba9a",
  "#e0a050",
  "#9b7ed9",
  "#e07a8a",
  "#5aa6b5",
  "#8f9a6a",
  "#c48a6a",
];

const state = {
  data: null,
  view: "treemap",
  season: "2026-2027",
  metric: "xg",
  situations: new Set(), // empty = all situations
  per90: false,
  againstDim: "situation",
  teams: new Set(),
  drawer: null,
  focusTeam: null,
  focusSlices: new Set(), // multi-select legend filters on linked mix
};

const els = {};
let started = false;
let eventsBound = false;

function $(id) {
  return document.getElementById(id);
}

async function init() {
  if (started) {
    if (els.chart && els.chart.clientWidth) render();
    return;
  }
  bindEls();
  if (!els.chart) return;
  started = true;
  bindEvents();
  if (!$("app")) decorateNames(document.querySelector(".us-shots") || document);
  try {
    state.data = await fetch(DATA_URL).then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    });
    populateSeasons();
    populateSituations();
    resetPresetTeams();
    populateTeams();
    if (typeof d3 === "undefined") throw new Error("Chart library missing (vendor/d3.min.js).");
    setView("treemap");
  } catch (err) {
    if (els.status) els.status.textContent = `Failed to load ${DATA_URL}: ${err.message}`;
  }
}

window.initUnderstatShots = init;
if (document.body?.classList.contains("us-shots-standalone")) {
  document.addEventListener("DOMContentLoaded", init);
}

function bindEls() {
  const root = document.querySelector(".us-shots") || document;
  els.season = $("us-season");
  els.metric = $("us-metric");
  els.metricLabel = $("us-metric-label");
  els.sitToggle = $("us-situations-toggle");
  els.sitMenu = $("us-situations-menu");
  els.sitDrop = $("us-situations-drop");
  els.per90 = $("us-per90");
  els.againstDim = $("us-against-dim");
  els.againstWrap = $("us-against-dim-wrap");
  els.teams = $("us-team-pills");
  els.topTeamsBtn = $("us-top-teams");
  els.chart = $("us-chart");
  els.matrix = $("us-matrix");
  els.status = $("us-status");
  els.footnote = $("us-footnote");
  els.drawer = $("us-drawer");
  els.drawerTitle = $("us-drawer-title");
  els.drawerBody = $("us-drawer-body");
  els.tip = $("us-tip");
  els.defs = $("us-defs");
  els.tabs = [...root.querySelectorAll("[data-view]")];
}

function bindEvents() {
  if (eventsBound) return;
  eventsBound = true;
  els.tabs.forEach((btn) => btn.addEventListener("click", () => setView(btn.dataset.view)));
  els.season.addEventListener("change", () => {
    state.season = els.season.value;
    state.focusTeam = null;
    state.focusSlices.clear();
    resetPresetTeams();
    populateTeams();
    render();
  });
  els.metric.addEventListener("change", () => {
    state.metric = els.metric.value;
    render();
    if (state.drawer && !els.drawer.hidden) openDrawer(state.drawer.team, state.drawer.player);
  });
  els.per90.addEventListener("change", () => {
    state.per90 = els.per90.checked;
    render();
    if (state.drawer && !els.drawer.hidden) openDrawer(state.drawer.team, state.drawer.player);
  });
  els.againstDim.addEventListener("change", () => {
    state.againstDim = els.againstDim.value;
    if (state.view === "against") render();
  });
  els.sitToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    const open = els.sitMenu.hidden;
    els.sitMenu.hidden = !open;
    els.sitToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("click", (e) => {
    if (!els.sitDrop.contains(e.target)) {
      els.sitMenu.hidden = true;
      els.sitToggle.setAttribute("aria-expanded", "false");
    }
  });
  $("us-all-teams").addEventListener("click", () => {
    state.teams = new Set(seasonTeamsAll().map((t) => String(t.team_code)));
    populateTeams();
    render();
  });
  els.topTeamsBtn.addEventListener("click", () => {
    resetPresetTeams();
    populateTeams();
    render();
  });
  $("us-help-open").addEventListener("click", () => {
    fillDefs();
    els.defs.showModal();
  });
  $("us-drawer-close").addEventListener("click", () => {
    els.drawer.hidden = true;
    state.drawer = null;
  });
  window.addEventListener("resize", debounce(() => {
    if (els.chart && els.chart.clientWidth) render();
  }, 120));
}

function decorateNames(root) {
  root.querySelectorAll("[data-name]").forEach((el) => {
    if (el.querySelector(":scope > .name-dot")) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "name-dot";
    btn.title = el.dataset.name;
    btn.setAttribute("aria-label", `Copy element name ${el.dataset.name}`);
    btn.textContent = "i";
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      try {
        await navigator.clipboard.writeText(el.dataset.name);
        btn.classList.add("copied");
        setTimeout(() => btn.classList.remove("copied"), 900);
      } catch {
        /* ignore */
      }
    });
    el.insertBefore(btn, el.firstChild);
  });
}

function populateSeasons() {
  const seasons = state.data.seasons || [];
  els.season.innerHTML = seasons.map((s) => `<option value="${s}">${s}</option>`).join("");
  state.season = state.data.default_season || state.season;
  if (!seasons.includes(state.season)) state.season = seasons[0] || state.season;
  els.season.value = state.season;
}

function populateSituations() {
  const order = state.data.situation_order || [];
  const allOn = !state.situations.size;
  els.sitMenu.innerHTML =
    `<label class="ms-opt"><input type="checkbox" data-sit="all" ${allOn ? "checked" : ""}/> All situations</label>` +
    order
      .map((s) => {
        const on = !allOn && state.situations.has(s);
        return `<label class="ms-opt"><input type="checkbox" data-sit="${s}" ${on ? "checked" : ""}/> ${s}</label>`;
      })
      .join("");

  updateSituationsToggleLabel();

  els.sitMenu.querySelectorAll("input").forEach((input) => {
    input.addEventListener("change", () => {
      const sit = input.dataset.sit;
      if (sit === "all") {
        state.situations.clear();
      } else if (input.checked) {
        state.situations.add(sit);
      } else {
        state.situations.delete(sit);
      }
      populateSituations();
      render();
      if (state.drawer && !els.drawer.hidden) openDrawer(state.drawer.team, state.drawer.player);
    });
  });
}

function updateSituationsToggleLabel() {
  if (!state.situations.size) {
    els.sitToggle.textContent = "All situations";
    return;
  }
  const list = [...state.situations];
  els.sitToggle.textContent =
    list.length <= 2 ? list.join(", ") : `${list.length} situations`;
}

function shortSit(s) {
  return (
    {
      DirectFreekick: "FK",
      FromCorner: "Corner",
      OpenPlay: "Open",
      Penalty: "Pen",
      SetPiece: "SP",
    }[s] || s
  );
}

/** Active situation filter set; empty means all. */
function activeSituations() {
  if (!state.situations.size) return null;
  return state.situations;
}

/** All teams in the selected season (for filter pills). */
function seasonTeamsAll() {
  return (state.data.teams || []).filter((t) => t.season === state.season);
}

function priorSeason() {
  const seasons = state.data.seasons || [];
  const i = seasons.indexOf(state.season);
  if (i > 0) return seasons[i - 1];
  return state.season;
}

function topTeamCodesByLastYearXg() {
  const ref = priorSeason();
  const present = new Set(seasonTeamsAll().map((t) => String(t.team_code)));
  return (state.data.teams || [])
    .filter((t) => t.season === ref)
    .slice()
    .sort((a, b) => (b.xg || 0) - (a.xg || 0))
    .map((t) => String(t.team_code))
    .filter((c) => present.has(c))
    .slice(0, TOP_TEAMS);
}

/** xGC = sum of against-situation xGA for the current season. */
function teamXgc(t) {
  return (t.against_situation || []).reduce((a, r) => a + (Number(r.xga) || 0), 0);
}

function bottomTeamCodesByXgc() {
  return seasonTeamsAll()
    .slice()
    .sort((a, b) => teamXgc(b) - teamXgc(a))
    .slice(0, TOP_TEAMS)
    .map((t) => String(t.team_code));
}

function isAgainstView() {
  return state.view === "against";
}

function resetPresetTeams() {
  const codes = isAgainstView() ? bottomTeamCodesByXgc() : topTeamCodesByLastYearXg();
  state.teams = new Set(codes);
}

function updateAgainstControls() {
  const against = isAgainstView();
  if (els.metricLabel) els.metricLabel.textContent = against ? "Metric (Against)" : "Metric";
  if (els.topTeamsBtn) {
    els.topTeamsBtn.textContent = against ? "Bottom 10" : "Top 10";
    els.topTeamsBtn.title = against
      ? "Select 10 teams with highest xGC (xG conceded)"
      : "Select top 10 by prior-season xG created";
  }
}

function populateTeams() {
  const teams = seasonTeamsAll()
    .slice()
    .sort((a, b) => a.team_short.localeCompare(b.team_short));
  const preset = new Set(isAgainstView() ? bottomTeamCodesByXgc() : topTeamCodesByLastYearXg());
  els.teams.innerHTML = teams
    .map((t) => {
      const code = String(t.team_code);
      const on = state.teams.has(code);
      const isPreset = preset.has(code);
      const tip = isAgainstView()
        ? isPreset
          ? `Bottom 10 by xGC (${fmt(teamXgc(t))})`
          : t.team || t.team_short
        : isPreset
          ? "Top 10 by prior-season xG"
          : t.team || t.team_short;
      return `<button type="button" class="pill ${on ? "on" : ""} ${isPreset ? "is-top" : ""}" data-code="${code}" title="${tip}">${t.team_short}</button>`;
    })
    .join("");
  els.teams.querySelectorAll(".pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      const code = btn.dataset.code;
      if (state.teams.has(code)) state.teams.delete(code);
      else state.teams.add(code);
      if (!state.teams.size) resetPresetTeams();
      populateTeams();
      render();
    });
  });
}

/** Teams currently shown in charts (selected pills; default top/bottom 10). */
function visibleTeams() {
  const all = seasonTeamsAll();
  if (!state.teams.size) {
    const preset = new Set(isAgainstView() ? bottomTeamCodesByXgc() : topTeamCodesByLastYearXg());
    return all.filter((t) => preset.has(String(t.team_code)));
  }
  return all.filter((t) => state.teams.has(String(t.team_code)));
}

function metricKey() {
  const m = state.metric;
  if (state.per90) {
    if (m === "xg") return "xg_p90";
    if (m === "shots") return "shots_p90";
    if (m === "sot") return "sot_p90";
    if (m === "cc") return "cc_p90";
    if (m === "cc_xg") return "cc_xg_p90";
  }
  return m;
}

function metricLabel() {
  const opt = els.metric.selectedOptions[0];
  return `${opt?.textContent || state.metric}${state.per90 ? " /90" : ""}`;
}

function metricShort() {
  const m = state.metric;
  if (m === "xg") return state.per90 ? "xG/90" : "xG";
  if (m === "shots") return state.per90 ? "Sh/90" : "Sh";
  if (m === "sot") return state.per90 ? "SoT/90" : "SoT";
  if (m === "cc") return state.per90 ? "CC/90" : "CC";
  if (m === "cc_xg") return state.per90 ? "xGA/90" : "xG assisted";
  return metricLabel();
}

function setView(view) {
  const wasAgainst = state.view === "against";
  state.view = view;
  els.tabs.forEach((b) => b.classList.toggle("on", b.dataset.view === view));
  const againstOnly = view === "against";
  els.againstWrap.hidden = !againstOnly;
  if (againstOnly) els.againstWrap.removeAttribute("hidden");
  else els.againstWrap.setAttribute("hidden", "");
  els.againstWrap.setAttribute("aria-hidden", againstOnly ? "false" : "true");
  updateAgainstControls();
  // Switching into/out of Against refreshes the Top/Bottom 10 preset
  if (wasAgainst !== againstOnly) {
    resetPresetTeams();
    populateTeams();
    state.focusSlices.clear();
  }
  const treemap = view === "treemap";
  els.chart.hidden = !treemap;
  els.matrix.hidden = treemap;
  render();
}

function dimMap(rows, labelKey) {
  const out = {};
  for (const row of rows || []) {
    const k = row[labelKey];
    if (!k) continue;
    out[k] = row;
  }
  return out;
}

function teamDim(team, mode) {
  if (mode === "situation") return dimMap(team.by_situation, "situation");
  if (mode === "last_action") return dimMap(team.by_last_action_group, "group");
  if (state.againstDim === "last_action") return dimMap(team.against_last_action_group, "group");
  return dimMap(team.against_situation, "situation");
}

function render() {
  if (state.view === "treemap") renderTreemap();
  else if (state.view === "situation") renderLinked("situation");
  else if (state.view === "last_action") renderLinked("last_action");
  else renderLinked("against");
}

function renderTreemap() {
  const teams = visibleTeams();
  const key = metricKey();
  const label = metricLabel();
  const sitActive = activeSituations();

  const nodes = teams
    .map((t) => {
      const players = (t.players || [])
        .slice()
        .sort((a, b) => val(b, key) - val(a, key))
        .filter((p) => val(p, key) > 0)
        .slice(0, TOP_N)
        .map((p) => ({
          ...p,
          name: shortName(p.player_name),
          fullName: decodeHtml(p.player_name),
          value: Math.max(val(p, key), 0.0001),
          team_code: t.team_code,
          team_short: t.team_short,
        }));

      let teamValue = players.reduce((a, p) => a + p.value, 0);
      if (sitActive) {
        teamValue = (t.by_situation || [])
          .filter((r) => sitActive.has(r.situation))
          .reduce((a, r) => a + situationCellValue(r, false), 0);
        teamValue = Math.max(teamValue, 0.0001);
      }

      return { ...t, value: Math.max(teamValue, 0.0001), players };
    })
    .filter((t) => t.players.length);

  const prior = priorSeason();
  const nAll = seasonTeamsAll().length;
  const sitNote = sitActive ? ` · ${[...sitActive].join(", ")}` : "";
  els.status.textContent = `Showing ${nodes.length} of ${nAll} teams · default top ${TOP_TEAMS} by ${prior} xG · ${label}${sitNote}`;
  els.footnote.textContent = `Sh = shots · SoT = on target. Use team pills / Top ${TOP_TEAMS} / All teams to change who appears. Source: Understat · ${state.data.built_at_utc || ""}`;

  const width = els.chart.clientWidth || 1000;
  const height = els.chart.clientHeight || 640;
  els.chart.innerHTML = "";
  const svg = d3.select(els.chart).append("svg").attr("viewBox", `0 0 ${width} ${height}`);

  if (!nodes.length) {
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", height / 2)
      .attr("text-anchor", "middle")
      .attr("fill", "#8fa59a")
      .text("No data for this filter — try another season/metric or clear team filters.");
    return;
  }

  const root = d3
    .hierarchy({ name: "root", children: nodes })
    .sum((d) => d.value)
    .sort((a, b) => (b.value || 0) - (a.value || 0));

  d3.treemap().size([width, height]).paddingInner(6).paddingOuter(4).round(true)(root);

  const teamNodes = root.children || [];
  const playerLeaves = [];

  for (const tn of teamNodes) {
    const tw = Math.max(0, tn.x1 - tn.x0);
    const th = Math.max(0, tn.y1 - tn.y0);
    const contentX0 = tn.x0 + 3;
    const contentY0 = tn.y0 + HEADER_H;
    const contentW = Math.max(1, tw - 6);
    const contentH = Math.max(1, th - HEADER_H - 3);

    const innerRoot = d3
      .hierarchy({ name: tn.data.team_short, children: tn.data.players })
      .sum((d) => d.value)
      .sort((a, b) => (b.value || 0) - (a.value || 0));

    d3.treemap()
      .size([contentW, contentH])
      .paddingInner(2)
      .paddingOuter(0)
      .round(true)(innerRoot);

    for (const leaf of innerRoot.leaves()) {
      playerLeaves.push({
        ...leaf,
        x0: contentX0 + leaf.x0,
        x1: contentX0 + leaf.x1,
        y0: contentY0 + leaf.y0,
        y1: contentY0 + leaf.y1,
        teamNode: tn,
        teamMax: Math.max(...tn.data.players.map((p) => p.value)),
      });
    }
  }

  const gTeams = svg.append("g");
  gTeams
    .selectAll("rect.team-shell")
    .data(teamNodes)
    .join("rect")
    .attr("class", "team-shell")
    .attr("x", (d) => d.x0)
    .attr("y", (d) => d.y0)
    .attr("width", (d) => Math.max(0, d.x1 - d.x0))
    .attr("height", (d) => Math.max(0, d.y1 - d.y0))
    .attr("rx", 14)
    .attr("ry", 14)
    .attr("fill", (d) => teamFill(d.data.team_short, 0.55))
    .on("click", (_, d) => openDrawer(d.data))
    .on("mousemove", (event, d) => showTip(event, teamTip(d.data)))
    .on("mouseleave", hideTip);

  // Subtle header wash — light tint of team pastel
  gTeams
    .selectAll("rect.team-band")
    .data(teamNodes.filter((d) => d.y1 - d.y0 > 40 && d.x1 - d.x0 > 56))
    .join("rect")
    .attr("class", "team-band")
    .attr("x", (d) => d.x0 + 3)
    .attr("y", (d) => d.y0 + 3)
    .attr("width", (d) => Math.max(0, d.x1 - d.x0 - 6))
    .attr("height", HEADER_H - 6)
    .attr("rx", 8)
    .attr("ry", 8)
    .attr("fill", (d) => teamFill(d.data.team_short, 0.35))
    .attr("pointer-events", "none");

  gTeams
    .selectAll("text.team-label")
    .data(teamNodes.filter((d) => d.x1 - d.x0 > 48))
    .join("text")
    .attr("class", "team-label")
    .attr("x", (d) => d.x0 + 12)
    .attr("y", (d) => d.y0 + 18)
    .attr("font-size", 14)
    .attr("fill", (d) => textOnTeam(d.data.team_short))
    .attr("paint-order", "stroke")
    .attr("stroke", (d) => (textOnTeam(d.data.team_short) === "#1a2420" ? "rgba(255,255,255,0.35)" : "rgba(8,12,10,0.35)"))
    .attr("stroke-width", 2.5)
    .text((d) => d.data.team_short);

  gTeams
    .selectAll("text.team-sub")
    .data(teamNodes.filter((d) => d.x1 - d.x0 > 100 && d.y1 - d.y0 > 48))
    .join("text")
    .attr("class", "team-sub")
    .attr("x", (d) => d.x0 + 12)
    .attr("y", (d) => d.y0 + 34)
    .attr("font-size", 10)
    .attr("fill", (d) => textOnTeam(d.data.team_short))
    .attr("opacity", 0.85)
    .attr("paint-order", "stroke")
    .attr("stroke", (d) => (textOnTeam(d.data.team_short) === "#1a2420" ? "rgba(255,255,255,0.3)" : "rgba(8,12,10,0.3)"))
    .attr("stroke-width", 2)
    .text((d) => teamMeta(d.data, key));

  const gPlayers = svg.append("g");
  gPlayers
    .selectAll("g.player")
    .data(playerLeaves)
    .join("g")
    .attr("class", "player")
    .each(function (d) {
      const g = d3.select(this);
      const w = d.x1 - d.x0;
      const h = d.y1 - d.y0;
      const intensity = d.teamMax > 0 ? d.data.value / d.teamMax : 0.5;
      const fill = teamFill(d.data.team_short, 0.72 + intensity * 0.28);
      const ink = textOnTeam(d.data.team_short);

      g.append("rect")
        .attr("class", "player")
        .attr("x", d.x0)
        .attr("y", d.y0)
        .attr("width", Math.max(0, w))
        .attr("height", Math.max(0, h))
        .attr("rx", 6)
        .attr("ry", 6)
        .attr("fill", fill)
        .on("click", () => openDrawer(d.teamNode.data, d.data))
        .on("mousemove", (event) =>
          showTip(
            event,
            `<strong>${d.data.fullName}</strong><br>${d.data.team_short} · ${label} ${fmt(d.data.value)}`
          )
        )
        .on("mouseleave", hideTip);

      // Font scales with metric share within the team (top player largest).
      const ratio = d.teamMax > 0 ? d.data.value / d.teamMax : 1;
      const idealName = MIN_FONT + ratio * 13; // ~5→18
      const tileCap = Math.min(w / 4.2, h / 2.1);
      const nameFs = Math.max(MIN_FONT, Math.min(idealName, tileCap));
      const valFs = Math.max(MIN_FONT, Math.min(nameFs * 0.72, nameFs - 1));
      const cx = d.x0 + w / 2;
      const showVal = h >= nameFs + valFs + 3 && w >= 18;

      g.append("text")
        .attr("class", "player-name")
        .attr("x", cx)
        .attr("y", showVal ? d.y0 + h / 2 - 1 : d.y0 + h / 2 + nameFs * 0.35)
        .attr("text-anchor", "middle")
        .attr("font-size", nameFs)
        .attr("fill", ink)
        .text(truncate(d.data.name, Math.max(2, Math.floor(w / (nameFs * 0.5)))));

      if (showVal) {
        g.append("text")
          .attr("class", "player-val")
          .attr("x", cx)
          .attr("y", d.y0 + h / 2 + valFs + 1)
          .attr("text-anchor", "middle")
          .attr("font-size", valFs)
          .attr("fill", ink)
          .attr("opacity", 0.85)
          .text(fmt(d.data.value));
      }
    });
}

/**
 * Linked rank → mix → detail for situation / last-action / against tabs.
 */
function renderLinked(mode) {
  const teams = visibleTeams();
  const label = metricLabel();
  const against = mode === "against";
  const title = against
    ? `Against (${state.againstDim})`
    : mode === "situation"
      ? `Situation mix`
      : `Last-action mix`;

  const order =
    (against
      ? state.againstDim === "last_action"
        ? state.data.last_action_group_order
        : state.data.situation_order
      : mode === "last_action"
        ? state.data.last_action_group_order
        : state.data.situation_order) || [];

  const dims = new Set();
  teams.forEach((t) => Object.keys(teamDim(t, mode)).forEach((k) => dims.add(k)));
  let cols = [...order.filter((c) => dims.has(c)), ...[...dims].filter((c) => !order.includes(c)).sort()];

  const sitMode =
    mode === "situation" || (mode === "against" && state.againstDim === "situation");
  const sitActive = activeSituations();
  if (sitMode && sitActive) {
    cols = cols.filter((c) => sitActive.has(c));
  }

  const prior = priorSeason();
  const nAll = seasonTeamsAll().length;
  els.status.textContent = `Showing ${teams.length} of ${nAll} · ${title} · ${against ? mixShortLabel(true) : label} · click rank or mix to link panes`;
  els.footnote.textContent = `Rank = who leads · Mix = how share breaks down · Detail = absolute values + top players. Default top ${TOP_TEAMS} by ${prior} xG. Source: Understat · ${state.data.built_at_utc || ""}`;

  if (!teams.length || !cols.length) {
    els.matrix.innerHTML = `<p class="empty">No data for this filter.</p>`;
    return;
  }

  const rows = teams
    .map((t) => {
      const map = teamDim(t, mode);
      const cells = cols.map((c) => {
        const cell = map[c] || {};
        return { col: c, value: situationCellValue(cell, against), cell };
      });
      const total = cells.reduce((a, c) => a + c.value, 0);
      const focusVal = sliceMetric(cells, state.focusSlices);
      const focusPct = total > 0 ? (focusVal / total) * 100 : 0;
      return { team: t, cells, total, focusVal, focusPct, code: String(t.team_code) };
    });

  // Sort: with legend multi-select → by slice metric (rank) / by % (mix uses same order)
  if (state.focusSlices.size) {
    rows.sort((a, b) => b.focusVal - a.focusVal || b.focusPct - a.focusPct);
  } else {
    rows.sort((a, b) => b.total - a.total);
  }

  // Keep focus valid
  if (state.focusTeam && !rows.some((r) => r.code === state.focusTeam)) {
    state.focusTeam = rows[0]?.code || null;
  }
  if (!state.focusTeam) state.focusTeam = rows[0]?.code || null;
  // Drop invalid legend selections
  for (const s of [...state.focusSlices]) {
    if (!cols.includes(s)) state.focusSlices.delete(s);
  }

  const unit = against ? mixShortLabel(true) : mixShortLabel(false);
  const focusRow = rows.find((r) => r.code === state.focusTeam) || rows[0];

  els.matrix.innerHTML = `
    <div class="linked" data-name="shots.linked">
      <section class="linked-pane" data-name="shots.linked.rank">
        <header class="linked-head">
          <h3>Rank</h3>
          <p>${unit} ${state.focusSlices.size ? "· selected slices" : "total"} · click a team</p>
        </header>
        <div id="linked-rank" class="linked-rank"></div>
      </section>
      <section class="linked-pane" data-name="shots.linked.mix">
        <header class="linked-head">
          <h3>Mix</h3>
          <p>100% share · multi-select legend to sort</p>
        </header>
        <div id="linked-mix" class="linked-mix"></div>
        <div id="linked-legend" class="linked-legend"></div>
      </section>
      <section class="linked-pane linked-detail-pane" data-name="shots.linked.detail">
        <header class="linked-head">
          <h3>Detail</h3>
          <p id="linked-detail-title">${focusRow?.team.team_short || "—"}</p>
        </header>
        <div id="linked-detail" class="linked-detail"></div>
      </section>
    </div>`;

  decorateNames(els.matrix);
  drawRank(rows, unit);
  drawMix(rows, cols, unit);
  drawDetail(focusRow, cols, unit, against, mode);
}

function sliceMetric(cells, focusSet) {
  if (!focusSet.size) return cells.reduce((a, c) => a + c.value, 0);
  return cells.filter((c) => focusSet.has(c.col)).reduce((a, c) => a + c.value, 0);
}

function drawRank(rows, unit) {
  const host = document.getElementById("linked-rank");
  const focused = state.focusSlices.size > 0;
  const max = Math.max(0.0001, ...rows.map((r) => (focused ? r.focusVal : r.total)));
  host.innerHTML = rows
    .map((r) => {
      const on = r.code === state.focusTeam ? "on" : "";
      const show = focused ? r.focusVal : r.total;
      const widthPct = (show / max) * 100;
      return `
        <button type="button" class="rank-row ${on}" data-code="${r.code}">
          <span class="rank-label" style="color:${teamSolid(r.team.team_short)}">${r.team.team_short}</span>
          <span class="rank-track"><i style="width:${Math.max(2, widthPct)}%;background:${teamFill(r.team.team_short, 0.92)}"></i></span>
          <span class="rank-val">${fmt(show)}</span>
        </button>`;
    })
    .join("");

  host.querySelectorAll(".rank-row").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.focusTeam = btn.dataset.code;
      render();
    });
  });
}

function drawMix(rows, cols, unit) {
  const host = document.getElementById("linked-mix");
  const legend = document.getElementById("linked-legend");
  const color = (i) => SLICE_COLORS[i % SLICE_COLORS.length];
  const focused = state.focusSlices.size > 0;

  // Mix list sorted by % of selected slices when filtering
  const mixRows = rows.slice();
  if (focused) mixRows.sort((a, b) => b.focusPct - a.focusPct || b.focusVal - a.focusVal);

  legend.innerHTML = cols
    .map(
      (c, i) => `
      <button type="button" class="leg ${state.focusSlices.has(c) ? "on" : ""}" data-slice="${c}">
        <i style="background:${color(i)}"></i>${c}
      </button>`
    )
    .join("");

  host.innerHTML = mixRows
    .map((r) => {
      const on = r.code === state.focusTeam ? "on" : "";
      const total = r.total || 0.0001;
      const segs = r.cells
        .map((c, i) => {
          const pct = (c.value / total) * 100;
          if (pct <= 0) return "";
          const hi = !focused || state.focusSlices.has(c.col);
          return `<i class="seg ${hi ? "" : "dim"}" data-slice="${c.col}" data-code="${r.code}" style="width:${pct}%;background:${color(i)}" title="${c.col}: ${unit} ${fmt(c.value)} (${pct.toFixed(0)}%)"></i>`;
        })
        .join("");
      const pctLabel = focused ? `${r.focusPct.toFixed(0)}%` : "";
      return `
        <div class="mix-row-chart ${on}" data-code="${r.code}">
          <span class="mix-lab">${r.team.team_short}</span>
          <div class="mix-stack">${segs}</div>
          <span class="mix-pct">${pctLabel}</span>
        </div>`;
    })
    .join("");

  legend.querySelectorAll(".leg").forEach((btn) => {
    btn.addEventListener("click", () => {
      const s = btn.dataset.slice;
      if (state.focusSlices.has(s)) state.focusSlices.delete(s);
      else state.focusSlices.add(s);
      // Deselect all → reset to initial sort
      render();
    });
  });

  host.querySelectorAll(".mix-row-chart").forEach((row) => {
    row.addEventListener("click", () => {
      state.focusTeam = row.dataset.code;
      render();
    });
  });

  host.querySelectorAll(".seg").forEach((seg) => {
    seg.addEventListener("mouseenter", (e) => {
      showTip(e, `<strong>${seg.dataset.slice}</strong><br>${seg.getAttribute("title") || ""}`);
      host.querySelectorAll(".seg").forEach((s) => {
        s.classList.toggle("dim", s.dataset.slice !== seg.dataset.slice);
      });
    });
    seg.addEventListener("mousemove", (e) =>
      showTip(e, `<strong>${seg.dataset.slice}</strong><br>${seg.getAttribute("title") || ""}`)
    );
    seg.addEventListener("mouseleave", () => {
      hideTip();
      host.querySelectorAll(".seg").forEach((s) => {
        s.classList.toggle("dim", !!(state.focusSlices.size && !state.focusSlices.has(s.dataset.slice)));
      });
    });
    seg.addEventListener("click", (e) => {
      e.stopPropagation();
      state.focusTeam = seg.dataset.code;
      const s = seg.dataset.slice;
      if (state.focusSlices.has(s)) state.focusSlices.delete(s);
      else state.focusSlices.add(s);
      render();
    });
  });
}

function drawDetail(focusRow, cols, unit, against, mode) {
  const host = document.getElementById("linked-detail");
  const title = document.getElementById("linked-detail-title");
  if (!focusRow) {
    host.innerHTML = `<p class="empty">Select a team</p>`;
    return;
  }
  const t = focusRow.team;
  title.textContent = `${t.team_short} · ${unit}`;

  // Always sort detail rows by metric value (high → low)
  const detailCells = focusRow.cells.slice().sort((a, b) => b.value - a.value);
  const max = Math.max(0.0001, ...detailCells.map((c) => c.value));
  const total = focusRow.total || 0.0001;
  const key = metricKey();
  const focused = state.focusSlices.size > 0;

  const players = (t.players || [])
    .slice()
    .sort((a, b) => val(b, key) - val(a, key))
    .filter((p) => val(p, key) > 0)
    .slice(0, TOP_N);

  const sliceNote = focused
    ? `<p class="detail-note">Highlighting <strong>${[...state.focusSlices].join(", ")}</strong> across rank & mix.</p>`
    : "";

  const colIndex = Object.fromEntries(cols.map((c, i) => [c, i]));

  host.innerHTML = `
    ${sliceNote}
    <div class="detail-abs">
      ${detailCells
        .map((c) => {
          const i = colIndex[c.col] ?? 0;
          const pct = ((c.value / total) * 100).toFixed(0);
          const hi = !focused || state.focusSlices.has(c.col);
          return `
          <button type="button" class="detail-row ${hi ? "" : "dim"} ${state.focusSlices.has(c.col) ? "on" : ""}" data-slice="${c.col}">
            <span class="swatch" style="background:${SLICE_COLORS[i % SLICE_COLORS.length]}"></span>
            <span class="dl">${c.col}</span>
            <span class="dv">${unit} ${fmt(c.value)} <em>(${pct}%)</em></span>
            <span class="dbar"><i style="width:${(c.value / max) * 100}%;background:${SLICE_COLORS[i % SLICE_COLORS.length]}"></i></span>
          </button>`;
        })
        .join("")}
    </div>
    <h4>Top players · ${metricShort()}</h4>
    <div class="detail-players">
      ${players
        .map(
          (p) => `
        <button type="button" class="player-chip" data-id="${p.player_id}">
          <span>${shortName(p.player_name)}</span>
          <b>${fmt(val(p, key))}</b>
        </button>`
        )
        .join("") || "<p class='empty'>No players</p>"}
    </div>
    <button type="button" class="ghost detail-open" id="detail-open-drawer">Open full drawer</button>
  `;

  host.querySelectorAll(".detail-row").forEach((btn) => {
    btn.addEventListener("click", () => {
      const s = btn.dataset.slice;
      if (state.focusSlices.has(s)) state.focusSlices.delete(s);
      else state.focusSlices.add(s);
      render();
    });
  });

  host.querySelectorAll(".player-chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      const p = players.find((x) => String(x.player_id) === btn.dataset.id);
      if (p) openDrawer(t, { ...p, fullName: decodeHtml(p.player_name) });
    });
  });

  document.getElementById("detail-open-drawer")?.addEventListener("click", () => openDrawer(t));
}

function situationCellValue(cell, against) {
  if (!cell) return 0;
  const m = state.metric;
  if (against) {
    if (m === "shots") return Number(cell.shots_faced) || 0;
    if (m === "sot") return Number(cell.sot_faced) || 0;
    return Number(cell.xga) || 0;
  }
  if (m === "shots") return Number(cell.shots) || 0;
  if (m === "sot") return Number(cell.sot) || 0;
  return Number(cell.xg) || 0;
}

function mixShortLabel(against) {
  const m = state.metric;
  if (against) {
    if (m === "shots") return "Sh faced";
    if (m === "sot") return "SoT faced";
    return "xGA";
  }
  if (m === "shots") return "Sh";
  if (m === "sot") return "SoT";
  if (m === "cc" || m === "cc_xg") return "xG";
  return "xG";
}

function openDrawer(team, player) {
  state.drawer = { team, player: player || null };
  els.drawer.hidden = false;
  els.drawerTitle.textContent = player
    ? `${player.fullName || decodeHtml(player.player_name)} · ${team.team_short}`
    : `${team.team || team.team_name || team.team_short}`;

  const key = metricKey();
  const short = metricShort();
  const mixLabel = mixShortLabel(false);
  const againstLabel = mixShortLabel(true);
  const sitActive = activeSituations();

  let sit = (team.by_situation || []).slice();
  if (sitActive) sit = sit.filter((v) => sitActive.has(v.situation));
  sit.sort((a, b) => situationCellValue(b, false) - situationCellValue(a, false));

  const lag = (team.by_last_action_group || [])
    .slice()
    .sort((a, b) => situationCellValue(b, false) - situationCellValue(a, false));

  const ag = (team.against_situation || [])
    .slice()
    .sort((a, b) => situationCellValue(b, true) - situationCellValue(a, true));

  const sitTotal = sit.reduce((a, v) => a + situationCellValue(v, false), 0) || 0.0001;
  const lagTotal = lag.reduce((a, v) => a + situationCellValue(v, false), 0) || 0.0001;
  const agTotal = ag.reduce((a, v) => a + situationCellValue(v, true), 0) || 0.0001;
  const maxSit = Math.max(0.0001, ...sit.map((v) => situationCellValue(v, false)));
  const maxLag = Math.max(0.0001, ...lag.map((v) => situationCellValue(v, false)));
  const maxAg = Math.max(0.0001, ...ag.map((v) => situationCellValue(v, true)));

  const subject = player || team;
  const metaVal = fmt(val(subject, key));
  const metaSh = player ? Math.round(player.shots || 0) : Math.round(team.shots || 0);
  const metaSot = player ? Math.round(player.sot || 0) : Math.round(team.sot || 0);

  const splitNote =
    state.metric === "cc" || state.metric === "cc_xg"
      ? `<p class="drawer-note">Situation / last-action splits use xG (CC is not split in the source).</p>`
      : "";

  els.drawerBody.innerHTML = `
    <p class="drawer-meta">${short} ${metaVal} · Sh ${metaSh} · SoT ${metaSot} · matches ${team.matches || "—"}</p>
    ${splitNote}
    <h4>Situation mix (attack) · ${mixLabel}</h4>
    ${
      mixRows(
        sit.map((v) => ({
          label: v.situation,
          value: situationCellValue(v, false),
          max: maxSit,
          total: sitTotal,
        })),
        mixLabel
      ) || '<p class="empty">No data</p>'
    }
    <h4>Last-action groups · ${mixLabel}</h4>
    ${
      mixRows(
        lag.map((v) => ({
          label: v.group,
          value: situationCellValue(v, false),
          max: maxLag,
          total: lagTotal,
        })),
        mixLabel
      ) || '<p class="empty">No data</p>'
    }
    <h4>Against — situation conceded · ${againstLabel}</h4>
    ${
      mixRows(
        ag.map((v) => ({
          label: v.situation,
          value: situationCellValue(v, true),
          max: maxAg,
          total: agTotal,
        })),
        againstLabel
      ) || '<p class="empty">No data</p>'
    }
  `;
}

function mixRows(rows, unit) {
  if (!rows.length) return "";
  return rows
    .map((r) => {
      const pct = ((r.value / r.total) * 100).toFixed(0);
      return `
      <div class="mix-row">
        <span>${r.label}</span>
        <b>${unit} ${fmt(r.value)} <em>(${pct}%)</em></b>
        <div class="bar" style="grid-column:1/-1"><i style="width:${(r.value / r.max) * 100}%"></i></div>
      </div>`;
    })
    .join("");
}

function fillDefs() {
  const notes = state.data?.notes || {};
  const groups = state.data?.last_action_groups || [];
  const lagHtml = groups
    .map(
      (g) =>
        `<div class="def-block"><h3>${g.group}</h3><p>${g.definition}</p><code>${(g.values || []).join(", ")}</code></div>`
    )
    .join("");

  const body = $("us-defs-body");
  body.innerHTML = `
    <div class="def-block"><h3>Teams filter</h3><p>All clubs stay in the pill list. Creation views default to <em>Top 10</em> by prior-season xG. Against view uses <em>Bottom 10</em> by <strong>xGC</strong> (xG conceded = sum of against-situation xGA).</p></div>
    <div class="def-block"><h3>Linked panes</h3><p>Rank → Mix → Detail. Multi-select mix legends to sort Rank by absolute metric and Mix by %; clear all legends to reset.</p></div>
    <div class="def-block"><h3>Source</h3><p>${notes.source || "Understat shot model metrics."}</p></div>
    <div class="def-block"><h3>SoT</h3><p>${notes.sot || "Goal + SavedShot + ShotOnPost. Blocked shots excluded."}</p></div>
    <div class="def-block"><h3>Chances created</h3><p>${notes.cc || "From shot player_assisted (passer before the shot)."}</p></div>
    <div class="def-block"><h3>Per 90</h3><p>${notes.per90_team || ""} ${notes.per90_player || ""}</p></div>
    <div class="def-block"><h3>Situations</h3><p>OpenPlay, FromCorner, SetPiece, DirectFreekick, Penalty — how the shot chance arose.</p></div>
    <div class="def-block"><h3>Last-action groups</h3><p>Preceding action before the shot, rolled into readable groups:</p></div>
    ${lagHtml || "<div class='def-block'><p>Combination, Through ball, Crosses, Dribble, Turnover, Second ball, Unknown.</p></div>"}
    <div class="def-block"><h3>Against (defence)</h3><p>Shots / xG conceded (xGC), split by situation or last-action of the attacking side. Metric label becomes Metric (Against).</p></div>
    <div class="def-block"><h3>Labels</h3><p>Sh = shots · SoT = shots on target · xGC = xG conceded. Hover <em>i</em> copies <code>data-name</code>.</p></div>
  `;
}

function teamTip(t) {
  const key = metricKey();
  return `<strong>${t.team_short}</strong><br>${metricLabel()} ${fmt(val(t, key))}<br>Sh ${t.shots || 0} · SoT ${t.sot || 0}`;
}

function teamMeta(t, key) {
  const sitActive = activeSituations();
  if (sitActive) {
    const rows = (t.by_situation || []).filter((r) => sitActive.has(r.situation));
    const v = rows.reduce((a, r) => a + situationCellValue(r, false), 0);
    const sh = rows.reduce((a, r) => a + (r.shots || 0), 0);
    const sot = rows.reduce((a, r) => a + (r.sot || 0), 0);
    return `${metricShort()} ${fmt(v)} · Sh ${sh} · SoT ${sot}`;
  }
  if (key.startsWith("cc")) return `CC ${fmt(t.cc)} · xG asst ${fmt(t.cc_xg)}`;
  if (key === "shots" || key === "shots_p90") return `Sh ${fmt(val(t, key))} · SoT ${t.sot || 0}`;
  if (key === "sot" || key === "sot_p90") return `SoT ${fmt(val(t, key))} · Sh ${t.shots || 0}`;
  return `xG ${fmt(val(t, key))} · Sh ${t.shots || 0} · SoT ${t.sot || 0}`;
}

function teamColor(short) {
  if (TEAM_COLOR_INDEX[short] != null) return PALETTE[TEAM_COLOR_INDEX[short] % PALETTE.length];
  // stable fallback from short code
  let h = 0;
  const s = String(short || "");
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return PALETTE[h % PALETTE.length];
}

/** Preferred pastel index per club so neighbours stay distinct. */
const TEAM_COLOR_INDEX = {
  ARS: 3,
  AVL: 8,
  BHA: 7,
  BOU: 2,
  BRE: 11,
  BUR: 12,
  CHE: 5,
  COV: 6,
  CRY: 9,
  EVE: 1,
  FUL: 14,
  HUL: 13,
  IPS: 4,
  LEE: 14,
  LIV: 10,
  MCI: 7,
  MUN: 3,
  NEW: 15,
  NFO: 11,
  SUN: 2,
  TOT: 14,
  WHU: 12,
  WOL: 0,
};

function hexToRgb(hex) {
  const h = hex.replace("#", "");
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
}

function teamFill(short, alpha = 1) {
  const [r, g, b] = hexToRgb(teamColor(short));
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function teamSolid(short) {
  return teamColor(short);
}

function textOnTeam(short) {
  const [r, g, b] = hexToRgb(teamColor(short));
  const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return lum > 0.58 ? "#1a2420" : "#f4fff8";
}

function val(obj, key) {
  const v = obj?.[key];
  return Number.isFinite(v) ? v : 0;
}

function fmt(n) {
  if (!Number.isFinite(n)) return "—";
  if (Math.abs(n) >= 100) return n.toFixed(0);
  if (Math.abs(n) >= 10) return n.toFixed(1);
  return n.toFixed(2);
}

function shortName(name) {
  const clean = decodeHtml(name || "");
  const parts = clean.trim().split(/\s+/);
  return parts.length <= 1 ? clean : parts[parts.length - 1];
}

function decodeHtml(s) {
  const el = document.createElement("textarea");
  el.innerHTML = s || "";
  return el.value;
}

function truncate(s, n) {
  if (!s) return "";
  return s.length <= n ? s : `${s.slice(0, Math.max(1, n - 1))}…`;
}

function showTip(event, html) {
  els.tip.hidden = false;
  els.tip.innerHTML = html;
  const x = Math.min(window.innerWidth - 220, event.clientX + 14);
  const y = Math.min(window.innerHeight - 80, event.clientY + 14);
  els.tip.style.transform = `translate(${x}px, ${y}px)`;
}

function hideTip() {
  els.tip.hidden = true;
}

function debounce(fn, ms) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}
