#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path


SKILL_NAME = "ai-video-production-director"


def default_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home) if codex_home else Path.home() / ".codex") / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and install the AI video production director skill.")
    parser.add_argument("--dest", type=Path, default=default_skills_dir(), help="Parent skills directory")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    skills_dir = args.dest.expanduser().resolve()
    destination = skills_dir / SKILL_NAME
    if destination == source or source in destination.parents or destination in source.parents:
        print("Refusing overlapping source and destination", file=sys.stderr)
        return 2

    validator = source / "scripts" / "validate_skill.py"
    result = subprocess.run([sys.executable, str(validator), str(source)], check=False)
    if result.returncode:
        return result.returncode

    skills_dir.mkdir(parents=True, exist_ok=True)
    stage = skills_dir / f".{SKILL_NAME}.stage-{uuid.uuid4().hex}"
    backup = skills_dir / f".{SKILL_NAME}.backup-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    shutil.copytree(source, stage, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    moved_existing = False
    try:
        if destination.exists():
            os.replace(destination, backup)
            moved_existing = True
        os.replace(stage, destination)
    except Exception:
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        if moved_existing and backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise

    print(f"Installed {SKILL_NAME} to {destination}")
    if moved_existing:
        print(f"Previous install preserved at {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
