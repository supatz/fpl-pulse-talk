/* Download visible insight charts as PNG with caption header + FPL Pulse Talk footer. */
(() => {
  const HEADER_H = 54;
  const BANNER_H = 38;
  const BG = "#121820";
  const PAPER = "#1a2430";
  const INK = "#f4f7f6";
  const MUTED = "#9aafb8";
  const ACCENT = "#3ddc97";
  const HANDLE = "@fpl_pulse_talk";
  /** Export raster scale — high enough for crisp labels in downloads. */
  const EXPORT_SCALE = Math.max(3, Math.min(4, Math.round((window.devicePixelRatio || 2) + 1)));
  const SANS = '"Avenir Next", "Segoe UI", Roboto, ui-sans-serif, system-ui, sans-serif';
  const SERIF = '"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif';

  function basename(prefix) {
    const stamp = new Date().toISOString().slice(0, 10);
    return `${prefix || "fpl-pulse-talk"}-${stamp}.png`;
  }

  function triggerDownload(canvas, filename) {
    const a = document.createElement("a");
    a.download = filename;
    a.href = canvas.toDataURL("image/png");
    a.click();
  }

  function drawPulseMark(ctx, x, y, size) {
    const s = size / 48;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(s, s);
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    // Ring
    ctx.strokeStyle = ACCENT;
    ctx.lineWidth = 1.6;
    ctx.globalAlpha = 0.55;
    ctx.beginPath();
    ctx.arc(24, 24, 17.5, 0, Math.PI * 2);
    ctx.stroke();
    ctx.globalAlpha = 1;

    // Pulse (behind mic)
    ctx.strokeStyle = "#e9fffa";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(6.5, 24);
    ctx.lineTo(12.7, 24);
    ctx.lineTo(15, 15.8);
    ctx.lineTo(18.8, 32.6);
    ctx.lineTo(21.1, 24);
    ctx.lineTo(22.2, 24);
    ctx.moveTo(25.8, 24);
    ctx.lineTo(27.4, 24);
    ctx.lineTo(29.5, 17.2);
    ctx.lineTo(32.9, 30.8);
    ctx.lineTo(35, 24);
    ctx.lineTo(41.5, 24);
    ctx.stroke();

    // Vintage mint mic (option A)
    const ink = "#0a1612";
    const micGrad = ctx.createLinearGradient(18, 12, 30, 32);
    micGrad.addColorStop(0, "#7af5c4");
    micGrad.addColorStop(0.48, ACCENT);
    micGrad.addColorStop(1, "#1f9a68");
    const yokeGrad = ctx.createLinearGradient(16, 16, 32, 36);
    yokeGrad.addColorStop(0, "#5ee4b0");
    yokeGrad.addColorStop(1, "#2bb87a");

    // Base + neck
    ctx.fillStyle = yokeGrad;
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    ctx.ellipse(24, 37.2, 5.4, 1.7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(21.6, 33.2);
    ctx.lineTo(26.4, 33.2);
    ctx.lineTo(26.4, 36.4);
    ctx.quadraticCurveTo(26.4, 37.7, 24, 37.7);
    ctx.quadraticCurveTo(21.6, 37.7, 21.6, 36.4);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Yoke
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2.7;
    ctx.beginPath();
    ctx.moveTo(17.2, 15.6);
    ctx.lineTo(17.2, 25);
    ctx.arc(24, 25, 6.8, Math.PI, 0, true);
    ctx.lineTo(30.8, 15.6);
    ctx.stroke();
    ctx.strokeStyle = ACCENT;
    ctx.lineWidth = 1.55;
    ctx.beginPath();
    ctx.moveTo(17.2, 15.6);
    ctx.lineTo(17.2, 25);
    ctx.arc(24, 25, 6.8, Math.PI, 0, true);
    ctx.lineTo(30.8, 15.6);
    ctx.stroke();

    // Pivots
    ctx.fillStyle = micGrad;
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1.05;
    for (const px of [17.2, 30.8]) {
      ctx.beginPath();
      ctx.arc(px, 16.2, 1.35, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    // Capsule
    ctx.fillStyle = micGrad;
    ctx.lineWidth = 1.25;
    roundRectPath(ctx, 18.6, 10.4, 10.8, 18.4, 5.4);
    ctx.fill();
    ctx.stroke();

    // Grille
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1.35;
    ctx.globalAlpha = 0.92;
    ctx.beginPath();
    for (const gy of [14.2, 16.6, 19, 21.4]) {
      ctx.moveTo(21.1, gy);
      ctx.lineTo(26.9, gy);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
    ctx.restore();
  }

  function roundRectPath(ctx, x, y, w, h, r) {
    const rr = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + rr, y);
    ctx.arcTo(x + w, y, x + w, y + h, rr);
    ctx.arcTo(x + w, y + h, x, y + h, rr);
    ctx.arcTo(x, y + h, x, y, rr);
    ctx.arcTo(x, y, x + w, y, rr);
    ctx.closePath();
  }

  function drawXIcon(ctx, x, y, size) {
    ctx.save();
    ctx.translate(x, y);
    const s = size / 24;
    ctx.scale(s, s);
    ctx.fillStyle = INK;
    ctx.beginPath();
    // Compact X / Twitter mark
    ctx.moveTo(4, 4);
    ctx.lineTo(10.3, 12.4);
    ctx.lineTo(4.4, 20);
    ctx.lineTo(7, 20);
    ctx.lineTo(11.5, 14.2);
    ctx.lineTo(15.8, 20);
    ctx.lineTo(20, 20);
    ctx.lineTo(13.5, 11.3);
    ctx.lineTo(19.1, 4);
    ctx.lineTo(16.5, 4);
    ctx.lineTo(12.3, 9.5);
    ctx.lineTo(8.2, 4);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  function fitText(ctx, text, maxWidth) {
    const raw = String(text || "").trim();
    if (!raw) return "";
    if (ctx.measureText(raw).width <= maxWidth) return raw;
    const ell = "…";
    let lo = 0;
    let hi = raw.length;
    while (lo < hi) {
      const mid = Math.ceil((lo + hi) / 2);
      if (ctx.measureText(raw.slice(0, mid) + ell).width <= maxWidth) lo = mid;
      else hi = mid - 1;
    }
    return lo > 0 ? raw.slice(0, lo) + ell : ell;
  }

  /** Compact top strip: plain-English title + small metric glossary. */
  function drawCaptionBanner(ctx, width, y, caption) {
    const title = String(caption?.title || "").trim();
    const metrics = String(caption?.metrics || "").trim();
    const meta = String(caption?.meta || "").trim();
    if (!title && !metrics) return 0;

    ctx.fillStyle = PAPER;
    ctx.fillRect(0, y, width, HEADER_H);
    ctx.fillStyle = ACCENT;
    ctx.fillRect(0, y + HEADER_H - 1.5, width, 1.5);

    const pad = Math.max(12, Math.round(width * 0.02));
    const titleSize = Math.max(12, Math.min(15, width / 68));
    const metaSize = Math.max(9, Math.min(10.5, width / 100));
    const glossSize = Math.max(9, Math.min(11, width / 92));
    const titleY = y + 18;
    const glossY = y + 38;

    let rightReserve = pad;
    if (meta) {
      ctx.fillStyle = MUTED;
      ctx.font = `500 ${metaSize}px ${SANS}`;
      ctx.textBaseline = "middle";
      const metaText = fitText(ctx, meta, width * 0.34);
      const metaW = ctx.measureText(metaText).width;
      ctx.fillText(metaText, width - pad - metaW, titleY);
      rightReserve = pad + metaW + 14;
    }

    ctx.fillStyle = INK;
    ctx.font = `600 ${titleSize}px ${SERIF}`;
    ctx.textBaseline = "middle";
    ctx.fillText(fitText(ctx, title, width - pad - rightReserve), pad, titleY);

    if (metrics) {
      ctx.fillStyle = MUTED;
      ctx.font = `400 ${glossSize}px ${SANS}`;
      ctx.textBaseline = "middle";
      ctx.fillText(fitText(ctx, metrics, width - pad * 2), pad, glossY);
    }
    return HEADER_H;
  }

  function drawBrandBanner(ctx, width, y) {
    ctx.fillStyle = PAPER;
    ctx.fillRect(0, y, width, BANNER_H);
    ctx.fillStyle = ACCENT;
    ctx.fillRect(0, y, width, 1.5);

    const pad = Math.max(12, Math.round(width * 0.02));
    const mark = 22;
    drawPulseMark(ctx, pad, y + (BANNER_H - mark) / 2, mark);

    ctx.fillStyle = INK;
    ctx.font = `600 ${Math.max(11, Math.min(13, width / 70))}px ${SERIF}`;
    ctx.textBaseline = "middle";
    ctx.fillText("FPL PULSE TALK", pad + mark + 8, y + BANNER_H / 2);

    const right = width - pad;
    const handleSize = Math.max(10, Math.min(12, width / 80));
    ctx.fillStyle = MUTED;
    ctx.font = `500 ${handleSize}px ${SANS}`;
    const handleW = ctx.measureText(HANDLE).width;
    const icon = 12;
    const gap = 6;
    const blockW = icon + gap + handleW;
    drawXIcon(ctx, right - blockW, y + (BANNER_H - icon) / 2, icon);
    ctx.fillStyle = MUTED;
    ctx.textBaseline = "middle";
    ctx.fillText(HANDLE, right - handleW, y + BANNER_H / 2 + 0.5);
  }

  function svgPixelSize(svg) {
    const vb = (svg.getAttribute("viewBox") || "").trim().split(/[\s,]+/).map(Number);
    const wAttr = Number(svg.getAttribute("width"));
    const hAttr = Number(svg.getAttribute("height"));
    const vbW = vb.length === 4 && Number.isFinite(vb[2]) ? vb[2] : 0;
    const vbH = vb.length === 4 && Number.isFinite(vb[3]) ? vb[3] : 0;
    // Prefer the larger of display size and viewBox so exports are not soft.
    const w = Math.max(svg.clientWidth || 0, wAttr || 0, vbW, 1000);
    const h = Math.max(svg.clientHeight || 0, hAttr || 0, vbH, 640);
    return { width: Math.max(1, Math.round(w)), height: Math.max(1, Math.round(h)) };
  }

  function prepareSvgClone(svg, width, height, pixelWidth, pixelHeight) {
    const clone = svg.cloneNode(true);
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
    if (!clone.getAttribute("viewBox")) {
      clone.setAttribute("viewBox", `0 0 ${width} ${height}`);
    }
    // Rasterize at pixelWidth×pixelHeight while keeping logical viewBox — sharper text.
    clone.setAttribute("width", String(pixelWidth));
    clone.setAttribute("height", String(pixelHeight));
    const style = document.createElementNS("http://www.w3.org/2000/svg", "style");
    // Do not force fill on team/player labels — inline fills carry contrast colors.
    style.textContent = `
      .perf-grid .domain, .perf-grid line { stroke: #2d3d4a; }
      .perf-grid line { stroke-opacity: 0.45; }
      .perf-grid text, .perf-axis-title { fill: ${MUTED}; }
      .perf-parity { stroke: ${MUTED}; stroke-opacity: 0.5; }
      text {
        font-family: "Roboto", "Helvetica Neue", "Segoe UI", sans-serif;
        text-rendering: geometricPrecision;
      }
    `;
    clone.insertBefore(style, clone.firstChild);
    // Solid backdrop so transparent SVG does not become black/white noise.
    const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    bg.setAttribute("width", "100%");
    bg.setAttribute("height", "100%");
    bg.setAttribute("fill", BG);
    clone.insertBefore(bg, clone.firstChild);
    return clone;
  }

  function loadImage(url) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error("Failed to rasterize chart"));
      img.src = url;
    });
  }

  async function rasterizeSvg(svg) {
    const { width, height } = svgPixelSize(svg);
    const pixelW = Math.round(width * EXPORT_SCALE);
    const pixelH = Math.round(height * EXPORT_SCALE);
    const clone = prepareSvgClone(svg, width, height, pixelW, pixelH);
    const xml = new XMLSerializer().serializeToString(clone);
    const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;
    const img = await loadImage(url);
    return { img, width: pixelW, height: pixelH, logicalWidth: width, logicalHeight: height };
  }

  function collectPageCss() {
    const parts = [];
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) parts.push(rule.cssText);
      } catch {
        /* cross-origin sheets ignored */
      }
    }
    return parts.join("\n");
  }

  async function rasterizeHtml(node) {
    const width = Math.max(1, Math.round(node.scrollWidth || node.clientWidth || 900));
    const height = Math.max(1, Math.round(node.scrollHeight || node.clientHeight || 600));
    const pixelW = Math.round(width * EXPORT_SCALE);
    const pixelH = Math.round(height * EXPORT_SCALE);
    const clone = node.cloneNode(true);
    clone.querySelectorAll(".tip, .fpl-map-tip, [hidden]").forEach((n) => n.remove());
    clone.removeAttribute("hidden");
    clone.style.width = `${width}px`;
    clone.style.height = `${height}px`;
    clone.style.background = getComputedStyle(node).backgroundColor || BG;
    const html = new XMLSerializer().serializeToString(clone);
    const css = collectPageCss();
    const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${pixelW}" height="${pixelH}" viewBox="0 0 ${width} ${height}">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml" style="width:${width}px;height:${height}px;background:${BG};color:${INK};">
      <style>${css}</style>
      ${html}
    </div>
  </foreignObject>
</svg>`;
    const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    const img = await loadImage(url);
    return { img, width: pixelW, height: pixelH, logicalWidth: width, logicalHeight: height };
  }

  async function captureNode(node) {
    if (!node) throw new Error("Nothing to export");
    if (node.matches?.("svg")) return rasterizeSvg(node);
    const childSvg = node.querySelector(":scope > svg");
    const isHtmlBoard = Boolean(
      node.querySelector("table, .timing-cell, .timing-row, .matrix-table, .tempo-board .timing-cell")
    );
    if (childSvg && !isHtmlBoard) return rasterizeSvg(childSvg);
    return rasterizeHtml(node);
  }

  async function downloadChart(node, filenamePrefix, caption) {
    const { img, width, height } = await captureNode(node);
    const logicalW = width / EXPORT_SCALE;
    const hasCaption = Boolean(caption && (caption.title || caption.metrics));
    const headerLogical = hasCaption ? HEADER_H : 0;
    const headerH = Math.round(headerLogical * EXPORT_SCALE);
    const bannerH = Math.round(BANNER_H * EXPORT_SCALE);
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = headerH + height + bannerH;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.scale(EXPORT_SCALE, EXPORT_SCALE);
    if (hasCaption) drawCaptionBanner(ctx, logicalW, 0, caption);
    ctx.restore();

    ctx.drawImage(img, 0, headerH, width, height);

    ctx.save();
    ctx.scale(EXPORT_SCALE, EXPORT_SCALE);
    drawBrandBanner(ctx, logicalW, headerLogical + height / EXPORT_SCALE);
    ctx.restore();
    triggerDownload(canvas, basename(filenamePrefix));
  }

  function visiblePanel(candidates) {
    for (const el of candidates) {
      if (!el || el.hidden) continue;
      if (el.offsetParent === null && getComputedStyle(el).display === "none") continue;
      if (el.clientWidth < 8 && el.clientHeight < 8) continue;
      return el;
    }
    return candidates.find((el) => el && !el.hidden) || null;
  }

  function bindChartDownload(button, getNode, filenamePrefix, getCaption) {
    if (!button) return;
    button.addEventListener("click", async () => {
      const prev = button.textContent;
      button.disabled = true;
      button.textContent = "Saving…";
      try {
        const node = typeof getNode === "function" ? getNode() : getNode;
        const prefix = typeof filenamePrefix === "function" ? filenamePrefix() : filenamePrefix;
        const caption = typeof getCaption === "function" ? getCaption() : getCaption;
        await downloadChart(node, prefix, caption);
      } catch (err) {
        console.error(err);
        button.textContent = "Failed";
        setTimeout(() => {
          button.textContent = prev;
          button.disabled = false;
        }, 1400);
        return;
      }
      button.textContent = "Saved";
      setTimeout(() => {
        button.textContent = prev;
        button.disabled = false;
      }, 900);
    });
  }

  window.ChartExport = { downloadChart, bindChartDownload, visiblePanel };
})();
