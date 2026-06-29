# Ingredient Knowledge Base API Contract

This document describes the shape your app/API should expose after compiling this package.

## Core endpoint shapes

### `GET /ingredients/{ingredient_id}`

Returns one evidence pack.

```json
{
  "ingredient_id": "ing_salt",
  "canonical_name": "Salt",
  "category": "core",
  "subcategory": "mineral seasoning",
  "source_type": "mineral",
  "functional_purpose": "flavor and preservation",
  "common_foods": "bread|snacks|pickles",
  "app_note": "...",
  "risk_note": "...",
  "review_status": "draft",
  "aliases": [],
  "facts": [],
  "regulatory_status": [],
  "history": [],
  "display_safety": {
    "can_show_as_verified": false,
    "requires_uncertainty_label": true,
    "hide_medical_claims": true
  }
}
```

### `GET /ingredients/search?q={query}`

Returns alias-matched ingredient candidates.

```json
{
  "query": "sodlum chloride",
  "normalized_query": "sodium chloride",
  "matches": [
    {
      "ingredient_id": "ing_salt",
      "canonical_name": "Salt",
      "alias": "sodium chloride",
      "match_type": "ocr_alias",
      "confidence": 0.92
    }
  ]
}
```

### `POST /labels/analyze`

Input:

```json
{
  "raw_text": "INGREDIENTS: wheat flour, sugar, soybean oil, salt",
  "jurisdiction": "Canada",
  "include_draft_content": false
}
```

Output:

```json
{
  "original_text": "INGREDIENTS: wheat flour, sugar, soybean oil, salt",
  "jurisdiction": "Canada",
  "matched_ingredients": [],
  "unmatched_terms": [],
  "warnings": [],
  "uncertainty_notes": []
}
```

## Display rules

- `reviewed`: may be shown as verified if citation is present.
- `needs_source`: show only if internal/debug mode is enabled, or display with visible uncertainty.
- `draft`: suitable for general educational copy, not regulatory/safety claims.
- `generated`: machine-generated lookup data; do not show as a fact.
- `mined`: statistical product-data signal; do not show as a curated fact.

## Matching rules

Recommended order:

1. Exact normalized alias match.
2. OCR alias correction match.
3. High-confidence fuzzy match.
4. Unknown term queue.

Always preserve the user's original label text for auditability.
