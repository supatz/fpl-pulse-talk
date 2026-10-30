/* FPL-Core scatter: free X / Y / bubble / sort metrics. */
(() => {
  const DATA_URL = "./data/players_matches.json";
  const MIN_MINUTES_PER_APP = 45;

  /** Selectable metrics — field is the players_matches key (or derived). */
  const METRICS = [
    { id: "G", field: "G", short: "G", name: "Goals", digits: 0 },
    { id: "xG", field: "xG", short: "xG", name: "Expected goals", digits: 2 },
    { id: "A", field: "A", short: "A", name: "Assists", digits: 0 },
    { id: "xA", field: "xA", short: "xA", name: "Expected assists", digits: 2 },
    { id: "GI", field: "GI", short: "GI", name: "Goal involvements", digits: 0 },
    { id: "xGI", field: "xGI", short: "xGI", name: "Expected goal involvements", digits: 2 },
    { id: "DC", field: "DefCon", short: "DC", name: "Defensive contributions", digits: 0 },
    { id: "CS", field: "cs", short: "CS", name: "Clean sheets", digits: 0 },
    { id: "GC", field: "GC", short: "GC", name: "Goals conceded", digits: 0 },
    { id: "xGC", field: "xGC", short: "xGC", name: "Expected goals conceded (FPL on-pitch)", digits: 2 },
    { id: "xGOT", field: "xGOT", short: "xGOT", name: "Expected goals on target", digits: 2 },
    { id: "CC", field: "CC", short: "CC", name: "Chances created", digits: 0 },
    { id: "npxG", field: "npxG", short: "npxG", name: "Non-penalty xG", digits: 2 },
    { id: "Sh", field: "Sh", short: "Sh", name: "Shots", digits: 0 },
    { id: "SoT", field: "SoT", short: "SoT", name: "Shots on target", digits: 0 },
    { id: "TiB", field: "TiB", short: "TiB", name: "Touches in box", digits: 0 },
    { id: "SiB", field: "SiB", short: "SiB", name: "Shots in box (US)", digits: 0 },
    { id: "BCC", field: "BCC", short: "BCC", name: "Big chances created (US)", digits: 0 },
    { id: "BCT", field: "BCT", short: "BCT", name: "Big chances taken (US)", digits: 0 },
    { id: "BCS", field: "BCS", short: "BCS", name: "Big chances scored (US)", digits: 0 },
    { id: "BCM", field: "BCM", short: "BCM", name: "Big chances missed (US)", digits: 0 },
  ];
  const METRIC_BY_ID = Object.fromEntries(METRICS.map((m) => [m.id, m]));
  const SUM_FIELDS = [
    "G", "A", "xG", "xA", "xGI", "DefCon", "cs", "GC", "xGC", "xGOT", "CC", "npxG", "Sh", "SoT", "TiB", "SiB",
    "BCC", "BCT", "BCS", "BCM",
  ];

  const state = {
    rows: [],
    season: null,
    xMetric: "xG",
    yMetric: "G",
    sizeMetric: "SoT",
    sortMetric: "xGI",
    sortDir: "desc",
    topN: 20,
    position: "ALL",
    gwFrom: 1,
    gwTo: 38,
    per90: false,
    min45: false,
    trend: false,
    exclude: new Set(), // player keys (pc || pid)
    excludeQuery: "",
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
    fillMetricSelects();
    try {
      const res = await fetch(DATA_URL, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      state.rows = await res.json();
      populateSeasons();
      syncGwBounds(true);
      render();
    } catch (err) {
      els.status.textContent = `Failed to load FPL player data: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("perf-root");
    els.season = $("perf-season");
    els.xMetric = $("perf-x");
    els.yMetric = $("perf-y");
    els.sizeMetric = $("perf-size");
    els.sortMetric = $("perf-sort");
    els.sortDir = $("perf-sort-dir");
    els.top = $("perf-top");
    els.position = $("perf-position");
    els.gwRange = $("perf-gw-range");
    els.gwLabel = $("perf-gw-label");
    els.gwControl = null;
    els.per90 = $("perf-per90");
    els.min45 = $("perf-min45");
    els.trend = $("perf-trend");
    els.excludeSearch = $("perf-exclude-search");
    els.excludeMenu = $("perf-exclude-menu");
    els.excludeChips = $("perf-exclude-chips");
    els.excludeDrop = $("perf-exclude-drop");
    els.status = $("perf-status");
    els.chart = $("perf-chart");
    els.tip = $("perf-tip");
    els.chartDl = $("perf-chart-dl");
  }

  function fillMetricSelects() {
    const opts = METRICS.map(
      (m) => `<option value="${m.id}">${m.short} — ${m.name}</option>`
    ).join("");
    for (const [el, value] of [
      [els.xMetric, state.xMetric],
      [els.yMetric, state.yMetric],
      [els.sizeMetric, state.sizeMetric],
      [els.sortMetric, state.sortMetric],
    ]) {
      if (!el) continue;
      el.innerHTML = opts;
      el.value = value;
    }
  }

  function bindEvents() {
    els.season.addEventListener("change", () => {
      state.season = els.season.value;
      state.exclude.clear();
      state.excludeQuery = "";
      if (els.excludeSearch) els.excludeSearch.value = "";
      syncGwBounds(true);
      render();
    });
    els.xMetric.addEventListener("change", () => {
      state.xMetric = els.xMetric.value;
      render();
    });
    els.yMetric.addEventListener("change", () => {
      state.yMetric = els.yMetric.value;
      render();
    });
    els.sizeMetric.addEventListener("change", () => {
      state.sizeMetric = els.sizeMetric.value;
      render();
    });
    els.sortMetric.addEventListener("change", () => {
      state.sortMetric = els.sortMetric.value;
      render();
    });
    els.sortDir?.addEventListener("change", () => {
      state.sortDir = els.sortDir.value === "asc" ? "asc" : "desc";
      render();
    });
    els.top.addEventListener("change", () => {
      state.topN = Number(els.top.value) || 20;
      render();
    });
    els.position.addEventListener("change", () => {
      state.position = els.position.value;
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
          updateGwLabel();
          render();
        },
      });
    }
    els.per90.addEventListener("change", () => {
      state.per90 = els.per90.checked;
      render();
    });
    els.min45.addEventListener("change", () => {
      state.min45 = els.min45.checked;
      render();
    });
    els.trend?.addEventListener("change", () => {
      state.trend = !!els.trend.checked;
      render();
    });

    els.excludeSearch?.addEventListener("focus", () => openExcludeMenu());
    els.excludeSearch?.addEventListener("input", () => {
      state.excludeQuery = els.excludeSearch.value.trim();
      openExcludeMenu();
      paintExcludeMenu(aggregatePool());
    });
    els.excludeSearch?.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeExcludeMenu();
    });
    document.addEventListener("click", (e) => {
      if (!els.excludeDrop?.contains(e.target)) closeExcludeMenu();
    });
    if (els.chartDl && window.ChartExport && !els.chartDl.dataset.bound) {
      els.chartDl.dataset.bound = "1";
      window.ChartExport.bindChartDownload(
        els.chartDl,
        () => els.chart,
        () => `fpl-pulse-talk-performance-${state.xMetric || "x"}-${state.yMetric || "y"}`,
        exportCaption
      );
    }

    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-player-performance")?.hidden) render();
      }, 120);
    });
  }

  function exportCaption() {
    const x = METRIC_BY_ID[state.xMetric] || { short: state.xMetric, name: state.xMetric };
    const y = METRIC_BY_ID[state.yMetric] || { short: state.yMetric, name: state.yMetric };
    const size = METRIC_BY_ID[state.sizeMetric] || { short: state.sizeMetric, name: state.sizeMetric };
    const rate = state.per90 ? " per 90 minutes" : "";
    const gloss = [
      `${x.short} = ${x.name}`,
      `${y.short} = ${y.name}`,
      `Bubble = ${size.name}`,
    ];
    if (state.sortMetric && METRIC_BY_ID[state.sortMetric]) {
      const sort = METRIC_BY_ID[state.sortMetric];
      const dir = state.sortDir === "asc" ? "ascending" : "descending";
      gloss.push(`Ranked by ${sort.name} (${dir})`);
    }
    if (state.trend) gloss.push("Trend line on");
    return {
      title: `${y.name} vs ${x.name}${rate}`,
      metrics: gloss.join(" · "),
      meta: [state.season, `GW ${state.gwFrom}–${state.gwTo}`, `Top ${state.topN}`]
        .filter(Boolean)
        .join(" · "),
    };
  }

  function populateSeasons() {
    const seasons = [...new Set(state.rows.map((r) => r.s).filter(Boolean))].sort();
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

  function seasonRows() {
    return state.rows.filter((r) => r.s === state.season && r.c === "Premier League");
  }

  function syncGwBounds(reset) {
    const gws = seasonRows().map((r) => Number(r.gw)).filter((v) => Number.isFinite(v) && v > 0);
    const min = gws.length ? Math.min(...gws) : 1;
    const max = gws.length ? Math.max(...gws) : 38;
    if (reset) {
      state.gwFrom = min;
      state.gwTo = max;
    } else {
      state.gwFrom = Math.min(max, Math.max(min, state.gwFrom));
      state.gwTo = Math.min(max, Math.max(min, state.gwTo));
      if (state.gwFrom > state.gwTo) [state.gwFrom, state.gwTo] = [min, max];
    }
    if (els.gwControl) {
      els.gwControl.setBounds(min, max);
      els.gwControl.set(state.gwFrom, state.gwTo);
    }
    updateGwLabel();
  }

  function updateGwLabel() {
    els.gwLabel.textContent = `GW ${state.gwFrom}–${state.gwTo}`;
  }

  function metric(id) {
    return METRIC_BY_ID[id] || METRIC_BY_ID.G;
  }

  function num(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function positionMatches(position) {
    if (state.position === "ALL") return true;
    if (state.position === "MID") return position === "Midfielder";
    if (state.position === "ATT") return position === "Forward";
    return position === "Defender" || position === "Goalkeeper";
  }

  function playerKey(r) {
    return String(r.pc || r.pid);
  }

  /** Aggregate every metric for the current window (before top-N / exclude). */
  function aggregatePool() {
    const rows = seasonRows().filter(
      (r) =>
        Number(r.gw) >= state.gwFrom &&
        Number(r.gw) <= state.gwTo &&
        num(r.m) > 0 &&
        positionMatches(r.pos)
    );
    const players = new Map();
    for (const r of rows) {
      const key = playerKey(r);
      if (!players.has(key)) {
        const base = {
          key,
          player_name: r.n,
          team_short: r.tm || "—",
          position: r.pos,
          apps: 0,
          minutes: 0,
        };
        for (const f of SUM_FIELDS) base[f] = 0;
        base.GI = 0;
        players.set(key, base);
      }
      const p = players.get(key);
      p.apps += 1;
      p.minutes += num(r.m);
      p.team_short = r.tm || p.team_short;
      p.player_name = r.n || p.player_name;
      for (const f of SUM_FIELDS) p[f] += num(r[f]);
      p.GI += num(r.G) + num(r.A);
    }
    let list = [...players.values()].filter((p) => p.minutes > 0);
    if (state.min45) {
      list = list.filter((p) => p.minutes / p.apps >= MIN_MINUTES_PER_APP);
    }
    return list;
  }

  function metricTotal(player, m) {
    return num(player[m.field]);
  }

  function shape() {
    const xM = metric(state.xMetric);
    const yM = metric(state.yMetric);
    const sizeM = metric(state.sizeMetric);
    const sortM = metric(state.sortMetric);

    let players = aggregatePool().filter((p) => !state.exclude.has(p.key));
    for (const p of players) {
      const factor = state.per90 ? 90 / p.minutes : 1;
      p.x = metricTotal(p, xM) * factor;
      p.y = metricTotal(p, yM) * factor;
      // Bubble stays on raw totals so cameo rates do not inflate markers.
      p.size = metricTotal(p, sizeM);
      p.sortVal = metricTotal(p, sortM) * factor;
    }
    const asc = state.sortDir === "asc";
    return players
      .filter((p) => p.x > 0 || p.y > 0 || p.size > 0 || p.sortVal > 0)
      .sort((a, b) => {
        const primary = asc ? a.sortVal - b.sortVal : b.sortVal - a.sortVal;
        if (primary) return primary;
        const secondary = asc ? a.y - b.y : b.y - a.y;
        if (secondary) return secondary;
        return asc ? a.x - b.x : b.x - a.x;
      })
      .slice(0, state.topN);
  }

  function openExcludeMenu() {
    if (els.excludeMenu) els.excludeMenu.hidden = false;
  }

  function closeExcludeMenu() {
    if (els.excludeMenu) els.excludeMenu.hidden = true;
  }

  function paintExcludeChips() {
    if (!els.excludeChips) return;
    if (!state.exclude.size) {
      els.excludeChips.innerHTML = "";
      return;
    }
    const pool = aggregatePool();
    const byKey = new Map(pool.map((p) => [p.key, p]));
    els.excludeChips.innerHTML = [...state.exclude]
      .map((key) => {
        const p = byKey.get(key);
        const label = p ? `${shortName(p.player_name)} (${p.team_short})` : key;
        return `<button type="button" class="perf-chip" data-key="${escapeAttr(key)}" title="Remove">${escapeHtml(label)} ×</button>`;
      })
      .join("");
    els.excludeChips.querySelectorAll(".perf-chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.exclude.delete(btn.dataset.key);
        paintExcludeChips();
        paintExcludeMenu(aggregatePool());
        render();
      });
    });
  }

  function paintExcludeMenu(pool) {
    if (!els.excludeMenu) return;
    const q = state.excludeQuery.toLowerCase();
    const matches = pool
      .filter((p) => {
        if (!q) return true;
        const hay = `${p.player_name} ${p.team_short}`.toLowerCase();
        return hay.includes(q);
      })
      .sort((a, b) => a.player_name.localeCompare(b.player_name))
      .slice(0, 40);
    if (!matches.length) {
      els.excludeMenu.innerHTML = `<div class="perf-ms-empty">No players match</div>`;
      return;
    }
    els.excludeMenu.innerHTML = matches
      .map((p) => {
        const on = state.exclude.has(p.key);
        return `<label class="perf-ms-opt"><input type="checkbox" data-key="${escapeAttr(p.key)}" ${on ? "checked" : ""}/> ${escapeHtml(p.player_name)} <span>${escapeHtml(p.team_short)}</span></label>`;
      })
      .join("");
    els.excludeMenu.querySelectorAll("input").forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) state.exclude.add(input.dataset.key);
        else state.exclude.delete(input.dataset.key);
        paintExcludeChips();
        render();
      });
    });
  }

  function render() {
    if (!state.rows.length || !els.chart?.clientWidth) return;
    paintExcludeChips();
    if (els.excludeMenu && !els.excludeMenu.hidden) paintExcludeMenu(aggregatePool());

    const xM = metric(state.xMetric);
    const yM = metric(state.yMetric);
    const sizeM = metric(state.sizeMetric);
    const sortM = metric(state.sortMetric);
    const players = shape();
    const unit = state.per90 ? " per 90" : "";
    const minsNote = state.min45 ? " · 45+ mins/app" : "";
    const exclNote = state.exclude.size ? ` · ${state.exclude.size} excluded` : "";
    const dirNote = state.sortDir === "asc" ? " ↑" : " ↓";
    const trendNote = state.trend ? " · trend line" : "";
    const position = els.position.options[els.position.selectedIndex]?.textContent || "All positions";
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · ${position} · top ${players.length} by ${sortM.short}${dirNote}${unit}${minsNote}${exclNote}${trendNote} · X ${xM.short} · Y ${yM.short} · bubble ${sizeM.short} (relative)${state.per90 ? " · size totals" : ""} · kit colours · FPL-Core`;

    const width = els.chart.clientWidth || 900;
    const height = els.chart.clientHeight || 600;
    els.chart.replaceChildren();
    const svg = d3.select(els.chart).append("svg").attr("viewBox", `0 0 ${width} ${height}`);
    if (!players.length) {
      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .attr("fill", "#8fa59a")
        .text("No players match these filters.");
      return;
    }
    draw(svg, players, { xM, yM, sizeM, sortM }, width, height);
  }

  function draw(svg, players, metrics, width, height) {
    const { xM, yM, sizeM } = metrics;
    const margin = { top: 22, right: 28, bottom: 46, left: 58 };
    const plotW = Math.max(10, width - margin.left - margin.right);
    const plotH = Math.max(10, height - margin.top - margin.bottom);
    const xTop = Math.max(...players.map((p) => p.x), 0.01) * 1.08;
    const yTop = Math.max(...players.map((p) => p.y), 0.01) * 1.08;
    const x = d3.scaleLinear().domain([0, xTop]).nice().range([0, plotW]);
    const y = d3.scaleLinear().domain([0, yTop]).nice().range([plotH, 0]);
    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    g.append("g")
      .attr("class", "perf-grid")
      .attr("transform", `translate(0,${plotH})`)
      .call(axisTicks(d3.axisBottom(x).tickSize(-plotH), x, xM));
    g.append("g")
      .attr("class", "perf-grid")
      .call(axisTicks(d3.axisLeft(y).tickSize(-plotW), y, yM));

    const per90 = state.per90 ? " /90" : "";
    g.append("text")
      .attr("class", "perf-axis-title")
      .attr("x", plotW / 2)
      .attr("y", plotH + 38)
      .attr("text-anchor", "middle")
      .text(`${xM.short}${per90}`);
    g.append("text")
      .attr("class", "perf-axis-title")
      .attr("transform", `translate(-42,${plotH / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .text(`${yM.short}${per90}`);

    if (state.trend) drawTrendLine(g, players, x, y);

    // Size relative to the displayed pool so top-N variance is visible.
    const sizeVals = players.map((p) => p.size);
    const sMin = d3.min(sizeVals);
    const sMax = d3.max(sizeVals);
    const radius =
      sMax - sMin < 1e-9
        ? () => 12
        : d3.scaleSqrt().domain([sMin, sMax]).range([7, 24]).clamp(true);
    const kitFill = (short) =>
      window.TeamColors?.teamKitFill?.(short, 0.5) ||
      window.TeamColors?.teamFill?.(short, 0.5) ||
      "rgba(61, 220, 151, 0.5)";
    const dots = g
      .selectAll("g.perf-dot")
      .data(players)
      .join("g")
      .attr("class", "perf-dot")
      .attr("transform", (d) => `translate(${x(d.x)},${y(d.y)})`);

    dots
      .append("circle")
      .attr("r", (d) => radius(d.size))
      .attr("fill", (d) => kitFill(d.team_short))
      .attr("stroke", "rgba(255,255,255,0.35)")
      .attr("stroke-width", 1)
      .on("mousemove", (event, d) => showTip(event, d, metrics))
      .on("mouseleave", hideTip);

    placeLabels(dots, players, x, y, plotW, plotH, radius);
  }

  function linearTrend(players) {
    const n = players.length;
    if (n < 2) return null;
    let sx = 0;
    let sy = 0;
    let sxx = 0;
    let sxy = 0;
    for (const p of players) {
      sx += p.x;
      sy += p.y;
      sxx += p.x * p.x;
      sxy += p.x * p.y;
    }
    const den = n * sxx - sx * sx;
    if (Math.abs(den) < 1e-12) return null;
    const slope = (n * sxy - sx * sy) / den;
    const intercept = (sy - slope * sx) / n;
    return { slope, intercept };
  }

  function drawTrendLine(g, players, x, y) {
    const fit = linearTrend(players);
    if (!fit) return;
    const [x0, x1] = x.domain();
    const yAt = (xv) => fit.slope * xv + fit.intercept;
    const yLo = Math.min(...y.domain());
    const yHi = Math.max(...y.domain());
    g.append("line")
      .attr("class", "perf-trend")
      .attr("x1", x(x0))
      .attr("y1", y(Math.min(yHi, Math.max(yLo, yAt(x0)))))
      .attr("x2", x(x1))
      .attr("y2", y(Math.min(yHi, Math.max(yLo, yAt(x1)))))
      .attr("stroke", "#f0c674")
      .attr("stroke-width", 1.75)
      .attr("stroke-dasharray", "6 4")
      .attr("stroke-opacity", 0.9)
      .attr("pointer-events", "none");
  }

  function axisTicks(axis, scale, m) {
    if (state.per90 || m.digits > 0) return axis.ticks(7).tickFormat(d3.format("~g"));
    const [lo, hi] = scale.domain();
    const steps = Math.max(1, Math.ceil((hi - lo) / 7));
    const ticks = [];
    for (let v = Math.ceil(lo); v <= hi; v += steps) ticks.push(v);
    return axis.tickValues(ticks).tickFormat(d3.format("d"));
  }

  function placeLabels(dots, players, x, y, plotW, plotH, radius) {
    const OVERHANG = 26;
    const boxes = players.map((p) => ({
      x0: x(p.x) - radius(p.size) - 2,
      x1: x(p.x) + radius(p.size) + 2,
      y0: y(p.y) - radius(p.size) - 2,
      y1: y(p.y) + radius(p.size) + 2,
    }));
    dots.each(function (d) {
      const r = radius(d.size);
      const slots = [
        { dx: 0, dy: -(r + 5), anchor: "middle" },
        { dx: 0, dy: r + 13, anchor: "middle" },
        { dx: r + 4, dy: 4, anchor: "start" },
        { dx: -(r + 4), dy: 4, anchor: "end" },
        { dx: r + 3, dy: -(r * 0.6 + 3), anchor: "start" },
        { dx: -(r + 3), dy: -(r * 0.6 + 3), anchor: "end" },
        { dx: r + 3, dy: r * 0.6 + 11, anchor: "start" },
        { dx: -(r + 3), dy: r * 0.6 + 11, anchor: "end" },
        { dx: 0, dy: -(r + 17), anchor: "middle" },
        { dx: 0, dy: r + 25, anchor: "middle" },
        { dx: 0, dy: -(r + 29), anchor: "middle" },
        { dx: 0, dy: r + 37, anchor: "middle" },
      ];
      const text = shortName(d.player_name);
      const w = text.length * 6.4 + 4;
      const cx = x(d.x);
      const cy = y(d.y);
      const pick =
        slots.find((slot) => {
          const left = cx + slot.dx - (slot.anchor === "middle" ? w / 2 : slot.anchor === "end" ? w : 0);
          const box = { x0: left, x1: left + w, y0: cy + slot.dy - 10, y1: cy + slot.dy + 2 };
          if (box.x0 < -OVERHANG || box.x1 > plotW + OVERHANG || box.y0 < -8 || box.y1 > plotH + 8) return false;
          return !boxes.some((b) => box.x0 < b.x1 && box.x1 > b.x0 && box.y0 < b.y1 && box.y1 > b.y0);
        }) || slots[0];
      const left = cx + pick.dx - (pick.anchor === "middle" ? w / 2 : pick.anchor === "end" ? w : 0);
      boxes.push({ x0: left, x1: left + w, y0: cy + pick.dy - 10, y1: cy + pick.dy + 2 });
      d3.select(this)
        .append("text")
        .attr("class", "perf-label")
        .attr("x", pick.dx)
        .attr("y", pick.dy)
        .attr("text-anchor", pick.anchor)
        .attr("fill", "#f4f7f6")
        .attr("font-family", "Roboto, Helvetica Neue, Segoe UI, sans-serif")
        .attr("font-weight", 500)
        .text(text);
    });
  }

  function showTip(event, player, metrics) {
    const { xM, yM, sizeM, sortM } = metrics;
    const per90 = state.per90 ? " /90" : "";
    const xDigits = state.per90 ? 2 : xM.digits;
    const yDigits = state.per90 ? 2 : yM.digits;
    const sortDigits = state.per90 ? 2 : sortM.digits;
    els.tip.innerHTML = `<strong>${escapeHtml(player.player_name)} · ${escapeHtml(player.team_short)}</strong>
      ${xM.short}${per90}: ${format(player.x, xDigits)} · ${yM.short}${per90}: ${format(player.y, yDigits)}<br>
      ${sizeM.short}: ${format(player.size, sizeM.digits)} · ${sortM.short}${per90}: ${format(player.sortVal, sortDigits)}<br>
      <span>${player.apps} apps · ${format(player.minutes, 0)} mins · ${format(player.minutes / player.apps, 0)} mins/app</span>`;
    els.tip.hidden = false;
    els.tip.style.left = `${Math.min(window.innerWidth - 295, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 140, event.clientY + 14)}px`;
  }

  function hideTip() {
    els.tip.hidden = true;
  }

  function format(value, digits) {
    return Number(value || 0).toFixed(digits).replace(/\.00$/, "");
  }

  function shortName(name) {
    const full = String(name || "—").trim();
    const last = full.split(/\s+/).at(-1) || "—";
    return last.length <= 2 || last.endsWith(".") ? full : last;
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function escapeAttr(value) {
    return escapeHtml(value).replaceAll("'", "&#39;");
  }

  window.initPlayerPerformance = init;
})();
