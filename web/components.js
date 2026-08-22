import { METRICS, STORAGE_KEY, MIN_MINS_OPTIONS } from "./registry.js";

const tipEl = () => document.getElementById("tooltip");

export function initTooltip() {
  const tip = tipEl();
  if (!tip) return;
  document.addEventListener("pointerover", (e) => {
    const node = e.target.closest("[data-tip], [title]");
    if (!node) return;
    if (node.hasAttribute("title") && !node.dataset.tip) {
      node.dataset.tip = node.getAttribute("title");
      node.removeAttribute("title");
    }
    const text = node.dataset.tip;
    if (!text) return;
    tip.textContent = text;
    tip.hidden = false;
    moveTip(e);
  });
  document.addEventListener("pointermove", (e) => {
    if (!tip.hidden) moveTip(e);
  });
  document.addEventListener("pointerout", (e) => {
    if (e.target.closest("[data-tip]")) tip.hidden = true;
  });
}

function moveTip(e) {
  const tip = tipEl();
  const pad = 14;
  let x = e.clientX + 16;
  let y = e.clientY + 18;
  const r = tip.getBoundingClientRect();
  if (x + r.width + pad > window.innerWidth) x = e.clientX - r.width - 12;
  if (y + r.height + pad > window.innerHeight) y = e.clientY - r.height - 12;
  tip.style.transform = `translate(${x}px, ${y}px)`;
}

export function nameDot(name) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "name-dot";
  b.dataset.tip = name;
  b.setAttribute("aria-label", `Copy element name ${name}`);
  b.textContent = "i";
  b.addEventListener("click", async (e) => {
    e.stopPropagation();
    e.preventDefault();
    try {
      await navigator.clipboard.writeText(name);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = name;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    }
    b.textContent = "✓";
    b.classList.add("copied");
    setTimeout(() => {
      b.textContent = "i";
      b.classList.remove("copied");
    }, 900);
  });
  return b;
}

const SKIP_DOT = new Set(["insight-row", "insight-chip", "match-stat", "fx-card"]);

export function decorateNames(root = document) {
  root.querySelectorAll("[data-name]").forEach((el) => {
    if (el.querySelector(":scope > .name-dot")) return;
    if (el.classList.contains("name-dot") || el.classList.contains("skip-dot")) return;
    if ([...el.classList].some((c) => SKIP_DOT.has(c))) return;
    if (el.closest("tbody")) return;
    el.insertBefore(nameDot(el.dataset.name), el.firstChild);
  });
}

export function fmt(value, kind, { dash = "—" } = {}) {
  if (value === null || value === undefined || Number.isNaN(value)) return dash;
  if (kind === "text") return String(value);
  const n = Number(value);
  if (!Number.isFinite(n)) return dash;
  if (kind === "int") return String(Math.round(n));
  if (kind === "1dp") return n.toFixed(1);
  if (kind === "2dp") return n.toFixed(2);
  return String(n);
}

export function loadState(view) {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}")[view] || {};
  } catch {
    return {};
  }
}

export function saveState(view, state) {
  try {
    const all = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    all[view] = { ...all[view], ...state };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  } catch {
    /* ignore */
  }
}

function labeledCtrl(name, tip, innerHTML) {
  const box = document.createElement("label");
  box.className = "ctrl";
  box.dataset.name = name;
  box.dataset.tip = tip;
  box.innerHTML = innerHTML;
  box.insertBefore(nameDot(name), box.firstChild);
  return box;
}

export function activeGw(upcoming, competition = "Premier League") {
  const rows = (upcoming || []).filter((f) => competition === "all" || f.competition === competition);
  if (!rows.length) return null;
  return Math.min(...rows.map((f) => f.gw).filter((g) => g != null));
}

export function renderFixtureCards(el, fixtures, { competition = "Premier League" } = {}) {
  const host = typeof el === "string" ? document.getElementById(el) : el;
  host.innerHTML = "";
  const rows = (fixtures || []).filter((f) => competition === "all" || f.competition === competition);
  const gw = activeGw(rows, "all");
  const shown = rows.filter((f) => f.gw === gw);
  const banner = document.getElementById("fixtures-gw-label");
  if (banner) banner.textContent = gw != null ? `Gameweek ${gw} only — the next GW unlocks when these matches are finished.` : "";
  if (!shown.length) {
    host.innerHTML = `<p class="empty">No upcoming fixtures in this filter.</p>`;
    return;
  }
  shown.forEach((f) => {
    const card = document.createElement("article");
    card.className = "fx-card";
    card.id = f.id;
    card.classList.add("skip-dot");
    const when = f.kickoff_utc
      ? new Date(f.kickoff_utc).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })
      : "TBD";
    card.innerHTML = `
      <header>
        <span class="fx-comp">${f.competition} · GW${f.gw ?? "—"}</span>
        <time data-tip="Kickoff (UTC stored, shown in your timezone)">${when}</time>
      </header>
      <div class="fx-sides">
        ${side(f, "home")}
        <div class="fx-score" data-tip="Predicted xG: 0.5 × (team xGf + opponent xGa), home × 1.08">
          <b>${fmt(f.pred_home, "2dp")}</b><span>pred xG</span><b>${fmt(f.pred_away, "2dp")}</b>
        </div>
        ${side(f, "away")}
      </div>`;
    host.appendChild(card);
  });
  decorateNames(host);
}

