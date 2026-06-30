#!/usr/bin/env python3
"""Promote mined Open Food Facts terms into a review-ready curated CSV.

This does not automatically mark terms as reviewed. It creates a draft queue that a
human/editor/agent can classify into real ingredient records.

Example:
  python scripts/promote_mined_terms.py \
    --input data/generated/ingredient_frequency.csv \
    --output data/generated/promoted_terms_review.csv \
    --min-count 25 \
    --limit 1000
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ID_RE = re.compile(r"[^a-z0-9]+")


def make_id(term: str) -> str:
    slug = ID_RE.sub("_", term.lower()).strip("_")
    return f"ing_{slug}"[:80]


def title_case(term: str) -> str:
    small = {"and", "or", "of", "with", "in"}
    words = term.split()
    return " ".join(w if w in small else w.capitalize() for w in words)


def promote(input_path: Path, output_path: Path, min_count: int, limit: int | None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    promoted = []
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count = int(row.get("product_count") or 0)
            if count < min_count:
                continue
            term = (row.get("ingredient_name") or "").strip()
            if not term:
                continue
            promoted.append(
                {
                    "ingredient_id": make_id(term),
                    "canonical_name": title_case(term),
                    "category": "needs_classification",
                    "subcategory": "mined_from_openfoodfacts",
                    "common_aliases": term,
                    "source_type": "unknown",
                    "functional_purpose": "needs_review",
                    "common_foods": row.get("top_category", ""),
                    "history_estimate": "unknown",
                    "app_note": f"Mined from product labels; appears in about {count} products in the source sample.",
                    "risk_note": "Do not show safety claims until reviewed.",
                    "review_status": "needs_source",
                    "product_count": str(count),
                    "raw_example": row.get("raw_example", ""),
                }
            )
            if limit and len(promoted) >= limit:
                break

    fieldnames = [
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
        "product_count",
        "raw_example",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(promoted)
    print(f"Promoted {len(promoted)} mined terms into {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    promote(args.input, args.output, args.min_count, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
