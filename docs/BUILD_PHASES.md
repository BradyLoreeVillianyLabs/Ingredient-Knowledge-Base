# Ingredient Knowledge Base Build Phases

## Phase 0 - Repository foundation

Goal: create the durable package structure so every future data list is predictable.

Deliverables:
- README
- canonical CSV schema
- folder structure
- validation script
- CI workflow
- list manifest
- build plan

Status: started in PR #1.

## Phase 1 - Human-readable ingredient lists

Goal: generate broad, app-friendly lists that help the product recognize and explain common label ingredients.

Deliverables:
- core ingredients
- preservatives
- sweeteners
- emulsifiers
- stabilizers
- thickeners
- colors
- allergens
- oils and fats
- vitamins
- minerals
- amino acids
- flavor enhancers
- herbs and spices

Output quality: usable as draft app seed data. Rows that need citations or jurisdiction review stay marked `needs_source`.

## Phase 2 - Alias and OCR intelligence

Goal: make the scanner resilient to real package labels and camera/OCR mistakes.

Deliverables:
- ingredient aliases
- E-number aliases
- multilingual names
- OCR misspellings
- punctuation-normalized names
- parenthetical ingredient parsing examples
- brand/category-specific term variants

## Phase 3 - Evidence and safety layer

Goal: separate neutral facts from safety-sensitive claims.

Deliverables:
- source-backed facts
- regulatory status by jurisdiction
- allergen flags
- dietary flags
- evidence confidence
- risk-summary templates
- app disclaimer language

## Phase 4 - Large source ingestion

Goal: ingest high-volume public datasets rather than manually authoring every row.

Primary targets:
- Open Food Facts products and ingredient strings
- USDA FoodData Central nutrition references
- additive/regulatory lists from official agencies
- food-compound datasets where licensing permits

Deliverables:
- source registry
- raw import scripts
- normalized ingredient tables
- product-to-ingredient relationship tables
- duplicate and synonym detection

## Phase 5 - Derived intelligence

Goal: create unique app value from the raw database.

Deliverables:
- ingredient frequency by category
- ingredient frequency by country
- brand/category co-occurrence
- common ingredient combinations
- emerging ingredient detection
- replacement/substitution groups
- scan confidence scoring

## Phase 6 - App-ready compiled package

Goal: make the knowledge base fast and easy to ship inside the app.

Deliverables:
- compiled SQLite or DuckDB database
- JSON indexes for mobile lookup
- search index
- embedding-ready text chunks
- versioned releases
- changelog

## Phase 7 - Review, QA, and release governance

Goal: prevent false claims and dataset drift.

Deliverables:
- review queues
- source-required gates
- CI validation
- changelog checks
- field completeness reports
- human review workflow for sensitive rows

## Cycling rule

Each generation cycle should:

1. Pick the next `planned` list from `data/metadata/list_manifest.csv`.
2. Create the CSV in the right folder.
3. Use the canonical schema when the list describes ingredients.
4. Mark uncertain or safety-sensitive claims as `needs_source`.
5. Update the manifest row from `planned` to `seeded`.
6. Run CSV validation through CI.
7. Continue to the next list.
