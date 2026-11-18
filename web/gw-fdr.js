/* GW FDR — future gameweek goal / CS outlook from season history. */
(() => {
  const META_URL = "./data/meta.json";
  const TG_URL = "./data/teams_gw.json";
  const FX_URL = "./data/fixtures.json";
  const PL = "Premier League";
  const TOP_N = 7;
  const FROST_DEF_N = 4;
  const COLOR_HOME = "#9ec9f5";
  const COLOR_AWAY = "#ff9a9a";
  /** Clockwise from top: attack, then matching -A opposite (xG↔xG-A, etc.). */
  const SPIDER_AXES = [
    { key: "xg", label: "xG" },
    { key: "sot", label: "SoT" },
    { key: "sib", label: "SiB" },
    { key: "bcc", label: "BCC" },
    { key: "xga", label: "xG-A" },
    { key: "sotA", label: "SoT-A" },
    { key: "sibA", label: "SiB-A" },
    { key: "bccA", label: "BCC-A" },
  ];

  const state = {
    meta: null,
    teams: [],
    fixtures: [],
    season: null,
    gw: null,
    lastN: null,
    perMatch: false,
  };
  const els = {};
  let started = false;

  function $(id) {
    return document.getElementById(id);
  }

  function num(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
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
      const [metaRes, tgRes, fxRes] = await Promise.all([
        fetch(META_URL, { cache: "no-store" }),
        fetch(TG_URL, { cache: "no-store" }),
        fetch(FX_URL, { cache: "no-store" }),
      ]);
      if (!metaRes.ok) throw new Error(`meta HTTP ${metaRes.status}`);
      if (!tgRes.ok) throw new Error(`teams_gw HTTP ${tgRes.status}`);
      if (!fxRes.ok) throw new Error(`fixtures HTTP ${fxRes.status}`);
      state.meta = await metaRes.json();
      state.teams = await tgRes.json();
      const fx = await fxRes.json();
      state.fixtures = (fx.upcoming || []).filter(
        (f) => (!f.competition || f.competition === PL) && f.gw != null
      );
      state.season = state.meta.current_season || state.meta.analysis_season;
      populateGw();
      syncLastNBounds(true);
      render();
    } catch (err) {
      if (els.status) els.status.textContent = `Failed to load: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("gwfdr-root");
    els.gw = $("gwfdr-gw");
    els.lastN = $("gwfdr-lastn");
    els.lastNVal = $("gwfdr-lastn-val");
    els.status = $("gwfdr-status");
    els.seasonBoard = $("gwfdr-season-board");
    els.gwScore = $("gwfdr-gw-score");
    els.fixtures = $("gwfdr-fixtures");
    els.fxTitle = $("gwfdr-fx-title");
    els.fxDl = $("gwfdr-fx-dl");
    els.perMatch = $("gwfdr-per-match");
    els.tip = $("gwfdr-tip");
  }

  function bindEvents() {
    els.gw?.addEventListener("change", () => {
      state.gw = Number(els.gw.value);
      render();
    });
    els.lastN?.addEventListener("input", () => {
      syncLastNFromUi();
      render();
    });
    els.perMatch?.addEventListener("change", () => {
      state.perMatch = Boolean(els.perMatch.checked);
      render();
    });
    if (els.fxDl && !els.fxDl.dataset.bound) {
      els.fxDl.dataset.bound = "1";
      els.fxDl.addEventListener("click", () => downloadFixturesAll());
    }
  }

  function raf2() {
    return new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  }

  /** Export all fixture cards in one image. */
  async function downloadFixturesAll() {
    const btn = els.fxDl;
    if (!btn || !els.fixtures || !window.ChartExport?.downloadChart) return;
    const list = els.fixtures.querySelector(".gwfdr-fx-list");
    if (!list || !list.querySelector(".gwfdr-fx")) return;

    const prev = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Saving…";
    const lede = els.fixtures.querySelector(".gwfdr-lede");
    const ledeWasHidden = lede?.hidden;
    if (lede) lede.hidden = true;

    try {
      list.classList.add("gwfdr-fx-export");
      // Fixed 1080 social canvas — independent of phone viewport media queries.
      list.style.width = "1080px";
      list.style.maxWidth = "1080px";
      list.style.position = "fixed";
      list.style.left = "-12000px";
      list.style.top = "0";
      list.style.zIndex = "-1";
      list.style.pointerEvents = "none";
      const spiderData = state._spiderData || [];
      list.querySelectorAll("[data-spider-idx]").forEach((host) => {
        const i = Number(host.getAttribute("data-spider-idx"));
        const d = spiderData[i];
        if (d) renderFixtureSpider(host, d.home, d.away, d.hShort, d.aShort);
      });
      await raf2();
      await window.ChartExport.downloadChart(
        list,
        `fpl-pulse-talk-gw${state.gw}-fixtures`,
        {
          title: `GW ${state.gw} fixtures`,
          meta: state.season || "",
          metrics: state.perMatch ? "Per match · Attack | Defence (-A)" : "Totals · Attack | Defence (-A)",
        }
      );
      btn.textContent = "Saved";
    } catch (err) {
      console.error(err);
      btn.textContent = "Failed";
    } finally {
      list.classList.remove("gwfdr-fx-export");
      list.style.width = "";
      list.style.maxWidth = "";
      list.style.position = "";
      list.style.left = "";
      list.style.top = "";
      list.style.zIndex = "";
      list.style.pointerEvents = "";
      const spiderData = state._spiderData || [];
      list.querySelectorAll("[data-spider-idx]").forEach((host) => {
        const i = Number(host.getAttribute("data-spider-idx"));
        const d = spiderData[i];
        if (d) renderFixtureSpider(host, d.home, d.away, d.hShort, d.aShort);
      });
      if (lede) lede.hidden = Boolean(ledeWasHidden);
      setTimeout(() => {
        btn.textContent = prev;
        btn.disabled = false;
      }, 900);
    }
  }

  function populateGw() {
    const gws = [...new Set(state.fixtures.map((f) => Number(f.gw)).filter((g) => g > 0))].sort(
      (a, b) => a - b
    );
    const next = Number(state.meta?.upcoming_gw) || gws[0] || null;
    state.gw = gws.includes(next) ? next : gws[0] || null;
    if (!els.gw) return;
    els.gw.replaceChildren(
      ...gws.map((g) => {
        const opt = document.createElement("option");
        opt.value = String(g);
        opt.textContent = `GW ${g}`;
        opt.selected = g === state.gw;
        return opt;
      })
    );
  }

  function finishedPl(season) {
    return (state.teams || []).filter(
      (r) =>
        r.finished &&
        r.season === season &&
        (!r.competition || r.competition === PL) &&
        r.team_code != null
    );
  }

  function maxFinishedGw(season) {
    return Math.max(0, ...finishedPl(season).map((r) => Number(r.gw) || 0));
  }

  function syncLastNBounds(resetValue) {
    const maxFin = maxFinishedGw(state.season) || 1;
    if (els.lastN) {
      els.lastN.min = "1";
      els.lastN.max = String(maxFin);
      if (resetValue || state.lastN == null) {
        state.lastN = maxFin;
        els.lastN.value = String(maxFin);
      } else {
        state.lastN = Math.max(1, Math.min(maxFin, Number(state.lastN) || maxFin));
        els.lastN.value = String(state.lastN);
      }
    } else if (state.lastN == null) {
      state.lastN = maxFin;
    }
    syncLastNLabel();
  }

  function syncLastNFromUi() {
    const maxFin = Number(els.lastN?.max) || maxFinishedGw(state.season) || 1;
    state.lastN = Math.max(1, Math.min(maxFin, Number(els.lastN?.value) || maxFin));
    syncLastNLabel();
  }

  function syncLastNLabel() {
    if (els.lastNVal) els.lastNVal.textContent = String(state.lastN ?? "—");
  }

  function windowLabel(beforeGw) {
    const n = state.lastN;
    const maxFin = maxFinishedGw(state.season);
    if (n != null && n < maxFin) return `last ${n} finished GWs`;
    return `season to date (before GW ${beforeGw})`;
  }

  /** Per-team rates using matches finished before `beforeGw` (exclusive). */
  function teamRates(season, beforeGw, lastN) {
    const rows = finishedPl(season).filter((r) => Number(r.gw) < Number(beforeGw));
    const byTeam = new Map();
    for (const r of rows) {
      const code = String(r.team_code);
      if (!byTeam.has(code)) byTeam.set(code, []);
      byTeam.get(code).push(r);
    }
    const out = new Map();
    const take = lastN != null && lastN > 0 ? lastN : null;
    for (const [code, list] of byTeam) {
      const sorted = [...list].sort((a, b) => Number(a.gw) - Number(b.gw));
      const win = take ? sorted.slice(-take) : sorted;
      if (!win.length) continue;
      const sum = (k) => win.reduce((a, r) => a + num(r[k]), 0);
      const n = win.length;
      const last = win[win.length - 1];
      out.set(code, {
        team_code: code,
        short: last.short || last.team || code,
        apps: n,
        gf: sum("goals_for") / n,
        xg: sum("xg") / n,
        sh: sum("shots") / n,
        sot: sum("shots_on_target") / n,
        sib: sum("shots_inside_box") / n,
        cc: sum("CC") / n,
        bcc: sum("big_chances") / n,
        ga: sum("goals_against") / n,
        xga: sum("xga") / n,
        shA: sum("shots_conceded") / n,
        sotA: sum("sot_conceded") / n,
        sibA: sum("shots_inside_box_against") / n,
        ccA: sum("CC_A") / n,
        bccA: sum("big_chances_conceded") / n,
        gfTot: sum("goals_for"),
        xgTot: sum("xg"),
        shTot: sum("shots"),
        sotTot: sum("shots_on_target"),
        sibTot: sum("shots_inside_box"),
        ccTot: sum("CC"),
        bccTot: sum("big_chances"),
        gaTot: sum("goals_against"),
        xgaTot: sum("xga"),
        shATot: sum("shots_conceded"),
        sotATot: sum("sot_conceded"),
        sibATot: sum("shots_inside_box_against"),
        ccATot: sum("CC_A"),
        bccATot: sum("big_chances_conceded"),
      });
    }
    return out;
  }

  /** Ranks for Firewire / Frost / Shield using the page form window (last N). */
  function seasonRanks(season, lastN) {
    const maxFinished = maxFinishedGw(season);
    const before = maxFinished + 1;
    const rates = teamRates(season, before, lastN);
    const list = [...rates.values()];
    const byG = [...list].sort((a, b) => b.gf - a.gf);
    const byXga = [...list].sort((a, b) => b.xga - a.xga); // high xGA = leaky
    const byTight = [...list].sort((a, b) => a.xga - b.xga); // low xGA = strong defence
    const topAttack = new Set(byG.slice(0, TOP_N).map((t) => t.team_code));
    const weakAttack = new Set(byG.slice(-TOP_N).map((t) => t.team_code));
    const leakyDef = new Set(byXga.slice(0, TOP_N).map((t) => t.team_code));
    const tightDef = new Set(byTight.slice(0, TOP_N).map((t) => t.team_code));
    const eliteDef = new Set(byTight.slice(0, FROST_DEF_N).map((t) => t.team_code));
    return { rates, topAttack, weakAttack, leakyDef, tightDef, eliteDef, maxFinished };
  }

  function fixturesForGw(gw) {
    return state.fixtures
      .filter((f) => Number(f.gw) === Number(gw) && f.season === state.season)
      .sort((a, b) => String(a.kickoff_utc || "").localeCompare(String(b.kickoff_utc || "")));
  }

  function futureGws() {
    return [...new Set(state.fixtures.filter((f) => f.season === state.season).map((f) => Number(f.gw)))]
      .filter((g) => g > 0)
      .sort((a, b) => a - b);
  }

  /** Firewire: top-7 G attack facing top-7 xGC (leaky) defence. */
  function isFirewire(f, ranks) {
    const h = String(f.home_code);
    const a = String(f.away_code);
    return (
      (ranks.topAttack.has(h) && ranks.leakyDef.has(a)) ||
      (ranks.topAttack.has(a) && ranks.leakyDef.has(h))
    );
  }

  function isShield(f, ranks) {
    const h = String(f.home_code);
    const a = String(f.away_code);
    return (
      (ranks.weakAttack.has(h) && ranks.tightDef.has(a)) ||
      (ranks.weakAttack.has(a) && ranks.tightDef.has(h))
    );
  }

  /** Frost: top-7 G attack facing top-4 elite (lowest xGC) defence — low-scoring clash. */
  function isFrost(f, ranks) {
    const h = String(f.home_code);
    const a = String(f.away_code);
    const elite = ranks.eliteDef || ranks.tightDef;
    return (
      (ranks.topAttack.has(h) && elite.has(a)) || (ranks.topAttack.has(a) && elite.has(h))
    );
  }

  function countFirewire(fxList, ranks) {
    return fxList.filter((f) => isFirewire(f, ranks)).length;
  }

  /** Shield: bottom-7 G attack facing top-7 tight (low xGA) defence. */
  function countShield(fxList, ranks) {
    return fxList.filter((f) => isShield(f, ranks)).length;
  }

  function countFrost(fxList, ranks) {
    return fxList.filter((f) => isFrost(f, ranks)).length;
  }

  function fixtureGLine(f, ranks) {
    const home = ranks.rates.get(String(f.home_code));
    const away = ranks.rates.get(String(f.away_code));
    const hShort = f.home_short || home?.short || "HOME";
    const aShort = f.away_short || away?.short || "AWAY";
    return {
      home: hShort,
      away: aShort,
      hg: home ? home.gf : null,
      ag: away ? away.gf : null,
    };
  }

  function hideTip() {
    if (els.tip) els.tip.hidden = true;
  }

  function showBogieTip(event, gw, ranks) {
    if (!els.tip) return;
    const fx = fixturesForGw(gw);
    const fire = fx.filter((f) => isFirewire(f, ranks)).map((f) => fixtureGLine(f, ranks));
    const frost = fx.filter((f) => isFrost(f, ranks)).map((f) => fixtureGLine(f, ranks));
    const shield = fx.filter((f) => isShield(f, ranks)).map((f) => fixtureGLine(f, ranks));
    const row = (list) =>
      list.length
        ? list
            .map(
              (r) => `<div class="gwfdr-tip-fx">
                <span class="gwfdr-tip-home">${escapeHtml(r.home)} <b>${fmt2(r.hg)}</b></span>
                <span class="gwfdr-tip-vs">vs</span>
                <span class="gwfdr-tip-away"><b>${fmt2(r.ag)}</b> ${escapeHtml(r.away)}</span>
              </div>`
            )
            .join("")
        : `<div class="gwfdr-tip-empty">None</div>`;
    els.tip.hidden = false;
    els.tip.innerHTML = `<strong>GW ${gw}</strong>
      <span>G / match · home left · away right</span>
      <div class="gwfdr-tip-sec gwfdr-tip-sec--fire"><em>Firewire</em>${row(fire)}</div>
      <div class="gwfdr-tip-sec gwfdr-tip-sec--frost"><em>Frost</em>${row(frost)}</div>
      <div class="gwfdr-tip-sec gwfdr-tip-sec--shield"><em>Shield</em>${row(shield)}</div>`;
    const pad = 14;
    const tw = els.tip.offsetWidth || 280;
    const th = els.tip.offsetHeight || 160;
    els.tip.style.left = `${Math.min(window.innerWidth - tw - 8, event.clientX + pad)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - th - 8, event.clientY + pad)}px`;
  }

  /** Tag counts for every remaining GW (for relative Pulse heats). */
  function seasonTagProfile(ranks) {
    return futureGws().map((gw) => {
      const fx = fixturesForGw(gw);
      return {
        gw,
        n: fx.length,
        firewire: countFirewire(fx, ranks),
        frost: countFrost(fx, ranks),
        shield: countShield(fx, ranks),
      };
    });
  }

  function scaleHeat(val, series) {
    if (!series.length) return 5;
    const min = Math.min(...series);
    const max = Math.max(...series);
    if (max <= min) return 5;
    return Math.round((10 * (val - min)) / (max - min));
  }

  /**
   * FDR Pulse: dual 0–10 heats scaled vs remaining GWs (not a cancelled Fire−Shield net).
   * Goal ← Firewire · CS ← Shield · Frost shown separately. Verdict names the climate.
   */
  function gwPulse(fxList, ranks) {
    const firewire = countFirewire(fxList, ranks);
    const frost = countFrost(fxList, ranks);
    const shield = countShield(fxList, ranks);
    if (!fxList.length) {
      return {
        firewire: 0,
        frost: 0,
        shield: 0,
        goalHeat: null,
        csHeat: null,
        frostHeat: null,
        verdict: "—",
        verdictTone: "eq",
      };
    }
    const profile = seasonTagProfile(ranks);
    const goalHeat = scaleHeat(
      firewire,
      profile.map((p) => p.firewire)
    );
    const csHeat = scaleHeat(
      shield,
      profile.map((p) => p.shield)
    );
    const frostHeat = scaleHeat(
      frost,
      profile.map((p) => p.frost)
    );
    let verdict = "Balanced GW";
    let verdictTone = "eq";
    const goalHi = goalHeat >= 7;
    const csHi = csHeat >= 7;
    const goalLo = goalHeat <= 3;
    const csLo = csHeat <= 3;
    if (goalHi && csHi) {
      verdict = "Polarised — hauls and blanks";
      verdictTone = "split";
    } else if (goalHi && csLo) {
      verdict = "Goal-heavy GW";
      verdictTone = "hi";
    } else if (csHi && goalLo) {
      verdict = "CS-friendly GW";
      verdictTone = "lo";
    } else if (frostHeat >= 7 && goalLo) {
      verdict = "Frosty — elite vs elite";
      verdictTone = "frost";
    } else if (goalHeat >= csHeat + 2) {
      verdict = "Slight goal lean";
      verdictTone = "hi";
    } else if (csHeat >= goalHeat + 2) {
      verdict = "Slight CS lean";
      verdictTone = "lo";
    }
    return {
      firewire,
      frost,
      shield,
      goalHeat,
      csHeat,
      frostHeat,
      verdict,
      verdictTone,
    };
  }

  /** League top-3 / bottom-3 sets per metric (by per-match rate in the active window). */
  function leagueExtremes(rates) {
    const specs = [
      "gf",
      "xg",
      "sh",
      "sot",
      "sib",
      "cc",
      "bcc",
      "ga",
      "xga",
      "shA",
      "sotA",
      "sibA",
      "ccA",
      "bccA",
    ];
    const teams = [...rates.values()];
    const out = {};
    for (const key of specs) {
      const sorted = [...teams].sort((a, b) => num(b[key]) - num(a[key]));
      out[key] = {
        top: new Set(sorted.slice(0, 3).map((t) => String(t.team_code))),
        bot: new Set(sorted.slice(-3).map((t) => String(t.team_code))),
      };
    }
    return out;
  }

  function heatBar(score, tone) {
    const s = score == null ? 0 : score;
    const pct = Math.max(0, Math.min(100, s * 10));
    return `<div class="gwfdr-heat gwfdr-heat--${tone}" title="${s}/10">
      <i style="width:${pct}%"></i><b>${s == null ? "—" : s}</b>
    </div>`;
  }

  function fmt1(v) {
    return v == null || !Number.isFinite(v) ? "—" : v.toFixed(1);
  }

  function fmt2(v) {
    return v == null || !Number.isFinite(v) ? "—" : v.toFixed(2);
  }

  function renderSeasonBoard(ranks) {
    if (!els.seasonBoard) return;
    const gws = futureGws();
    const cars = gws.map((gw) => {
      const fx = fixturesForGw(gw);
      return {
        gw,
        firewire: countFirewire(fx, ranks),
        frost: countFrost(fx, ranks),
        shield: countShield(fx, ranks),
      };
    });
    els.seasonBoard.innerHTML = `
      <div class="name-row"><h2>Season outlook</h2></div>
      <p class="lede gwfdr-lede">Remaining GWs as a train (tags use the form window above). Hover for tagged fixtures; click to select that GW.</p>
      <ul class="gwfdr-legend">
        <li><strong class="gwfdr-fire">Firewire</strong> — top-${TOP_N} G vs leaky top-${TOP_N} xGC</li>
        <li><strong class="gwfdr-frost">Frost</strong> — top-${TOP_N} G vs top-${FROST_DEF_N} elite/tight defence (low-scoring)</li>
        <li><strong class="gwfdr-shield">Shield</strong> — bottom-${TOP_N} G vs top-${TOP_N} tight defence</li>
      </ul>
      <div class="gwfdr-train" role="list" aria-label="Season outlook by gameweek">
        ${cars
          .map(
            (c, i) => `${i ? `<div class="gwfdr-coupler" aria-hidden="true"></div>` : ""}
            <button type="button" class="gwfdr-bogie${c.gw === state.gw ? " is-active" : ""}" role="listitem"
              data-jump-gw="${c.gw}" aria-label="GW ${c.gw}, Firewire ${c.firewire}, Frost ${c.frost}, Shield ${c.shield}">
              <span class="gwfdr-bogie-roof"></span>
              <span class="gwfdr-bogie-gw">GW ${c.gw}</span>
              <span class="gwfdr-bogie-metric gwfdr-fire"><i>Firewire</i><b>${c.firewire}</b></span>
              <span class="gwfdr-bogie-metric gwfdr-frost"><i>Frost</i><b>${c.frost}</b></span>
              <span class="gwfdr-bogie-metric gwfdr-shield"><i>Shield</i><b>${c.shield}</b></span>
              <span class="gwfdr-bogie-wheels" aria-hidden="true"><i></i><i></i></span>
            </button>`
          )
          .join("")}
      </div>`;
    els.seasonBoard.querySelectorAll("[data-jump-gw]").forEach((btn) => {
      const g = Number(btn.getAttribute("data-jump-gw"));
      btn.addEventListener("click", () => {
        if (!g || !els.gw) return;
        els.gw.value = String(g);
        state.gw = g;
        render();
      });
      btn.addEventListener("mousemove", (event) => showBogieTip(event, g, ranks));
      btn.addEventListener("mouseleave", hideTip);
      btn.addEventListener("blur", hideTip);
    });
  }

  function sideRaw(t, perMatch) {
    const z = Object.fromEntries(SPIDER_AXES.map((a) => [a.key, 0]));
    if (!t) return z;
    const v = (rate, tot) => (perMatch ? num(t[rate]) : num(t[tot] ?? t[rate] * t.apps));
    return {
      xg: v("xg", "xgTot"),
      sot: v("sot", "sotTot"),
      sib: v("sib", "sibTot"),
      bcc: v("bcc", "bccTot"),
      xga: v("xga", "xgaTot"),
      sotA: v("sotA", "sotATot"),
      sibA: v("sibA", "sibATot"),
      bccA: v("bccA", "bccATot"),
    };
  }

  function polarPoint(cx, cy, r, angle) {
    return [cx + r * Math.sin(angle), cy - r * Math.cos(angle)];
  }

  function renderFixtureSpider(host, homeVals, awayVals, hLabel, aLabel) {
    if (!host || typeof d3 === "undefined") return;
    host.replaceChildren();
    const width = host.clientWidth || 168;
    const height = width;
    const svg = d3.select(host).append("svg").attr("viewBox", `0 0 ${width} ${height}`);
    const cx = width / 2;
    const cy = height / 2;
    const radius = width * 0.34;
    const n = SPIDER_AXES.length;
    const angle = (i) => (i / n) * Math.PI * 2;

    [0.35, 0.7, 1].forEach((t) => {
      const pts = SPIDER_AXES.map((_, i) => polarPoint(cx, cy, radius * t, angle(i)));
      svg
        .append("polygon")
        .attr("points", pts.map((p) => p.join(",")).join(" "))
        .attr("fill", "none")
        .attr("stroke", "rgba(255,255,255,0.12)")
        .attr("stroke-width", 1);
    });

    SPIDER_AXES.forEach((axis, i) => {
      const [x, y] = polarPoint(cx, cy, radius, angle(i));
      svg
        .append("line")
        .attr("x1", cx)
        .attr("y1", cy)
        .attr("x2", x)
        .attr("y2", y)
        .attr("stroke", "rgba(255,255,255,0.14)")
        .attr("stroke-width", 1);
      const [lx, ly] = polarPoint(cx, cy, radius + 14, angle(i));
      svg
        .append("text")
        .attr("x", lx)
        .attr("y", ly)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .attr("fill", i < 4 ? "#8fd9b4" : "#f0a0a0")
        .attr("font-size", Math.max(9, Math.round(width * 0.048)))
        .attr("font-weight", 700)
        .attr("pointer-events", "none")
        .text(axis.label);
    });

    const maxByAxis = Object.fromEntries(
      SPIDER_AXES.map((a) => [
        a.key,
        Math.max(homeVals[a.key], awayVals[a.key], a.key.includes("xg") ? 0.01 : 1),
      ])
    );

    function poly(vals, color, opacity) {
      const pts = SPIDER_AXES.map((a, i) => {
        const t = maxByAxis[a.key] ? vals[a.key] / maxByAxis[a.key] : 0;
        return polarPoint(cx, cy, radius * Math.min(1, Math.max(0, t)), angle(i));
      });
      svg
        .append("polygon")
        .attr("points", pts.map((p) => p.join(",")).join(" "))
        .attr("fill", color)
        .attr("fill-opacity", opacity)
        .attr("stroke", color)
        .attr("stroke-width", 1.6)
        .attr("pointer-events", "none");
      pts.forEach(([x, y]) => {
        svg
          .append("circle")
          .attr("cx", x)
          .attr("cy", y)
          .attr("r", 2.4)
          .attr("fill", color)
          .attr("stroke", "rgba(0,0,0,0.35)")
          .attr("stroke-width", 0.6);
      });
    }
    poly(homeVals, COLOR_HOME, 0.2);
    poly(awayVals, COLOR_AWAY, 0.16);

    svg
      .append("title")
      .text(`${hLabel} vs ${aLabel} · each attack axis opposite its -A`);
  }

    function sideMetrics(t, perMatch) {
    const keys = ["gf", "xg", "sh", "sot", "sib", "cc", "bcc", "ga", "xga", "shA", "sotA", "sibA", "ccA", "bccA"];
    const empty = Object.fromEntries(keys.map((k) => [k, "—"]));
    if (!t) return empty;
    const pick = (rateKey, totKey, digits) => {
      const v = perMatch ? t[rateKey] : t[totKey] ?? t[rateKey] * t.apps;
      return digits === 2 ? fmt2(v) : fmt1(v);
    };
    return {
      gf: pick("gf", "gfTot", perMatch ? 2 : 1),
      xg: pick("xg", "xgTot", 2),
      sh: pick("sh", "shTot", perMatch ? 2 : 1),
      sot: pick("sot", "sotTot", perMatch ? 2 : 1),
      sib: pick("sib", "sibTot", perMatch ? 2 : 1),
      cc: pick("cc", "ccTot", perMatch ? 2 : 1),
      bcc: pick("bcc", "bccTot", perMatch ? 2 : 1),
      ga: pick("ga", "gaTot", perMatch ? 2 : 1),
      xga: pick("xga", "xgaTot", 2),
      shA: pick("shA", "shATot", perMatch ? 2 : 1),
      sotA: pick("sotA", "sotATot", perMatch ? 2 : 1),
      sibA: pick("sibA", "sibATot", perMatch ? 2 : 1),
      ccA: pick("ccA", "ccATot", perMatch ? 2 : 1),
      bccA: pick("bccA", "bccATot", perMatch ? 2 : 1),
    };
  }

  function metricCell(value, band, key, teamCode, extremes) {
    const code = teamCode == null ? "" : String(teamCode);
    const ex = extremes?.[key];
    let mark = "";
    let cls = `col-${band}`;
    let tip = "";
    if (ex && code) {
      if (ex.top.has(code)) {
        cls += " is-top3";
        mark = `<sup>▲</sup>`;
        tip = ` title="Top 3 in league for this metric"`;
      } else if (ex.bot.has(code)) {
        cls += " is-bot3";
        mark = `<sup>▼</sup>`;
        tip = ` title="Bottom 3 in league for this metric"`;
      }
    }
    return `<b class="${cls}"${tip}>${value}${mark}</b>`;
  }

  function metricCells(m, teamCode, extremes) {
    const atk = ["gf", "xg", "sh", "sot", "sib", "cc", "bcc"];
    const deff = ["ga", "xga", "shA", "sotA", "sibA", "ccA", "bccA"];
    return (
      atk.map((k) => metricCell(m[k], "attack", k, teamCode, extremes)).join("") +
      deff.map((k) => metricCell(m[k], "defend", k, teamCode, extremes)).join("")
    );
  }

  function renderFixtures(ranks) {
    if (!els.fixtures || !els.gwScore) return;
    const fx = fixturesForGw(state.gw);
    const rates = teamRates(state.season, state.gw, state.lastN);
    const pulse = gwPulse(fx, ranks);
    const extremes = leagueExtremes(rates);
    const wLabel = windowLabel(state.gw);
    const scaleLabel = state.perMatch ? "per match" : "totals";
    if (els.fxTitle) els.fxTitle.textContent = `GW ${state.gw} fixtures`;

    els.gwScore.innerHTML = `
      <div class="gwfdr-score-card">
        <div class="gwfdr-score-main">
          <span class="gwfdr-score-label">GW ${state.gw} FDR Pulse</span>
          <span class="gwfdr-verdict gwfdr-verdict--${pulse.verdictTone}">${escapeHtml(pulse.verdict)}</span>
        </div>
        <div class="gwfdr-heat-grid" aria-label="Relative heats vs remaining gameweeks">
          <div class="gwfdr-heat-row">
            <span class="gwfdr-heat-label gwfdr-fire">Goal heat <em>${pulse.firewire} Firewire</em></span>
            ${heatBar(pulse.goalHeat, "hi")}
          </div>
          <div class="gwfdr-heat-row">
            <span class="gwfdr-heat-label gwfdr-shield">CS heat <em>${pulse.shield} Shield</em></span>
            ${heatBar(pulse.csHeat, "lo")}
          </div>
          <div class="gwfdr-heat-row">
            <span class="gwfdr-heat-label gwfdr-frost">Frost heat <em>${pulse.frost} Frost</em></span>
            ${heatBar(pulse.frostHeat, "frost")}
          </div>
        </div>
        <p class="gwfdr-score-meta">Heats are 0–10 vs other remaining GWs (not a cancelled Fire−Shield net). Window = ${wLabel}.</p>
      </div>`;

    if (!fx.length) {
      els.fixtures.innerHTML = `<p class="empty">No upcoming Premier League fixtures for GW ${state.gw}.</p>`;
      return;
    }

    const spiderData = [];
    state._spiderData = spiderData;
    els.fixtures.innerHTML = `
      <p class="lede gwfdr-lede">${scaleLabel[0].toUpperCase() + scaleLabel.slice(1)} in the selected window (${wLabel}). ▲ top-3 / ▼ bottom-3 league for that metric (per-match rate). Spider pairs each metric with its -A opposite.</p>
      <div class="gwfdr-fx-list">
        ${fx
          .map((f, idx) => {
            const home = rates.get(String(f.home_code));
            const away = rates.get(String(f.away_code));
            const hm = sideMetrics(home, state.perMatch);
            const am = sideMetrics(away, state.perMatch);
            const hShort = f.home_short || home?.short || "HOME";
            const aShort = f.away_short || away?.short || "AWAY";
            spiderData.push({
              home: sideRaw(home, state.perMatch),
              away: sideRaw(away, state.perMatch),
              hShort,
              aShort,
            });
            const fire = isFirewire(f, ranks);
            const frost = isFrost(f, ranks);
            const shield = isShield(f, ranks);
            const badges = [
              fire ? `<span class="gwfdr-badge gwfdr-badge--fire">Firewire</span>` : "",
              frost ? `<span class="gwfdr-badge gwfdr-badge--frost">Frost</span>` : "",
              shield ? `<span class="gwfdr-badge gwfdr-badge--shield">Shield</span>` : "",
            ]
              .filter(Boolean)
              .join("");
            return `<article class="gwfdr-fx">
              <div class="gwfdr-fx-top">
                <div class="gwfdr-fx-match">
                  <strong class="gwfdr-fx-home-name">${escapeHtml(hShort)}</strong>
                  <span class="gwfdr-fx-vs">vs</span>
                  <strong class="gwfdr-fx-away-name">${escapeHtml(aShort)}</strong>
                </div>
                <div class="gwfdr-fx-badges">${badges || `<span class="gwfdr-badge gwfdr-badge--flat">—</span>`}</div>
              </div>
              <div class="gwfdr-fx-body">
                <div class="gwfdr-fx-spider" data-spider-idx="${idx}" role="img" aria-label="${escapeHtml(hShort)} vs ${escapeHtml(aShort)} spider"></div>
                <div class="gwfdr-fx-stats">
                  <div class="gwfdr-fx-band" aria-hidden="true">
                    <span class="gwfdr-fx-band-lead"></span>
                    <span class="gwfdr-fx-band-atk">Attack</span>
                    <span class="gwfdr-fx-band-def">Defence (-A)</span>
                  </div>
                  <div class="gwfdr-fx-stats-head" aria-hidden="true">
                    <span></span>
                    <span class="col-attack">G</span><span class="col-attack">xG</span><span class="col-attack">Sh</span><span class="col-attack">SoT</span><span class="col-attack">SiB</span><span class="col-attack">CC</span><span class="col-attack">BCC</span>
                    <span class="col-defend">G-A</span><span class="col-defend">xG-A</span><span class="col-defend">Sh-A</span><span class="col-defend">SoT-A</span><span class="col-defend">SiB-A</span><span class="col-defend">CC-A</span><span class="col-defend">BCC-A</span>
                  </div>
                  <div class="gwfdr-fx-row gwfdr-fx-home">
                    <span class="gwfdr-fx-team">${escapeHtml(hShort)}</span>
                    ${metricCells(hm, f.home_code, extremes)}
                  </div>
                  <div class="gwfdr-fx-row gwfdr-fx-away">
                    <span class="gwfdr-fx-team">${escapeHtml(aShort)}</span>
                    ${metricCells(am, f.away_code, extremes)}
                  </div>
                </div>
              </div>
            </article>`;
          })
          .join("")}
      </div>`;

    els.fixtures.querySelectorAll("[data-spider-idx]").forEach((host) => {
      const i = Number(host.getAttribute("data-spider-idx"));
      const d = spiderData[i];
      if (d) renderFixtureSpider(host, d.home, d.away, d.hShort, d.aShort);
    });
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function render() {
    if (!state.season || state.gw == null) {
      if (els.status) els.status.textContent = "No upcoming Premier League gameweeks in fixtures.";
      return;
    }
    syncLastNFromUi();
    state.perMatch = Boolean(els.perMatch?.checked);
    const ranks = seasonRanks(state.season, state.lastN);
    if (els.status) {
      const form =
        state.lastN != null && state.lastN < ranks.maxFinished
          ? ` · form last ${state.lastN} GWs`
          : " · form season to date";
      els.status.textContent = `${state.season} · ranks through GW ${ranks.maxFinished} · viewing GW ${state.gw}${form}`;
    }
    renderSeasonBoard(ranks);
    renderFixtures(ranks);
  }

  window.initGwFdr = init;
})();
