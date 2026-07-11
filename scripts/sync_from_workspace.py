#!/usr/bin/env python3
"""Copy release-approved RW skills from the workspace source tree."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    source_root = args.source_root or plugin_root.parents[1] / "skills"
    manifest = json.loads((plugin_root / "manifest.json").read_text(encoding="utf-8"))
    target_root = plugin_root / "skills"
    target_root.mkdir(exist_ok=True)
    release_skills = list(dict.fromkeys(manifest["skills"]))
    for existing in target_root.iterdir():
        if existing.is_dir() and existing.name not in release_skills:
            shutil.rmtree(existing)
    copied: list[str] = []
    for name in release_skills:
        source = source_root / name
        target = target_root / name
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"missing source skill: {source}")
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        copied.append(name)

    print(json.dumps({"copied": copied}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
