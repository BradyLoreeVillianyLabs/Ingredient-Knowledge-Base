#!/usr/bin/env python3
"""Sync generated knowledge-base assets into a sibling app project.

Run from the Ingredient-Knowledge-Base repo after `python scripts/build_all.py`.

Example:
  python app_integration/sync_to_app.py \
    --app-root ../Food-Ingredient-Analyzer \
    --target-subdir app/data/ingredient-kb
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
GENERATED_DIR = ROOT / "data" / "generated"


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sync(app_root: Path, target_subdir: Path) -> None:
    target = app_root / target_subdir
    target.mkdir(parents=True, exist_ok=True)

    copy_file(DIST_DIR / "ingredient_knowledge_base.sqlite", target / "ingredient_knowledge_base.sqlite")
    copy_file(GENERATED_DIR / "ingredient_alias_index.csv", target / "ingredient_alias_index.csv")
    copy_file(GENERATED_DIR / "evidence_packs_index.json", target / "evidence_packs_index.json")
    copy_tree(GENERATED_DIR / "json", target / "json")
    copy_tree(GENERATED_DIR / "evidence_packs", target / "evidence_packs")
    copy_file(ROOT / "docs" / "DATASET_REPORT.md", target / "DATASET_REPORT.md")

    print(f"Synced ingredient knowledge base into {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-root", required=True, type=Path)
    parser.add_argument("--target-subdir", default=Path("app/data/ingredient-kb"), type=Path)
    args = parser.parse_args()

    if not args.app_root.exists():
        raise SystemExit(f"App root does not exist: {args.app_root}")
    sync(args.app_root, args.target_subdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
