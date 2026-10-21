/* Finishing insight: SoT% (Y) vs shots/90 (X). */
(() => {
  const DATA_URL = "./data/players_matches.json";
  const MIN_MINUTES_PER_APP = 45;

  const state = {
    rows: [],
    season: null,
    topN: 20,
    position: "ALL",
    gwFrom: 1,
    gwTo: 38,
    per90: true,
    min45: true,
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
      els.status.textContent = `Failed to load data: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("fin-root");
    els.season = $("fin-season");
    els.position = $("fin-position");
    els.top = $("fin-top");
    els.gwRange = $("fin-gw-range");
    els.gwLabel = $("fin-gw-label");
    els.per90 = $("fin-per90");
    els.min45 = $("fin-min45");
    els.status = $("fin-status");
    els.chart = $("fin-chart");
    els.tip = $("fin-tip");
    els.chartDl = $("fin-chart-dl");
    els.gwControl = null;
  }

  function bindEvents() {
    els.season?.addEventListener("change", () => {
      state.season = els.season.value;
      syncGwBounds(true);
      render();
    });
    els.position?.addEventListener("change", () => {
      state.position = els.position.value;
      render();
    });
    els.top?.addEventListener("change", () => {
      state.topN = Number(els.top.value) || 20;
      render();
    });
    els.per90?.addEventListener("change", () => {
      state.per90 = Boolean(els.per90.checked);
      render();
    });
    els.min45?.addEventListener("change", () => {
      state.min45 = Boolean(els.min45.checked);
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
          els.gwLabel.textContent = `GW ${from}–${to}`;
          render();
        },
      });
    }
    if (els.chartDl && window.ChartExport && !els.chartDl.dataset.bound) {
      els.chartDl.dataset.bound = "1";
      window.ChartExport.bindChartDownload(
        els.chartDl,
        () => els.chart,
        () => "fpl-pulse-talk-finishing",
        () => ({
          title: "Who shoots often — and puts shots on target?",
          metrics: state.per90
            ? "X = Shots / 90 · Y = Shot on target % · Bubble = xG/90 · Colour = club"
            : "X = Shots · Y = Shot on target % · Bubble = xG · Colour = club",
          meta: `${state.season} · GW ${state.gwFrom}–${state.gwTo} · Top ${state.topN}${state.per90 ? " · Per 90" : ""}`,
        })
      );
    }
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-finishing")?.hidden) render();
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

  function syncGwBounds(reset) {
    const gws = state.rows.filter((r) => r.s === state.season).map((r) => Number(r.gw)).filter((g) => g > 0);
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
    els.gwLabel.textContent = `GW ${state.gwFrom}–${state.gwTo}`;
  }

  function num(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }

  function positionMatches(position) {
    if (state.position === "ALL") return true;
    if (state.position === "MID") return position === "Midfielder";
    if (state.position === "ATT") return position === "Forward";
    return position === "Defender" || position === "Goalkeeper";
  }

  function shortName(name) {
    const full = String(name || "—").trim();
    const last = full.split(/\s+/).at(-1) || "—";
    return last.length <= 2 || last.endsWith(".") ? full : last;
  }

  function aggregate() {
    const rows = state.rows.filter(
      (r) =>
        r.s === state.season &&
        Number(r.gw) >= state.gwFrom &&
        Number(r.gw) <= state.gwTo &&
        num(r.m) > 0 &&
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
          apps: 0,
          minutes: 0,
          Sh: 0,
          SoT: 0,
          G: 0,
          xG: 0,
        });
      }
      const p = map.get(key);
      p.apps += 1;
      p.minutes += num(r.m);
      p.Sh += num(r.Sh);
      p.SoT += num(r.SoT);
      p.G += num(r.G);
      p.xG += num(r.xG);
      p.player_name = r.n || p.player_name;
      p.team_short = r.tm || p.team_short;
    }
    let list = [...map.values()].filter((p) => p.minutes > 0 && p.Sh > 0);
    if (state.min45) list = list.filter((p) => p.minutes / p.apps >= MIN_MINUTES_PER_APP);
    list = list
      .map((p) => {
        const sh90 = (p.Sh * 90) / p.minutes;
        const xg90 = (p.xG * 90) / p.minutes;
        return {
          ...p,
          sh90,
          xg90,
          sotPct: (p.SoT / p.Sh) * 100,
          xVal: state.per90 ? sh90 : p.Sh,
          sizeVal: state.per90 ? xg90 : p.xG,
        };
      })
      .sort((a, b) => b.Sh - a.Sh)
      .slice(0, state.topN);
    return list;
  }

  function placeLabels(dots, players, x, y, plotW, plotH, radius) {
    const OVERHANG = 26;
    const boxes = players.map((p) => ({
      x0: x(p.xVal) - radius(p.sizeVal) - 2,
      x1: x(p.xVal) + radius(p.sizeVal) + 2,
      y0: y(p.sotPct) - radius(p.sizeVal) - 2,
      y1: y(p.sotPct) + radius(p.sizeVal) + 2,
    }));
    dots.each(function (d) {
      const r = radius(d.sizeVal);
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
      const cx = x(d.xVal);
      const cy = y(d.sotPct);
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
        .attr("stroke", "rgba(8,12,10,0.75)")
        .attr("stroke-width", 3)
        .attr("paint-order", "stroke")
        .attr("font-family", "Roboto, Helvetica Neue, Segoe UI, sans-serif")
        .attr("font-weight", 600)
        .attr("font-size", 11)
        .text(text);
    });
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function showTip(event, d) {
    if (!els.tip) return;
    const bubble = state.per90 ? "xG/90" : "xG";
    els.tip.hidden = false;
    els.tip.innerHTML = `<strong>${escapeHtml(d.player_name)}</strong>
      <span>${escapeHtml(d.team_short)} · ${d.apps} apps · ${Math.round(d.minutes)} mins</span>
      <div class="fpl-tip-grid">
        <span>SoT%</span><b>${d.sotPct.toFixed(1)}</b>
        <span>Sh/90</span><b>${d.sh90.toFixed(2)}</b>
        <span>Sh</span><b>${Math.round(d.Sh)}</b>
        <span>SoT</span><b>${Math.round(d.SoT)}</b>
        <span>G</span><b>${Math.round(d.G)}</b>
        <span>xG</span><b>${d.xG.toFixed(2)}</b>
        <span>xG/90</span><b>${d.xg90.toFixed(2)}</b>
        <span>Bubble</span><b>${bubble}</b>
      </div>`;
    els.tip.style.left = `${Math.min(window.innerWidth - 295, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 180, event.clientY + 14)}px`;
  }

  function hideTip() {
    if (els.tip) els.tip.hidden = true;
  }

  function render() {
    if (!els.chart) return;
    const players = aggregate();
    const xLabel = state.per90 ? "Shots / 90" : "Shots";
    const bubbleLabel = state.per90 ? "xG/90" : "xG";
    const unitNote = state.per90 ? " · Per 90" : "";
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · Top ${players.length} by total shots${unitNote} · Bubble = ${bubbleLabel} · Colour = club · Y = SoT% · X = ${xLabel}`;
    const width = els.chart.clientWidth || 960;
    const height = els.chart.clientHeight || 560;
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
    const margin = { top: 28, right: 36, bottom: 48, left: 56 };
    const innerW = width - margin.left - margin.right;
    const innerH = height - margin.top - margin.bottom;
    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
    // Auto-scale axes to the visible cohort (with padding), not a fixed 0–floor domain.
    const xExt = d3.extent(players, (d) => d.xVal);
    const yExt = d3.extent(players, (d) => d.sotPct);
    const xPad = Math.max((xExt[1] - xExt[0]) * 0.12, state.per90 ? 0.15 : 1);
    const yPad = Math.max((yExt[1] - yExt[0]) * 0.12, 3);
    const x0 = Math.max(0, xExt[0] - xPad);
    const x1 = Math.max(x0 + 0.01, xExt[1] + xPad);
    const y0 = Math.max(0, yExt[0] - yPad);
    const y1 = Math.min(100, Math.max(y0 + 1, yExt[1] + yPad));
    const x = d3.scaleLinear().domain([x0, x1]).nice().range([0, innerW]);
    const y = d3.scaleLinear().domain([y0, y1]).nice().range([innerH, 0]);
    const radius = d3.scaleSqrt().domain([0, d3.max(players, (d) => d.sizeVal) || 0.01]).range([5, 18]);

    g.append("g").attr("class", "perf-grid").call(d3.axisBottom(x).ticks(6).tickSize(-innerH)).attr("transform", `translate(0,${innerH})`);
    g.append("g").attr("class", "perf-grid").call(d3.axisLeft(y).ticks(6).tickSize(-innerW));
    g.selectAll(".perf-grid text").attr("fill", "#9aafb8");
    g.selectAll(".perf-grid line").attr("stroke", "#2d3d4a");
    g.selectAll(".domain").attr("stroke", "#2d3d4a");

    g.append("text").attr("class", "perf-axis-title").attr("x", innerW / 2).attr("y", innerH + 40).attr("text-anchor", "middle").attr("fill", "#9aafb8").text(xLabel);
    g.append("text").attr("class", "perf-axis-title").attr("transform", "rotate(-90)").attr("x", -innerH / 2).attr("y", -42).attr("text-anchor", "middle").attr("fill", "#9aafb8").text("Shot on target %");

    const fill = window.TeamColors?.teamFill
      ? (d) => window.TeamColors.teamFill(d.team_short)
      : () => "#3ddc97";

    const dots = g
      .selectAll("g.fin-dot")
      .data(players)
      .join("g")
      .attr("class", "fin-dot")
      .attr("transform", (d) => `translate(${x(d.xVal)},${y(d.sotPct)})`);

    dots
      .append("circle")
      .attr("r", (d) => radius(d.sizeVal))
      .attr("fill", fill)
      .attr("fill-opacity", 0.88)
      .attr("stroke", "rgba(8,12,10,0.55)")
      .attr("stroke-width", 1.2)
      .style("cursor", "pointer")
      .on("mousemove", (event, d) => showTip(event, d))
      .on("mouseleave", hideTip);

    placeLabels(dots, players, x, y, innerW, innerH, radius);
  }

  window.initFinishing = init;
})();
