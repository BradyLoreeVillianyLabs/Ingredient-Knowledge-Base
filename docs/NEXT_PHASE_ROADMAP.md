# Next Phase Roadmap

## Phase 1: Source verification

Goal: convert high-risk `needs_source` rows into citation-backed rows.

Priority order:

1. Canadian allergen and sulfite rules
2. US major allergen rules
3. FDA color additive status
4. Health Canada food additive permissions
5. FDA additive status rows
6. EU additive differences for high-attention ingredients

Deliverables:

- Add `citation_id` columns to regulatory/fact/history tables where needed.
- Mark verified rows as `reviewed`.
- Keep ambiguous rows as `needs_source`.

## Phase 2: Open Food Facts mining

Goal: produce real-world ingredient frequency and co-occurrence data.

Deliverables:

- `data/generated/ingredient_frequency.csv`
- `data/generated/ingredient_combinations.csv`
- `data/generated/unknown_ingredient_candidates.csv`

Recommended process:

1. Download a sample export locally.
2. Run `scripts/mine_openfoodfacts.py`.
3. Review top 1,000 mined ingredient names.
4. Promote reviewed terms into curated ingredient CSVs.
5. Add alias corrections for OCR and spelling variants.

## Phase 3: App-ready evidence packs

Goal: make scan results useful and safe.

Each evidence pack should include:

- plain-language description
- functional purpose
- common foods
- aliases
- allergen flags
- jurisdiction-sensitive warnings
- citations
- uncertainty level

## Phase 4: Product integration

Goal: compile the CSV package into the app database.

Recommended target:

- SQLite for mobile/local cache
- Postgres for hosted API
- DuckDB for offline analytics and mining

## Phase 5: Quality gates

Add tests for:

- duplicate ingredient IDs
- duplicate aliases pointing to conflicting ingredient IDs
- missing citations for `reviewed` regulatory rows
- invalid jurisdiction codes
- unsafe medical language in public app facts
