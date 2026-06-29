#!/usr/bin/env python3
"""Mine Open Food Facts exports into app-ready ingredient statistics.

Input:
  A CSV/TSV file exported from Open Food Facts. The full export is large; for local
  development, start with a sampled file.

Example:
  python scripts/mine_openfoodfacts.py \
    --input data/raw/openfoodfacts_sample.tsv \
    --output-dir data/generated

Outputs:
  - ingredient_frequency.csv
  - ingredient_combinations.csv
  - unknown_ingredient_candidates.csv

Notes:
  This script intentionally avoids making safety claims. It mines occurrence,
  co-occurrence, and raw label terms for later review.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import re
from collections import Counter, defaultdict
from pathlib import Path

INGREDIENT_SPLIT_RE = re.compile(r",|;|\n")
PAREN_RE = re.compile(r"[()\[\]{}]")
SPACE_RE = re.compile(r"\s+")


def normalize_term(value: str) -> str:
    value = value.lower().strip()
    value = PAREN_RE.sub(" ", value)
    value = value.replace("*", " ").replace("_", " ")
    value = re.sub(r"[^a-z0-9%+\- ]+", " ", value)
    value = SPACE_RE.sub(" ", value).strip(" -")
    return value


def parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []
    terms = []
    for part in INGREDIENT_SPLIT_RE.split(raw):
        term = normalize_term(part)
        if not term:
            continue
        if len(term) < 2:
            continue
        terms.append(term)
    return sorted(set(terms))


def sniff_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    if sample.count("\t") > sample.count(","):
        return "\t"
    return ","


def mine(input_path: Path, output_dir: Path, max_rows: int | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    delimiter = sniff_delimiter(input_path)

    ingredient_counts: Counter[str] = Counter()
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    country_counts: dict[str, Counter[str]] = defaultdict(Counter)
    combination_counts: Counter[tuple[str, str]] = Counter()
    raw_examples: dict[str, str] = {}

    with input_path.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row_index, row in enumerate(reader, start=1):
            if max_rows and row_index > max_rows:
                break

            raw_ingredients = (
                row.get("ingredients_text")
                or row.get("ingredients_text_en")
                or row.get("ingredients")
                or ""
            )
            terms = parse_ingredients(raw_ingredients)
            if not terms:
                continue

            category = normalize_term(row.get("categories") or row.get("main_category") or "unknown")
            country = normalize_term(row.get("countries") or row.get("countries_en") or "unknown")

            for term in terms:
                ingredient_counts[term] += 1
                category_counts[term][category] += 1
                country_counts[term][country] += 1
                raw_examples.setdefault(term, raw_ingredients[:300])

            for left, right in itertools.combinations(terms[:50], 2):
                combination_counts[(left, right)] += 1

    with (output_dir / "ingredient_frequency.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ingredient_name",
            "product_count",
            "top_category",
            "top_country",
            "raw_example",
            "review_status",
        ])
        for term, count in ingredient_counts.most_common():
            writer.writerow([
                term,
                count,
                category_counts[term].most_common(1)[0][0] if category_counts[term] else "",
                country_counts[term].most_common(1)[0][0] if country_counts[term] else "",
                raw_examples.get(term, ""),
                "mined",
            ])

    with (output_dir / "ingredient_combinations.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ingredient_a", "ingredient_b", "cooccurrence_count", "review_status"])
        for (left, right), count in combination_counts.most_common():
            writer.writerow([left, right, count, "mined"])

    with (output_dir / "unknown_ingredient_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_name", "product_count", "raw_example", "review_status"])
        for term, count in ingredient_counts.most_common():
            if count < 2:
                writer.writerow([term, count, raw_examples.get(term, ""), "needs_review"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    mine(args.input, args.output_dir, args.max_rows)
    print(f"Mined ingredient stats into {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
