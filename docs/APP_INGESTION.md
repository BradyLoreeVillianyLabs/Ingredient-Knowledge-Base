# App Ingestion Guide

This repository should be treated as a versioned ingredient intelligence package.

## Recommended ingestion flow

1. Pull the repository at a pinned commit SHA or release tag.
2. Validate CSVs with:

```bash
python scripts/validate_csvs.py
```

3. Generate alias lookup tables:

```bash
python scripts/build_alias_index.py
```

4. Optional: mine Open Food Facts exports:

```bash
python scripts/mine_openfoodfacts.py \
  --input data/raw/openfoodfacts_sample.tsv \
  --output-dir data/generated \
  --max-rows 100000
```

5. Compile CSVs into app database tables.

## Recommended app tables

### `ingredients`

Primary fields:

- `ingredient_id`
- `canonical_name`
- `category`
- `subcategory`
- `source_type`
- `functional_purpose`
- `app_note`
- `risk_note`
- `review_status`

### `ingredient_aliases`

Primary fields:

- `ingredient_id`
- `alias`
- `normalized_alias`
- `source_file`

### `ingredient_facts`

Primary fields:

- `fact_id`
- `ingredient_id`
- `fact_type`
- `fact_text`
- `evidence_level`
- `review_status`

### `ingredient_regulatory_status`

Primary fields:

- `ingredient_id`
- `jurisdiction`
- `status`
- `requires_warning`
- `allowed_use_notes`
- `review_status`

### `ingredient_frequency`

Primary fields:

- `ingredient_name`
- `product_count`
- `top_category`
- `top_country`

### `ingredient_combinations`

Primary fields:

- `ingredient_a`
- `ingredient_b`
- `cooccurrence_count`

## Runtime matching order

For OCR labels:

1. Preserve original label text.
2. Normalize the detected text.
3. Check exact alias match.
4. Check OCR alias corrections.
5. Check fuzzy match only when confidence is high.
6. Mark unmatched terms as `unknown_ingredient_candidates`.
7. Do not show safety claims for unmatched or low-confidence matches.

For barcodes:

1. Check local product cache.
2. Check Open Food Facts API fallback.
3. Save normalized product + ingredients locally.
4. Record source and timestamp.

## Safety display rules

- `reviewed`: can be shown with citation.
- `needs_source`: show only as draft/internal or with a visible uncertainty label.
- `draft`: suitable for general educational facts, not medical/regulatory claims.
- `mined`: statistical signal only, not a curated fact.
