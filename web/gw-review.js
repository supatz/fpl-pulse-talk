/* GW Review — FPL snapshot boards built for social download. */
(() => {
  const PM_URL = "./data/players_matches.json";
  const META_URL = "./data/meta.json";
  const TG_URL = "./data/teams_gw.json";
  const PG_URL = "./data/players_gw.json";
  const PL = "Premier League";
  // FPL DefCon thresholds for the 2-point award (approximate season rules).
  const DEFCON_PTS = { Goalkeeper: 10, Defender: 10, Midfielder: 12, Forward: 12 };

  const state = {
    rows: [],
    teams: [],
    playersGw: [],
    meta: null,
    season: null,
    gw: null,
  };
  const els = {};
  let started = false;

  function $(id) {
    return document.getElementById(id);
  }

  async function init() {
    bindEls();
    if (!els.root) return;
    if (started) {
      render();
      return;
    }
    started = true;
    bindEvents();
    try {
      const [pmRes, metaRes, tgRes, pgRes] = await Promise.all([
        fetch(PM_URL, { cache: "no-store" }),
        fetch(META_URL, { cache: "no-store" }),
        fetch(TG_URL, { cache: "no-store" }),
        fetch(PG_URL, { cache: "no-store" }),
      ]);
      if (!pmRes.ok) throw new Error(`players_matches HTTP ${pmRes.status}`);
      if (!metaRes.ok) throw new Error(`meta HTTP ${metaRes.status}`);
      if (!tgRes.ok) throw new Error(`teams_gw HTTP ${tgRes.status}`);
      if (!pgRes.ok) throw new Error(`players_gw HTTP ${pgRes.status}`);
      state.rows = await pmRes.json();
      state.meta = await metaRes.json();
      state.teams = await tgRes.json();
      state.playersGw = await pgRes.json();
      populateFilters();
      render();
    } catch (err) {
      if (els.status) els.status.textContent = `Failed to load: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("gwrev-root");
    els.season = $("gwrev-season");
    els.gw = $("gwrev-gw");
    els.status = $("gwrev-status");
    els.board = $("gwrev-board");
  }

  function bindEvents() {
    els.season?.addEventListener("change", () => {
      state.season = els.season.value;
      populateGwOptions(true);
      render();
    });
    els.gw?.addEventListener("change", () => {
      state.gw = Number(els.gw.value);
      render();
    });
  }

  function populateFilters() {
    const seasons = [
      ...new Set(state.rows.filter((r) => r.c === PL).map((r) => r.s).filter(Boolean)),
    ].sort();
    state.season = state.meta?.analysis_season || state.meta?.current_season || seasons.at(-1) || null;
    if (els.season) {
      els.season.replaceChildren(
        ...seasons.map((s) => {
          const o = document.createElement("option");
          o.value = s;
          o.textContent = s;
          o.selected = s === state.season;
          return o;
        })
      );
    }
    populateGwOptions(true);
  }

  function populateGwOptions(preferLatest) {
    const gws = [
      ...new Set(
        state.rows
          .filter((r) => r.s === state.season && r.c === PL)
          .map((r) => Number(r.gw))
          .filter((g) => g > 0)
      ),
    ].sort((a, b) => a - b);
    const upcoming = Number(state.meta?.upcoming_gw);
    let pick = preferLatest ? gws.at(-1) : state.gw;
    if (preferLatest && Number.isFinite(upcoming) && gws.includes(upcoming - 1)) pick = upcoming - 1;
    if (!gws.includes(pick)) pick = gws.at(-1) || 1;
    state.gw = pick;
    if (els.gw) {
      els.gw.replaceChildren(
        ...gws.map((g) => {
          const o = document.createElement("option");
          o.value = String(g);
          o.textContent = `GW ${g}`;
          o.selected = g === state.gw;
          return o;
        })
      );
    }
  }

  function num(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }

  function priceOf(pc) {
    const p = state.meta?.prices?.[String(pc)];
    return p != null ? Number(p) : null;
  }

  function posShort(pos) {
    if (pos === "Goalkeeper") return "GK";
    if (pos === "Defender") return "DEF";
    if (pos === "Midfielder") return "MID";
    if (pos === "Forward") return "FWD";
    return "—";
  }

  function shortName(name) {
    const full = String(name || "—").trim();
    const parts = full.split(/\s+/);
    const last = parts.at(-1) || "—";
    return last.length <= 2 || last.endsWith(".") ? full : last;
  }

  function fmt(v, digits = 0) {
    if (v == null || !Number.isFinite(Number(v))) return "—";
    return Number(v).toFixed(digits).replace(/\.0+$/, "");
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function kpiHtml(label, value, meta, badges = "") {
    return `<div class="gwrev-kpi">
      <div class="gwrev-kpi-label">${label}</div>
      <div class="gwrev-kpi-value">${value}</div>
      <div class="gwrev-kpi-meta">${meta}</div>
      ${badges ? `<div class="gwrev-kpi-badges">${badges}</div>` : ""}
    </div>`;
  }

  function repeatEmoji(emoji, n) {
    const c = Math.max(0, Math.floor(num(n)));
    return c > 0 ? emoji.repeat(c) : "";
  }

  /** Icons for what drove the haul / involvement (goals, assists, CS, DefCon pts). */
  function haulBadges(p, { goalsOnly = false } = {}) {
    if (!p) return "";
    const bits = [];
    if (p.G > 0) bits.push(repeatEmoji("⚽", p.G));
    if (goalsOnly) return bits.join("");
    if (p.A > 0) bits.push(repeatEmoji("🅰️", p.A));
    if (p.cs > 0 && (p.pos === "Goalkeeper" || p.pos === "Defender")) bits.push("🛡️");
    const need = DEFCON_PTS[p.pos] ?? 12;
    if (p.DefCon >= need) bits.push("🧱");
    return bits.join("");
  }

  function gwGoalTotal(gw) {
    return state.rows
      .filter((r) => r.s === state.season && r.c === PL && Number(r.gw) === gw && num(r.m) > 0)
      .reduce((a, r) => a + num(r.G), 0);
  }

  /** Distinct PL teams with a clean sheet in the GW (team flag — not player CS rollup). */
  function teamCleanSheetCount(gw) {
    const seen = new Set();
    for (const r of state.teams) {
      if (r.season !== state.season || r.competition !== PL) continue;
      if (Number(r.gw) !== gw || !r.finished || !r.clean_sheet) continue;
      seen.add(String(r.team_code ?? r.short));
    }
    return seen.size;
  }

  function deltaValueHtml(curr, prev) {
    if (prev == null || !Number.isFinite(Number(prev))) return fmt(curr);
    const d = Number(curr) - Number(prev);
    const cls = d > 0 ? "up" : d < 0 ? "down" : "flat";
    const arrow = d > 0 ? "▲" : d < 0 ? "▼" : "●";
    const sign = d > 0 ? "+" : "";
    return `${fmt(curr)} <span class="gwrev-delta ${cls}">(${arrow}${sign}${d})</span>`;
  }

  function goalsValueHtml(curr) {
    const prevGw = Number(state.gw) - 1;
    if (!Number.isFinite(prevGw) || prevGw < 1) return fmt(curr);
    return deltaValueHtml(curr, gwGoalTotal(prevGw));
  }

  function teamCsValueHtml(curr) {
    const prevGw = Number(state.gw) - 1;
    if (!Number.isFinite(prevGw) || prevGw < 1) return fmt(curr);
    return deltaValueHtml(curr, teamCleanSheetCount(prevGw));
  }

  function ownershipOf(pid) {
    if (pid == null) return null;
    if (!state._ownIdx || state._ownIdxGw !== state.gw) {
      const idx = new Map();
      for (const r of state.playersGw) {
        if (Number(r.gw) !== Number(state.gw)) continue;
        const v = Number(r.selected_by_percent);
        if (Number.isFinite(v)) idx.set(Number(r.player_id), v);
      }
      state._ownIdx = idx;
      state._ownIdxGw = state.gw;
    }
    const v = state._ownIdx.get(Number(pid));
    return v != null ? v : null;
  }

  /** Aggregate DGW rows into one player line for the selected GW. */
  function gwPlayers() {
    const scoped = state.rows.filter(
      (r) => r.s === state.season && r.c === PL && Number(r.gw) === state.gw && num(r.m) > 0
    );
    const map = new Map();
    for (const r of scoped) {
      const key = String(r.pc || r.pid);
      if (!map.has(key)) {
        map.set(key, {
          key,
          pc: r.pc,
          pid: r.pid,
          player_name: r.n,
          team_short: r.tm || "—",
          pos: r.pos,
          mins: 0,
          pts: 0,
          G: 0,
          A: 0,
          PenG: 0,
          xG: 0,
          xA: 0,
          xGI: 0,
          npxG: 0,
          SoT: 0,
          Sh: 0,
          CC: 0,
          BCC: 0,
          BPS: 0,
          Bon: 0,
          cs: 0,
          GC: 0,
          DefCon: 0,
          CBI: 0,
          Sv: 0,
          apps: 0,
        });
      }
      const p = map.get(key);
      p.player_name = r.n || p.player_name;
      p.team_short = r.tm || p.team_short;
      p.pos = r.pos || p.pos;
      if (r.pid != null) p.pid = r.pid;
      p.mins += num(r.m);
      p.pts += num(r.pts);
      p.G += num(r.G);
      p.A += num(r.A);
      p.PenG += num(r.PenG);
      p.xG += num(r.xG);
      p.xA += num(r.xA);
      p.xGI += num(r.xGI);
      p.npxG += num(r.npxG);
      p.SoT += num(r.SoT);
      p.Sh += num(r.Sh);
      p.CC += num(r.CC);
      p.BCC += num(r.BCC);
      p.BPS += num(r.BPS);
      p.Bon += num(r.Bon);
      p.cs += num(r.cs);
      p.GC += num(r.GC);
      p.DefCon += num(r.DefCon);
      p.CBI += num(r.CBI);
      p.Sv += num(r.Sv);
      p.apps += 1;
    }
    return [...map.values()].map((p) => ({
      ...p,
      price: priceOf(p.pc),
      own: ownershipOf(p.pid),
      npG: Math.max(0, p.G - p.PenG),
      delta: p.pts - p.xGI * 4, // rough FPL-ish haul vs involvement (display only)
    }));
  }

  function topN(list, key, n = 8, min = 0) {
    return [...list]
      .filter((p) => num(p[key]) > min || (min === 0 && num(p[key]) >= 0))
      .sort((a, b) => num(b[key]) - num(a[key]) || num(b.pts) - num(a.pts) || a.player_name.localeCompare(b.player_name))
      .slice(0, n);
  }

  function pickXi(players) {
    const byPts = (a, b) => b.pts - a.pts || b.Bon - a.Bon || a.player_name.localeCompare(b.player_name);
    const gkPool = [...players].filter((p) => p.pos === "Goalkeeper").sort(byPts);
    const defPool = [...players].filter((p) => p.pos === "Defender").sort(byPts);
    const midPool = [...players].filter((p) => p.pos === "Midfielder").sort(byPts);
    const fwdPool = [...players].filter((p) => p.pos === "Forward").sort(byPts);

    // Valid FPL shapes: 1 GK + DEF(3–5) + MID(2–5) + FWD(1–3) = 11
    const shapes = [];
    for (let d = 3; d <= 5; d++) {
      for (let m = 2; m <= 5; m++) {
        const f = 10 - d - m;
        if (f >= 1 && f <= 3) shapes.push([d, m, f]);
      }
    }

    let best = null;
    for (const [dN, mN, fN] of shapes) {
      if (gkPool.length < 1 || defPool.length < dN || midPool.length < mN || fwdPool.length < fN) continue;
      const gk = gkPool.slice(0, 1);
      const def = defPool.slice(0, dN);
      const mid = midPool.slice(0, mN);
      const fwd = fwdPool.slice(0, fN);
      const xi = [...gk, ...def, ...mid, ...fwd];
      const total = xi.reduce((a, p) => a + p.pts, 0);
      const bon = xi.reduce((a, p) => a + p.Bon, 0);
      if (
        !best ||
        total > best.total ||
        (total === best.total && bon > best.bon) ||
        (total === best.total && bon === best.bon && `${dN}-${mN}-${fN}` < best.formation)
      ) {
        best = { gk, def, mid, fwd, formation: `${dN}-${mN}-${fN}`, total, bon };
      }
    }

    if (best) return best;
    // Thin pools fallback: fill what we can toward 11 without breaking mins
    const gk = gkPool.slice(0, 1);
    const def = defPool.slice(0, Math.min(5, Math.max(3, defPool.length)));
    const mid = midPool.slice(0, Math.min(5, Math.max(2, midPool.length)));
    const fwd = fwdPool.slice(0, Math.min(3, Math.max(1, fwdPool.length)));
    return { gk, def, mid, fwd, formation: `${def.length}-${mid.length}-${fwd.length}` };
  }

  function rowHtml(p, cols) {
    const sub = `${escapeHtml(p.team_short)} · ${posShort(p.pos)}${
      p.price != null ? ` · £${fmt(p.price, 1)}m` : ""
    }`;
    return `<tr>
      <td class="gwrev-name">
        <div class="gwrev-name-main">${escapeHtml(p.player_name)}</div>
        <div class="gwrev-name-sub">${sub}</div>
      </td>
      ${cols.map((c) => `<td>${c(p)}</td>`).join("")}
    </tr>`;
  }

  function pitchPlayerHtml(p) {
    const fill = window.TeamColors?.teamFill?.(p.team_short) || "#3ddc97";
    const own =
      p.own != null ? ` · ${Number(p.own).toFixed(1).replace(/\.0$/, "")}%` : "";
    const badges = haulBadges(p);
    return `<div class="gwrev-pitch-player">
      <div class="gwrev-kit" style="background:${escapeHtml(fill)}">${escapeHtml(p.team_short)}</div>
      <div class="gwrev-pitch-name">${escapeHtml(shortName(p.player_name))}</div>
      <div class="gwrev-pitch-pts">${fmt(p.pts)} pts${own}</div>
      ${badges ? `<div class="gwrev-pitch-badges">${badges}</div>` : ""}
    </div>`;
  }

  function pitchRowHtml(list) {
    return `<div class="gwrev-pitch-row">${list.map(pitchPlayerHtml).join("")}</div>`;
  }

  function pitchBoardHtml(xi, { compact = false } = {}) {
    const cls = compact ? "gwrev-pitch gwrev-pitch--compact" : "gwrev-pitch";
    return `<div class="${cls}" aria-label="Team of the week ${escapeHtml(xi.formation)}">
      ${pitchRowHtml(xi.gk)}
      ${pitchRowHtml(xi.def)}
      ${pitchRowHtml(xi.mid)}
      ${pitchRowHtml(xi.fwd)}
    </div>`;
  }

  function tableHtml(headers, bodyRows) {
    return `<table class="gwrev-table">
      <thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
      <tbody>${bodyRows}</tbody>
    </table>`;
  }

  function sectionShell(id, kicker, title, subtitle, bodyHtml) {
    return `<article class="gwrev-card" data-name="gw_review.section.${id}">
      <div class="gwrev-export" id="${id}">
        <header class="gwrev-card-head">
          <p class="gwrev-kicker">${escapeHtml(kicker)}</p>
          <h2>${escapeHtml(title)}</h2>
          <p class="gwrev-sub">${escapeHtml(subtitle)}</p>
        </header>
        <div class="gwrev-card-body">${bodyHtml}</div>
      </div>
      <div class="gwrev-card-foot chart-dl-row">
        <button type="button" class="chart-dl" data-export="${id}">Download for X / Twitter</button>
      </div>
    </article>`;
  }

  function render() {
    if (!els.board) return;
    const players = gwPlayers();
    if (!players.length) {
      els.status.textContent = `${state.season} · GW ${state.gw} · no PL player minutes yet`;
      els.board.innerHTML = `<p class="empty">No Premier League player rows for this gameweek.</p>`;
      return;
    }

    const hauls = players.filter((p) => p.pts >= 10).length;
    const goals = players.reduce((a, p) => a + p.G, 0);
    const teamCs = teamCleanSheetCount(state.gw);
    const topPts = topN(players, "pts", 1)[0];
    const topXgi = topN(players, "xGI", 1)[0];
    const topHaulBadges = haulBadges(topPts);
    const topXgiBadges = haulBadges(topXgi, { goalsOnly: true });

    els.status.textContent = `${state.season} · GW ${state.gw} · ${players.length} players with minutes · ready to download section cards`;

    const LEAD = 8;
    const ptsLeaders = topN(players, "pts", 10, -1).filter((p) => p.pts > 0);
    const xgiLeaders = topN(players, "xGI", LEAD, -1);
    const goalLeaders = topN(players, "G", LEAD, -1);
    const chanceLeaders = [...players]
      .sort(
        (a, b) =>
          b.CC - a.CC || b.BCC - a.BCC || b.pts - a.pts || a.player_name.localeCompare(b.player_name)
      )
      .slice(0, LEAD);
    const assistLeaders = topN(players, "A", LEAD, -1);
    const defPool = players.filter((p) => p.pos === "Defender" || p.pos === "Goalkeeper");
    const defPts = topN(defPool, "pts", LEAD, -1);
    const defCon = topN(
      players.filter((p) => p.pos !== "Goalkeeper"),
      "DefCon",
      LEAD,
      -1
    );
    const over = [...players]
      .filter((p) => p.mins >= 60)
      .sort((a, b) => b.pts - b.xGI * 5 - (a.pts - a.xGI * 5))
      .slice(0, LEAD);
    const under = [...players]
      .filter((p) => p.mins >= 60 && p.xGI >= 0.4)
      .sort((a, b) => a.pts - a.xGI * 5 - (b.pts - b.xGI * 5))
      .slice(0, LEAD);
    const xi = pickXi(players);

    const snapshotBody = `
      <div class="gwrev-hero">
        <div class="gwrev-hero-gw">GW ${state.gw}</div>
        <div class="gwrev-hero-copy">
          <strong>${escapeHtml(state.season)}</strong>
          <span>🎙️ FPL Pulse Talk · quick read for the timeline</span>
        </div>
      </div>
      <div class="gwrev-kpis">
        ${kpiHtml("⚽ Goals", goalsValueHtml(goals), "across the PL")}
        ${kpiHtml("🛡️ Team clean sheets", teamCsValueHtml(teamCs), "teams that kept a CS")}
        ${kpiHtml("💎 10+ pts Haul", fmt(hauls), "players")}
        ${kpiHtml("🔥 Top haul", escapeHtml(topPts?.player_name || "—"), `${fmt(topPts?.pts)} pts`, topHaulBadges)}
        ${kpiHtml("🎯 Best xGI", escapeHtml(topXgi?.player_name || "—"), fmt(topXgi?.xGI, 2), topXgiBadges)}
      </div>
      <div class="gwrev-split gwrev-split--snapshot">
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🏆 Points leaders</h3>
          ${tableHtml(
            ["Player", "Pts", "G", "A", "Bonus"],
            ptsLeaders
              .map((p) =>
                rowHtml(p, [
                  (x) => fmt(x.pts),
                  (x) => fmt(x.G),
                  (x) => fmt(x.A),
                  (x) => fmt(x.Bon),
                ])
              )
              .join("")
          )}
        </div>
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">⭐ Team of the week · ${escapeHtml(xi.formation)}</h3>
          ${pitchBoardHtml(xi, { compact: true })}
        </div>
      </div>`;

    const attackBody = `
      <div class="gwrev-split">
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🎯 xGI leaders</h3>
          ${tableHtml(
            ["Player", "xGI", "xG", "xA", "Pts"],
            xgiLeaders
              .map((p) =>
                rowHtml(p, [
                  (x) => fmt(x.xGI, 2),
                  (x) => fmt(x.xG, 2),
                  (x) => fmt(x.xA, 2),
                  (x) => fmt(x.pts),
                ])
              )
              .join("")
          )}
        </div>
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">⚽ Goals</h3>
          ${tableHtml(
            ["Player", "G", "npxG", "Pts"],
            goalLeaders
              .map((p) =>
                rowHtml(p, [(x) => fmt(x.G), (x) => fmt(x.npxG, 2), (x) => fmt(x.pts)])
              )
              .join("")
          )}
        </div>
      </div>
      <hr class="gwrev-rule" />
      <div class="gwrev-split">
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🪄 Chances created</h3>
          ${tableHtml(
            ["Player", "CC", "BCC", "Pts"],
            chanceLeaders
              .map((p) =>
                rowHtml(p, [(x) => fmt(x.CC), (x) => fmt(x.BCC), (x) => fmt(x.pts)])
              )
              .join("")
          )}
        </div>
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🅰️ Assists</h3>
          ${tableHtml(
            ["Player", "A", "xA", "Pts"],
            assistLeaders
              .map((p) =>
                rowHtml(p, [(x) => fmt(x.A), (x) => fmt(x.xA, 2), (x) => fmt(x.pts)])
              )
              .join("")
          )}
        </div>
      </div>
      <hr class="gwrev-rule" />
      <h3 class="gwrev-h3">⚡ Haul vs involvement</h3>
      <p class="gwrev-note">Over = points ahead of xGI involvement · Under = quiet night despite xGI</p>
      <div class="gwrev-split">
        <div class="gwrev-panel">
          <h4 class="gwrev-h4">📈 Overperformed</h4>
          ${tableHtml(
            ["Player", "Pts", "xGI"],
            over.map((p) => rowHtml(p, [(x) => fmt(x.pts), (x) => fmt(x.xGI, 2)])).join("")
          )}
        </div>
        <div class="gwrev-panel">
          <h4 class="gwrev-h4">📉 Underperformed</h4>
          ${tableHtml(
            ["Player", "Pts", "xGI"],
            under.map((p) => rowHtml(p, [(x) => fmt(x.pts), (x) => fmt(x.xGI, 2)])).join("")
          )}
        </div>
      </div>`;

    const defenceBody = `
      <div class="gwrev-split">
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🛡️ DEF + GK by points</h3>
          ${tableHtml(
            ["Player", "Pts", "CS", "GC", "Sv"],
            defPts
              .map((p) =>
                rowHtml(p, [
                  (x) => fmt(x.pts),
                  (x) => fmt(x.cs),
                  (x) => fmt(x.GC),
                  (x) => fmt(x.Sv),
                ])
              )
              .join("")
          )}
        </div>
        <div class="gwrev-panel">
          <h3 class="gwrev-h3">🧱 DefCon leaders</h3>
          ${tableHtml(
            ["Player", "DefCon", "CBI", "Pts"],
            defCon
              .map((p) =>
                rowHtml(p, [(x) => fmt(x.DefCon), (x) => fmt(x.CBI), (x) => fmt(x.pts)])
              )
              .join("")
          )}
        </div>
      </div>`;

    const xiBody = `
      <p class="gwrev-note">⭐ Best ${xi.formation} by FPL points in GW ${state.gw} · 1 GK · DEF 3–5 · MID 2–5 · FWD 1–3 · always 11 (no budget / ownership filter)</p>
      ${pitchBoardHtml(xi)}
      <p class="gwrev-xi-total">XI total · <strong>${fmt(
        [...xi.gk, ...xi.def, ...xi.mid, ...xi.fwd].reduce((a, p) => a + p.pts, 0)
      )} pts</strong></p>`;

    els.board.innerHTML = [
      sectionShell(
        "gwrev-snapshot",
        "🎙️ FPL Pulse Talk",
        `GW ${state.gw} snapshot`,
        "Headline KPIs + points leaders + team of the week",
        snapshotBody
      ),
      sectionShell(
        "gwrev-attack",
        `GW ${state.gw} · ⚔️ Attack`,
        "Chance & finishing",
        "xGI, goals, chances, assists, and haul vs involvement",
        attackBody
      ),
      sectionShell(
        "gwrev-defence",
        `GW ${state.gw} · 🛡️ Defence`,
        "Clean sheets & DefCon",
        "Back line returns and defensive contribution",
        defenceBody
      ),
      sectionShell(
        "gwrev-xi",
        `GW ${state.gw} · ⭐ Team of the week`,
        "Points XI",
        "Best haul by position — pitch view",
        xiBody
      ),
    ].join("");

    bindExports();
  }

  function bindExports() {
    els.board.querySelectorAll("[data-export]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      const id = btn.getAttribute("data-export");
      window.ChartExport?.bindChartDownload(
        btn,
        () => document.getElementById(id),
        () => `fpl-pulse-talk-gw${state.gw}-${id.replace("gwrev-", "")}`,
        () => ({
          title: captionTitle(id),
          metrics: "FPL-Core PL match layer · DGW rows summed · pts / xG / xA / xGI / DefCon",
          meta: `${state.season} · GW ${state.gw} · @fpl_pulse_talk`,
        })
      );
    });
  }

  function captionTitle(id) {
    if (id === "gwrev-snapshot") return `GW ${state.gw} FPL snapshot — points & hauls`;
    if (id === "gwrev-attack") return `GW ${state.gw} attack board — xGI · G · A`;
    if (id === "gwrev-defence") return `GW ${state.gw} defence board — CS · DefCon`;
    if (id === "gwrev-xi") return `GW ${state.gw} points XI`;
    return `GW ${state.gw} review`;
  }

  window.initGwReview = init;
})();
