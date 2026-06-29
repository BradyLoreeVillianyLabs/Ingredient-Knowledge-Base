#!/usr/bin/env python3
"""Validate Ingredient Knowledge Base CSV files.

Checks:
- every CSV can be parsed
- data list CSVs contain the required schema columns
- ingredient_id values are lowercase slug-like identifiers
- review_status uses approved values
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REQUIRED_COLUMNS = [
    "ingredient_id",
    "canonical_name",
    "category",
    "subcategory",
    "common_aliases",
    "source_type",
    "functional_purpose",
    "common_foods",
    "history_estimate",
    "app_note",
    "risk_note",
    "review_status",
]
VALID_REVIEW_STATUS = {"draft", "needs_source", "reviewed"}
SLUG_RE = re.compile(r"^[a-z0-9_]+$")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return [f"{path}: missing header"]

        # Metadata files may intentionally have different schemas.
        is_ingredient_list = "ingredient_id" in reader.fieldnames
        if is_ingredient_list:
            missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
            if missing:
                errors.append(f"{path}: missing columns {missing}")

        for line_number, row in enumerate(reader, start=2):
            if not is_ingredient_list:
                continue
            ingredient_id = (row.get("ingredient_id") or "").strip()
            if not ingredient_id:
                errors.append(f"{path}:{line_number}: missing ingredient_id")
            elif not SLUG_RE.match(ingredient_id):
                errors.append(f"{path}:{line_number}: invalid ingredient_id {ingredient_id!r}")

            name = (row.get("canonical_name") or "").strip()
            if not name:
                errors.append(f"{path}:{line_number}: missing canonical_name")

            review_status = (row.get("review_status") or "").strip()
            if review_status not in VALID_REVIEW_STATUS:
                errors.append(
                    f"{path}:{line_number}: invalid review_status {review_status!r}"
                )
    return errors


def main() -> int:
    csv_files = sorted(DATA_DIR.rglob("*.csv"))
    if not csv_files:
        print("No CSV files found under data/.")
        return 1

    errors: list[str] = []
    for path in csv_files:
        errors.extend(validate_file(path))

    if errors:
        print("CSV validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(csv_files)} CSV files successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