function side(f, which) {
  const name = f[which];
  const star = f[`${which}_star`];
  const gf = f[`${which}_gf`];
  const ga = f[`${which}_ga`];
  const est = f[`estimate_${which}`];
  return `<div class="fx-team">
    <strong>${name || "—"}</strong>
    ${est ? `<em class="est" data-tip="Limited sample (promoted or missing xG) — treat as an estimate">est.</em>` : ""}
    <span class="fx-star" data-tip="Standout attacker by last-5 xGI">${star || "—"}</span>
    <span class="fx-form" data-tip="Last-season goals for / against per game">${fmt(gf, "2dp")} GF · ${fmt(ga, "2dp")} GA</span>
  </div>`;
}

export function renderTicker(el, ticker) {
  const host = typeof el === "string" ? document.getElementById(el) : el;
  host.innerHTML = "";
  if (!ticker?.length) {
    host.innerHTML = `<p class="empty">Ticker appears once upcoming Premier League fixtures are scheduled.</p>`;
    return;
  }
  const table = document.createElement("table");
  table.className = "ticker";
  const max = Math.max(...ticker.map((t) => t.fixtures.length), 0);
  table.innerHTML = `<thead><tr><th>Team</th>${Array.from({ length: max }, () => `<th>GW</th>`).join("")}</tr></thead>`;
  const tb = document.createElement("tbody");
  ticker.forEach((t) => {
    const tr = document.createElement("tr");
    tr.innerHTML =
      `<th>${t.short || t.team}</th>` +
      t.fixtures
        .map(
          (c) => `<td class="d${c.diff}" data-tip="GW${c.gw} · ${c.opp} (${c.venue}) · difficulty ${c.diff}/5">
        <span>${c.opp}</span><small>${c.venue}${c.gw ? " · " + c.gw : ""}</small></td>`
        )
        .join("");
    tb.appendChild(tr);
  });
  table.appendChild(tb);
  host.appendChild(table);
}

export function renderInsightList(el, rows, opts = {}) {
  const host = typeof el === "string" ? document.getElementById(el) : el;
  host.innerHTML = "";
  host.className = "insight-list";
  if (!rows?.length) {
    host.innerHTML = `<p class="empty">${opts.empty || "Not enough minutes in this window."}</p>`;
    return;
  }
  rows.forEach((r, i) => {
    const row = document.createElement("div");
    const tone = r.tone || (typeof r.value === "number" ? (r.value > 0.05 ? "good" : r.value < -0.05 ? "bad" : "flat") : "flat");
    row.className = `insight-row tone-${tone}`;
    row.innerHTML = `<span class="rank">${i + 1}</span>
      <span class="who">${r.player || r.team || "—"} <em>${r.player && r.team ? r.team : ""}</em></span>
      <span class="val">${r.valueText ?? fmt(r.value, opts.fmt || "2dp")}</span>
      <span class="more">${r.meta || ""}</span>`;
    host.appendChild(row);
  });
}

const SUM_FIELDS = [
  "G", "A", "PenG", "xG", "xA", "xGI", "Sh", "SoT", "CC", "TiB", "BCM", "xGOT",
  "Sv", "GC", "xGOTf", "xGP", "Tkl", "CBI", "DefCon", "npxG", "F3", "Dr", "YC",
  "Aer", "Clr", "Int", "Blk", "Rec", "SiB", "HC", "SW",
];

function inList(list, value) {
  if (list == null) return true;
  if (!list.length) return false;
  return list.includes(value);
}

export function filterMatches(matches, state) {
  return (matches || []).filter((r) => {
    if (!inList(state.seasons, r.s)) return false;
    if (!inList(state.competitions, r.c)) return false;
    const venue = r.h === true ? "H" : r.h === false ? "A" : null;
    if (venue && !inList(state.venues, venue)) return false;
    if (state.positions?.length && !state.positions.includes(r.pos)) return false;
    if (!inList(state.posFilter, r.pos)) return false;
    if (state.currentOnly && state.roster && r.pc != null && !state.roster.has(Number(r.pc))) return false;
    if (state.players?.length && !state.players.includes(String(r.pc ?? r.pid))) return false;
    return true;
  });
}

export function gwRangeSlice(rows, from, to) {
  const gws = rows.map((r) => r.gw).filter((g) => g != null && g > 0);
  if (!gws.length) return { rows, from: null, to: null };
  const lo = from != null ? from : Math.min(...gws);
  const hi = to != null ? to : Math.max(...gws);
  const a = Math.min(lo, hi);
  const b = Math.max(lo, hi);
  return { rows: rows.filter((r) => r.gw >= a && r.gw <= b), from: a, to: b };
}

export function lastGwSlice(rows, n) {
  const gws = rows.map((r) => r.gw).filter((g) => g != null && g > 0);
  if (!gws.length) return { rows, from: null, to: null };
  const to = Math.max(...gws);
  const from = Math.max(1, to - n + 1);
  return { rows: rows.filter((r) => r.gw >= from && r.gw <= to), from, to };
}

