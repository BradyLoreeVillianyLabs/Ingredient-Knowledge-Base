#!/usr/bin/env python3
"""Smoke tests for generated package artifacts.

This is intentionally dependency-free so GitHub Actions can run it with stock Python.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_exists(path: Path) -> None:
    assert path.exists(), f"Missing expected file: {path}"
    assert path.stat().st_size > 0, f"Expected non-empty file: {path}"


def test_generated_files() -> None:
    assert_exists(ROOT / "data" / "generated" / "ingredient_alias_index.csv")
    assert_exists(ROOT / "data" / "generated" / "json" / "ingredients.json")
    assert_exists(ROOT / "data" / "generated" / "evidence_packs_index.json")
    assert_exists(ROOT / "docs" / "DATASET_REPORT.md")


def test_json_payloads() -> None:
    ingredients = json.loads((ROOT / "data" / "generated" / "json" / "ingredients.json").read_text())
    assert isinstance(ingredients, list)
    assert ingredients, "ingredients.json should not be empty"
    first = ingredients[0]
    assert "ingredient_id" in first
    assert "canonical_name" in first

    packs = json.loads((ROOT / "data" / "generated" / "evidence_packs_index.json").read_text())
    assert isinstance(packs, list)
    assert packs, "evidence_packs_index.json should not be empty"
    assert "pack_path" in packs[0]


def test_sqlite_database() -> None:
    db_path = ROOT / "dist" / "ingredient_knowledge_base.sqlite"
    assert_exists(db_path)
    conn = sqlite3.connect(db_path)
    try:
        ingredient_count = conn.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0]
        alias_count = conn.execute("SELECT COUNT(*) FROM ingredient_aliases").fetchone()[0]
        assert ingredient_count > 0
        assert alias_count > 0
    finally:
        conn.close()


def main() -> int:
    test_generated_files()
    test_json_payloads()
    test_sqlite_database()
    print("Smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
