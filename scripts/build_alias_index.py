#!/usr/bin/env python3
"""Build a normalized ingredient alias index from curated ingredient CSV files.

Output:
  data/generated/ingredient_alias_index.csv

This creates a lookup table for OCR matching and ingredient search. It combines:
- canonical names
- common_aliases pipe-delimited values
- E-number-like aliases present in common_aliases

Metadata tables are intentionally excluded because they may contain ingredient_id
references without being canonical ingredient records.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "generated"
OUT_PATH = OUT_DIR / "ingredient_alias_index.csv"
SPACE_RE = re.compile(r"\s+")


def normalize(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9+\- ]+", " ", value)
    value = SPACE_RE.sub(" ", value)
    return value.strip()


def is_curated_ingredient_file(path: Path) -> bool:
    return "metadata" not in path.parts and "generated" not in path.parts and "raw" not in path.parts


def iter_ingredient_rows():
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if not is_curated_ingredient_file(path):
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "ingredient_id" not in reader.fieldnames:
                continue
            for row in reader:
                yield path, row


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[tuple[str, str]] = set()
    rows: list[dict[str, str]] = []

    for path, row in iter_ingredient_rows():
        ingredient_id = (row.get("ingredient_id") or "").strip()
        canonical_name = (row.get("canonical_name") or "").strip()
        if not ingredient_id or not canonical_name:
            continue

        aliases = [canonical_name]
        aliases.extend(
            alias.strip()
            for alias in (row.get("common_aliases") or "").split("|")
            if alias.strip()
        )

        for alias in aliases:
            normalized = normalize(alias)
            if not normalized:
                continue
            key = (ingredient_id, normalized)
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "ingredient_id": ingredient_id,
                    "canonical_name": canonical_name,
                    "alias": alias,
                    "normalized_alias": normalized,
                    "source_file": str(path.relative_to(ROOT)),
                    "review_status": "generated",
                }
            )

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "ingredient_id",
                "canonical_name",
                "alias",
                "normalized_alias",
                "source_file",
                "review_status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} aliases to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