export function aggregatePlayers(matches, state, { prices = {} } = {}) {
  const filtered = filterMatches(matches, { ...state, players: null });
  const sliced =
    state.gwFrom != null && state.gwTo != null
      ? gwRangeSlice(filtered, state.gwFrom, state.gwTo)
      : lastGwSlice(filtered, 5);
  const { rows: windowed, from, to } = sliced;
  const groups = new Map();
  for (const r of windowed) {
    const key = r.pc || r.pid;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(r);
  }
  const career = new Map();
  for (const r of filtered) {
    if (r.m == null || r.m <= 0) continue;
    const key = r.pc || r.pid;
    if (!career.has(key)) career.set(key, []);
    career.get(key).push(r);
  }
  const out = [];
  for (const [key, list] of groups) {
    const last = list[list.length - 1];
    const apps = list.filter((r) => r.m > 0);
    const mins = apps.reduce((a, r) => a + (r.m || 0), 0);
    const row = {
      player: last.n,
      team: last.tm,
      pos: last.pos,
      pc: last.pc,
      pid: last.pid,
      season: last.s,
      competition: (state.competitions || []).join(", "),
      apps: apps.length,
      mins,
      gw_from: from,
      gw_to: to,
      Cost: prices[String(last.pc)] ?? null,
    };
    const life = career.get(key) || apps;
    row.mins_per_app = life.length ? life.reduce((a, r) => a + (r.m || 0), 0) / life.length : null;
    for (const f of SUM_FIELDS) {
      const vals = list.map((r) => r[f]).filter((v) => v != null);
      row[f] = vals.length ? vals.reduce((a, b) => a + Number(b), 0) : null;
    }
    row.Saves = row.Sv;
    const ptsByGw = new Map();
    const csByGw = new Map();
    for (const r of list) {
      if (r.pts != null && !ptsByGw.has(r.gw)) ptsByGw.set(r.gw, r.pts);
      if (r.cs != null && !csByGw.has(r.gw)) csByGw.set(r.gw, r.cs);
    }
    row.Pts = [...ptsByGw.values()].reduce((a, b) => a + Number(b), 0);
    row.CS = [...csByGw.values()].reduce((a, b) => a + Number(b), 0);
    out.push(row);
  }
  return out;
}

export function aggregateTeamRows(rows, state) {
  const filtered = (rows || []).filter((r) => {
    if (!r.finished) return false;
    if (!inList(state.seasons, r.season)) return false;
    if (!inList(state.competitions, r.competition)) return false;
    const venue = r.is_home === true ? "H" : r.is_home === false ? "A" : null;
    if (venue && !inList(state.venues, venue)) return false;
    return true;
  });
  const sliced =
    state.gwFrom != null && state.gwTo != null
      ? gwRangeSlice(filtered, state.gwFrom, state.gwTo)
      : lastGwSlice(filtered, 5);
  const { rows: win, from, to } = sliced;
  const byTeam = new Map();
  for (const r of win) {
    const key = `${r.season}|${r.team_code}`;
    if (!byTeam.has(key)) byTeam.set(key, []);
    byTeam.get(key).push(r);
  }
  const out = [];
  for (const list of byTeam.values()) {
    const last = list[list.length - 1];
    const sum = (k) => list.reduce((a, r) => a + (Number(r[k]) || 0), 0);
    const mean = (k) => {
      const vals = list.map((r) => r[k]).filter((v) => v != null);
      return vals.length ? vals.reduce((a, b) => a + Number(b), 0) / vals.length : null;
    };
    out.push({
      season: last.season,
      competition: (state.competitions || []).join(", "),
      team: last.short || last.team,
      team_code: last.team_code,
      apps: list.length,
      mins_per_app: 90,
      PtsT: sum("points"),
      GF: sum("goals_for"),
      GA: sum("goals_against"),
      xGf: sum("xg"),
      xGa: sum("xga"),
      ShT: sum("shots"),
      SoTT: sum("shots_on_target"),
      Poss: mean("possession"),
      CST: list.filter((r) => r.clean_sheet).length,
      gw_from: from,
      gw_to: to,
    });
  }
  return out;
}

export function computeInsights(matches, state, { prices = {} } = {}) {
  const base = {
    ...state,
    positions: state.positions || ["Forward", "Midfielder"],
    currentOnly: state.currentOnly ?? true,
  };
  const scoped = filterMatches(matches, base);
  const n = Math.min(state.window || 5, 10);
  const nowWin = lastGwSlice(scoped, n);
  const priorWin = lastGwSlice(scoped, n * 2);
  const now = aggregatePlayers(matches, { ...base, gwFrom: nowWin.from, gwTo: nowWin.to }, { prices });
  const prior = aggregatePlayers(matches, { ...base, gwFrom: priorWin.from, gwTo: priorWin.to }, { prices });
  const priorMap = new Map(prior.map((r) => [r.pc || r.pid, r]));

  const top = [...now].filter((r) => r.xGI != null && (r.mins || 0) >= 60).sort((a, b) => b.xGI - a.xGI).slice(0, 8)
    .map((r) => ({ player: r.player, team: r.team, value: r.xGI, tone: "flat", meta: `${fmt(r.mins_per_app, "1dp")} min/app` }));

  const rising = [];
  for (const r of now) {
    const p = priorMap.get(r.pc || r.pid);
    if (!p || !r.mins || r.mins < 90 || !p.mins || p.mins <= r.mins) continue;
    const priorMins = p.mins - r.mins;
    const priorXgi = (p.xGI || 0) - (r.xGI || 0);
    if (priorMins < 90) continue;
    const cur90 = (r.xGI || 0) * 90 / r.mins;
    const prior90 = priorXgi * 90 / priorMins;
    const delta = cur90 - prior90;
    rising.push({
      player: r.player,
      team: r.team,
      value: delta,
      tone: delta >= 0 ? "good" : "bad",
      meta: `${cur90.toFixed(2)} vs ${prior90.toFixed(2)} /90`,
    });
  }
  rising.sort((a, b) => b.value - a.value);

  const finishing = now
    .filter((r) => r.G != null && r.xG != null && (r.mins || 0) >= 180)
    .map((r) => {
      const v = r.G - r.xG;
      return {
        player: r.player,
        team: r.team,
        value: v,
        tone: v > 0.15 ? "good" : v < -0.15 ? "bad" : "flat",
        meta: `${fmt(r.G, "int")} G / ${fmt(r.xG, "2dp")} xG`,
      };
    })
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

  const quiet = now
    .filter((r) => r.xGI != null && (r.mins || 0) >= 180 && r.xGI >= 1.2)
    .map((r) => {
      const ret = (r.G || 0) + (r.A || 0);
      return {
        player: r.player,
        team: r.team,
        value: r.xGI - ret,
        tone: "watch",
        meta: `${fmt(r.xGI, "2dp")} xGI · ${ret} G+A`,
      };
    })
    .filter((r) => r.value > 0.4)
    .sort((a, b) => b.value - a.value);

  return {
    top_xgi: top.slice(0, 8),
    rising: rising.slice(0, 8),
    finishing: finishing.slice(0, 8),
    quiet: quiet.slice(0, 8),
  };
}

