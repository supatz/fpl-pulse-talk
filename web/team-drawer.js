/* Gameweek drawer for Teams table rows. */
import { METRICS } from "./registry.js";
import { fmt, gwRangeSlice, lastGwSlice } from "./components.js";

const SKIP = new Set(["team", "apps"]);
const SUM_RAW = [
  ["G", "goals_for"],
  ["G-A", "goals_against"],
  ["xG", "xg"],
  ["xG-A", "xga"],
  ["Sh", "shots"],
  ["Sh-A", "shots_conceded"],
  ["SoT", "shots_on_target"],
  ["SoT-A", "sot_conceded"],
  ["CC", "CC"],
  ["CC-A", "CC_A"],
  ["BCC", "big_chances"],
  ["BCC-A", "big_chances_conceded"],
  ["Pts", "points"],
];

function $(id) {
  return document.getElementById(id);
}

function num(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

export function openTeamDrawer(team, ctx) {
  const drawer = $("player-drawer");
  const body = $("player-drawer-body");
  const title = $("player-drawer-title");
  const meta = $("player-drawer-meta");
  if (!drawer || !body || !team) return;

  const matches = typeof ctx.matches === "function" ? ctx.matches() : ctx.matches || [];
  const state = ctx.state || {};
  const metricKeys = (ctx.columns || []).filter((key) => !SKIP.has(key));
  const keys = ["gw", "opp", "venue", ...metricKeys];
  const rows = teamGwRows(matches, team, state);

  title.textContent = team.team || "Team";
  const from = rows[0]?.gw_from ?? state.gwFrom;
  const to = rows[0]?.gw_to ?? state.gwTo;
  meta.textContent = [from && to ? `GW ${from}–${to}` : "", `${rows.length} matches`].filter(Boolean).join(" · ");

  const totals = { gw: "Total", opp: "", venue: "" };
  for (const key of metricKeys) totals[key] = 0;
  let any = Object.fromEntries(metricKeys.map((k) => [k, false]));
  for (const row of rows) {
    for (const key of metricKeys) {
      if (key === "Poss") continue;
      if (row[key] != null) {
        totals[key] += num(row[key]);
        any[key] = true;
      }
    }
  }
  if (metricKeys.includes("Poss")) {
    const vals = rows.map((r) => r.Poss).filter((v) => v != null);
    totals.Poss = vals.length ? vals.reduce((a, b) => a + Number(b), 0) / vals.length : null;
    any.Poss = vals.length > 0;
  }
  if (metricKeys.includes("CS")) {
    totals.CS = rows.reduce((a, r) => a + (r.CS ? 1 : 0), 0);
    any.CS = true;
  }
  for (const key of metricKeys) {
    if (!any[key]) totals[key] = null;
  }

  body.innerHTML = `
    <div class="player-drawer-scroll">
      <table class="data-table player-gw-table">
        <thead><tr>${keys.map((key) => `<th>${header(key)}</th>`).join("")}</tr></thead>
        <tbody>
          ${
            rows
              .map((row) => `<tr>${keys.map((key) => `<td>${cell(row, key)}</td>`).join("")}</tr>`)
              .join("") || `<tr><td colspan="${keys.length}">No matches in this window.</td></tr>`
          }
        </tbody>
        <tfoot>
          <tr class="is-total">${keys.map((key) => `<td>${cell(totals, key)}</td>`).join("")}</tr>
        </tfoot>
      </table>
    </div>
    <p class="player-drawer-note">One row per gameweek match. Against metrics use the -A suffix (e.g. SoT-A = shots on target conceded).</p>
  `;
  drawer.hidden = false;
  const scrim = $("player-drawer-scrim");
  if (scrim) scrim.hidden = false;
}

function header(key) {
  if (key === "gw") return "GW";
  if (key === "opp") return "Opp";
  if (key === "venue") return "V";
  return (METRICS[key] || { label: key }).label;
}

function cell(row, key) {
  if (key === "gw") return row.gw ?? "—";
  if (key === "opp") return row.opp || "—";
  if (key === "venue") return row.venue || "—";
  if (key === "CS") {
    if (row.gw === "Total") return fmt(row.CS, "int");
    return row.CS ? "1" : "0";
  }
  const m = METRICS[key] || { fmt: "2dp" };
  return fmt(row[key], m.fmt);
}

function teamGwRows(matches, team, state) {
  const code = Number(team.team_code);
  const filtered = (matches || []).filter((r) => {
    if (!r.finished) return false;
    if (Number(r.team_code) !== code) return false;
    if (state.seasons?.length && !state.seasons.includes(r.season)) return false;
    if (state.competitions?.length && !state.competitions.includes(r.competition)) return false;
    const venue = r.is_home === true ? "H" : r.is_home === false ? "A" : null;
    if (venue && state.venues?.length && !state.venues.includes(venue)) return false;
    return true;
  });
  const sliced =
    state.gwFrom != null && state.gwTo != null
      ? gwRangeSlice(filtered, state.gwFrom, state.gwTo)
      : lastGwSlice(filtered, 5);
  return sliced.rows
    .slice()
    .sort((a, b) => (a.gw || 0) - (b.gw || 0))
    .map((r) => {
      const row = {
        gw: r.gw,
        gw_from: sliced.from,
        gw_to: sliced.to,
        opp: r.opp || "—",
        venue: r.is_home === true ? "H" : r.is_home === false ? "A" : "—",
        Poss: r.possession,
        CS: Boolean(r.clean_sheet),
      };
      for (const [key, src] of SUM_RAW) {
        row[key] = r[src] != null ? Number(r[src]) : null;
      }
      return row;
    });
}
