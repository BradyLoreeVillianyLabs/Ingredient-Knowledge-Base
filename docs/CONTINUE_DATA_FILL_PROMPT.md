# Continue Data Fill Prompt

Use this prompt with Codex or another coding agent when continuing the database fill.

```text
You are working in the Ingredient-Knowledge-Base repository.

Goal: continue filling the database with useful ingredient data until all manifest sections are populated.

Rules:
1. Do not add vague placeholder values like `needs_source` unless a row truly cannot be described safely.
2. Prefer concrete, stable food-function facts: what the ingredient is, why it appears on labels, common foods, source type, allergen/diet flags, and neutral cautions.
3. Do not make medical claims, disease claims, or universal regulatory claims without citations.
4. Use `reviewed` for stable non-medical food-function rows.
5. Use `draft` only for broad but useful rows that still need refinement.
6. Keep every CSV parseable.
7. Run `python scripts/build_all.py` and `python tests/smoke_test_pipeline.py` after edits.

Next sections to add or expand:
- fermented foods and cultures
- enzymes
- legumes nuts and seeds
- beverages and stimulant sources
- packaging/contact watchlist
- source-backed regulatory rows
- public citation registry rows
- more OCR alias rows
- ingredient combinations
- ingredient facts
- historical use rows

For every new ingredient list, use this header:

ingredient_id,canonical_name,category,subcategory,common_aliases,source_type,functional_purpose,common_foods,history_estimate,app_note,risk_note,review_status

For app-support files, use clear columns and include `review_status`.
```
