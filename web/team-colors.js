/* Shared club pastel palette for the Understat and FPL treemaps. */
(() => {
  /** Soft pastel palette from design swatch (16). */
  const PALETTE = [
    "#fff699",
    "#fee8c3",
    "#ffcfa1",
    "#fbaea6",
    "#e9ed98",
    "#b6eea7",
    "#a6f5d8",
    "#b7e7f3",
    "#a1c4fc",
    "#d5bcfe",
    "#ffbdfb",
    "#feb9cc",
    "#bcaea1",
    "#d2c09a",
    "#dddddd",
    "#66747f",
  ];

  /** Preferred pastel index per club so neighbours stay distinct. */
  const TEAM_COLOR_INDEX = {
    ARS: 3,
    AVL: 8,
    BHA: 7,
    BOU: 2,
    BRE: 11,
    BUR: 12,
    CHE: 5,
    COV: 6,
    CRY: 9,
    EVE: 1,
    FUL: 14,
    HUL: 13,
    IPS: 4,
    LEE: 14,
    LIV: 10,
    MCI: 7,
    MUN: 3,
    NEW: 15,
    NFO: 11,
    SUN: 2,
    TOT: 14,
    WHU: 12,
    WOL: 0,
  };

  function teamColor(short) {
    if (TEAM_COLOR_INDEX[short] != null) return PALETTE[TEAM_COLOR_INDEX[short] % PALETTE.length];
    // stable fallback from short code
    let h = 0;
    const s = String(short || "");
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return PALETTE[h % PALETTE.length];
  }

  function hexToRgb(hex) {
    const h = hex.replace("#", "");
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }

  function teamFill(short, alpha = 1) {
    const [r, g, b] = hexToRgb(teamColor(short));
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  /** Jersey-like fills for scatter bubbles — reds/blues kept distinct across clubs. */
  const KIT = {
    ARS: "#E31B23",
    AVL: "#670E36",
    BHA: "#0057B8",
    BOU: "#DA291C",
    BRE: "#E30613",
    BUR: "#6C1D45",
    CHE: "#034694",
    CRY: "#1B458F",
    EVE: "#003399",
    FUL: "#000000",
    IPS: "#0033A0",
    LEE: "#FFCD00",
    LIV: "#C8102E",
    MCI: "#6CABDD",
    MUN: "#DA291C",
    NEW: "#241F20",
    NFO: "#DD0000",
    SUN: "#EB172B",
    TOT: "#132257",
    WHU: "#7A263A",
    WOL: "#FDB913",
    // slight offset for BOU vs MUN both #DA291C — BOU shifts warmer
  };
  // Differentiate same-family reds / dark blues
  KIT.BOU = "#B50A1F";
  KIT.BRE = "#D2000F";
  KIT.NFO = "#9B0000";
  KIT.SUN = "#F73B3B";
  KIT.MUN = "#DA291C";
  KIT.ARS = "#EF0107";
  KIT.LIV = "#C8102E";

  function teamKit(short) {
    const s = String(short || "");
    if (KIT[s]) return KIT[s];
    return teamColor(s);
  }

  function teamKitFill(short, alpha = 1) {
    const [r, g, b] = hexToRgb(teamKit(short));
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  function textOnTeam(short) {
    const [r, g, b] = hexToRgb(teamColor(short));
    const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    // Darker ink on pastels; pale ink on slate clubs (e.g. NEW).
    return lum > 0.58 ? "#0b0f0e" : "#f4fff8";
  }

  window.TeamColors = {
    PALETTE,
    TEAM_COLOR_INDEX,
    KIT,
    teamColor,
    teamKit,
    hexToRgb,
    teamFill,
    teamKitFill,
    textOnTeam,
  };
})();
