# Contributing

## Principles

1. Preserve original ingredient label text.
2. Separate mined data from reviewed data.
3. Never turn a draft row into a medical or regulatory claim without citations.
4. Prefer additive, reviewable CSV changes over giant untraceable rewrites.
5. Keep jurisdiction-specific logic explicit.

## Row status meanings

- `draft`: usable for general educational content, not verified claims.
- `needs_source`: needs citation before being shown as fact/regulatory/safety content.
- `reviewed`: citation-backed and ready for public display.
- `generated`: produced by scripts.
- `mined`: extracted statistically from product data.

## Adding a new curated ingredient row

1. Add the row to the best category CSV under `data/`.
2. Use a stable `ingredient_id`.
3. Add aliases in `common_aliases` using pipe separators.
4. Keep `risk_note` neutral.
5. Mark as `needs_source` if safety, health, or regulatory language is present.
6. Run:

```bash
python scripts/validate_csvs.py
python scripts/build_alias_index.py
python scripts/quality_gate.py
python scripts/compile_sqlite.py --output /tmp/ingredient_knowledge_base.sqlite
```

## Adding citations

1. Add the source to `data/metadata/source_registry.csv` if it is new.
2. Add the citation to `data/metadata/citation_registry.csv`.
3. Add `citation_id` to the relevant row if the table supports it.
4. Only then move `review_status` to `reviewed`.

## Mined Open Food Facts terms

1. Generate frequency stats with `scripts/mine_openfoodfacts.py`.
2. Promote high-frequency terms with `scripts/promote_mined_terms.py`.
3. Review promoted terms manually or with a review agent.
4. Move accepted rows into curated files.
5. Keep uncertain rows in the review queue.
