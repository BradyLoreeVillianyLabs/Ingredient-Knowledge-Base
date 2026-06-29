#!/usr/bin/env python3
"""Check generated rich ingredient profile count for CI."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "generated" / "rich_ingredient_profiles.csv"
EXPECTED_ROWS = 500


def main() -> int:
    with PROFILE_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != EXPECTED_ROWS:
        print(f"Expected {EXPECTED_ROWS} rich profiles, found {len(rows)}")
        return 1
    print("Rich profile count ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
