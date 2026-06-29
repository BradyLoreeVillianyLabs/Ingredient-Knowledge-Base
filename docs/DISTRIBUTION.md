# Distribution Guide

This repository can produce several distribution formats.

## Build command

```bash
python scripts/build_all.py
```

Default SQLite output:

```text
dist/ingredient_knowledge_base.sqlite
```

Generated but usually uncommitted outputs:

```text
data/generated/ingredient_alias_index.csv
data/generated/json/*.json
data/generated/evidence_packs/*.json
data/generated/evidence_packs_index.json
docs/DATASET_REPORT.md
```

## Distribution formats

### CSV package

Best for transparent review and editing.

Contains:

```text
data/**/*.csv
schema/*.csv
schema/*.sql
docs/*.md
```

### SQLite package

Best for mobile/local app cache.

Generated with:

```bash
python scripts/build_all.py --sqlite-output dist/ingredient_knowledge_base.sqlite
```

### JSON package

Best for static hosting, API seeding, and frontend prototypes.

Generated with:

```bash
python scripts/build_alias_index.py
python scripts/export_json_pack.py
python scripts/build_evidence_packs.py
```

### Evidence packs

Best for scan-result pages.

Each file includes:

- ingredient identity
- category
- aliases
- facts
- regulatory status rows
- history rows
- display safety flags

## Release recommendation

For a GitHub release, attach:

1. `ingredient_knowledge_base.sqlite`
2. zipped CSV package
3. zipped JSON package
4. `DATASET_REPORT.md`

## Versioning

Suggested progression:

- `v0.1.0`: seeded CSV schema
- `v0.2.0`: generated aliases + SQLite compile
- `v0.3.0`: source registry + citation framework
- `v0.4.0`: first Open Food Facts mined frequency pack
- `v1.0.0`: reviewed public core pack
