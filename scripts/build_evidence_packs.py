#!/usr/bin/env python3
"""Build per-ingredient evidence packs for app scan results.

Output:
  data/generated/evidence_packs/<ingredient_id>.json
  data/generated/evidence_packs_index.json

Each pack is safe-by-design: it includes review status and does not hide uncertainty.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "generated" / "evidence_packs"
INDEX_PATH = DATA_DIR / "generated" / "evidence_packs_index.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def collect_ingredients() -> dict[str, dict[str, str]]:
    ingredients: dict[str, dict[str, str]] = {}
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if "metadata" in path.parts or "generated" in path.parts:
            continue
        for row in read_csv(path):
            ingredient_id = (row.get("ingredient_id") or "").strip()
            if ingredient_id and ingredient_id not in ingredients:
                row = dict(row)
                row["source_file"] = str(path.relative_to(ROOT))
                ingredients[ingredient_id] = row
    return ingredients


def group_by_ingredient(path: Path) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(path):
        ingredient_id = (row.get("ingredient_id") or "").strip()
        if ingredient_id:
            grouped[ingredient_id].append(row)
    return grouped


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ingredients = collect_ingredients()
    aliases = group_by_ingredient(DATA_DIR / "generated" / "ingredient_alias_index.csv")
    facts = group_by_ingredient(DATA_DIR / "metadata" / "16_ingredient_facts.csv")
    regulatory = group_by_ingredient(DATA_DIR / "metadata" / "15_regulatory_status.csv")
    history = group_by_ingredient(DATA_DIR / "metadata" / "17_historical_use.csv")

    index = []
    for ingredient_id, ingredient in sorted(ingredients.items()):
        pack = {
            "ingredient_id": ingredient_id,
            "canonical_name": ingredient.get("canonical_name", ""),
            "category": ingredient.get("category", ""),
            "subcategory": ingredient.get("subcategory", ""),
            "source_type": ingredient.get("source_type", ""),
            "functional_purpose": ingredient.get("functional_purpose", ""),
            "common_foods": ingredient.get("common_foods", ""),
            "app_note": ingredient.get("app_note", ""),
            "risk_note": ingredient.get("risk_note", ""),
            "review_status": ingredient.get("review_status", ""),
            "source_file": ingredient.get("source_file", ""),
            "aliases": aliases.get(ingredient_id, []),
            "facts": facts.get(ingredient_id, []),
            "regulatory_status": regulatory.get(ingredient_id, []),
            "history": history.get(ingredient_id, []),
            "display_safety": {
                "can_show_as_verified": ingredient.get("review_status") == "reviewed",
                "requires_uncertainty_label": ingredient.get("review_status") in {"draft", "needs_source"},
                "hide_medical_claims": True,
            },
        }
        out_path = OUT_DIR / f"{ingredient_id}.json"
        out_path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        index.append(
            {
                "ingredient_id": ingredient_id,
                "canonical_name": ingredient.get("canonical_name", ""),
                "pack_path": str(out_path.relative_to(ROOT)),
                "review_status": ingredient.get("review_status", ""),
            }
        )

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(index)} evidence packs to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
