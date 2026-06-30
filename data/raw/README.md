# Raw Data Directory

Place large downloaded source files here for local processing only.

Do **not** commit full raw exports such as the complete Open Food Facts CSV/TSV dump unless the repository is intentionally configured for large files.

Recommended local files:

```text
data/raw/openfoodfacts_sample.tsv
data/raw/openfoodfacts_full.csv.gz
```

Processing example:

```bash
python scripts/mine_openfoodfacts.py \
  --input data/raw/openfoodfacts_sample.tsv \
  --output-dir data/generated \
  --max-rows 100000
```

Generated files belong in `data/generated/`.
