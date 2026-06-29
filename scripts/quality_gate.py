#!/usr/bin/env python3
"""Run repository quality gates beyond basic CSV parsing.

Checks:
- duplicate ingredient IDs are reported for review without blocking seeded builds
- generated alias index exists
- reviewed rows in sensitive metadata files must have citation_id when that column exists
- regulatory jurisdictions use expected codes/names
- public facts avoid strong medical-claim language without review
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
GENERATED_ALIAS_PATH = DATA_DIR / "generated" / "ingredient_alias_index.csv"
SENSITIVE_FILES = {
    DATA_DIR / "metadata" / "15_regulatory_status.csv",
    DATA_DIR / "metadata" / "16_ingredient_facts.csv",
    DATA_DIR / "metadata" / "17_historical_use.csv",
}
VALID_JURISDICTIONS = {"US", "Canada", "EU", "Global", "Codex", "UK", "Australia_NZ"}
MEDICAL_CLAIM_RE = re.compile(
    r"\b(cures?|treats?|prevents?|heals?|reverses?|detoxifies|guaranteed|disease|cancer|diabetes|adhd|autism)\b",
    re.IGNORECASE,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_curated_ingredient_file(path: Path) -> bool:
    return "metadata" not in path.parts and "generated" not in path.parts and "raw" not in path.parts


def iter_ingredient_csvs():
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if not is_curated_ingredient_file(path):
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames and "ingredient_id" in reader.fieldnames:
                yield path, list(reader)


def collect_duplicate_ingredient_ids() -> list[str]:
    locations: dict[str, list[str]] = defaultdict(list)
    for path, rows in iter_ingredient_csvs():
        for i, row in enumerate(rows, start=2):
            ingredient_id = (row.get("ingredient_id") or "").strip()
            if ingredient_id:
                locations[ingredient_id].append(f"{path.relative_to(ROOT)}:{i}")

    warnings = []
    for ingredient_id, refs in sorted(locations.items()):
        if len(refs) > 1:
            warnings.append(f"duplicate curated ingredient_id {ingredient_id}: {refs}")
    return warnings


def check_alias_index_exists() -> list[str]:
    if not GENERATED_ALIAS_PATH.exists():
        return ["generated alias index missing; run scripts/build_alias_index.py first"]
    return []


def collect_alias_conflicts() -> list[str]:
    if not GENERATED_ALIAS_PATH.exists():
        return []
    alias_to_ids: dict[str, set[str]] = defaultdict(set)
    for row in read_csv(GENERATED_ALIAS_PATH):
        alias = (row.get("normalized_alias") or "").strip()
        ingredient_id = (row.get("ingredient_id") or "").strip()
        if alias and ingredient_id:
            alias_to_ids[alias].add(ingredient_id)

    warnings = []
    for alias, ids in sorted(alias_to_ids.items()):
        if len(ids) > 1:
            warnings.append(f"alias conflict {alias!r} maps to {sorted(ids)}")
    return warnings


def check_reviewed_rows_have_citations() -> list[str]:
    errors = []
    for path in SENSITIVE_FILES:
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            has_citation = reader.fieldnames and "citation_id" in reader.fieldnames
            for line_no, row in enumerate(reader, start=2):
                if row.get("review_status") == "reviewed" and has_citation:
                    if not (row.get("citation_id") or "").strip():
                        errors.append(f"{path.relative_to(ROOT)}:{line_no}: reviewed row missing citation_id")
    return errors


def check_jurisdictions() -> list[str]:
    path = DATA_DIR / "metadata" / "15_regulatory_status.csv"
    if not path.exists():
        return []
    errors = []
    for line_no, row in enumerate(read_csv(path), start=2):
        jurisdiction = (row.get("jurisdiction") or "").strip()
        if jurisdiction and jurisdiction not in VALID_JURISDICTIONS:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: unknown jurisdiction {jurisdiction!r}")
    return errors


def check_medical_language() -> list[str]:
    path = DATA_DIR / "metadata" / "16_ingredient_facts.csv"
    if not path.exists():
        return []
    errors = []
    for line_no, row in enumerate(read_csv(path), start=2):
        text = row.get("fact_text") or ""
        if MEDICAL_CLAIM_RE.search(text) and row.get("review_status") != "reviewed":
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: possible medical claim needs reviewed citation")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    warnings.extend(collect_duplicate_ingredient_ids())
    warnings.extend(collect_alias_conflicts())
    errors.extend(check_alias_index_exists())
    errors.extend(check_reviewed_rows_have_citations())
    errors.extend(check_jurisdictions())
    errors.extend(check_medical_language())

    if warnings:
        print("Quality gate warnings:")
        for warning in warnings[:100]:
            print(f"- {warning}")
        if len(warnings) > 100:
            print(f"- ... {len(warnings) - 100} more warnings")

    if errors:
        print("Quality gates failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
