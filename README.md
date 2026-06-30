# Ingredient Knowledge Base

A structured, app-ready ingredient intelligence dataset for the Food Ingredient Analyzer project.

This repository now functions as a versioned package for ingredient search, label parsing, evidence display, and downstream app integration. It combines curated CSV knowledge with generated lookup artifacts, SQLite output, and release documentation so the dataset can be consumed by apps and analysts without re-deriving the base structure.

## What is included

- Curated ingredient lists across core foods, additives, allergens, nutrition, culinary categories, and metadata
- Alias and OCR-normalization data for label parsing and scanner matching
- Rich ingredient profiles and evidence packs for explainable app experiences
- JSON and SQLite exports for app integration and offline use
- Validation, build, and quality-gate scripts so the package can be regenerated consistently

## Directory structure

```text
data/
  core/
  additives/
  nutrition/
  safety/
  culinary/
  metadata/
  generated/
schema/
scripts/
docs/
dist/
.github/workflows/
```

## Common workflows

```bash
python scripts/check_python_syntax.py
python scripts/validate_csvs.py
python scripts/build_all.py --skip-release-zips
python tests/smoke_test_pipeline.py
```

## Important note

This dataset is for educational ingredient analysis. It should not be presented as medical advice. Health, allergy, and regulatory statements should be cited and reviewed before production use.
