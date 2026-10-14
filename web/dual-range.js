/* Two-thumb range slider. Both ends move; used for GW and price filters. */
(() => {
  function clamp(n, lo, hi) {
    return Math.min(hi, Math.max(lo, n));
  }

  function snap(n, step) {
    if (!step) return n;
    const inv = 1 / step;
    return Math.round(n * inv) / inv;
  }

  /**
   * @param {HTMLElement} el
   * @param {{ min:number, max:number, step?:number, from:number, to:number, onInput?:(from:number,to:number)=>void }} opts
   */
  function mountDualRange(el, opts) {
    if (!el) return null;
    let min = Number(opts.min);
    let max = Number(opts.max);
    let step = Number(opts.step) || 1;
    let from = clamp(snap(Number(opts.from), step), min, max);
    let to = clamp(snap(Number(opts.to), step), min, max);
    if (from > to) [from, to] = [to, from];

    el.classList.add("range-2");
    el.innerHTML = `
      <div class="range-2-rail" aria-hidden="true">
        <div class="range-2-fill"></div>
      </div>
      <input type="range" class="range-2-input range-2-from" aria-label="Range start" />
      <input type="range" class="range-2-input range-2-to" aria-label="Range end" />
    `;
    const fromEl = el.querySelector(".range-2-from");
    const toEl = el.querySelector(".range-2-to");
    const fill = el.querySelector(".range-2-fill");

    const applyBounds = () => {
      for (const input of [fromEl, toEl]) {
        input.min = String(min);
        input.max = String(max);
        input.step = String(step);
      }
    };

    const paint = () => {
      fromEl.value = String(from);
      toEl.value = String(to);
      const span = max - min || 1;
      const left = ((from - min) / span) * 100;
      const right = ((to - min) / span) * 100;
      fill.style.left = `${left}%`;
      fill.style.width = `${Math.max(0, right - left)}%`;
      fromEl.style.zIndex = from > max - (max - min) * 0.05 ? "5" : "3";
      toEl.style.zIndex = "4";
    };

    const emit = () => opts.onInput?.(from, to);

    const syncFrom = () => {
      from = clamp(snap(Number(fromEl.value), step), min, to);
      paint();
      emit();
    };
    const syncTo = () => {
      to = clamp(snap(Number(toEl.value), step), from, max);
      paint();
      emit();
    };

    applyBounds();
    paint();
    fromEl.addEventListener("input", syncFrom);
    toEl.addEventListener("input", syncTo);

    return {
      get: () => ({ from, to, min, max, step }),
      set: (nextFrom, nextTo) => {
        from = clamp(snap(Number(nextFrom), step), min, max);
        to = clamp(snap(Number(nextTo), step), min, max);
        if (from > to) [from, to] = [to, from];
        paint();
      },
      setBounds: (nextMin, nextMax, { reset = false } = {}) => {
        min = Number(nextMin);
        max = Number(nextMax);
        if (min > max) [min, max] = [max, min];
        applyBounds();
        if (reset) {
          from = min;
          to = max;
        } else {
          from = clamp(from, min, max);
          to = clamp(to, min, max);
          if (from > to) [from, to] = [min, max];
        }
        paint();
      },
      el,
    };
  }

  /** Price band from meta.prices (£m), snapped to 0.5. */
  function priceBounds(prices) {
    const vals = Object.values(prices || {})
      .map(Number)
      .filter((n) => Number.isFinite(n) && n > 0);
    if (!vals.length) return { min: 4, max: 16 };
    const lo = Math.floor(Math.min(...vals) * 2) / 2;
    const hi = Math.ceil(Math.max(...vals) * 2) / 2;
    return { min: lo, max: Math.max(hi, lo + 0.5) };
  }

  window.mountDualRange = mountDualRange;
  window.priceBounds = priceBounds;
})();
