/* FPL-Core player treemap: primary metric sizes tiles; paired metric adds context. */
(() => {
  const DATA_URL = "./data/players_matches.json";
  const TOP_PLAYERS_PER_TEAM = 6;
  const TOP_TEAMS = 10;
  const HEADER_H = 42;
  const MIN_FONT = 5;
  const BC_KEYS = ["BCC", "BCT", "BCS", "BCM"];
  const METRICS = {
    G: {
      name: "Goals",
      keys: ["G", "SoT", "xG", "npxG", ...BC_KEYS],
      show: ["G", "xG"],
      extra: ["SoT", "npxG", ...BC_KEYS],
      lines: [["G"], ["xG"]],
    },
    A: {
      name: "Assists",
      keys: ["A", "CC", ...BC_KEYS],
      show: ["A", "CC"],
      extra: [...BC_KEYS],
      lines: [["A"], ["CC"]],
    },
    xGI: {
      name: "Expected goal involvements",
      keys: ["xGI", "xG", ...BC_KEYS],
      show: ["xGI", "xG"],
      extra: [...BC_KEYS],
      lines: [["xGI"], ["xG"]],
    },
    DefCon: {
      name: "Defensive contributions",
      keys: ["DefCon", "CS", ...BC_KEYS],
      show: ["DefCon", "CS"],
      extra: [...BC_KEYS],
      lines: [["DefCon"], ["CS"]],
    },
    BigChance: {
      name: "Big chances",
      keys: [...BC_KEYS],
      show: ["BCT", "BCS", "BCM"],
      extra: ["BCC"],
      lines: [["BCT"], ["BCS", "BCM"]],
    },
  };
  const FIELDS = {
    G: { label: "G", name: "Goals", digits: 0 },
    SoT: { label: "SoT", name: "Shots on target", digits: 0 },
    xG: { label: "xG", name: "Expected goals", digits: 2 },
    npxG: { label: "npxG", name: "Non-penalty expected goals", short: "Non-penalty xG", digits: 2 },
    A: { label: "A", name: "Assists", digits: 0 },
    CC: { label: "CC", name: "Chances created", digits: 0 },
    xGI: { label: "xGI", name: "Expected goal involvements", short: "Expected involvement", digits: 2 },
    DefCon: { label: "DC", name: "Defensive contributions", digits: 0 },
    CS: { label: "CS", name: "Clean sheets", digits: 0 },
    BCC: { label: "BCC", name: "Big chances created", short: "Big chance created (US)", digits: 0 },
    BCT: { label: "BCT", name: "Big chances taken", short: "Big chance taken (US)", digits: 0 },
    BCS: { label: "BCS", name: "Big chances scored", short: "Big chance scored (US)", digits: 0 },
    BCM: { label: "BCM", name: "Big chances missed", short: "Big chance missed (US)", digits: 0 },
  };
  const { teamFill, textOnTeam } = window.TeamColors;
  const TILE_FONT = "Roboto, Helvetica Neue, Segoe UI, sans-serif";

  const state = {
    rows: [],
    season: null,
    metric: "G",
    sortMetric: "G",
    position: "ALL",
    gwFrom: 1,
    gwTo: 38,
    teams: new Set(),
    teamMode: "preset",
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
      populateSortOptions();
      applyTeamMode();
    } catch (err) {
      els.status.textContent = `Failed to load FPL player data: ${err.message}`;
    }
  }

  function bindEls() {
    els.root = $("fpl-map-root");
    els.season = $("fpl-map-season");
    els.metric = $("fpl-map-metric");
    els.sort = $("fpl-map-sort");
    els.position = $("fpl-map-position");
    els.gwRange = $("fpl-map-gw-range");
    els.gwLabel = $("fpl-map-gw-label");
    els.gwControl = null;
    els.status = $("fpl-map-status");
    els.chart = $("fpl-map-chart");
    els.tip = $("fpl-map-tip");
    els.teamPills = $("fpl-map-team-pills");
    els.topTeams = $("fpl-map-top-teams");
    els.allTeams = $("fpl-map-all-teams");
    els.chartDl = $("fpl-map-chart-dl");
  }

  function bindEvents() {
    els.season.addEventListener("change", () => {
      state.season = els.season.value;
      syncGwBounds(true);
      if (state.teamMode === "custom") {
        populateTeams();
        render();
      } else applyTeamMode();
    });
    els.metric.addEventListener("change", () => {
      state.metric = els.metric.value;
      populateSortOptions();
      state.teamMode = "preset";
      applyTeamMode();
    });
    els.sort.addEventListener("change", () => {
      state.sortMetric = els.sort.value;
      if (state.teamMode === "all") render();
      else {
        state.teamMode = "preset";
        applyTeamMode();
      }
    });
    els.position.addEventListener("change", () => {
      state.position = els.position.value;
      state.teamMode = "preset";
      applyTeamMode();
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
          if (state.teamMode === "custom") {
            populateTeams();
            render();
          } else applyTeamMode();
        },
      });
    }
    els.topTeams.addEventListener("click", () => {
      state.teamMode = "preset";
      applyTeamMode();
    });
    els.allTeams.addEventListener("click", () => {
      state.teamMode = "all";
      applyTeamMode();
    });
    if (els.chartDl && window.ChartExport && !els.chartDl.dataset.bound) {
      els.chartDl.dataset.bound = "1";
      window.ChartExport.bindChartDownload(
        els.chartDl,
        () => els.chart,
        () => `fpl-pulse-talk-treemap-${state.metric || "chart"}`,
        exportCaption
      );
    }
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!$("page-insights-fpl-treemap")?.hidden) render();
      }, 120);
    });
  }

  function exportCaption() {
    const group = METRICS[state.metric] || METRICS.G;
    const titles = {
      G: "Who's scoring — and are the chances deserved?",
      A: "Who's creating the chances and assists?",
      xGI: "Who's involved in the best chances?",
      DefCon: "Who's putting in the defensive work?",
      BigChance: "Who's taking, scoring, or missing the big chances?",
    };
    const gloss = [];
    for (const key of group.show || []) {
      const f = FIELDS[key];
      if (f) gloss.push(`${f.label} = ${f.name}`);
    }
    const sortField = FIELDS[state.sortMetric];
    if (sortField) gloss.push(`Tile size = ${sortField.name}`);
    const pos =
      state.position === "ALL"
        ? "All positions"
        : state.position === "ATT"
          ? "Forwards"
          : state.position === "MID"
            ? "Midfielders"
            : state.position === "DEF"
              ? "Defenders"
              : state.position === "GK"
                ? "Goalkeepers"
                : state.position;
    return {
      title: titles[state.metric] || group.name,
      metrics: gloss.join(" · "),
      meta: [state.season, `GW ${state.gwFrom}–${state.gwTo}`, pos].filter(Boolean).join(" · "),
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

  function positionMatches(position) {
    if (state.position === "ALL") return true;
    if (state.position === "MID") return position === "Midfielder";
    if (state.position === "ATT") return position === "Forward";
    return position === "Defender" || position === "Goalkeeper";
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

  function populateSortOptions() {
    const keys = METRICS[state.metric].keys;
    if (!keys.includes(state.sortMetric)) state.sortMetric = keys[0];
    els.sort.replaceChildren(
      ...keys.map((key) => {
        const option = document.createElement("option");
        option.value = key;
        option.textContent = `${FIELDS[key].label} — ${FIELDS[key].short || FIELDS[key].name}`;
        option.selected = key === state.sortMetric;
        return option;
      })
    );
  }

  function teamTotals(players) {
    const totals = new Map();
    for (const player of players) {
      const code = String(player.team_code);
      if (!totals.has(code)) totals.set(code, { code, short: player.team_short, value: 0 });
      totals.get(code).value += player[state.sortMetric] || 0;
    }
    return [...totals.values()].sort((a, b) => b.value - a.value || a.short.localeCompare(b.short));
  }

  function presetTeamCodes() {
    return teamTotals(aggregate())
      .filter((team) => team.value > 0)
      .slice(0, TOP_TEAMS)
      .map((team) => team.code);
  }

  function applyTeamMode() {
    const all = teamTotals(aggregate());
    state.teams =
      state.teamMode === "all"
        ? new Set(all.map((team) => team.code))
        : new Set(presetTeamCodes());
    populateTeams();
    render();
  }

  function populateTeams() {
    const teams = teamTotals(aggregate()).sort((a, b) => a.short.localeCompare(b.short));
    const preset = new Set(presetTeamCodes());
    els.teamPills.replaceChildren(
      ...teams.map((team) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `fpl-map-pill${state.teams.has(team.code) ? " on" : ""}${preset.has(team.code) ? " is-top" : ""}`;
        button.dataset.code = team.code;
        button.textContent = team.short;
        button.title = `${team.short}: ${FIELDS[state.sortMetric].label} ${format(team.value, fieldDigits(state.sortMetric))}`;
        button.addEventListener("click", () => {
          state.teamMode = "custom";
          if (state.teams.has(team.code)) state.teams.delete(team.code);
          else state.teams.add(team.code);
          populateTeams();
          render();
        });
        return button;
      })
    );
    els.topTeams.classList.toggle("on", state.teamMode === "preset");
    els.allTeams.classList.toggle("on", state.teamMode === "all");
  }

  function num(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function aggregate() {
    const rows = seasonRows().filter(
      (r) =>
        Number(r.gw) >= state.gwFrom &&
        Number(r.gw) <= state.gwTo &&
        num(r.m) > 0 &&
        positionMatches(r.pos)
    );
    const players = new Map();
    for (const r of rows) {
      const teamCode = String(r.tc);
      const key = `${teamCode}|${r.pc || r.pid}`;
      if (!players.has(key)) {
        players.set(key, {
          player_code: r.pc,
          player_name: r.n,
          team_code: teamCode,
          team_short: r.tm || "—",
          position: r.pos,
          apps: 0,
          minutes: 0,
          G: 0,
          A: 0,
          xGI: 0,
          xG: 0,
          npxG: 0,
          SoT: 0,
          CC: 0,
          DefCon: 0,
          BCC: 0,
          BCT: 0,
          BCS: 0,
          BCM: 0,
          csByGw: new Map(),
        });
      }
      const p = players.get(key);
      p.apps += 1;
      p.minutes += num(r.m);
      for (const metric of ["G", "A", "xGI", "xG", "npxG", "SoT", "CC", "DefCon", "BCC", "BCT", "BCS", "BCM"]) {
        p[metric] += num(r[metric]);
      }
      if (r.cs != null && !p.csByGw.has(r.gw)) p.csByGw.set(r.gw, num(r.cs));
    }
    for (const p of players.values()) {
      p.CS = [...p.csByGw.values()].reduce((sum, value) => sum + value, 0);
      delete p.csByGw;
    }
    return [...players.values()];
  }

  function render() {
    if (!state.rows.length || !els.chart?.clientWidth) return;
    const metric = METRICS[state.metric];
    const sortKey = state.sortMetric;
    const players = aggregate().filter((p) => state.teams.has(String(p.team_code)));
    const byTeam = new Map();
    for (const player of players) {
      if (!byTeam.has(player.team_code)) {
        byTeam.set(player.team_code, {
          team_code: player.team_code,
          team_short: player.team_short,
          players: [],
        });
      }
      byTeam.get(player.team_code).players.push(player);
    }
    const teams = [...byTeam.values()]
      .map((team) => {
        team.totals = Object.fromEntries(
          metric.keys.map((key) => [key, team.players.reduce((sum, player) => sum + (player[key] || 0), 0)])
        );
        team.sortTotal = team.players.reduce((sum, player) => sum + (player[sortKey] || 0), 0);
        team.players = team.players
          .filter((player) => player[sortKey] > 0)
          .sort((a, b) => b[sortKey] - a[sortKey])
          .slice(0, TOP_PLAYERS_PER_TEAM);
        return team;
      })
      .filter((team) => team.players.length)
      .sort((a, b) => b.sortTotal - a.sortTotal);

    const mode = state.teamMode === "preset" ? "top 10 teams" : state.teamMode === "all" ? "all teams" : "custom teams";
    const position = els.position.options[els.position.selectedIndex]?.textContent || "All positions";
    const srcNote = BC_KEYS.includes(sortKey) || state.metric === "BigChance" ? "FPL + Understat big chances" : "FPL-Core";
    els.status.textContent = `${state.season} · GW ${state.gwFrom}–${state.gwTo} · ${position} · ${teams.length} teams (${mode}) · team and tile area follow ${FIELDS[sortKey].label} · top ${TOP_PLAYERS_PER_TEAM} positive players per team · ${srcNote}`;

    const width = els.chart.clientWidth || 1000;
    const height = els.chart.clientHeight || 640;
    els.chart.replaceChildren();
    const svg = d3.select(els.chart).append("svg").attr("viewBox", `0 0 ${width} ${height}`);
    if (!teams.length) {
      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .attr("fill", "#8fa59a")
        .text("No positive values for this metric and gameweek range.");
      return;
    }
    drawTreemap(svg, teams, metric, sortKey, width, height);
  }

  function drawTreemap(svg, teams, metric, sortKey, width, height) {
    // Teams are leaves of the outer map (players live under `players`, not `children`),
    // so each club's area follows its total of the sort metric.
    const root = d3
      .hierarchy({ children: teams })
      .sum((d) => Math.max(d.sortTotal || 0, 0.0001))
      .sort((a, b) => (b.value || 0) - (a.value || 0));
    d3.treemap().size([width, height]).paddingInner(6).paddingOuter(4).round(true)(root);

    const teamNodes = root.leaves();
    const tiles = [];
    for (const node of teamNodes) {
      const contentX0 = node.x0 + 3;
      const contentY0 = node.y0 + HEADER_H;
      const contentW = Math.max(1, node.x1 - node.x0 - 6);
      const contentH = Math.max(1, node.y1 - node.y0 - HEADER_H - 3);
      const inner = d3
        .hierarchy({ children: node.data.players })
        .sum((d) => Math.max(d[sortKey] || 0, 0.0001))
        .sort((a, b) => (b.value || 0) - (a.value || 0));
      d3.treemap().size([contentW, contentH]).paddingInner(2).paddingOuter(0).round(true)(inner);
      const teamMax = Math.max(...node.data.players.map((p) => p[sortKey] || 0), 0);
      for (const leaf of inner.leaves()) {
        tiles.push({
          data: leaf.data,
          team: node.data,
          teamMax,
          x0: contentX0 + leaf.x0,
          x1: contentX0 + leaf.x1,
          y0: contentY0 + leaf.y0,
          y1: contentY0 + leaf.y1,
        });
      }
    }

    const gTeams = svg.append("g");
    gTeams
      .selectAll("rect.fpl-map-shell")
      .data(teamNodes)
      .join("rect")
      .attr("class", "fpl-map-shell")
      .attr("x", (d) => d.x0)
      .attr("y", (d) => d.y0)
      .attr("width", (d) => Math.max(0, d.x1 - d.x0))
      .attr("height", (d) => Math.max(0, d.y1 - d.y0))
      .attr("rx", 14)
      .attr("fill", (d) => teamFill(d.data.team_short, 0.55))
      .on("mousemove", (event, d) => showTeamTip(event, d.data, metric))
      .on("mouseleave", hideTip);

    gTeams
      .selectAll("rect.fpl-map-band")
      .data(teamNodes.filter((d) => d.y1 - d.y0 > 40 && d.x1 - d.x0 > 56))
      .join("rect")
      .attr("class", "fpl-map-band")
      .attr("x", (d) => d.x0 + 3)
      .attr("y", (d) => d.y0 + 3)
      .attr("width", (d) => Math.max(0, d.x1 - d.x0 - 6))
      .attr("height", HEADER_H - 6)
      .attr("rx", 8)
      .attr("fill", (d) => teamFill(d.data.team_short, 0.78))
      .attr("pointer-events", "none");

    gTeams
      .selectAll("text.fpl-map-team-label")
      .data(teamNodes.filter((d) => d.x1 - d.x0 > 48))
      .join("text")
      .attr("class", "fpl-map-team-label")
      .attr("x", (d) => d.x0 + 12)
      .attr("y", (d) => d.y0 + 18)
      .attr("font-family", TILE_FONT)
      .attr("font-size", 13)
      .attr("font-weight", 600)
      .attr("fill", (d) => textOnTeam(d.data.team_short))
      .text((d) => d.data.team_short);

    gTeams
      .selectAll("text.fpl-map-team-sub")
      .data(teamNodes.filter((d) => d.x1 - d.x0 > 100 && d.y1 - d.y0 > 48))
      .join("text")
      .attr("class", "fpl-map-team-sub")
      .attr("x", (d) => d.x0 + 12)
      .attr("y", (d) => d.y0 + 34)
      .attr("font-family", TILE_FONT)
      .attr("font-size", 10)
      .attr("font-weight", 400)
      .attr("fill", (d) => textOnTeam(d.data.team_short))
      .text((d) =>
        tipKeys(metric, sortKey)
          .filter((key) => metric.show.includes(key) || key === sortKey)
          .map((key) => `${FIELDS[key].label} - ${format(d.data.totals[key], fieldDigits(key))}`)
          .join(" · ")
      );

    svg
      .append("g")
      .selectAll("g.fpl-map-tile")
      .data(tiles)
      .join("g")
      .attr("class", "fpl-map-tile")
      .attr("role", "img")
      .attr("aria-label", (d) => tileAria(d.data, metric))
      .each(function (d) {
        drawTile(d3.select(this), d, metric, sortKey);
      });
  }

  function tileLines(metric, sortKey) {
    const lines = metric.lines.map((keys) => [...keys]);
    const shown = new Set(lines.flat());
    // Always surface the Size / sort metric on the tile when it is not already paired.
    if (!shown.has(sortKey)) lines.unshift([sortKey]);
    return lines;
  }

  function tipKeys(metric, sortKey) {
    const keys = [...metric.show, ...metric.extra];
    if (!keys.includes(sortKey)) keys.unshift(sortKey);
    return keys;
  }

  function drawTile(g, tile, metric, sortKey) {
    const w = tile.x1 - tile.x0;
    const h = tile.y1 - tile.y0;
    const ink = textOnTeam(tile.team.team_short);
    const ratio = tile.teamMax > 0 ? (tile.data[sortKey] || 0) / tile.teamMax : 1;
    const lines = tileLines(metric, sortKey);

    g.append("rect")
      .attr("x", tile.x0)
      .attr("y", tile.y0)
      .attr("width", Math.max(0, w))
      .attr("height", Math.max(0, h))
      .attr("rx", 6)
      .attr("fill", teamFill(tile.team.team_short, 0.72 + ratio * 0.28))
      .on("mousemove", (event) => showTip(event, tile.data, metric, sortKey))
      .on("mouseleave", hideTip);

    // Name larger/medium weight; metric lines smaller and regular weight.
    const nameFs = Math.max(MIN_FONT + 1, Math.min(MIN_FONT + ratio * 12, w / 4.8, h / 2.8));
    const valFs = Math.max(MIN_FONT, Math.min(nameFs * 0.58, nameFs - 3));
    const cx = tile.x0 + w / 2;
    const showVals = h >= nameFs + valFs * Math.min(lines.length, 2) + 6 && w >= 24;
    g.append("text")
      .attr("class", "fpl-map-player-name")
      .attr("x", cx)
      .attr("y", showVals ? tile.y0 + h / 2 - valFs * 0.85 : tile.y0 + h / 2 + nameFs * 0.35)
      .attr("text-anchor", "middle")
      .attr("font-family", TILE_FONT)
      .attr("font-size", nameFs)
      .attr("font-weight", 500)
      .attr("fill", ink)
      .text(truncate(shortName(tile.data.player_name), Math.max(2, Math.floor(w / (nameFs * 0.55)))));
    if (!showVals) return;
    lines.slice(0, 3).forEach((keys, index) => {
      g.append("text")
        .attr("class", "fpl-map-player-val")
        .attr("x", cx)
        .attr("y", tile.y0 + h / 2 + valFs * (0.55 + index * 1.25))
        .attr("text-anchor", "middle")
        .attr("font-family", TILE_FONT)
        .attr("font-size", valFs)
        .attr("font-weight", 400)
        .attr("fill", ink)
        .attr("opacity", 0.92)
        .text(
          keys
            .map((key) => `${FIELDS[key].label} - ${format(tile.data[key], fieldDigits(key))}`)
            .join(" · ")
        );
    });
  }

  function showTip(event, player, metric, sortKey) {
    const metrics = tipKeys(metric, sortKey)
      .map((key) => `${FIELDS[key].name}: ${format(player[key], fieldDigits(key))}`)
      .join("<br>");
    els.tip.innerHTML = `<strong>${escapeHtml(player.player_name)} · ${escapeHtml(player.team_short)}</strong>
      ${metrics}<br>
      <span>${player.apps} apps · ${format(player.minutes, 0)} FPL/Opta minutes</span>`;
    placeTip(event);
  }

  function showTeamTip(event, team, metric) {
    const sortKey = state.sortMetric;
    const metrics = tipKeys(metric, sortKey)
      .map((key) => `${FIELDS[key].name}: ${format(team.totals[key], fieldDigits(key))}`)
      .join("<br>");
    els.tip.innerHTML = `<strong>${escapeHtml(team.team_short)}</strong><br>${metrics}`;
    placeTip(event);
  }

  function placeTip(event) {
    els.tip.hidden = false;
    els.tip.style.left = `${Math.min(window.innerWidth - 295, event.clientX + 14)}px`;
    els.tip.style.top = `${Math.min(window.innerHeight - 120, event.clientY + 14)}px`;
  }

  function hideTip() {
    els.tip.hidden = true;
  }

  function tileAria(player, metric) {
    return `${player.player_name}, ${[...metric.show, ...metric.extra]
      .map((key) => `${FIELDS[key].name} ${format(player[key], fieldDigits(key))}`)
      .join(", ")}`;
  }

  function fieldDigits(key) {
    return FIELDS[key]?.digits ?? 0;
  }

  function format(value, digits) {
    return Number(value || 0).toFixed(digits).replace(/\.00$/, "");
  }

  function shortName(name) {
    const parts = String(name || "—").trim().split(/\s+/);
    return parts.at(-1) || "—";
  }

  function truncate(value, max) {
    if (!value) return "";
    return value.length <= max ? value : `${value.slice(0, Math.max(1, max - 1))}…`;
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  window.initFplTreemap = init;
})();