function matchKey(row) {
  if (row.mid || row.match_id) return String(row.mid || row.match_id);
  const a = row.team_code || row.tc;
  const b = row.opponent_code;
  return `${row.season || row.s}|${row.gw}|${[a, b].filter(Boolean).sort().join("-")}`;
}

export function computeMatchInsights(playerMatches, teamRows, state) {
  const teams = (teamRows || []).filter((r) => {
    if (!r.finished) return false;
    if (!inList(state.seasons, r.season)) return false;
    if (!inList(state.competitions, r.competition)) return false;
    if (state.gws?.length && !state.gws.includes(r.gw)) return false;
    return true;
  });
  const byId = new Map();
  for (const r of teams) {
    const id = matchKey(r);
    if (!byId.has(id)) byId.set(id, { id, gw: r.gw, season: r.season, sides: [] });
    byId.get(id).sides.push(r);
  }
  const players = (playerMatches || []).filter((r) => {
    if (!inList(state.seasons, r.s)) return false;
    if (!inList(state.competitions, r.c)) return false;
    if (state.gws?.length && !state.gws.includes(r.gw)) return false;
    return true;
  });
  const playersByMatch = new Map();
  for (const r of players) {
    const id = matchKey(r);
    if (!playersByMatch.has(id)) playersByMatch.set(id, []);
    playersByMatch.get(id).push(r);
  }

  const bundles = [];
  for (const pack of byId.values()) {
    if (state.matches?.length && !state.matches.includes(pack.id)) continue;
    const home = pack.sides.find((s) => s.is_home) || pack.sides[0];
    const away = pack.sides.find((s) => !s.is_home) || pack.sides[1];
    if (!home || !away) continue;
    const plist = playersByMatch.get(pack.id) || [];
    const homeName = home.short || home.team;
    const awayName = away.short || away.team;
    const xgH = Number(home.xg) || 0;
    const xgA = Number(away.xg) || 0;
    const gfH = Number(home.goals_for) || 0;
    const gfA = Number(away.goals_for) || 0;
    const overH = gfH - xgH;
    const overA = gfA - xgA;
    const standout = [...plist].filter((p) => p.m > 0).sort((a, b) => (b.xGI || 0) - (a.xGI || 0))[0];
    const finisher = [...plist]
      .filter((p) => p.xG != null)
      .map((p) => ({ ...p, over: (p.G || 0) - p.xG }))
      .sort((a, b) => Math.abs(b.over) - Math.abs(a.over))[0];
    const misser = [...plist].filter((p) => p.BCM).sort((a, b) => (b.BCM || 0) - (a.BCM || 0))[0];
    const creator = [...plist].filter((p) => p.xA != null).sort((a, b) => (b.xA || 0) - (a.xA || 0))[0];
    const keeper = [...plist].filter((p) => p.pos === "Goalkeeper" && p.xGP != null).sort((a, b) => (b.xGP || 0) - (a.xGP || 0))[0];
    const chips = [
      {
        label: "Result vs xG",
        text: `${homeName} ${overH >= 0 ? "+" : ""}${overH.toFixed(2)} · ${awayName} ${overA >= 0 ? "+" : ""}${overA.toFixed(2)}`,
        tone: Math.abs(overH) > Math.abs(overA) ? (overH > 0.15 ? "good" : overH < -0.15 ? "bad" : "flat") : (overA > 0.15 ? "good" : overA < -0.15 ? "bad" : "flat"),
      },
    ];
    if (standout) chips.push({ label: "Highest xGI", text: `${standout.n} ${fmt(standout.xGI, "2dp")}`, tone: "flat" });
    if (finisher) chips.push({ label: "Finishing", text: `${finisher.n} ${finisher.over >= 0 ? "+" : ""}${finisher.over.toFixed(2)} G−xG`, tone: finisher.over > 0.2 ? "good" : finisher.over < -0.2 ? "bad" : "flat" });
    if (misser && misser.BCM > 0) chips.push({ label: "Big chances missed", text: `${misser.n} ${fmt(misser.BCM, "int")}`, tone: "watch" });
    if (creator && creator.xA > 0) chips.push({ label: "xA", text: `${creator.n} ${fmt(creator.xA, "2dp")}`, tone: "flat" });
    if (keeper) chips.push({ label: "xG prevented", text: `${keeper.n} ${fmt(keeper.xGP, "2dp")}`, tone: keeper.xGP > 0.2 ? "good" : keeper.xGP < -0.2 ? "bad" : "flat" });
    bundles.push({
      id: pack.id,
      gw: pack.gw,
      title: `${homeName} ${gfH}–${gfA} ${awayName}`,
      subtitle: `GW ${pack.gw} · xG ${xgH.toFixed(2)}–${xgA.toFixed(2)}`,
      chips,
    });
  }
  bundles.sort((a, b) => (b.gw - a.gw) || a.title.localeCompare(b.title));
  return bundles;
}

