/* Gameweek drawer for Attackers / Defenders / GK player names. */
import { METRICS } from "./registry.js";
import { filterMatches, fmt, gwRangeSlice, lastGwSlice } from "./components.js";

const SKIP = new Set(["player", "team", "pos", "Cost", "apps"]);
const SUM = [
  "G", "A", "PenG", "xG", "xA", "xGI", "Sh", "SoT", "CC", "TiB", "BCM", "xGOT",
  "Sv", "Saves", "GC", "xGOTf", "xGP", "Tkl", "CBI", "DefCon", "npxG", "F3", "Dr", "YC",
  "Aer", "Clr", "Int", "Blk", "Rec", "SiB", "HC", "SW", "Cr", "SPxG", "PS",
  "USMin", "USxG", "USxA", "USnpxG", "USxGC", "USxGB", "USSh", "USKP", "BCC", "BCT", "BCS", "BCM",
];

let bound = false;

function $(id) {
  return document.getElementById(id);
}

function num(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

export function bindPlayerDrawer() {
  if (bound) return;
  bound = true;
  $("player-drawer-close")?.addEventListener("click", closePlayerDrawer);
  $("player-drawer-scrim")?.addEventListener("click", closePlayerDrawer);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("player-drawer")?.hidden) closePlayerDrawer();
  });
}

export function closePlayerDrawer() {
  const drawer = $("player-drawer");
  const scrim = $("player-drawer-scrim");
  if (drawer) drawer.hidden = true;
  if (scrim) scrim.hidden = true;
}

export function openPlayerDrawer(player, ctx) {
  bindPlayerDrawer();
  const drawer = $("player-drawer");
  const body = $("player-drawer-body");
  const title = $("player-drawer-title");
  const meta = $("player-drawer-meta");
  if (!drawer || !body || !player) return;

  const matches = typeof ctx.matches === "function" ? ctx.matches() : ctx.matches || [];
  const state = ctx.state || {};
  const cfg = ctx.cfg || {};
  const metricKeys = (ctx.columns || []).filter((key) => !SKIP.has(key));
  const keys = ["gw", "opp", "venue", "mins", ...metricKeys.filter((k) => k !== "mins")];
  const rows = playerGwRows(matches, player, state);

  title.textContent = `${player.player || "Player"} · ${player.team || ""}`;
  const from = rows[0]?.gw_from ?? state.gwFrom;
  const to = rows[0]?.gw_to ?? state.gwTo;
  const range = from && to ? `GW ${from}–${to}` : "";
  meta.textContent = [player.pos, range, player.Cost != null ? `£${Number(player.Cost).toFixed(1)}m` : ""]
    .filter(Boolean)
    .join(" · ");

  const totals = { gw: "Total", opp: "", venue: "", mins: 0 };
  for (const key of metricKeys) totals[key] = 0;
  let any = Object.fromEntries(metricKeys.map((k) => [k, false]));
  for (const row of rows) {
    totals.mins += num(row.mins);
    for (const key of metricKeys) {
      if (row[key] != null) {
        totals[key] += num(row[key]);
        any[key] = true;
      }
    }
  }
  for (const key of metricKeys) {
    if (!any[key]) totals[key] = null;
  }

  const per90 = { gw: "Per 90", opp: "", venue: "", mins: totals.mins || null };
  const per90Keys = new Set([...(cfg.per90Keys || []), ...(cfg.always90Keys || [])]);
  for (const key of metricKeys) {
    if (!per90Keys.has(key) || totals[key] == null || !totals.mins) per90[key] = null;
    else per90[key] = (num(totals[key]) * 90) / totals.mins;
  }

  body.innerHTML = `
    <div class="player-drawer-scroll">
      <table class="data-table player-gw-table">
        <thead><tr>${keys.map((key) => `<th>${header(key, cfg)}</th>`).join("")}</tr></thead>
        <tbody>
          ${
            rows
              .map((row) => `<tr>${keys.map((key) => `<td>${cell(row, key)}</td>`).join("")}</tr>`)
              .join("") || `<tr><td colspan="${keys.length}">No appearances in this window.</td></tr>`
          }
        </tbody>
        <tfoot>
          <tr class="is-total">${keys.map((key) => `<td>${cell(totals, key)}</td>`).join("")}</tr>
          <tr class="is-per90">${keys.map((key) => `<td>${cell(per90, key, true)}</td>`).join("")}</tr>
        </tfoot>
      </table>
    </div>
    <p class="player-drawer-note">Gameweek rows are totals. Per 90 uses the window minutes. FPL points and clean sheets are one figure per GW (not per match on a DGW).</p>
  `;
  drawer.hidden = false;
  const scrim = $("player-drawer-scrim");
  if (scrim) scrim.hidden = false;
}

function header(key, cfg) {
  if (key === "gw") return "GW";
  if (key === "opp") return "Opp";
  if (key === "venue") return "V";
  if (key === "mins") return "Min";
  const m = METRICS[key] || { label: key };
  if ((cfg.always90Keys || []).includes(key)) return m.label.replace(/\/90$/, "");
  return m.label;
}

function cell(row, key, as90 = false) {
  if (key === "gw") return row.gw ?? "—";
  if (key === "opp") return row.opp || "—";
  if (key === "venue") return row.venue || "—";
  if (key === "mins") return fmt(row.mins, "int");
  const m = METRICS[key] || { fmt: "2dp" };
  const kind = as90 && (m.fmt === "int" || m.fmt === "1dp") ? "2dp" : m.fmt;
  return fmt(row[key], kind);
}

function playerGwRows(matches, player, state) {
  const id = String(player.pc ?? player.pid);
  const filtered = filterMatches(matches, { ...state, players: [id] });
  const sliced =
    state.gwFrom != null && state.gwTo != null
      ? gwRangeSlice(filtered, state.gwFrom, state.gwTo)
      : lastGwSlice(filtered, 5);
  const byGw = new Map();
  for (const r of sliced.rows) {
    if (r.gw == null) continue;
    if (!byGw.has(r.gw)) byGw.set(r.gw, []);
    byGw.get(r.gw).push(r);
  }
  const rows = [];
  for (const [gw, list] of [...byGw.entries()].sort((a, b) => a[0] - b[0])) {
    const apps = list.filter((r) => r.m > 0);
    if (!apps.length) continue;
    const row = {
      gw,
      gw_from: sliced.from,
      gw_to: sliced.to,
      opp: [...new Set(apps.map((r) => r.opp).filter(Boolean))].join("+") || "—",
      venue: [...new Set(apps.map((r) => (r.h === true ? "H" : r.h === false ? "A" : null)).filter(Boolean))].join("+"),
      mins: apps.reduce((a, r) => a + num(r.m), 0),
    };
    for (const f of SUM) {
      const vals = list.map((r) => (f === "Saves" ? r.Sv ?? r.Saves : r[f])).filter((v) => v != null);
      row[f] = vals.length ? vals.reduce((a, b) => a + Number(b), 0) : null;
    }
    row.Saves = row.Saves ?? row.Sv;
    const first = (field) => {
      for (const r of list) {
        if (r[field] != null) return Number(r[field]);
      }
      return null;
    };
    row.Pts = first("pts");
    row.CS = first("cs");
    row.Bon = first("Bon");
    row.BPS = first("BPS");
    rows.push(row);
  }
  return rows;
}
