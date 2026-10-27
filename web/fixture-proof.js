/* Fixture Proof: npG+A / npxG+xA per 90 vs top 5 · rest · bottom 5 opponents. */
(() => {
  const PM_URL = "./data/players_matches.json";
  const TG_URL = "./data/teams_gw.json";
  const PL = "Premier League";
  const MIN_MINUTES_PER_APP = 45;
  const MIN_MATCH_SHARE = 0.3;

  const POS_OPTS = [
    { value: "MID", label: "MID" },
    { value: "ATT", label: "ATT" },
    { value: "DEF", label: "DEF + GK" },
  ];
  const RANK_LABELS = {
    xG: "xG / 90",
    xGI: "xGI / 90",
    npxG: "npxG / 90",
    G: "G / 90",
    A: "A / 90",
    xA: "xA / 90",
    npgia: "npG+A / 90",
    npxgia: "npxG+xA / 90",
  };

  const state = {
    players: [],
    teamsGw: [],
    season: null,
    metric: "npgia",
    rankMetric: "xG",
    topBasis: "xg",
    bottomBasis: "xga",
    positions: new Set(["ATT"]),
    topN: 15,
    sort: "top",
    gwFrom: 1,
    gwTo: 38,
    minSample: true,
    exclude: new Set(),
    include: new Set(),
    excludeQuery: "",
    includeQuery: "",
    nameByKey: new Map(),
  };
  const els = {};
  let started = false;
  let resizeTimer = null;

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
      const [pmRes, tgRes] = await Promise.all([
        fetch(PM_URL, { cache: "no-store" }),
        fetch(TG_URL, { cache: "no-store" }),
      ]);
      if (!pmRes.ok) throw new Error(`players_matches HTTP ${pmRes.status}`);
      if (!tgRes.ok) throw new Error(`teams_gw HTTP ${tgRes.status}`);
      state.players = await pmRes.json();
      state.teamsGw = await tgRes.json();
      populateSeasons();
      syncGwBounds(true);
      render();
    } catch (err) {
      if (els.status) els.status.textContent = `Failed to load: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("fp-root");
    els.season = $("fp-season");
    els.metric = $("fp-metric");
    els.rank = $("fp-rank");
    els.topBasis = $("fp-top-basis");
    els.bottomBasis = $("fp-bottom-basis");
    els.positionMs = $("fp-position-ms");
    els.top = $("fp-top");
    els.sort = $("fp-sort");
    els.gwRange = $("fp-gw-range");
    els.gwLabel = $("fp-gw-label");
    els.minSample = $("fp-min-sample");
    els.status = $("fp-status");
    els.teams = $("fp-teams");
    els.chart = $("fp-chart");
    els.tip = $("fp-tip");
    els.chartDl = $("fp-chart-dl");
    els.gwControl = null;
    els.excludeSearch = $("fp-exclude-search");
    els.excludeMenu = $("fp-exclude-menu");
    els.excludeChips = $("fp-exclude-chips");
    els.excludeDrop = $("fp-exclude-drop");
    els.includeSearch = $("fp-include-search");
    els.includeMenu = $("fp-include-menu");
    els.includeChips = $("fp-include-chips");
    els.includeDrop = $("fp-include-drop");
  }

  function bindEvents() {
    els.season?.addEventListener("change", () => {
      state.season = els.season.value;
      state.exclude.clear();
      state.include.clear();
      clearPickerInputs();
      syncGwBounds(true);
      render();
    });
    els.metric?.addEventListener("change", () => {
      state.metric = els.metric.value;
      render();
    });
    els.rank?.addEventListener("change", () => {
      state.rankMetric = els.rank.value;
      render();
    });
    els.topBasis?.addEventListener("change", () => {
      state.topBasis = els.topBasis.value;
      render();
    });
    els.bottomBasis?.addEventListener("change", () => {
      state.bottomBasis = els.bottomBasis.value;
      render();
    });
    els.top?.addEventListener("change", () => {
      state.topN = Number(els.top.value) || 15;
      render();
    });
    els.sort?.addEventListener("change", () => {
      state.sort = els.sort.value;
      render();
    });
    els.minSample?.addEventListener("change", () => {
      state.minSample = Boolean(els.minSample.checked);
      render();
    });
    if (els.gwRange && window.mountDualRange && !els.gwControl) {
      els.gwControl = window.mountDualRange(els.gwRange, {
        min: 1,
        max: 38,
        step: 1,
        from: state.gwFrom,
        to: state.gwTo,
        onInput: (from, to) => {
          state.gwFrom = from;
          state.gwTo = to;
          if (els.gwLabel) els.gwLabel.textContent = `GW ${from}–${to}`;
          render();
        },
      });
    }

    mountPositionMultiSelect();
    wirePicker("exclude");
    wirePicker("include");

    if (els.chartDl && window.ChartExport && !els.chartDl.dataset.bound) {
      els.chartDl.dataset.bound = "1";
      window.ChartExport.bindChartDownload(
        els.chartDl,
        () => els.chart,
        () => "fpl-pulse-talk-fixture-proof",
        () => ({
          title: "Who performs against the best — and the softest?",
          metrics: `Dots = ${metricLabel()} · Top N by ${rankLabel()} · green = vs top 5 · open = vs rest · red = vs bottom 5`,
          meta: `${state.season} · GW ${state.gwFrom}–${state.gwTo} · ${positionLabel()}${
            state.minSample ? " · 45+/30%" : ""
          }`,
        })
      );
    }
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-fixture-proof")?.hidden) renderChart(lastRows, lastBands);
      }, 120);
    });
  }

  function clearPickerInputs() {
    state.excludeQuery = "";
    state.includeQuery = "";
    if (els.excludeSearch) els.excludeSearch.value = "";
    if (els.includeSearch) els.includeSearch.value = "";
  }

  function wirePicker(kind) {
    const search = kind === "exclude" ? els.excludeSearch : els.includeSearch;
    const drop = kind === "exclude" ? els.excludeDrop : els.includeDrop;
    search?.addEventListener("focus", () => openPicker(kind));
    search?.addEventListener("input", () => {
      if (kind === "exclude") state.excludeQuery = search.value.trim();
      else state.includeQuery = search.value.trim();
      openPicker(kind);
      paintPicker(kind);
    });
    search?.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closePicker(kind);
    });
    document.addEventListener("click", (e) => {
      if (!drop?.contains(e.target)) closePicker(kind);
    });
  }

  function populateSeasons() {
    const seasons = [
      ...new Set(
        state.players
          .filter((r) => r.c === PL)
          .map((r) => r.s)
          .filter(Boolean)
      ),
    ].sort();
    state.season = seasons.at(-1) || null;
    els.season.replaceChildren(
      ...seasons.map((season) => {
        const option = document.createElement("option");
        option.value = season;
        option.textContent = season;
        option.selected = season === state.season;
        return option;
      })
    );
  }

  function syncGwBounds(reset) {
    const gws = state.players
      .filter((r) => r.s === state.season && r.c === PL)
      .map((r) => Number(r.gw))
      .filter((g) => g > 0);
    const min = gws.length ? Math.min(...gws) : 1;
    const max = gws.length ? Math.max(...gws) : 38;
    if (reset) {
      state.gwFrom = min;
      state.gwTo = max;
    } else {
      state.gwFrom = Math.min(max, Math.max(min, state.gwFrom));
      state.gwTo = Math.min(max, Math.max(min, state.gwTo));
    }
    els.gwControl?.setBounds(min, max);
    els.gwControl?.set(state.gwFrom, state.gwTo);
    if (els.gwLabel) els.gwLabel.textContent = `GW ${state.gwFrom}–${state.gwTo}`;
  }

  function inGw(gw) {
    const g = Number(gw);
    if (!Number.isFinite(g) || g <= 0) return true;
    return g >= state.gwFrom && g <= state.gwTo;
  }

  function num(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }

  /** Finished PL matches per team short in the selected GW window. */
  function teamMatchCounts() {
    const counts = new Map();
    for (const r of state.teamsGw) {
      if (r.season !== state.season || r.competition !== PL || !r.finished || !r.short) continue;
      if (!inGw(r.gw)) continue;
      counts.set(r.short, (counts.get(r.short) || 0) + 1);
    }
    return counts;
  }

  function mountPositionMultiSelect() {
    if (!els.positionMs || els.positionMs.dataset.ready) return;
    els.positionMs.dataset.ready = "1";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "fp-ms-btn";
    btn.id = "fp-position";
    const panel = document.createElement("div");
    panel.className = "fp-ms-panel";
    panel.hidden = true;
    els.positionMs.append(btn, panel);

    function summary() {
      if (!state.positions.size || state.positions.size === POS_OPTS.length) return "All";
      return POS_OPTS.filter((o) => state.positions.has(o.value))
        .map((o) => o.label)
        .join(", ");
    }

    function paint() {
      btn.textContent = summary();
      panel.replaceChildren();
      const actions = document.createElement("div");
      actions.className = "fp-ms-actions";
      const all = document.createElement("button");
      all.type = "button";
      all.textContent = "All";
      all.addEventListener("click", () => {
        state.positions = new Set(POS_OPTS.map((o) => o.value));
        paint();
        render();
      });
      const none = document.createElement("button");
      none.type = "button";
      none.textContent = "None";
      none.addEventListener("click", () => {
        state.positions = new Set();
        paint();
        render();
      });
      actions.append(all, none);
      panel.appendChild(actions);
      POS_OPTS.forEach((o) => {
        const row = document.createElement("label");
        row.className = "fp-ms-opt";
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = state.positions.has(o.value);
        cb.addEventListener("change", () => {
          if (cb.checked) state.positions.add(o.value);
          else state.positions.delete(o.value);
          btn.textContent = summary();
          render();
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
      if (!els.positionMs.contains(e.target)) panel.hidden = true;
    });
    paint();
    els.positionPaint = paint;
  }

  function positionMatches(position) {
    if (!state.positions.size) return false;
    if (state.positions.size === POS_OPTS.length) return true;
    if (state.positions.has("MID") && position === "Midfielder") return true;
    if (state.positions.has("ATT") && position === "Forward") return true;
    if (state.positions.has("DEF") && (position === "Defender" || position === "Goalkeeper")) return true;
    return false;
  }

  function metricLabel() {
    return state.metric === "npxgia" ? "npxG+xA / 90" : "npG+A / 90";
  }

  function rankLabel() {
    return RANK_LABELS[state.rankMetric] || state.rankMetric;
  }

  function positionLabel() {
    if (!state.positions.size) return "no positions";
    if (state.positions.size === POS_OPTS.length) return "All positions";
    return POS_OPTS.filter((o) => state.positions.has(o.value))
      .map((o) => o.label)
      .join(", ");
  }

  function rowValue(r) {
    if (state.metric === "npxgia") return num(r.npxG) + num(r.xA);
    return Math.max(0, num(r.G) - num(r.PenG)) + num(r.A);
  }

  function rankRowValue(r) {
    switch (state.rankMetric) {
      case "xG":
        return num(r.xG);
      case "xGI":
        return num(r.xGI);
      case "npxG":
        return num(r.npxG);
      case "G":
        return num(r.G);
      case "A":
        return num(r.A);
      case "xA":
        return num(r.xA);
      case "npxgia":
        return num(r.npxG) + num(r.xA);
      case "npgia":
        return Math.max(0, num(r.G) - num(r.PenG)) + num(r.A);
      default:
        return num(r.xG);
    }
  }

  /** Live PL standings for finished matches in the selected GW window. */
  function seasonBands() {
    const rows = state.teamsGw.filter(
      (r) =>
        r.season === state.season &&
        r.competition === PL &&
        r.finished &&
        r.short &&
        inGw(r.gw)
    );
    const by = new Map();
    for (const r of rows) {
      const code = String(r.team_code);
      if (!by.has(code)) {
        by.set(code, {
          team_code: code,
          short: r.short,
          team: r.team || r.short,
          g: 0,
          xg: 0,
          gc: 0,
          xga: 0,
        });
      }
      const t = by.get(code);
      t.g += num(r.goals_for);
      t.xg += num(r.xg);
      t.gc += num(r.goals_against);
      t.xga += num(r.xga);
      t.short = r.short || t.short;
      t.team = r.team || t.team;
    }
    const list = [...by.values()];
    const attackKey = state.topBasis === "g" ? "g" : "xg";
    const defendKey = state.bottomBasis === "gc" ? "gc" : "xga";
    const byAttack = [...list].sort((a, b) => b[attackKey] - a[attackKey] || a.short.localeCompare(b.short));
    const top5 = byAttack.slice(0, 5);
    const topSet = new Set(top5.map((t) => t.short));
    const remaining = list.filter((t) => !topSet.has(t.short));
    const byConcede = [...remaining].sort((a, b) => b[defendKey] - a[defendKey] || a.short.localeCompare(b.short));
    const bottom5 = byConcede.slice(0, 5);
    const bottomSet = new Set(bottom5.map((t) => t.short));
    const rest = list.filter((t) => !topSet.has(t.short) && !bottomSet.has(t.short));
    return {
      top5,
      bottom5,
      rest,
      topSet,
      bottomSet,
      attackKey,
      defendKey,
      attackLabel: state.topBasis === "g" ? "G" : "xG",
      defendLabel: state.bottomBasis === "gc" ? "GC" : "xGC",
    };
  }

  function bucketForOpp(opp, bands) {
    if (!opp) return "rest";
    if (bands.topSet.has(opp)) return "top";
    if (bands.bottomSet.has(opp)) return "bottom";
    return "rest";
  }

  function emptyBucket() {
    return { minutes: 0, value: 0, apps: 0 };
  }

  function rate(b) {
    return b.minutes > 0 ? (b.value * 90) / b.minutes : null;
  }

  function nineties(b) {
    return b.minutes / 90;
  }

  function avgMins(b) {
    return b.apps > 0 ? b.minutes / b.apps : null;
  }

  /** Full pool for pickers / top-N seed. */
  function aggregatePool(bands) {
    const rows = state.players.filter(
      (r) =>
        r.s === state.season &&
        r.c === PL &&
        num(r.m) > 0 &&
        inGw(r.gw) &&
        positionMatches(r.pos)
    );
    const map = new Map();
    for (const r of rows) {
      const key = String(r.pc || r.pid);
      if (!map.has(key)) {
        map.set(key, {
          key,
          player_name: r.n,
          team_short: r.tm || "—",
          overall: emptyBucket(),
          rank: emptyBucket(),
          top: emptyBucket(),
          rest: emptyBucket(),
          bottom: emptyBucket(),
        });
      }
      const p = map.get(key);
      const mins = num(r.m);
      const val = rowValue(r);
      const rankVal = rankRowValue(r);
      p.player_name = r.n || p.player_name;
      p.team_short = r.tm || p.team_short;
      p.overall.minutes += mins;
      p.overall.value += val;
      p.overall.apps += 1;
      p.rank.minutes += mins;
      p.rank.value += rankVal;
      p.rank.apps += 1;
      const bucket = bucketForOpp(r.opp, bands);
      p[bucket].minutes += mins;
      p[bucket].value += val;
      p[bucket].apps += 1;
    }
    const teamMatches = teamMatchCounts();
    let list = [...map.values()]
      .filter((p) => p.overall.minutes > 0)
      .map((p) => {
        const overall90 = rate(p.overall);
        const rank90 = rate(p.rank);
        const top90 = rate(p.top);
        const rest90 = rate(p.rest);
        const bottom90 = rate(p.bottom);
        const teamApps = teamMatches.get(p.team_short) || 0;
        const matchShare = teamApps > 0 ? p.overall.apps / teamApps : 0;
        const minsPerApp = p.overall.apps > 0 ? p.overall.minutes / p.overall.apps : 0;
        return {
          ...p,
          overall90: overall90 || 0,
          rank90: rank90 || 0,
          top90,
          rest90,
          bottom90,
          drop: top90 != null && rest90 != null ? rest90 - top90 : null,
          topN90: nineties(p.top),
          restN90: nineties(p.rest),
          bottomN90: nineties(p.bottom),
          topApps: p.top.apps,
          restApps: p.rest.apps,
          bottomApps: p.bottom.apps,
          totalApps: p.overall.apps,
          topAvgMins: avgMins(p.top),
          restAvgMins: avgMins(p.rest),
          bottomAvgMins: avgMins(p.bottom),
          matchShare,
          minsPerApp,
          teamApps,
        };
      });
    if (state.minSample) {
      list = list.filter(
        (p) => p.minsPerApp >= MIN_MINUTES_PER_APP && p.matchShare >= MIN_MATCH_SHARE
      );
    }
    state.nameByKey = new Map(list.map((p) => [p.key, `${p.player_name} (${p.team_short})`]));
    return list;
  }

  function selectedPlayers(pool) {
    const ranked = [...pool].sort((a, b) => b.rank90 - a.rank90 || a.player_name.localeCompare(b.player_name));
    const auto = ranked.filter((p) => !state.exclude.has(p.key)).slice(0, state.topN);
    const keys = new Set(auto.map((p) => p.key));
    for (const key of state.include) {
      if (keys.has(key) || state.exclude.has(key)) continue;
      const p = pool.find((row) => row.key === key);
      if (p) {
        auto.push(p);
        keys.add(key);
      }
    }
    const sorter = {
      top: (a, b) => (b.top90 ?? -1) - (a.top90 ?? -1),
      drop: (a, b) => (b.drop ?? -999) - (a.drop ?? -999),
      overall: (a, b) => b.overall90 - a.overall90,
      rank: (a, b) => b.rank90 - a.rank90,
    }[state.sort];
    return auto.sort((a, b) => sorter(a, b) || a.player_name.localeCompare(b.player_name));
  }

  function openPicker(kind) {
    const menu = kind === "exclude" ? els.excludeMenu : els.includeMenu;
    if (menu) menu.hidden = false;
  }

  function closePicker(kind) {
    const menu = kind === "exclude" ? els.excludeMenu : els.includeMenu;
    if (menu) menu.hidden = true;
  }

  function paintChips(kind) {
    const host = kind === "exclude" ? els.excludeChips : els.includeChips;
    const set = kind === "exclude" ? state.exclude : state.include;
    if (!host) return;
    if (!set.size) {
      host.innerHTML = "";
      return;
    }
    host.innerHTML = [...set]
      .map((key) => {
        const label = state.nameByKey.get(key) || key;
        return `<button type="button" class="perf-chip" data-key="${escapeAttr(key)}">${escapeHtml(label)} ×</button>`;
      })
      .join("");
    host.querySelectorAll(".perf-chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        set.delete(btn.dataset.key);
        render();
      });
    });
  }

  function paintPicker(kind) {
    const menu = kind === "exclude" ? els.excludeMenu : els.includeMenu;
    if (!menu) return;
    const q = (kind === "exclude" ? state.excludeQuery : state.includeQuery).toLowerCase();
    const set = kind === "exclude" ? state.exclude : state.include;
    const pool = lastPool || [];
    const matches = pool
      .filter((p) => !q || `${p.player_name} ${p.team_short}`.toLowerCase().includes(q))
      .slice(0, 40);
    if (!matches.length) {
      menu.innerHTML = `<div class="perf-ms-empty">No players match</div>`;
      return;
    }
    menu.innerHTML = matches
      .map((p) => {
        const on = set.has(p.key);
        return `<label class="perf-ms-opt"><input type="checkbox" data-key="${escapeAttr(p.key)}" ${
          on ? "checked" : ""
        }/><b>${escapeHtml(p.player_name)}</b><span>${escapeHtml(p.team_short)}</span></label>`;
      })
      .join("");
    menu.querySelectorAll("input").forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) set.add(input.dataset.key);
        else set.delete(input.dataset.key);
        render();
      });
    });
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(value) {
    return escapeHtml(value).replace(/'/g, "&#39;");
  }

  function fmtRate(v) {
    if (v == null || !Number.isFinite(v)) return "—";
    return v.toFixed(2);
  }

  function fmtDiff(v) {
    if (v == null || !Number.isFinite(v)) return "—";
    const sign = v > 0 ? "+" : "";
    return `${sign}${v.toFixed(2)}`;
  }

  function fmtN90(v) {
    return v.toFixed(v >= 10 ? 0 : 1);
  }

  function fmtMins(v) {
    if (v == null || !Number.isFinite(v)) return "—";
    return String(Math.round(v));
  }

  function fmtAppsMins(p) {
    return `${p.totalApps} · ${fmtMins(p.topAvgMins)}/${fmtMins(p.restAvgMins)}/${fmtMins(p.bottomAvgMins)}`;
  }

  let lastPool = [];
  let lastRows = [];
  let lastBands = null;

  function render() {
    if (!els.chart) return;
    const bands = seasonBands();
    lastBands = bands;
    lastPool = aggregatePool(bands);
    const rows = selectedPlayers(lastPool);
    lastRows = rows;

    const topNames = bands.top5.map((t) => t.short).join(", ");
    const botNames = bands.bottom5.map((t) => t.short).join(", ");
    if (els.teams) {
      els.teams.innerHTML = `<strong>Top 5</strong> by ${bands.attackLabel}: ${escapeHtml(topNames) || "—"}
        · <strong>Bottom 5</strong> by ${bands.defendLabel} conceded: ${escapeHtml(botNames) || "—"}
        · Rest: ${bands.rest.map((t) => t.short).join(", ") || "—"}`;
    }
    const sampleNote = state.minSample ? " · 45+ mins/app · ≥30% team matches" : "";
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · chart ${metricLabel()} · Top ${state.topN} by ${rankLabel()} · ${rows.length} shown · ${positionLabel()}${sampleNote}`;

    paintChips("exclude");
    paintChips("include");
    if (els.excludeMenu && !els.excludeMenu.hidden) paintPicker("exclude");
    if (els.includeMenu && !els.includeMenu.hidden) paintPicker("include");

    renderChart(rows, bands);
  }

  function renderChart(rows, bands) {
    if (!els.chart) return;
    els.chart.replaceChildren();
    if (!rows.length) {
      els.chart.innerHTML = `<p class="empty">No players match these filters.</p>`;
      return;
    }

    const width = els.chart.clientWidth || 960;
    const rowH = 36;
    const headH = 28;
    const footH = 26;
    const leftW = 120;
    const rightW = 292;
    const height = headH + rows.length * rowH + footH + 4;
    const plotW = Math.max(160, width - leftW - rightW - 16);
    const values = rows.flatMap((r) => [r.top90, r.rest90, r.bottom90].filter((v) => v != null));
    const xMax = Math.max(0.2, ...(values.length ? values : [0.2])) * 1.12;
    const x = d3.scaleLinear().domain([0, xMax]).nice().range([0, plotW]);
    const colDiff = leftW + plotW + 14;
    const col90s = colDiff + 78;
    const colApps = width - 8;

    const svg = d3
      .select(els.chart)
      .append("svg")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", width)
      .attr("height", height);

    // Header (column labels only — metric axis sits at bottom)
    svg
      .append("text")
      .attr("x", leftW)
      .attr("y", 18)
      .attr("fill", "#9aafb8")
      .attr("font-size", 11)
      .attr("font-family", "Roboto, sans-serif")
      .text(metricLabel());
    svg
      .append("text")
      .attr("x", colDiff)
      .attr("y", 18)
      .attr("fill", "#9aafb8")
      .attr("font-size", 11)
      .attr("font-family", "Roboto, sans-serif")
      .text("DIFF");
    svg
      .append("text")
      .attr("x", col90s)
      .attr("y", 18)
      .attr("fill", "#9aafb8")
      .attr("font-size", 11)
      .attr("font-family", "Roboto, sans-serif")
      .text("90s T/R/B");
    svg
      .append("text")
      .attr("x", colApps)
      .attr("y", 18)
      .attr("text-anchor", "end")
      .attr("fill", "#9aafb8")
      .attr("font-size", 11)
      .attr("font-family", "Roboto, sans-serif")
      .text("Apps · avg mins T/R/B");

    // Vertical grid through plot; tick labels on bottom axis
    const axisG = svg.append("g").attr("transform", `translate(${leftW},${headH})`);
    const ticks = x.ticks(6);
    const plotH = rows.length * rowH;
    ticks.forEach((t) => {
      axisG
        .append("line")
        .attr("x1", x(t))
        .attr("x2", x(t))
        .attr("y1", 0)
        .attr("y2", plotH)
        .attr("stroke", "#2d3d4a")
        .attr("stroke-width", 1);
    });
    const axisBottom = svg.append("g").attr("transform", `translate(${leftW},${headH + plotH + 14})`);
    ticks.forEach((t) => {
      axisBottom
        .append("text")
        .attr("x", x(t))
        .attr("y", 0)
        .attr("text-anchor", "middle")
        .attr("fill", "#7a9099")
        .attr("font-size", 10)
        .attr("font-family", "Roboto, sans-serif")
        .text(t.toFixed(1));
    });

    rows.forEach((p, i) => {
      const cy = headH + i * rowH + rowH / 2;
      const g = svg.append("g").attr("class", "fp-row");

      g.append("text")
        .attr("x", leftW - 10)
        .attr("y", cy + 4)
        .attr("text-anchor", "end")
        .attr("fill", "#e8f0ec")
        .attr("font-size", 13)
        .attr("font-weight", 600)
        .attr("font-family", "Roboto, sans-serif")
        .text(p.player_name);

      const pts = [
        { key: "top", v: p.top90, fill: "#1f7a4c", stroke: "#1f7a4c", open: false },
        { key: "rest", v: p.rest90, fill: "#0c1218", stroke: "#c5d0d6", open: true },
        { key: "bottom", v: p.bottom90, fill: "#e07070", stroke: "#e07070", open: false },
      ].filter((d) => d.v != null);

      if (pts.length >= 2) {
        const order = ["top", "rest", "bottom"];
        const ordered = order.map((k) => pts.find((d) => d.key === k)).filter(Boolean);
        for (let j = 0; j < ordered.length - 1; j++) {
          g.append("line")
            .attr("x1", leftW + x(ordered[j].v))
            .attr("x2", leftW + x(ordered[j + 1].v))
            .attr("y1", cy)
            .attr("y2", cy)
            .attr("stroke", "#c9a227")
            .attr("stroke-width", 2.2)
            .attr("stroke-linecap", "round");
        }
      }

      pts.forEach((d) => {
        g.append("circle")
          .attr("cx", leftW + x(d.v))
          .attr("cy", cy)
          .attr("r", 7)
          .attr("fill", d.fill)
          .attr("stroke", d.stroke)
          .attr("stroke-width", d.open ? 2 : 1.2)
          .style("cursor", "pointer")
          .on("mousemove", (event) => showTip(event, p, bands))
          .on("mouseleave", hideTip);
      });

      if (i === 0) {
        pts.forEach((d) => {
          const label = d.key === "top" ? "vs top 5" : d.key === "rest" ? "vs rest" : "vs bottom 5";
          g.append("text")
            .attr("x", leftW + x(d.v))
            .attr("y", cy - 12)
            .attr("text-anchor", "middle")
            .attr("fill", "#8fa59a")
            .attr("font-size", 10)
            .text(label);
        });
      }

      const diff = p.drop;
      const diffColor = diff == null ? "#8fa59a" : diff < -0.01 ? "#e07070" : diff > 0.01 ? "#3ddc97" : "#9aafb8";
      g.append("text")
        .attr("x", colDiff)
        .attr("y", cy + 4)
        .attr("fill", diffColor)
        .attr("font-size", 13)
        .attr("font-weight", 600)
        .attr("font-family", "Roboto, sans-serif")
        .text(fmtDiff(diff));

      g.append("text")
        .attr("x", col90s)
        .attr("y", cy + 4)
        .attr("fill", "#9aafb8")
        .attr("font-size", 12)
        .attr("font-family", "Roboto, sans-serif")
        .text(`${fmtN90(p.topN90)} / ${fmtN90(p.restN90)} / ${fmtN90(p.bottomN90)}`);

      g.append("text")
        .attr("x", colApps)
        .attr("y", cy + 4)
        .attr("text-anchor", "end")
        .attr("fill", "#c5d0d6")
        .attr("font-size", 12)
        .attr("font-family", "Roboto, sans-serif")
        .text(fmtAppsMins(p));
    });
  }

  function showTip(event, p, bands) {
    if (!els.tip) return;
    els.tip.hidden = false;
    els.tip.innerHTML = `<strong>${escapeHtml(p.player_name)}</strong>
      <span>${escapeHtml(p.team_short)} · ${metricLabel()} · ${p.totalApps} apps · ${fmtMins(p.minsPerApp)} avg mins</span>
      <div class="fpl-tip-grid">
        <span>vs top 5</span><b>${fmtRate(p.top90)}</b>
        <span>vs rest</span><b>${fmtRate(p.rest90)}</b>
        <span>vs bottom 5</span><b>${fmtRate(p.bottom90)}</b>
        <span>Overall</span><b>${fmtRate(p.overall90)}</b>
        <span>Apps T/R/B</span><b>${p.topApps} / ${p.restApps} / ${p.bottomApps}</b>
        <span>Avg mins T/R/B</span><b>${fmtMins(p.topAvgMins)} / ${fmtMins(p.restAvgMins)} / ${fmtMins(p.bottomAvgMins)}</b>
        <span>90s T/R/B</span><b>${fmtN90(p.topN90)} / ${fmtN90(p.restN90)} / ${fmtN90(p.bottomN90)}</b>
        <span>rest−top</span><b>${fmtDiff(p.drop)}</b>
      </div>
      <span style="display:block;margin-top:6px">Top: ${escapeHtml(bands.top5.map((t) => t.short).join(", "))} · Bottom: ${escapeHtml(
        bands.bottom5.map((t) => t.short).join(", ")
      )}</span>`;
    els.tip.style.left = `${Math.min(window.innerWidth - 300, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 240, event.clientY + 14)}px`;
  }

  function hideTip() {
    if (els.tip) els.tip.hidden = true;
  }

  window.initFixtureProof = init;
})();