export function matchFilterOptions(teamRows, state) {
  const teams = (teamRows || []).filter((r) => r.finished && inList(state.seasons, r.season) && inList(state.competitions, r.competition));
  const gws = [...new Set(teams.map((r) => r.gw).filter((g) => g > 0))].sort((a, b) => a - b);
  const scoped = state.gws?.length ? teams.filter((r) => state.gws.includes(r.gw)) : teams;
  const seen = new Map();
  for (const r of scoped) {
    const id = matchKey(r);
    if (seen.has(id)) continue;
    const home = scoped.find((s) => matchKey(s) === id && s.is_home) || r;
    const away = scoped.find((s) => matchKey(s) === id && !s.is_home);
    seen.set(id, {
      value: id,
      label: `GW${r.gw} ${home.short || home.team}${away ? ` vs ${away.short || away.team}` : ""}`,
    });
  }
  return { gws, matches: [...seen.values()] };
}

export function computeTeamInsights(teamRows, state) {
  const rows = aggregateTeamRows(teamRows, {
    ...state,
    gwFrom: state.gwFrom,
    gwTo: state.gwTo,
  });
  const attack = [...rows].filter((r) => r.xGf != null).sort((a, b) => b.xGf - a.xGf).slice(0, 8)
    .map((r) => ({ team: r.team, value: r.xGf, tone: "flat", meta: `${fmt(r.GF, "1dp")} GF` }));
  const defend = [...rows].filter((r) => r.xGa != null).sort((a, b) => a.xGa - b.xGa).slice(0, 8)
    .map((r) => ({ team: r.team, value: r.xGa, tone: "good", meta: `${fmt(r.GA, "1dp")} GA · ${r.CST} CS` }));
  const over = [...rows].filter((r) => r.GF != null && r.xGf != null)
    .map((r) => {
      const v = r.GF - r.xGf;
      return { team: r.team, value: v, tone: v > 0.2 ? "good" : v < -0.2 ? "bad" : "flat", meta: `${fmt(r.GF, "1dp")} / ${fmt(r.xGf, "2dp")} xG` };
    })
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 8);
  const leak = [...rows].filter((r) => r.GA != null && r.xGa != null)
    .map((r) => {
      const v = r.GA - r.xGa;
      return { team: r.team, value: v, tone: v > 0.2 ? "bad" : v < -0.2 ? "good" : "flat", meta: `${fmt(r.GA, "1dp")} GA / ${fmt(r.xGa, "2dp")} xGA` };
    })
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 8);
  return { attack, defend, over, leak };
}

export function renderMatchBoard(el, bundles, { headline } = {}) {
  const host = typeof el === "string" ? document.getElementById(el) : el;
  if (!host) return;
  host.innerHTML = "";
  if (headline) {
    const h = document.createElement("p");
    h.className = "lede tight";
    h.textContent = headline;
    host.appendChild(h);
  }
  if (!bundles?.length) {
    const p = document.createElement("p");
    p.className = "empty";
    p.textContent = "No finished Premier League matches in this filter.";
    host.appendChild(p);
    return;
  }
  const grid = document.createElement("div");
  grid.className = "match-grid";
  grid.dataset.name = "insights.matches.grid";
  bundles.forEach((b) => {
    const card = document.createElement("article");
    card.className = "match-card";
    card.innerHTML = `<header><strong>${b.title}</strong><span>${b.subtitle}</span></header>
      <div class="match-chips">${b.chips
        .map((c) => `<div class="insight-chip tone-${c.tone}"><span>${c.label}</span><b>${c.text}</b></div>`)
        .join("")}</div>`;
    grid.appendChild(card);
  });
  host.appendChild(grid);
  decorateNames(host);
}

function asArray(value, fallback) {
  if (Array.isArray(value) && value.length) return value;
  if (value && value !== "all") return [value];
  return fallback;
}

