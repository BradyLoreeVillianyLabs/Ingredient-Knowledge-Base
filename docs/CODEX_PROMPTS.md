# Codex Prompts

Use these prompts to continue the project in implementation mode.

## 1. Build app ingestion package

```text
You are working in the Ingredient-Knowledge-Base repository. Implement a robust ingestion command that runs:

1. scripts/validate_csvs.py
2. scripts/build_alias_index.py
3. scripts/quality_gate.py
4. scripts/export_json_pack.py
5. scripts/build_evidence_packs.py
6. scripts/build_dataset_report.py
7. scripts/compile_sqlite.py --output dist/ingredient_knowledge_base.sqlite

Add a single command entrypoint, tests, and docs. Do not commit raw Open Food Facts exports.
```

## 2. Add source-backed Canadian allergen verification

```text
Use official Canadian sources only. Update data/metadata/source_registry.csv and citation_registry.csv if needed. Add citation_id columns where needed. Verify Canadian priority allergen and sulphite rows. Convert only fully source-backed rows to reviewed. Keep uncertain rows as needs_source. Do not make medical claims.
```

## 3. Mine Open Food Facts sample

```text
Download or use a local Open Food Facts sample export. Run scripts/mine_openfoodfacts.py. Inspect the top 1000 terms. Use scripts/promote_mined_terms.py to create a review file. Curate the top 100 high-frequency terms into existing CSV categories. Preserve raw examples and do not create safety claims.
```

## 4. Build label analyzer prototype

```text
Create a small Python package that loads data/generated/evidence_packs_index.json and evidence pack files. Implement analyze_label(raw_text, jurisdiction='Canada') that tokenizes ingredient labels, matches aliases, returns matched ingredients, unmatched terms, warnings, and uncertainty notes. Include tests with OCR misspellings from data/metadata/14_ocr_aliases.csv.
```

## 5. Expand facts safely

```text
Expand data/metadata/16_ingredient_facts.csv to at least 500 rows. Keep every fact short, neutral, and app-friendly. Mark unsupported health/regulatory claims as needs_source. Only mark reviewed when citation_id is present and source-backed. Avoid medical claims.
```
