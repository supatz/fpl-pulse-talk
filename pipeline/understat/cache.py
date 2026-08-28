"""Disk cache for raw Understat JSON — re-runs never re-hit the network for hits."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pipeline.understat.config import CACHE_DIR

log = logging.getLogger("understat")


def cache_path(*parts: str) -> Path:
    path = CACHE_DIR.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def cached_get(rel_key: str, fetcher, *, force: bool = False) -> Any:
    """
    rel_key examples:
      league/EPL/2025/matches.json
      match/26602/shots.json
    """
    path = cache_path(*rel_key.split("/"))
    if not force:
        hit = read_json(path)
        if hit is not None:
            return hit
    data = fetcher()
    write_json(path, data)
    return data