export function makeMultiSelect({ name, label, tip, options, selected, onChange, searchable = false }) {
  const box = document.createElement("div");
  box.className = "ctrl ms-ctrl";
  box.dataset.name = name;
  box.dataset.tip = tip;
  box.appendChild(nameDot(name));
  const copy = document.createElement("div");
  copy.className = "ctrl-copy";
  const title = document.createElement("span");
  title.textContent = label;
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "ms-btn";
  const panel = document.createElement("div");
  panel.className = "ms-panel";
  panel.hidden = true;
  copy.append(title, btn, panel);
  box.appendChild(copy);

  let opts = options || [];
  let sel = new Set((selected || []).map(String));
  let query = "";

  function summary() {
    if (!sel.size || sel.size === opts.length) return "All";
    if (sel.size === 1) {
      const one = opts.find((o) => String(o.value) === [...sel][0]);
      return one?.label || "1 selected";
    }
    return `${sel.size} selected`;
  }

  function emit() {
    onChange([...sel]);
  }

  function paint() {
    btn.textContent = summary();
    panel.replaceChildren();
    if (searchable) {
      const q = document.createElement("input");
      q.type = "search";
      q.placeholder = "Find…";
      q.value = query;
      q.addEventListener("input", () => {
        query = q.value;
        paint();
        panel.querySelector("input[type=search]")?.focus();
      });
      panel.appendChild(q);
    }
    const actions = document.createElement("div");
    actions.className = "ms-actions";
    const all = document.createElement("button");
    all.type = "button";
    all.textContent = "All";
    all.addEventListener("click", () => {
      sel = new Set(opts.map((o) => String(o.value)));
      paint();
      emit();
    });
    const none = document.createElement("button");
    none.type = "button";
    none.textContent = "None";
    none.addEventListener("click", () => {
      sel = new Set();
      paint();
      emit();
    });
    actions.append(all, none);
    panel.appendChild(actions);
    const qlow = query.toLowerCase();
    opts
      .filter((o) => !qlow || String(o.label).toLowerCase().includes(qlow))
      .forEach((o) => {
        const row = document.createElement("label");
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = sel.has(String(o.value));
        cb.addEventListener("change", () => {
          if (cb.checked) sel.add(String(o.value));
          else sel.delete(String(o.value));
          btn.textContent = summary();
          emit();
        });
        row.append(cb, document.createTextNode(` ${o.label}`));
        panel.appendChild(row);
      });
  }

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    panel.hidden = !panel.hidden;
  });
  document.addEventListener("click", (e) => {
    if (!box.contains(e.target)) panel.hidden = true;
  });

  paint();
  return {
    el: box,
    setOptions(next, nextSel) {
      opts = next || [];
      if (nextSel) sel = new Set(nextSel.map(String));
      sel = new Set([...sel].filter((v) => opts.some((o) => String(o.value) === v)));
      paint();
    },
  };
}

