# Ingredient Knowledge Base Build Plan

## Current package

The package now establishes the file structure, core schema, validation script, CI workflow, and eighteen seeded lists:

1. Core ingredients
2. Preservatives
3. Sweeteners
4. Emulsifiers, stabilizers, and thickeners
5. Food colors
6. Common allergens
7. Oils and fats
8. Vitamins
9. Minerals
10. Amino acids
11. Flavor enhancers
12. Spices and herbs
13. Food compounds
14. OCR aliases
15. Regulatory status
16. Ingredient facts
17. Historical use
18. Common combinations

## Iteration loop

For each new list:

1. Create a CSV under the correct `data/` subfolder.
2. Use the standard schema from `schema/ingredient_list_schema.csv` unless the list is metadata-only.
3. Mark unsupported or jurisdiction-specific claims as `needs_source`.
4. Run `python scripts/validate_csvs.py`.
5. Commit the list.
6. Update `data/metadata/list_manifest.csv` from `planned` to `seeded` or `reviewed`.

## Next phase

The initial schema is now seeded. The next phase should expand row counts and add source-backed citations:

- Expand core ingredients toward 500 rows.
- Expand food compounds toward 1,000 rows.
- Expand OCR aliases toward 5,000 rows using OCR error mining.
- Expand ingredient facts toward 5,000 app-ready facts.
- Add source URLs and citation IDs for regulatory and safety-sensitive rows.
- Mine Open Food Facts for frequency and co-occurrence statistics.

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
