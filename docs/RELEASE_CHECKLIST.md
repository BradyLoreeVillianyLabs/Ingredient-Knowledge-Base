# Release Checklist

Use this before tagging a dataset release for app ingestion.

## Required checks

- [ ] `python scripts/validate_csvs.py` passes.
- [ ] `python scripts/build_alias_index.py` passes.
- [ ] `python scripts/quality_gate.py` passes.
- [ ] `python scripts/compile_sqlite.py --output /tmp/ingredient_knowledge_base.sqlite` passes.
- [ ] No `reviewed` regulatory rows are missing `citation_id`.
- [ ] No public app fact contains unsupported medical language.
- [ ] All P0 review queue items are closed or explicitly deferred.
- [ ] Source registry has license/terms reviewed for every external dataset.
- [ ] Raw exports are not committed to git.

## App safety checks

- [ ] App can distinguish `draft`, `needs_source`, `reviewed`, `generated`, and `mined` rows.
- [ ] App does not show `needs_source` rows as verified claims.
- [ ] App preserves original OCR text.
- [ ] App shows uncertainty for fuzzy matches.
- [ ] App supports jurisdiction-specific allergen/regulatory display.

## Release artifact options

- CSV package only
- CSV + generated alias index
- CSV + SQLite database
- CSV + SQLite + Open Food Facts mined stats

## Suggested versioning

Use semantic-ish dataset versions:

- `v0.1.0` initial seeded schema
- `v0.2.0` source/citation framework
- `v0.3.0` first mined OFF stats
- `v1.0.0` reviewed public-ready core ingredient pack
