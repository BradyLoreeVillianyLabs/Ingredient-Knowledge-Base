# Ingredient Knowledge Base Build Plan

## Current package

The first package establishes the file structure, core schema, validation script, CI workflow, and seven seeded lists:

1. Core ingredients
2. Preservatives
3. Sweeteners
4. Emulsifiers, stabilizers, and thickeners
5. Food colors
6. Common allergens
7. Oils and fats

## Iteration loop

For each new list:

1. Create a CSV under the correct `data/` subfolder.
2. Use the standard schema from `schema/ingredient_list_schema.csv` unless the list is metadata-only.
3. Mark unsupported or jurisdiction-specific claims as `needs_source`.
4. Run `python scripts/validate_csvs.py`.
5. Commit the list.
6. Update `data/metadata/list_manifest.csv` from `planned` to `seeded` or `reviewed`.

## Next lists to build

- Vitamins
- Minerals
- Amino acids
- Flavor enhancers
- Spices and herbs
- Food compounds
- OCR aliases
- Regulatory status
- Ingredient facts
- Historical use
- Common combinations mined from Open Food Facts

## App integration recommendation

The app should ingest this repository as a versioned package. Use the CSV files as source-of-truth seed data, then compile them into SQLite, DuckDB, or Postgres tables for fast lookup.

Recommended compiled tables:

- ingredients
- ingredient_aliases
- ingredient_categories
- ingredient_safety_flags
- ingredient_facts
- ingredient_regulatory_status
- ingredient_history
- source_imports

## Guardrails

- Do not present draft rows as verified science.
- Do not make medical claims without sources.
- Keep allergen and regulatory logic jurisdiction-aware.
- Preserve the original label text when matching OCR output.
