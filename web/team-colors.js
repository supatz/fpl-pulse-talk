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

  function textOnTeam(short) {
    const [r, g, b] = hexToRgb(teamColor(short));
    const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return lum > 0.58 ? "#1a2420" : "#f4fff8";
  }

  window.TeamColors = { PALETTE, TEAM_COLOR_INDEX, teamColor, hexToRgb, teamFill, textOnTeam };
})();
