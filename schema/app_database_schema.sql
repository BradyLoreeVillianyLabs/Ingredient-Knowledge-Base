-- App database schema for Ingredient Knowledge Base
-- Target: SQLite-compatible baseline. PostgreSQL can add indexes/types later.

CREATE TABLE IF NOT EXISTS ingredients (
  ingredient_id TEXT PRIMARY KEY,
  canonical_name TEXT NOT NULL,
  category TEXT NOT NULL,
  subcategory TEXT,
  source_type TEXT,
  functional_purpose TEXT,
  common_foods TEXT,
  history_estimate TEXT,
  app_note TEXT,
  risk_note TEXT,
  review_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient_aliases (
  alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ingredient_id TEXT NOT NULL,
  canonical_name TEXT NOT NULL,
  alias TEXT NOT NULL,
  normalized_alias TEXT NOT NULL,
  source_file TEXT,
  review_status TEXT NOT NULL,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE INDEX IF NOT EXISTS idx_ingredient_aliases_normalized
  ON ingredient_aliases(normalized_alias);

CREATE TABLE IF NOT EXISTS ingredient_facts (
  fact_id TEXT PRIMARY KEY,
  ingredient_id TEXT NOT NULL,
  canonical_name TEXT,
  fact_type TEXT,
  fact_text TEXT NOT NULL,
  evidence_level TEXT,
  review_status TEXT NOT NULL,
  citation_id TEXT,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE IF NOT EXISTS ingredient_regulatory_status (
  regulatory_id TEXT PRIMARY KEY,
  ingredient_id TEXT NOT NULL,
  canonical_name TEXT,
  jurisdiction TEXT NOT NULL,
  status TEXT NOT NULL,
  allowed_use_notes TEXT,
  requires_warning TEXT,
  review_status TEXT NOT NULL,
  citation_id TEXT,
  notes TEXT,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE IF NOT EXISTS ingredient_history (
  history_id TEXT PRIMARY KEY,
  ingredient_id TEXT NOT NULL,
  canonical_name TEXT,
  history_estimate TEXT,
  confidence TEXT,
  region_or_origin TEXT,
  notes TEXT,
  review_status TEXT NOT NULL,
  citation_id TEXT,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE IF NOT EXISTS source_registry (
  source_id TEXT PRIMARY KEY,
  source_name TEXT NOT NULL,
  source_type TEXT,
  homepage_url TEXT,
  download_url TEXT,
  license_or_terms TEXT,
  priority TEXT,
  use_case TEXT,
  review_status TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS citation_registry (
  citation_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  applies_to TEXT,
  claim_scope TEXT,
  review_status TEXT,
  notes TEXT,
  FOREIGN KEY (source_id) REFERENCES source_registry(source_id)
);

CREATE TABLE IF NOT EXISTS ingredient_frequency (
  ingredient_name TEXT PRIMARY KEY,
  product_count INTEGER NOT NULL,
  top_category TEXT,
  top_country TEXT,
  raw_example TEXT,
  review_status TEXT
);

CREATE TABLE IF NOT EXISTS ingredient_combinations (
  combination_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ingredient_a TEXT NOT NULL,
  ingredient_b TEXT NOT NULL,
  cooccurrence_count INTEGER NOT NULL,
  review_status TEXT
);

CREATE TABLE IF NOT EXISTS unknown_ingredient_candidates (
  candidate_name TEXT PRIMARY KEY,
  product_count INTEGER NOT NULL,
  raw_example TEXT,
  review_status TEXT
);
