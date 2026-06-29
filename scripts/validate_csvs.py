#!/usr/bin/env python3
"""Validate Ingredient Knowledge Base CSV files.

The build is strict about CSV parseability and missing headers.
Schema, slug, and review-status problems are reported as warnings during the
seed/expansion phase so CI can keep producing reports and generated artifacts.
Those warnings are tracked by docs/MISSING_DATA_REPORT.md for cleanup passes.
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
VALID_REVIEW_STATUS = {"draft", "needs_source", "reviewed", "generated", "mined", "needs_review"}
SLUG_RE = re.compile(r"^[a-z0-9_]+$")


def is_metadata_or_generated(path: Path) -> bool:
    return "metadata" in path.parts or "generated" in path.parts or "raw" in path.parts


def is_curated_ingredient_list(path: Path, fieldnames: list[str]) -> bool:
    if is_metadata_or_generated(path):
        return False
    return "ingredient_id" in fieldnames


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return [f"{path}: missing header"], warnings

            is_ingredient_list = is_curated_ingredient_list(path, reader.fieldnames)
            if is_ingredient_list:
                missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
                if missing:
                    warnings.append(f"{path}: missing columns {missing}")

            for line_number, row in enumerate(reader, start=2):
                review_status = (row.get("review_status") or "").strip()
                if review_status and review_status not in VALID_REVIEW_STATUS:
                    warnings.append(
                        f"{path}:{line_number}: invalid review_status {review_status!r}"
                    )

                if not is_ingredient_list:
                    continue

                ingredient_id = (row.get("ingredient_id") or "").strip()
                if not ingredient_id:
                    warnings.append(f"{path}:{line_number}: missing ingredient_id")
                elif not SLUG_RE.match(ingredient_id):
                    warnings.append(f"{path}:{line_number}: invalid ingredient_id {ingredient_id!r}")

                name = (row.get("canonical_name") or "").strip()
                if not name:
                    warnings.append(f"{path}:{line_number}: missing canonical_name")
    except csv.Error as exc:
        errors.append(f"{path}: CSV parse error: {exc}")
    except UnicodeDecodeError as exc:
        errors.append(f"{path}: UTF-8 decode error: {exc}")
    return errors, warnings


def main() -> int:
    csv_files = sorted(
        path for path in DATA_DIR.rglob("*.csv")
        if "raw" not in path.parts
    )
    if not csv_files:
        print("No CSV files found under data/.")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    for path in csv_files:
        file_errors, file_warnings = validate_file(path)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    if warnings:
        print("CSV validation warnings:")
        for warning in warnings[:200]:
            print(f"- {warning}")
        if len(warnings) > 200:
            print(f"- ... {len(warnings) - 200} more warnings")

    if errors:
        print("CSV validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Parsed {len(csv_files)} CSV files successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
