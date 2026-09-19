/* FPL-Core scatter: actual output against the matching expected model. */
(() => {
  const DATA_URL = "./data/players_matches.json";
  const MIN_MINUTES_PER_APP = 45;
  const METRICS = {
    G: {
      actual: "G",
      expected: "xG",
      size: "SoT",
      label: "Goals vs xG",
      actualName: "Goals",
      expectedName: "Expected goals",
      sizeName: "Shots on target",
      digits: 0,
    },
    A: {
      actual: "A",
      expected: "xA",
      size: "CC",
      label: "Assists vs xA",
      actualName: "Assists",
      expectedName: "Expected assists",
      sizeName: "Chances created",
      digits: 0,
    },
  };

  const state = {
    rows: [],
    season: null,
    metric: "G",
    topN: 20,
    gwFrom: 1,
    gwTo: 38,
    per90: false,
    min45: false,
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
    els.metric = $("perf-metric");
    els.top = $("perf-top");
    els.gwFrom = $("perf-gw-from");
    els.gwTo = $("perf-gw-to");
    els.gwLabel = $("perf-gw-label");
    els.per90 = $("perf-per90");
    els.min45 = $("perf-min45");
    els.status = $("perf-status");
    els.chart = $("perf-chart");
    els.tip = $("perf-tip");
  }

  function bindEvents() {
    els.season.addEventListener("change", () => {
      state.season = els.season.value;
      syncGwBounds(true);
      render();
    });
    els.metric.addEventListener("change", () => {
      state.metric = els.metric.value;
      render();
    });
    els.top.addEventListener("change", () => {
      state.topN = Number(els.top.value) || 20;
      render();
    });
    const syncGw = () => {
      let from = Number(els.gwFrom.value);
      let to = Number(els.gwTo.value);
      if (from > to) [from, to] = [to, from];
      state.gwFrom = from;
      state.gwTo = to;
      updateGwLabel();
      render();
    };
    els.gwFrom.addEventListener("input", syncGw);
    els.gwTo.addEventListener("input", syncGw);
    els.per90.addEventListener("change", () => {
      state.per90 = els.per90.checked;
      render();
    });
    els.min45.addEventListener("change", () => {
      state.min45 = els.min45.checked;
      render();
    });
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-player-performance")?.hidden) render();
      }, 120);
    });
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
    for (const input of [els.gwFrom, els.gwTo]) {
      input.min = String(min);
      input.max = String(max);
    }
    if (reset) {
      state.gwFrom = min;
      state.gwTo = max;
      els.gwFrom.value = String(min);
      els.gwTo.value = String(max);
    }
    updateGwLabel();
  }

  function updateGwLabel() {
    els.gwLabel.textContent = `GW ${state.gwFrom}–${state.gwTo}`;
  }

  function num(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function aggregate(metric) {
    const rows = seasonRows().filter(
      (r) => Number(r.gw) >= state.gwFrom && Number(r.gw) <= state.gwTo && num(r.m) > 0
    );
    const players = new Map();
    for (const r of rows) {
      const key = r.pc || r.pid;
      if (!players.has(key)) {
        players.set(key, {
          player_name: r.n,
          team_short: r.tm || "—",
          position: r.pos,
          apps: 0,
          minutes: 0,
          actual: 0,
          expected: 0,
          SoT: 0,
          CC: 0,
        });
      }
      const p = players.get(key);
      p.apps += 1;
      p.minutes += num(r.m);
      p.team_short = r.tm || p.team_short;
      p.actual += num(r[metric.actual]);
      p.expected += num(r[metric.expected]);
      p.SoT += num(r.SoT);
      p.CC += num(r.CC);
    }
    return [...players.values()];
  }

  function shape(metric) {
    let players = aggregate(metric).filter((p) => p.minutes > 0);
    if (state.min45) {
      players = players.filter((p) => p.minutes / p.apps >= MIN_MINUTES_PER_APP);
    }
    for (const p of players) {
      const factor = state.per90 ? 90 / p.minutes : 1;
      p.x = p.expected * factor;
      p.y = p.actual * factor;
      p.delta = p.y - p.x;
      p.size = p[metric.size];
    }
    return players
      .filter((p) => p.x > 0 || p.y > 0)
      .sort((a, b) => b.y - a.y || b.x - a.x)
      .slice(0, state.topN);
  }

  function render() {
    if (!state.rows.length || !els.chart?.clientWidth) return;
    const metric = METRICS[state.metric];
    const players = shape(metric);
    const unit = state.per90 ? " per 90" : "";
    const minsNote = state.min45 ? ` · 45+ mins per appearance` : "";
    // Bubbles stay on raw volume; a per-90 rate would inflate cameo appearances.
    const sizeNote = `${metric.sizeName.toLowerCase()}${state.per90 ? " (total, not per 90)" : ""}`;
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · top ${players.length} by ${metric.actualName.toLowerCase()}${unit}${minsNote} · above the line = overperforming · bubble size = ${sizeNote} · FPL-Core`;

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
        .text("No players match this season, gameweek range and minutes filter.");
      return;
    }
    draw(svg, players, metric, width, height);
  }

  function draw(svg, players, metric, width, height) {
    const margin = { top: 22, right: 28, bottom: 46, left: 58 };
    const plotW = Math.max(10, width - margin.left - margin.right);
    const plotH = Math.max(10, height - margin.top - margin.bottom);
    // Both axes start at zero and share one scale, so the parity line sits at a true 45°.
    const top = Math.max(...players.flatMap((p) => [p.x, p.y]), 1) * 1.08;
    const x = d3.scaleLinear().domain([0, top]).nice().range([0, plotW]);
    const y = d3.scaleLinear().domain([0, top]).nice().range([plotH, 0]);
    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    g.append("g")
      .attr("class", "perf-grid")
      .attr("transform", `translate(0,${plotH})`)
      .call(d3.axisBottom(x).ticks(7).tickSize(-plotH).tickFormat(d3.format("~g")));
    g.append("g")
      .attr("class", "perf-grid")
      .call(axisTicks(d3.axisLeft(y).tickSize(-plotW), y, metric));

    const per90 = state.per90 ? " per 90" : "";
    g.append("text")
      .attr("class", "perf-axis-title")
      .attr("x", plotW / 2)
      .attr("y", plotH + 38)
      .attr("text-anchor", "middle")
      .text(`${metric.expectedName}${per90}`);
    g.append("text")
      .attr("class", "perf-axis-title")
      .attr("transform", `translate(-42,${plotH / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .text(`${metric.actualName}${per90}`);

    // Parity line: on it means output matches the model.
    const parity = Math.min(x.domain()[1], y.domain()[1]);
    g.append("line")
      .attr("class", "perf-parity")
      .attr("x1", x(0))
      .attr("y1", y(0))
      .attr("x2", x(parity))
      .attr("y2", y(parity));

    // Area, not radius, carries the volume metric.
    const maxSize = Math.max(...players.map((p) => p.size), 1);
    const radius = d3.scaleSqrt().domain([0, maxSize]).range([5, 17]);
    const dots = g
      .selectAll("g.perf-dot")
      .data(players)
      .join("g")
      .attr("class", "perf-dot")
      .attr("transform", (d) => `translate(${x(d.x)},${y(d.y)})`);

    dots
      .append("circle")
      .attr("r", (d) => radius(d.size))
      .attr("fill", (d) => tone(d))
      .attr("fill-opacity", 0.85)
      .on("mousemove", (event, d) => showTip(event, d, metric))
      .on("mouseleave", hideTip);

    placeLabels(dots, players, x, y, plotW, plotH, radius);
  }

  /** Counts get whole-number ticks; per-90 rates keep d3's defaults. */
  function axisTicks(axis, scale, metric) {
    if (state.per90 || metric.digits > 0) return axis.ticks(7).tickFormat(d3.format("~g"));
    const [lo, hi] = scale.domain();
    const steps = Math.max(1, Math.ceil((hi - lo) / 7));
    const ticks = [];
    for (let v = Math.ceil(lo); v <= hi; v += steps) ticks.push(v);
    return axis.tickValues(ticks).tickFormat(d3.format("d"));
  }

  /** Nudge labels to the first free slot around the dot so names stay readable. */
  function placeLabels(dots, players, x, y, plotW, plotH, radius) {
    const OVERHANG = 26;
    // Reserve the bubbles first so labels never land on a marker.
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
        .text(text);
    });
  }

  function tone(player) {
    const band = Math.max(0.15, player.x * 0.1);
    if (player.delta > band) return "#3ecf8e";
    if (player.delta < -band) return "#ef7a72";
    return "#9fb0bd";
  }

  function showTip(event, player, metric) {
    const per90 = state.per90 ? " / 90" : "";
    const digits = state.per90 ? 2 : metric.digits;
    els.tip.innerHTML = `<strong>${escapeHtml(player.player_name)} · ${escapeHtml(player.team_short)}</strong>
      ${escapeHtml(metric.actualName)}${per90}: ${format(player.y, digits)}<br>
      ${escapeHtml(metric.expectedName)}${per90}: ${format(player.x, 2)}<br>
      ${player.delta >= 0 ? "Over" : "Under"} by ${format(Math.abs(player.delta), 2)}<br>
      Shots on target: ${format(player.SoT, 0)}<br>
      Chances created: ${format(player.CC, 0)}<br>
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
    // Some FPL names end in an initial ("Rodrigo G."); the surname alone would be meaningless.
    return last.length <= 2 || last.endsWith(".") ? full : last;
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  window.initPlayerPerformance = init;
})();
