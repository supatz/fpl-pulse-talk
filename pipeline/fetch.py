from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from pipeline.config import SOURCE_DIR, SOURCE_REPO

log = logging.getLogger("fpl")


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def fetch_source(dest: Path = SOURCE_DIR) -> tuple[Path, str]:
    """Shallow-clone or update the public source repo. No auth, no tokens."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    git_dir = dest / ".git"
    if git_dir.exists():
        log.info("Updating source clone at %s", dest)
        _run(["git", "remote", "set-url", "origin", SOURCE_REPO], cwd=dest)
        _run(["git", "fetch", "--depth", "1", "origin"], cwd=dest)
        # Detached shallow clone: reset to fetched default branch tip.
        try:
            _run(["git", "reset", "--hard", "origin/HEAD"], cwd=dest)
        except subprocess.CalledProcessError:
            branch = _run(["git", "rev-parse", "--abbrev-ref", "origin/HEAD"], cwd=dest)
            ref = branch.split("/")[-1]
            _run(["git", "reset", "--hard", f"origin/{ref}"], cwd=dest)
    else:
        if dest.exists():
            # Incomplete leftover — start clean.
            import shutil

            shutil.rmtree(dest)
        log.info("Shallow-cloning %s into %s", SOURCE_REPO, dest)
        _run(["git", "clone", "--depth", "1", SOURCE_REPO, str(dest)])
    sha = _run(["git", "rev-parse", "HEAD"], cwd=dest)
    log.info("Source commit %s", sha)
    return dest, sha
