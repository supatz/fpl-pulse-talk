/* Team shot side channels: sortable L/C/R table + dual pitch compare + spider. */
(() => {
  const DATA_URL = "./data/us_team_side_channels.json";
  const TEAMS_GW_URL = "./data/teams_gw.json";
  const SIDES = ["Left", "Center", "Right"];
  const COLOR_A = "#6eb6ff";
  const COLOR_B = "#ff6b6b";
  const SPIDER_AXES = [
    { key: "xg", label: "xG", digits: 2 },
    { key: "CC", label: "CC", digits: 0 },
    { key: "big_chances", label: "BCC", digits: 0 },
    { key: "shots_on_target", label: "SoT", digits: 0 },
    { key: "xga", label: "xG-A", digits: 2 },
    { key: "CC_A", label: "CC-A", digits: 0 },
    { key: "big_chances_conceded", label: "BC-A", digits: 0 },
    { key: "sot_conceded", label: "SoT-A", digits: 0 },
  ];

  const state = {
    data: null,
    teamsGw: [],
    season: null,
    metric: "shots",
    sizeMetric: "xg",
    sortMode: "value",
    gwFrom: 1,
    gwTo: 38,
    sortKey: "team",
    sortDir: "asc",
    teamA: null,
    teamB: null,
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
      const [sideRes, tgRes] = await Promise.all([
        fetch(DATA_URL, { cache: "no-store" }),
        fetch(TEAMS_GW_URL, { cache: "no-store" }),
      ]);
      if (!sideRes.ok) throw new Error(`side channels HTTP ${sideRes.status}`);
      state.data = await sideRes.json();
      if (tgRes.ok) state.teamsGw = await tgRes.json();
      populateSeasons();
      syncGwBounds(true);
      render();
    } catch (err) {
      els.status.textContent = `Failed to load side channels: ${err.message}. Rebuild Understat serving if missing.`;
    }
  }

  function bindEls() {
    els.root = $("side-root");
    els.season = $("side-season");
    els.metric = $("side-metric");
    els.sortMode = $("side-sort-mode");
    els.sizeMetric = $("side-size-metric");
    els.gwRange = $("side-gw-range");
    els.gwLabel = $("side-gw-label");
    els.status = $("side-status");
    els.chart = $("side-chart");
    els.pitches = $("side-pitches");
    els.radar = $("side-radar");
    els.teamA = $("side-team-a");
    els.teamB = $("side-team-b");
    els.tip = $("side-tip");
    els.chartDl = $("side-chart-dl");
    els.radarDl = $("side-radar-dl");
    els.pitchesDl = $("side-pitches-dl");
    els.gwControl = null;
  }

  function bindEvents() {
    els.season?.addEventListener("change", () => {
      state.season = els.season.value;
      syncGwBounds(true);
      state.teamA = null;
      state.teamB = null;
      render();
    });
    els.metric?.addEventListener("change", () => {
      state.metric = els.metric.value;
      render();
    });
    els.sortMode?.addEventListener("change", () => {
      state.sortMode = els.sortMode.value === "pct" ? "pct" : "value";
      renderTable();
    });
    els.sizeMetric?.addEventListener("change", () => {
      state.sizeMetric = els.sizeMetric.value;
      renderPitches();
    });
    els.teamA?.addEventListener("change", () => {
      state.teamA = els.teamA.value || null;
      renderPitches();
      renderSpider();
    });
    els.teamB?.addEventListener("change", () => {
      state.teamB = els.teamB.value || null;
      renderPitches();
      renderSpider();
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
        () => "fpl-pulse-talk-team-sides",
        () => ({
          title: "Where teams take and concede shots — Left, Center, Right",
          metrics: `Metric = ${state.metric === "xg" ? "xG = Expected goals" : "Sh = Shots"} · Sort = ${
            state.sortMode === "pct" ? "%" : "value"
          } · Bars = share by side`,
          meta: `${state.season} · GW ${state.gwFrom}–${state.gwTo}`,
        })
      );
    }
    if (els.radarDl && window.ChartExport && !els.radarDl.dataset.bound) {
      els.radarDl.dataset.bound = "1";
      window.ChartExport.bindChartDownload(
        els.radarDl,
        () => els.radar,
        () => "fpl-pulse-talk-team-sides-spider",
        () => {
          const a = els.teamA?.selectedOptions?.[0]?.textContent || "Team A";
          const b = els.teamB?.selectedOptions?.[0]?.textContent || "Team B";
          return {
            title: `${a} vs ${b} — attack & concede spider`,
            metrics: "xG · CC · BCC · SoT · xG-A · CC-A · BC-A · SoT-A (Opta / team CC)",
            meta: `${state.season} · GW ${state.gwFrom}–${state.gwTo}`,
          };
        }
      );
    }
    if (els.pitchesDl && window.ChartExport && !els.pitchesDl.dataset.bound) {
      els.pitchesDl.dataset.bound = "1";
      els.pitchesDl.addEventListener("click", async () => {
        const btn = els.pitchesDl;
        const prev = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Saving…";
        const wrap = document.createElement("div");
        wrap.style.cssText =
          "display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:8px;background:#0c141c;position:fixed;left:-10000px;top:0;width:900px;";
        els.pitches?.querySelectorAll("[data-pitch]").forEach((host) => {
          const cell = document.createElement("div");
          cell.style.cssText = "min-width:0;background:#122018;border-radius:10px;overflow:hidden;";
          const svg = host.querySelector("svg");
          if (svg) cell.appendChild(svg.cloneNode(true));
          wrap.appendChild(cell);
        });
        document.body.appendChild(wrap);
        try {
          const a = els.teamA?.selectedOptions?.[0]?.textContent || "Team A";
          const b = els.teamB?.selectedOptions?.[0]?.textContent || "Team B";
          await window.ChartExport.downloadChart(wrap, "fpl-pulse-talk-team-sides-pitches", {
            title: `${a} vs ${b} — shot side pitches`,
            metrics: `Circles = Understat xG · Size = ${state.sizeMetric === "equal" ? "equal" : "xG"}`,
            meta: `${state.season} · GW ${state.gwFrom}–${state.gwTo}`,
          });
          btn.textContent = "Saved";
        } catch (err) {
          console.error(err);
          btn.textContent = "Failed";
        } finally {
          wrap.remove();
          setTimeout(() => {
            btn.textContent = prev;
            btn.disabled = false;
          }, 900);
        }
      });
    }
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-team-sides")?.hidden) {
          renderPitches();
          renderSpider();
        }
      }, 120);
    });
  }

  function populateSeasons() {
    const seasons = [...new Set((state.data?.rows || []).map((r) => r.season).filter(Boolean))].sort();
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
    const gws = (state.data?.rows || [])
      .filter((r) => r.season === state.season && r.gw != null)
      .map((r) => Number(r.gw))
      .filter((g) => g > 0);
    const min = gws.length ? Math.min(...gws) : 1;
    const max = gws.length ? Math.max(...gws) : 38;
    if (reset) {
      state.gwFrom = min;
      state.gwTo = max;
    }
    els.gwControl?.setBounds(min, max);
    els.gwControl?.set(state.gwFrom, state.gwTo);
    els.gwLabel.textContent = `GW ${state.gwFrom}–${state.gwTo}`;
  }

  function num(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }

  function inGw(gw) {
    if (gw == null) return true;
    const g = Number(gw);
    return g >= state.gwFrom && g <= state.gwTo;
  }

  function teamRows() {
    const metric = state.metric === "xg" ? "xg" : "shots";
    const scoped = (state.data?.rows || []).filter((r) => r.season === state.season && inGw(r.gw));
    const byTeam = new Map();
    for (const r of scoped) {
      const code = String(r.team_code);
      if (!byTeam.has(code)) {
        byTeam.set(code, {
          team_code: code,
          team_short: r.team_short || r.team || code,
          for: { Left: 0, Center: 0, Right: 0 },
          against: { Left: 0, Center: 0, Right: 0 },
        });
      }
      const t = byTeam.get(code);
      const bucket = r.dir === "against" ? t.against : t.for;
      if (SIDES.includes(r.side)) bucket[r.side] += num(r[metric]);
    }
    return [...byTeam.values()]
      .map((t) => {
        const sum = (o) => SIDES.reduce((a, s) => a + o[s], 0);
        t.forTotal = sum(t.for);
        t.againstTotal = sum(t.against);
        t.forShare = Object.fromEntries(SIDES.map((s) => [s, t.forTotal ? t.for[s] / t.forTotal : 0]));
        t.againstShare = Object.fromEntries(SIDES.map((s) => [s, t.againstTotal ? t.against[s] / t.againstTotal : 0]));
        return t;
      })
      .filter((t) => t.forTotal + t.againstTotal > 0);
  }

  function sortValue(t, key) {
    if (key === "team") return t.team_short;
    const map = {
      L: ["for", "Left"],
      C: ["for", "Center"],
      R: ["for", "Right"],
      "L-A": ["against", "Left"],
      "C-A": ["against", "Center"],
      "R-A": ["against", "Right"],
    };
    const spec = map[key];
    if (!spec) return 0;
    const [dir, side] = spec;
    if (state.sortMode === "pct") {
      return dir === "for" ? t.forShare[side] : t.againstShare[side];
    }
    return dir === "for" ? t.for[side] : t.against[side];
  }

  function sortedTeams(teams) {
    const dir = state.sortDir === "desc" ? -1 : 1;
    return [...teams].sort((a, b) => {
      const av = sortValue(a, state.sortKey);
      const bv = sortValue(b, state.sortKey);
      if (typeof av === "string" || typeof bv === "string") {
        return dir * String(av).localeCompare(String(bv));
      }
      return dir * (num(av) - num(bv));
    });
  }

  function barHtml(share) {
    return `<div class="side-bar" title="L ${(share.Left * 100).toFixed(0)}% · C ${(share.Center * 100).toFixed(0)}% · R ${(share.Right * 100).toFixed(0)}%">
      <i class="L" style="width:${(share.Left * 100).toFixed(1)}%"></i>
      <i class="C" style="width:${(share.Center * 100).toFixed(1)}%"></i>
      <i class="R" style="width:${(share.Right * 100).toFixed(1)}%"></i>
    </div>`;
  }

  function fmtVal(v) {
    return state.metric === "xg" ? v.toFixed(2) : String(Math.round(v));
  }

  function fmtPct(share) {
    return `${(share * 100).toFixed(0)}%`;
  }

  function cellHtml(value, share) {
    return `${fmtVal(value)} <span class="side-pct">(${fmtPct(share)})</span>`;
  }

  function sortMark(key) {
    if (state.sortKey !== key) return "";
    return state.sortDir === "asc" ? " ▲" : " ▼";
  }

  function th(key, label) {
    const modeHint = key !== "team" && state.sortKey === key ? (state.sortMode === "pct" ? " %" : " #") : "";
    return `<th class="side-sort" data-sort="${key}" tabindex="0" role="button" aria-sort="${
      state.sortKey === key ? (state.sortDir === "asc" ? "ascending" : "descending") : "none"
    }">${label}${modeHint}${sortMark(key)}</th>`;
  }

  function bindSortHeaders() {
    els.chart?.querySelectorAll("th.side-sort").forEach((thEl) => {
      const activate = () => {
        const key = thEl.getAttribute("data-sort");
        if (!key) return;
        if (state.sortKey === key) {
          state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
        } else {
          state.sortKey = key;
          state.sortDir = key === "team" ? "asc" : "desc";
        }
        renderTable();
      };
      thEl.addEventListener("click", activate);
      thEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate();
        }
      });
    });
  }

  function populateTeamSelects(teams) {
    const opts = teams
      .slice()
      .sort((a, b) => a.team_short.localeCompare(b.team_short))
      .map((t) => ({ code: t.team_code, label: t.team_short }));
    if (!opts.length) {
      state.teamA = null;
      state.teamB = null;
    } else {
      if (!state.teamA || !opts.some((o) => o.code === state.teamA)) state.teamA = opts[0].code;
      if (!state.teamB || !opts.some((o) => o.code === state.teamB)) {
        state.teamB = opts[1]?.code || opts[0].code;
      }
    }
    const fill = (sel, value) => {
      if (!sel) return;
      sel.replaceChildren(
        ...opts.map((o) => {
          const option = document.createElement("option");
          option.value = o.code;
          option.textContent = o.label;
          option.selected = o.code === value;
          return option;
        })
      );
    };
    fill(els.teamA, state.teamA);
    fill(els.teamB, state.teamB);
  }

  function teamByCode(code) {
    return teamRows().find((t) => String(t.team_code) === String(code)) || null;
  }

  function scopedPoints(teamCode) {
    return (state.data?.points || []).filter(
      (p) =>
        p.s === state.season &&
        String(p.tc) === String(teamCode) &&
        inGw(p.gw)
    );
  }

  function showTip(event, p, label) {
    if (!els.tip) return;
    const side = p.side || "—";
    const dir = p.dir === "against" ? "Conceded" : "Attack";
    const shooter = p.pn || "—";
    const assister = p.an || "—";
    const xa =
      p.xa != null && Number.isFinite(Number(p.xa))
        ? num(p.xa).toFixed(2)
        : p.an
          ? num(p.xg).toFixed(2)
          : "—";
    els.tip.hidden = false;
    els.tip.innerHTML = `<strong>${escapeHtml(label)}</strong> · ${dir}${p.g ? " · Goal" : ""}
      <div class="fpl-tip-grid">
        <span>Shooter</span><b>${escapeHtml(shooter)}</b>
        <span>xG</span><b>${num(p.xg).toFixed(2)}</b>
        <span>Assist</span><b>${escapeHtml(assister)}</b>
        <span>xA</span><b>${xa}</b>
        <span>Side</span><b>${escapeHtml(side)}</b>
        <span>GW</span><b>${p.gw != null ? p.gw : "—"}</b>
      </div>`;
    els.tip.style.left = `${Math.min(window.innerWidth - 280, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 160, event.clientY + 14)}px`;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function hideTip() {
    if (els.tip) els.tip.hidden = true;
  }

  /** Vertical pitch: attack → top, concede → bottom; L/C/R as vertical bands. */
  function drawPitch(host, teamCode, teamLabel) {
    host.replaceChildren();
    const width = host.clientWidth || 360;
    const height = Math.max(420, Math.round(width * 1.35));
    const svg = d3.select(host).append("svg").attr("viewBox", `0 0 ${width} ${height}`);
    const m = { top: 22, right: 12, bottom: 28, left: 12 };
    const pw = width - m.left - m.right;
    const ph = height - m.top - m.bottom;
    const g = svg.append("g").attr("transform", `translate(${m.left},${m.top})`);

    g.append("rect").attr("width", pw).attr("height", ph).attr("rx", 6).attr("fill", "#1f6b3a");

    // Vertical L/C/R bands (attacking view: Left = screen left)
    const bandW = pw / 3;
    const bands = [
      { x: 0, side: "Left", label: "L" },
      { x: bandW, side: "Center", label: "C" },
      { x: bandW * 2, side: "Right", label: "R" },
    ];
    const team = teamByCode(teamCode);
    bands.forEach((b) => {
      g.append("rect")
        .attr("x", b.x)
        .attr("y", 0)
        .attr("width", bandW)
        .attr("height", ph)
        .attr("fill", b.side === "Center" ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.08)");
      g.append("text")
        .attr("x", b.x + bandW / 2)
        .attr("y", ph / 2 + 4)
        .attr("text-anchor", "middle")
        .attr("fill", "rgba(255,255,255,0.28)")
        .attr("font-size", 22)
        .attr("font-weight", 700)
        .attr("font-family", "Roboto, sans-serif")
        .text(b.label);

      if (team) {
        const attV = team.for[b.side];
        const attP = team.forShare[b.side];
        const defV = team.against[b.side];
        const defP = team.againstShare[b.side];
        // Near pitch centre (away from end-zone shot clusters): attack blue, defend red.
        g.append("text")
          .attr("x", b.x + bandW / 2)
          .attr("y", ph * 0.42)
          .attr("text-anchor", "middle")
          .attr("fill", "#6eb6ff")
          .attr("stroke", "rgba(8,20,12,0.65)")
          .attr("stroke-width", 3)
          .attr("paint-order", "stroke")
          .attr("font-size", 12)
          .attr("font-weight", 700)
          .attr("font-family", "Roboto, sans-serif")
          .text(`${fmtVal(attV)} (${fmtPct(attP)})`);
        g.append("text")
          .attr("x", b.x + bandW / 2)
          .attr("y", ph * 0.58)
          .attr("text-anchor", "middle")
          .attr("fill", "#ff6b6b")
          .attr("stroke", "rgba(8,20,12,0.65)")
          .attr("stroke-width", 3)
          .attr("paint-order", "stroke")
          .attr("font-size", 12)
          .attr("font-weight", 700)
          .attr("font-family", "Roboto, sans-serif")
          .text(`${fmtVal(defV)} (${fmtPct(defP)})`);
      }
    });

    g.append("rect")
      .attr("width", pw)
      .attr("height", ph)
      .attr("rx", 6)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.55)")
      .attr("stroke-width", 2);
    g.append("line")
      .attr("x1", 0)
      .attr("x2", pw)
      .attr("y1", ph / 2)
      .attr("y2", ph / 2)
      .attr("stroke", "rgba(255,255,255,0.45)")
      .attr("stroke-width", 1.5);
    g.append("circle")
      .attr("cx", pw / 2)
      .attr("cy", ph / 2)
      .attr("r", Math.min(pw, ph) * 0.1)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.4)")
      .attr("stroke-width", 1.5);

    // Goals: top = attack, bottom = concede
    const goalH = 8;
    const goalW = pw * 0.22;
    const goalX = (pw - goalW) / 2;
    g.append("rect")
      .attr("x", goalX)
      .attr("y", -goalH)
      .attr("width", goalW)
      .attr("height", goalH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.85)")
      .attr("stroke-width", 2);
    g.append("rect")
      .attr("x", goalX)
      .attr("y", ph)
      .attr("width", goalW)
      .attr("height", goalH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.85)")
      .attr("stroke-width", 2);

    const boxH = ph * 0.16;
    const boxW = pw * 0.55;
    const boxX = (pw - boxW) / 2;
    g.append("rect")
      .attr("x", boxX)
      .attr("y", 0)
      .attr("width", boxW)
      .attr("height", boxH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.4)")
      .attr("stroke-width", 1.2);
    g.append("rect")
      .attr("x", boxX)
      .attr("y", ph - boxH)
      .attr("width", boxW)
      .attr("height", boxH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.4)")
      .attr("stroke-width", 1.2);

    // Six-yard box (~20×6 yd inside ~44×18 yd penalty area)
    const sixW = boxW * (20 / 44);
    const sixH = boxH * (6 / 18);
    const sixX = (pw - sixW) / 2;
    g.append("rect")
      .attr("x", sixX)
      .attr("y", 0)
      .attr("width", sixW)
      .attr("height", sixH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.45)")
      .attr("stroke-width", 1.1);
    g.append("rect")
      .attr("x", sixX)
      .attr("y", ph - sixH)
      .attr("width", sixW)
      .attr("height", sixH)
      .attr("fill", "none")
      .attr("stroke", "rgba(255,255,255,0.45)")
      .attr("stroke-width", 1.1);

    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", 14)
      .attr("text-anchor", "middle")
      .attr("fill", "#e8f0ec")
      .attr("font-size", 12)
      .attr("font-weight", 700)
      .attr("font-family", "Roboto, sans-serif")
      .text(`${teamLabel || "—"} · Attack ↑`);
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", height - 8)
      .attr("text-anchor", "middle")
      .attr("fill", "#8fa59a")
      .attr("font-size", 11)
      .attr("font-family", "Roboto, sans-serif")
      .text("Concede ↓");

    const points = scopedPoints(teamCode);
    const maxXg = d3.max(points, (d) => num(d.xg)) || 0.3;
    const radius =
      state.sizeMetric === "equal"
        ? () => 4.5
        : d3.scaleSqrt().domain([0, maxXg]).range([2.5, 11]);

    // Vertical: attack → top (high x), concede → bottom; L high-y → left
    const plotX = (p) => (1 - num(p.y)) * pw;
    const plotY = (p) => {
      const x = num(p.x);
      return p.dir === "against" ? x * ph : (1 - x) * ph;
    };

    g.selectAll("circle.shot")
      .data(points)
      .join("circle")
      .attr("class", "shot")
      .attr("cx", plotX)
      .attr("cy", plotY)
      .attr("r", (d) => radius(num(d.xg)))
      .attr("fill", (d) => (d.dir === "against" ? "#ff6b6b" : "#6eb6ff"))
      .attr("fill-opacity", 0.8)
      .attr("stroke", (d) => (d.g ? "#fff" : "rgba(0,0,0,0.25)"))
      .attr("stroke-width", (d) => (d.g ? 1.4 : 0.6))
      .on("mousemove", (event, d) => showTip(event, d, teamLabel))
      .on("mouseleave", hideTip);
  }

  function renderPitches() {
    if (!els.pitches) return;
    const aHost = els.pitches.querySelector("[data-pitch='a']");
    const bHost = els.pitches.querySelector("[data-pitch='b']");
    if (!aHost || !bHost) return;
    const labelA = els.teamA?.selectedOptions?.[0]?.textContent || state.teamA || "Team A";
    const labelB = els.teamB?.selectedOptions?.[0]?.textContent || state.teamB || "Team B";
    drawPitch(aHost, state.teamA, labelA);
    drawPitch(bHost, state.teamB, labelB);
  }

  function emptyAxisTotals() {
    return Object.fromEntries(SPIDER_AXES.map((a) => [a.key, 0]));
  }

  function teamOptaTotals(teamCode) {
    const totals = emptyAxisTotals();
    if (teamCode == null) return totals;
    const code = String(teamCode);
    for (const r of state.teamsGw || []) {
      if (!r.finished) continue;
      if (r.season !== state.season) continue;
      // Match Teams page default: Premier League only (not cups / Europe).
      if (r.competition && r.competition !== "Premier League") continue;
      if (String(r.team_code) !== code) continue;
      if (!inGw(r.gw)) continue;
      for (const axis of SPIDER_AXES) totals[axis.key] += num(r[axis.key]);
    }
    return totals;
  }

  /** League-wide team totals in the current season + GW window (for spider benchmarks). */
  function spiderCohortTotals() {
    const byTeam = new Map();
    for (const r of state.teamsGw || []) {
      if (!r.finished) continue;
      if (r.season !== state.season) continue;
      if (!inGw(r.gw)) continue;
      if (r.competition && r.competition !== "Premier League") continue;
      const code = String(r.team_code);
      if (!byTeam.has(code)) {
        byTeam.set(code, {
          team_code: code,
          short: r.short || r.team || code,
          goals_for: 0,
          xg: 0,
          ...emptyAxisTotals(),
        });
      }
      const t = byTeam.get(code);
      t.goals_for += num(r.goals_for);
      t.xg += num(r.xg);
      for (const axis of SPIDER_AXES) t[axis.key] += num(r[axis.key]);
    }
    return [...byTeam.values()];
  }

  function meanAxisTotals(list) {
    const out = emptyAxisTotals();
    if (!list.length) return out;
    for (const axis of SPIDER_AXES) {
      out[axis.key] = list.reduce((a, t) => a + num(t[axis.key]), 0) / list.length;
    }
    return out;
  }

  function spiderBenchmarks() {
    const cohort = spiderCohortTotals();
    const league = meanAxisTotals(cohort);
    const top5 = meanAxisTotals(
      [...cohort].sort((a, b) => b.goals_for - a.goals_for || b.xg - a.xg).slice(0, 5)
    );
    return { cohort, league, top5 };
  }

  function fmtSpider(axis, value) {
    const v = num(value);
    return axis.digits ? v.toFixed(axis.digits) : String(Math.round(v));
  }

  function showSpiderTip(event, axis, labelA, labelB, valsA, valsB, top5, league) {
    if (!els.tip || !axis) return;
    els.tip.hidden = false;
    els.tip.innerHTML = `<strong>${escapeHtml(axis.label)}</strong>
      <div class="fpl-tip-grid">
        <span>${escapeHtml(labelA)}</span><b>${fmtSpider(axis, valsA[axis.key])}</b>
        <span>${escapeHtml(labelB)}</span><b>${fmtSpider(axis, valsB[axis.key])}</b>
        <span>Top 5 avg</span><b>${fmtSpider(axis, top5[axis.key])}</b>
        <span>League avg</span><b>${fmtSpider(axis, league[axis.key])}</b>
      </div>`;
    els.tip.style.left = `${Math.min(window.innerWidth - 280, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 160, event.clientY + 14)}px`;
  }

  function polarPoint(cx, cy, r, angle) {
    return [cx + r * Math.sin(angle), cy - r * Math.cos(angle)];
  }

  function renderSpider() {
    if (!els.radar) return;
    els.radar.replaceChildren();
    const labelA = els.teamA?.selectedOptions?.[0]?.textContent || state.teamA || "Team A";
    const labelB = els.teamB?.selectedOptions?.[0]?.textContent || state.teamB || "Team B";
    const valsA = teamOptaTotals(state.teamA);
    const valsB = teamOptaTotals(state.teamB);
    const { league, top5 } = spiderBenchmarks();

    const width = els.radar.clientWidth || 320;
    const height = Math.max(260, Math.round(width * 0.78));
    const svg = d3.select(els.radar).append("svg").attr("viewBox", `0 0 ${width} ${height}`);
    const cx = width / 2;
    const cy = height / 2 + 4;
    const radius = Math.min(width, height) * 0.36;
    const n = SPIDER_AXES.length;
    const angle = (i) => (i / n) * Math.PI * 2;

    [0.25, 0.5, 0.75, 1].forEach((t) => {
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
        .attr("stroke", "rgba(255,255,255,0.16)")
        .attr("stroke-width", 1);
      const [lx, ly] = polarPoint(cx, cy, radius + 16, angle(i));
      svg
        .append("text")
        .attr("x", lx)
        .attr("y", ly)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .attr("fill", "#d5e4dc")
        .attr("font-size", 11)
        .attr("font-weight", 700)
        .attr("font-family", "Roboto, sans-serif")
        .attr("pointer-events", "none")
        .text(axis.label);
    });

    const maxByAxis = Object.fromEntries(
      SPIDER_AXES.map((a) => [
        a.key,
        Math.max(valsA[a.key], valsB[a.key], league[a.key], top5[a.key], a.digits ? 0.01 : 1),
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
        .attr("stroke-width", 2)
        .attr("pointer-events", "none");
      pts.forEach(([x, y], i) => {
        svg
          .append("circle")
          .attr("cx", x)
          .attr("cy", y)
          .attr("r", 3.5)
          .attr("fill", color)
          .attr("stroke", "rgba(0,0,0,0.35)")
          .attr("stroke-width", 0.8)
          .style("cursor", "pointer")
          .on("mousemove", (event) => showSpiderTip(event, SPIDER_AXES[i], labelA, labelB, valsA, valsB, top5, league))
          .on("mouseleave", hideTip);
      });
    }
    poly(valsA, COLOR_A, 0.22);
    poly(valsB, COLOR_B, 0.18);

    // Invisible hit targets on each axis tip for easier hover
    SPIDER_AXES.forEach((axis, i) => {
      const [hx, hy] = polarPoint(cx, cy, radius + 4, angle(i));
      svg
        .append("circle")
        .attr("cx", hx)
        .attr("cy", hy)
        .attr("r", 16)
        .attr("fill", "transparent")
        .style("cursor", "pointer")
        .on("mousemove", (event) => showSpiderTip(event, axis, labelA, labelB, valsA, valsB, top5, league))
        .on("mouseleave", hideTip);
    });

    const legendY = 14;
    [
      [12, COLOR_A, labelA],
      [width / 2 + 4, COLOR_B, labelB],
    ].forEach(([x, color, label]) => {
      const gLeg = svg.append("g");
      gLeg.append("circle").attr("cx", x).attr("cy", legendY).attr("r", 5).attr("fill", color);
      gLeg
        .append("text")
        .attr("x", x + 10)
        .attr("y", legendY + 1)
        .attr("dominant-baseline", "middle")
        .attr("fill", "#e8f0ec")
        .attr("font-size", 11)
        .attr("font-weight", 700)
        .attr("font-family", "Roboto, sans-serif")
        .text(label);
    });

    const table = document.createElement("table");
    table.className = "side-radar-table";
    table.innerHTML = `
      <thead>
        <tr>
          <th></th>
          ${SPIDER_AXES.map((a) => `<th>${a.label}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        <tr class="side-radar-row-a">
          <th scope="row"><i style="background:${COLOR_A}"></i>${escapeHtml(labelA)}</th>
          ${SPIDER_AXES.map((a) => `<td>${fmtSpider(a, valsA[a.key])}</td>`).join("")}
        </tr>
        <tr class="side-radar-row-b">
          <th scope="row"><i style="background:${COLOR_B}"></i>${escapeHtml(labelB)}</th>
          ${SPIDER_AXES.map((a) => `<td>${fmtSpider(a, valsB[a.key])}</td>`).join("")}
        </tr>
      </tbody>`;
    table.querySelectorAll("thead th").forEach((th, i) => {
      if (i === 0) return;
      const axis = SPIDER_AXES[i - 1];
      th.style.cursor = "pointer";
      th.addEventListener("mousemove", (event) =>
        showSpiderTip(event, axis, labelA, labelB, valsA, valsB, top5, league)
      );
      th.addEventListener("mouseleave", hideTip);
    });
    table.querySelectorAll("tbody td").forEach((td, idx) => {
      const axis = SPIDER_AXES[idx % SPIDER_AXES.length];
      td.style.cursor = "pointer";
      td.addEventListener("mousemove", (event) =>
        showSpiderTip(event, axis, labelA, labelB, valsA, valsB, top5, league)
      );
      td.addEventListener("mouseleave", hideTip);
    });
    els.radar.appendChild(table);
  }

  function renderTable() {
    if (!els.chart) return;
    const teams = sortedTeams(teamRows());
    const unit = state.metric === "xg" ? "xG" : "shots";
    const sortBy = state.sortMode === "pct" ? "%" : "value";
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · ${teams.length} teams · ${unit} with % · sort by ${sortBy} (Understat Y thirds: low=Right, mid=Center, high=Left)`;
    if (!teams.length) {
      els.chart.innerHTML = `<p class="empty">No side-channel rows for this filter.</p>`;
      populateTeamSelects([]);
      renderPitches();
      renderSpider();
      return;
    }
    els.chart.innerHTML = `
      <table class="side-ch-table data-table">
        <thead>
          <tr>
            ${th("team", "Team")}
            <th>Attack mix</th>
            ${th("L", "L")}${th("C", "C")}${th("R", "R")}
            <th>Defence mix</th>
            ${th("L-A", "L-A")}${th("C-A", "C-A")}${th("R-A", "R-A")}
          </tr>
        </thead>
        <tbody>
          ${teams
            .map(
              (t) => `<tr>
              <td>${t.team_short}</td>
              <td>${barHtml(t.forShare)}</td>
              <td>${cellHtml(t.for.Left, t.forShare.Left)}</td>
              <td>${cellHtml(t.for.Center, t.forShare.Center)}</td>
              <td>${cellHtml(t.for.Right, t.forShare.Right)}</td>
              <td>${barHtml(t.againstShare)}</td>
              <td>${cellHtml(t.against.Left, t.againstShare.Left)}</td>
              <td>${cellHtml(t.against.Center, t.againstShare.Center)}</td>
              <td>${cellHtml(t.against.Right, t.againstShare.Right)}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
      <p class="footnote">Cells show value (% of that team’s attack or defence total). Use “Sort columns by” for value vs %. Attack = shots taken; Defence (-A) = conceded.</p>
    `;
    bindSortHeaders();
    populateTeamSelects(teams);
    renderPitches();
    renderSpider();
  }

  function render() {
    renderTable();
  }

  window.initTeamSides = init;
})();
