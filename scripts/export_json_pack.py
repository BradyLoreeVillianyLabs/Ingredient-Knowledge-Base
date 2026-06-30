#!/usr/bin/env python3
"""Export API-ready JSON ingredient packs from CSV/SQLite-ready data.

Output:
  data/generated/json/ingredients.json
  data/generated/json/aliases.json
  data/generated/json/facts.json
  data/generated/json/regulatory_status.json
  data/generated/json/history.json
  data/generated/json/sources.json

Run after:
  python scripts/build_alias_index.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "generated" / "json"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_json(name: str, rows: list[dict[str, str]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {path}")


def collect_ingredients() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if "metadata" in path.parts or "generated" in path.parts:
            continue
        for row in read_csv(path):
            ingredient_id = (row.get("ingredient_id") or "").strip()
            if not ingredient_id or ingredient_id in seen:
                continue
            seen.add(ingredient_id)
            row = dict(row)
            row["source_file"] = str(path.relative_to(ROOT))
            rows.append(row)
    return rows


def main() -> int:
    write_json("ingredients.json", collect_ingredients())
    write_json("aliases.json", read_csv(DATA_DIR / "generated" / "ingredient_alias_index.csv"))
    write_json("facts.json", read_csv(DATA_DIR / "metadata" / "16_ingredient_facts.csv"))
    write_json("regulatory_status.json", read_csv(DATA_DIR / "metadata" / "15_regulatory_status.csv"))
    write_json("history.json", read_csv(DATA_DIR / "metadata" / "17_historical_use.csv"))
    write_json("sources.json", read_csv(DATA_DIR / "metadata" / "source_registry.csv"))
    write_json("citations.json", read_csv(DATA_DIR / "metadata" / "citation_registry.csv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
