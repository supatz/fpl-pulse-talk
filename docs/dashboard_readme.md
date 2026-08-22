# FPL Pulse Talk — dashboard

Static multi-file site. Presentation lives in `web/`. Data lives in `serving/*.json` (copied to `web/data/` for deploy).

## Local

```bash
.venv/bin/python build_serving.py   # masters → JSON only; does not rebuild Parquet
.venv/bin/python serve.py           # http://127.0.0.1:8765/
```

Do **not** open `web/index.html` via `file://` — `fetch` of JSON is blocked in most browsers.

## What to edit for common tweaks

| Change | File | Cost |
|---|---|---|
| Rename a metric / tooltip / column order | `web/registry.js` | 🟢 |
| Look and feel | `web/styles.css` | 🟢 |
| Table behaviour | `web/components.js` `makeTable` | 🟢 |
| New view wiring | `web/app.js` + a `VIEWS` entry | 🟢 |
| New precomputed field | `build_serving.py` then `build_serving.py` | 🟠 |
| Rebuild Parquet masters | `build.py --refresh` | 🔴 |

Filters and sort are stored in `localStorage` key `fplpulse.v1`.

Hover any italic **i** to see `page.section.element`. Click to copy.
