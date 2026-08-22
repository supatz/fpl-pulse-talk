#!/usr/bin/env python3
"""Local static server so fetch('./data/...') works (file:// often blocks it)."""

from __future__ import annotations

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB = Path(__file__).resolve().parent / "web"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(WEB))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"FPL Pulse Talk → http://127.0.0.1:{args.port}/")
    print(f"Serving {WEB}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
