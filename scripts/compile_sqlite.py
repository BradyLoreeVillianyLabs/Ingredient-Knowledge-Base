#!/usr/bin/env python3
"""Compile CSV knowledge base into a SQLite database.

Example:
  python scripts/build_alias_index.py
  python scripts/compile_sqlite.py --output ingredient_knowledge_base.sqlite
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SCHEMA_PATH = ROOT / "schema" / "app_database_schema.sql"

INGREDIENT_COLUMNS = [
    "ingredient_id",
    "canonical_name",
    "category",
    "subcategory",
    "source_type",
    "functional_purpose",
    "common_foods",
    "history_estimate",
    "app_note",
    "risk_note",
    "review_status",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_ingredients(conn: sqlite3.Connection) -> None:
    seen: set[str] = set()
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if "metadata" in path.parts or "generated" in path.parts:
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "ingredient_id" not in reader.fieldnames:
                continue
            for row in reader:
                ingredient_id = (row.get("ingredient_id") or "").strip()
                if not ingredient_id or ingredient_id in seen:
                    continue
                seen.add(ingredient_id)
                values = [row.get(col, "") for col in INGREDIENT_COLUMNS]
                conn.execute(
                    f"INSERT OR REPLACE INTO ingredients ({','.join(INGREDIENT_COLUMNS)}) VALUES ({','.join(['?'] * len(INGREDIENT_COLUMNS))})",
                    values,
                )


def load_aliases(conn: sqlite3.Connection) -> None:
    path = DATA_DIR / "generated" / "ingredient_alias_index.csv"
    if not path.exists():
        return
    for row in read_csv(path):
        conn.execute(
            """
            INSERT INTO ingredient_aliases
              (ingredient_id, canonical_name, alias, normalized_alias, source_file, review_status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("ingredient_id", ""),
                row.get("canonical_name", ""),
                row.get("alias", ""),
                row.get("normalized_alias", ""),
                row.get("source_file", ""),
                row.get("review_status", "generated"),
            ),
        )


def load_facts(conn: sqlite3.Connection) -> None:
    path = DATA_DIR / "metadata" / "16_ingredient_facts.csv"
    if not path.exists():
        return
    for row in read_csv(path):
        conn.execute(
            """
            INSERT OR REPLACE INTO ingredient_facts
              (fact_id, ingredient_id, canonical_name, fact_type, fact_text, evidence_level, review_status, citation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("fact_id", ""),
                row.get("ingredient_id", ""),
                row.get("canonical_name", ""),
                row.get("fact_type", ""),
                row.get("fact_text", ""),
                row.get("evidence_level", ""),
                row.get("review_status", ""),
                row.get("citation_id", ""),
            ),
        )


def load_regulatory_status(conn: sqlite3.Connection) -> None:
    path = DATA_DIR / "metadata" / "15_regulatory_status.csv"
    if not path.exists():
        return
    for row in read_csv(path):
        conn.execute(
            """
            INSERT OR REPLACE INTO ingredient_regulatory_status
              (regulatory_id, ingredient_id, canonical_name, jurisdiction, status, allowed_use_notes, requires_warning, review_status, citation_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("regulatory_id", ""),
                row.get("ingredient_id", ""),
                row.get("canonical_name", ""),
                row.get("jurisdiction", ""),
                row.get("status", ""),
                row.get("allowed_use_notes", ""),
                row.get("requires_warning", ""),
                row.get("review_status", ""),
                row.get("citation_id", ""),
                row.get("notes", ""),
            ),
        )


def load_history(conn: sqlite3.Connection) -> None:
    path = DATA_DIR / "metadata" / "17_historical_use.csv"
    if not path.exists():
        return
    for row in read_csv(path):
        conn.execute(
            """
            INSERT OR REPLACE INTO ingredient_history
              (history_id, ingredient_id, canonical_name, history_estimate, confidence, region_or_origin, notes, review_status, citation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("history_id", ""),
                row.get("ingredient_id", ""),
                row.get("canonical_name", ""),
                row.get("history_estimate", ""),
                row.get("confidence", ""),
                row.get("region_or_origin", ""),
                row.get("notes", ""),
                row.get("review_status", ""),
                row.get("citation_id", ""),
            ),
        )


def load_registry(conn: sqlite3.Connection) -> None:
    source_path = DATA_DIR / "metadata" / "source_registry.csv"
    if source_path.exists():
        for row in read_csv(source_path):
            conn.execute(
                """
                INSERT OR REPLACE INTO source_registry
                  (source_id, source_name, source_type, homepage_url, download_url, license_or_terms, priority, use_case, review_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("source_id", ""),
                    row.get("source_name", ""),
                    row.get("source_type", ""),
                    row.get("homepage_url", ""),
                    row.get("download_url", ""),
                    row.get("license_or_terms", ""),
                    row.get("priority", ""),
                    row.get("use_case", ""),
                    row.get("review_status", ""),
                    row.get("notes", ""),
                ),
            )

    citation_path = DATA_DIR / "metadata" / "citation_registry.csv"
    if citation_path.exists():
        for row in read_csv(citation_path):
            conn.execute(
                """
                INSERT OR REPLACE INTO citation_registry
                  (citation_id, source_id, title, url, applies_to, claim_scope, review_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("citation_id", ""),
                    row.get("source_id", ""),
                    row.get("title", ""),
                    row.get("url", ""),
                    row.get("applies_to", ""),
                    row.get("claim_scope", ""),
                    row.get("review_status", ""),
                    row.get("notes", ""),
                ),
            )


def load_generated_stats(conn: sqlite3.Connection) -> None:
    freq_path = DATA_DIR / "generated" / "ingredient_frequency.csv"
    if freq_path.exists():
        for row in read_csv(freq_path):
            conn.execute(
                """
                INSERT OR REPLACE INTO ingredient_frequency
                  (ingredient_name, product_count, top_category, top_country, raw_example, review_status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("ingredient_name", ""),
                    int(row.get("product_count") or 0),
                    row.get("top_category", ""),
                    row.get("top_country", ""),
                    row.get("raw_example", ""),
                    row.get("review_status", ""),
                ),
            )

    combo_path = DATA_DIR / "generated" / "ingredient_combinations.csv"
    if combo_path.exists():
        for row in read_csv(combo_path):
            conn.execute(
                """
                INSERT INTO ingredient_combinations
                  (ingredient_a, ingredient_b, cooccurrence_count, review_status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    row.get("ingredient_a", ""),
                    row.get("ingredient_b", ""),
                    int(row.get("cooccurrence_count") or 0),
                    row.get("review_status", ""),
                ),
            )


def compile_database(output_path: Path) -> None:
    if output_path.exists():
        output_path.unlink()
    conn = sqlite3.connect(output_path)
    try:
        load_schema(conn)
        load_ingredients(conn)
        load_aliases(conn)
        load_facts(conn)
        load_regulatory_status(conn)
        load_history(conn)
        load_registry(conn)
        load_generated_stats(conn)
        conn.commit()
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    compile_database(args.output)
    print(f"Wrote SQLite database to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