export function makeTable(cfg) {
  const host = document.getElementById(cfg.el);
  if (!host) return;
  const view = cfg.view;
  const persisted = loadState(view);
  const seasons = cfg.seasons || [];
  const competitions = ["Premier League", ...(cfg.competitions || []).filter((c) => c !== "Premier League")];
  const state = {
    sort: persisted.sort || cfg.defaultSort,
    dir: persisted.dir || cfg.defaultDir || "desc",
    minMins: persisted.minMins ?? cfg.minMinsDefault ?? 60,
    search: persisted.search || "",
    per90: persisted.per90 ?? false,
    seasons: asArray(persisted.seasons || persisted.season, [cfg.season].filter(Boolean)),
    competitions: asArray(persisted.competitions || persisted.competition, ["Premier League"]),
    venues: asArray(persisted.venues || (persisted.venue && persisted.venue !== "all" ? persisted.venue : null), ["H", "A"]),
    posFilter: asArray(persisted.posFilter || persisted.position, cfg.positions || []),
    players: persisted.players || [],
    gwFrom: persisted.gwFrom ?? null,
    gwTo: persisted.gwTo ?? null,
    costMin: persisted.costMin ?? 4,
    costMax: persisted.costMax ?? 15,
    currentOnly: true,
    detail: persisted.detail ?? false,
    positions: cfg.positions,
    roster: cfg.roster,
  };

  host.innerHTML = "";
  const wrap = document.createElement("div");
  wrap.className = "table-wrap";
  wrap.dataset.name = `${view}.table`;
  const controls = document.createElement("div");
  controls.className = "controls";
  controls.dataset.name = `${view}.controls`;

  const gwCtrl = gwRangeControl(state, `${view}.filter.range`, render);
  const seasonMs = makeMultiSelect({
    name: `${view}.filter.season`,
    label: "Season",
    tip: "Season year. Multi-select.",
    options: seasons.map((s) => ({ value: s, label: s })),
    selected: state.seasons,
    onChange: (v) => {
      state.seasons = v;
      render();
    },
  });
  const compMs = makeMultiSelect({
    name: `${view}.filter.competition`,
    label: "Competition",
    tip: "Competition / tournament. Multi-select.",
    options: competitions.map((c) => ({ value: c, label: c })),
    selected: state.competitions,
    onChange: (v) => {
      state.competitions = v;
      render();
    },
  });
  const venueMs = makeMultiSelect({
    name: `${view}.filter.venue`,
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
  let posMs = null;
  if (cfg.positionFilter) {
    posMs = makeMultiSelect({
      name: `${view}.filter.position`,
      label: "Position",
      tip: "FPL position on attackers.",
      options: (cfg.positions || []).map((p) => ({ value: p, label: p })),
      selected: state.posFilter,
      onChange: (v) => {
        state.posFilter = v;
        render();
      },
    });
  }
  let playerMs = null;
  if (!cfg.hidePlayers) {
    playerMs = makeMultiSelect({
      name: `${view}.filter.players`,
      label: "Players",
      tip: "Select one or more players.",
      options: [],
      selected: state.players,
      searchable: true,
      onChange: (v) => {
        state.players = v;
        render();
      },
    });
  }

  const filterRow = document.createElement("div");
  filterRow.className = "controls-row";
  const sliderRow = document.createElement("div");
  sliderRow.className = "controls-row";
  filterRow.append(seasonMs.el, compMs.el, venueMs.el);
  if (posMs) filterRow.appendChild(posMs.el);
  if (playerMs) filterRow.appendChild(playerMs.el);
  if (!cfg.hideSearch) filterRow.appendChild(searchControl(state, `${view}.filter.search`, render));
  if (!cfg.hidePer90 && ((cfg.per90Keys && cfg.per90Keys.length) || (cfg.always90Keys && cfg.always90Keys.length))) {
    filterRow.appendChild(per90Control(state, `${view}.filter.per90`, render));
  }
  if (!cfg.hideDetail && cfg.extraColumns?.length) filterRow.appendChild(detailControl(state, `${view}.filter.detail`, render));
  sliderRow.appendChild(gwCtrl);
  if (!cfg.hideMins) sliderRow.appendChild(minsControl(state, `${view}.filter.mins`, render));
  if (!cfg.hideCost && !cfg.hidePlayers) sliderRow.appendChild(costControl(state, `${view}.filter.cost`, render));
  controls.append(filterRow, sliderRow);

  const count = document.createElement("p");
  count.className = "showing";
  count.dataset.name = `${view}.showing`;
  const scroller = document.createElement("div");
  scroller.className = "table-scroll";
  scroller.dataset.name = `${view}.grid`;
  const table = document.createElement("table");
  table.className = "data-table";
  scroller.appendChild(table);
  wrap.append(controls, count, scroller);
  host.appendChild(wrap);
  decorateNames(host);

  function columns() {
    return state.detail && cfg.extraColumns?.length ? cfg.columns.concat(cfg.extraColumns) : cfg.columns;
  }

  function render() {
    saveState(view, state);
    const source = typeof cfg.rows === "function" ? cfg.rows(state) : cfg.rows || [];
    if (playerMs) {
      const opts = [...source]
        .map((r) => ({ value: String(r.pc ?? r.pid), label: `${r.player} (${r.team || ""})` }))
        .sort((a, b) => a.label.localeCompare(b.label));
      const seen = new Set();
      const unique = opts.filter((o) => (seen.has(o.value) ? false : (seen.add(o.value), true)));
      playerMs.setOptions(unique, state.players);
    }
    let rows = source.filter((r) => (r.mins_per_app || 0) >= Number(state.minMins || 0));
    if (!cfg.hideCost && !cfg.hidePlayers) {
      rows = rows.filter((r) => r.Cost == null || (r.Cost >= state.costMin && r.Cost <= state.costMax));
    }
    if (state.players?.length) {
      rows = rows.filter((r) => state.players.includes(String(r.pc ?? r.pid)));
    }
    if (state.search) {
      const q = state.search.toLowerCase();
      rows = rows.filter((r) => `${r.player || ""} ${r.team || ""}`.toLowerCase().includes(q));
    }
    const cols = columns();
    const sorted = [...rows].sort((a, b) => cmp(cellValue(a, state.sort, state, cfg), cellValue(b, state.sort, state, cfg), state.dir));
    const thead = document.createElement("thead");
    const hr = document.createElement("tr");
    cols.forEach((key) => {
      const m = METRICS[key] || { label: key, tip: key, fmt: "text" };
      const th = document.createElement("th");
      th.dataset.key = key;
      th.dataset.name = `${view}.col.${key}`;
      th.dataset.tip = m.tip;
      if (state.sort === key) th.className = `sorted ${state.dir}`;
      th.append(nameDot(`${view}.col.${key}`), document.createTextNode(headerLabel(m, key, cfg, state)));
      th.addEventListener("click", (e) => {
        if (e.target.closest(".name-dot")) return;
        if (state.sort === key) state.dir = state.dir === "desc" ? "asc" : "desc";
        else {
          state.sort = key;
          state.dir = "desc";
        }
        render();
      });
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    table.replaceChildren(thead);
    const tb = document.createElement("tbody");
    tb.innerHTML =
      sorted
        .map(
          (r) =>
            `<tr>${cols
              .map((key) => {
                const m = METRICS[key] || { fmt: "text" };
                return `<td class="${key === "player" ? "sticky" : ""}">${fmt(cellValue(r, key, state, cfg), m.fmt)}</td>`;
              })
              .join("")}</tr>`
        )
        .join("") || `<tr><td colspan="${cols.length}">No rows match these filters.</td></tr>`;
    table.appendChild(tb);
    const from = sorted[0]?.gw_from ?? state.gwFrom;
    const to = sorted[0]?.gw_to ?? state.gwTo;
    if (from && to) {
      state.gwFrom = from;
      state.gwTo = to;
    }
    const range = from && to ? `GW ${from}–${to}` : "";
    count.textContent = `Showing ${sorted.length}${range ? ` · ${range}` : ""}`;
    const rangeLabel = host.querySelector("[data-range-label]");
    if (rangeLabel && from && to) rangeLabel.textContent = `GW ${from}–${to}`;
    const fromEl = host.querySelector("[data-from]");
    const toEl = host.querySelector("[data-to]");
    if (fromEl && toEl && from && to) {
      fromEl.value = from;
      toEl.value = to;
    }
  }

  render();
}

function headerLabel(m, key, cfg, state) {
  const always = (cfg.always90Keys || []).includes(key);
  const per90 = state.per90 && (cfg.per90Keys || []).includes(key);
  if (always || per90) return `${m.label.replace(/\/90$/, "")}/90`;
  return m.label;
}

function cellValue(row, key, state, cfg) {
  if (key === "team") return row.team;
  if (key === "Saves") return rate(row.Saves ?? row.Sv, row.mins, (cfg.per90Keys || []).includes("Saves") && state.per90);
  const always = (cfg.always90Keys || []).includes(key);
  const per90 = state.per90 && (cfg.per90Keys || []).includes(key);
  return rate(row[key], row.mins, always || per90);
}

function rate(raw, mins, as90) {
  if (raw == null) return null;
  if (as90 && mins) return (Number(raw) * 90) / mins;
  return raw;
}

function cmp(a, b, dir) {
  if (a == null && b == null) return 0;
  if (a == null) return 1;
  if (b == null) return -1;
  if (typeof a === "string" || typeof b === "string") {
    return String(a).localeCompare(String(b), undefined, { numeric: true }) * (dir === "asc" ? 1 : -1);
  }
  return (a - b) * (dir === "asc" ? 1 : -1);
}

function gwRangeControl(state, name, render) {
  const fromVal = state.gwFrom ?? 1;
  const toVal = state.gwTo ?? 38;
  const box = labeledCtrl(
    name,
    "Exact gameweek range inside the selected season.",
    `<span class="ctrl-copy"><span data-range-label>GW ${fromVal}–${toVal}</span>
    <span class="dual-range">
      <label class="range-leg">From<input data-from type="range" min="1" max="38" value="${fromVal}" /></label>
      <label class="range-leg">To<input data-to type="range" min="1" max="38" value="${toVal}" /></label>
    </span></span>`
  );
  const from = box.querySelector("[data-from]");
  const to = box.querySelector("[data-to]");
  const sync = () => {
    let a = Number(from.value);
    let b = Number(to.value);
    if (a > b) [a, b] = [b, a];
    state.gwFrom = a;
    state.gwTo = b;
    render();
  };
  from.addEventListener("input", sync);
  to.addEventListener("input", sync);
  return box;
}

function minsControl(state, name, render) {
  const box = labeledCtrl(
    name,
    "Minimum average minutes per appearance (season / competition / venue).",
    `<span class="ctrl-copy"><span>Min/app ≥ ${state.minMins}</span>
    <input type="range" min="0" max="${MIN_MINS_OPTIONS.length - 1}" value="${Math.max(0, MIN_MINS_OPTIONS.indexOf(Number(state.minMins)))}" /></span>`
  );
  const input = box.querySelector("input");
  const label = box.querySelector(".ctrl-copy span");
  input.addEventListener("input", () => {
    state.minMins = MIN_MINS_OPTIONS[Number(input.value)] ?? 0;
    label.textContent = `Min/app ≥ ${state.minMins}`;
    render();
  });
  return box;
}

function costControl(state, name, render) {
  const box = labeledCtrl(
    name,
    "Current-season FPL price in £m.",
    `<span class="ctrl-copy"><span data-cost-label>£${Number(state.costMin).toFixed(1)}–${Number(state.costMax).toFixed(1)}m</span>
    <span class="dual-range">
      <label class="range-leg">From £<input data-cost-from type="range" min="4" max="15" step="0.5" value="${state.costMin}" /></label>
      <label class="range-leg">To £<input data-cost-to type="range" min="4" max="15" step="0.5" value="${state.costMax}" /></label>
    </span></span>`
  );
  const from = box.querySelector("[data-cost-from]");
  const to = box.querySelector("[data-cost-to]");
  const label = box.querySelector("[data-cost-label]");
  const sync = () => {
    let a = Number(from.value);
    let b = Number(to.value);
    if (a > b) [a, b] = [b, a];
    state.costMin = a;
    state.costMax = b;
    label.textContent = `£${a.toFixed(1)}–${b.toFixed(1)}m`;
    render();
  };
  from.addEventListener("input", sync);
  to.addEventListener("input", sync);
  return box;
}

function searchControl(state, name, render) {
  const box = labeledCtrl(
    name,
    "Search player or team.",
    `<span class="ctrl-copy"><span>Search</span><input type="search" placeholder="Name or team" value="${escapeAttr(state.search)}" /></span>`
  );
  box.querySelector("input").addEventListener("input", (e) => {
    state.search = e.target.value;
    render();
  });
  return box;
}

function per90Control(state, name, render) {
  const box = labeledCtrl(
    name,
    "Rate counting stats per 90 minutes in the window. Defender Tkl/CBI/DefCon stay per 90.",
    `<span class="ctrl-copy check"><input type="checkbox" ${state.per90 ? "checked" : ""} /><span>Per 90</span></span>`
  );
  box.querySelector("input").addEventListener("change", (e) => {
    state.per90 = e.target.checked;
    render();
  });
  return box;
}

function detailControl(state, name, render) {
  const box = labeledCtrl(
    name,
    "Show extra detailed metrics. We will group these later.",
    `<span class="ctrl-copy check"><input type="checkbox" ${state.detail ? "checked" : ""} /><span>More metrics</span></span>`
  );
  box.querySelector("input").addEventListener("change", (e) => {
    state.detail = e.target.checked;
    render();
  });
  return box;
}

function escapeAttr(s) {
  return String(s || "").replace(/"/g, "&quot;");
}

export function renderCards(el, items) {
  const host = typeof el === "string" ? document.getElementById(el) : el;
  if (!host) return;
  host.innerHTML = "";
  host.classList.add("card-grid");
  items.forEach((it) => {
    const a = document.createElement(it.href ? "a" : "article");
    a.className = "stat-card";
    a.dataset.name = it.name;
    if (it.href) a.href = it.href;
    a.innerHTML = `<span class="stat-kicker">${it.kicker || ""}</span>
      <strong class="stat-title">${it.title || ""}</strong>
      <span class="stat-value">${it.value ?? ""}</span>
      <span class="stat-meta">${it.meta || ""}</span>`;
    host.appendChild(a);
  });
  decorateNames(host);
}

