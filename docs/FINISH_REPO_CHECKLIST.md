# Finish Repo Checklist

This checklist defines when the Ingredient Knowledge Base can be considered finished for the first app-ready release.

## Current state

- CI validation pipeline passes on the latest PR head.
- The package builds CSV, JSON, SQLite, evidence packs, dataset report, missing-data report, and 500 generated rich ingredient profiles.
- A backup branch exists at `backup/ingredient-list-package-before-squash` before history cleanup.

## Required before v0.1.0 release

### 1. Clean Git history

The feature branch accumulated many intermediate commits while the database was being built. Before merging, squash the PR branch into one clean commit so old failed check runs no longer clutter the PR.

Recommended command sequence:

```bash
git fetch origin
git checkout feature/ingredient-list-package
git branch backup/local-ingredient-list-package-before-squash
git reset --soft origin/main
git commit -m "feat: build ingredient knowledge base package"
git push --force-with-lease origin feature/ingredient-list-package
```

The remote backup branch `backup/ingredient-list-package-before-squash` preserves the pre-squash branch state.

### 2. Confirm CI after squash

After force-pushing the squashed branch, confirm the latest `Validate ingredient CSVs` workflow run passes.

Required passing steps:

- Python syntax check
- CSV validation
- alias index generation
- rich ingredient profile generation
- quality gates
- JSON export
- evidence-pack build
- dataset report
- missing-data audit
- SQLite compile
- release ZIP packaging
- smoke tests
- generated artifact checks
- 500 rich profile row-count check

### 3. Merge PR #1

Merge the clean PR into `main` only after the squashed commit is green.

### 4. Tag the release

After merging:

```bash
git checkout main
git pull origin main
git tag v0.1.0
git push origin v0.1.0
```

### 5. Preserve citation discipline

For v0.1.0, public-facing app logic must follow this rule:

- `reviewed` rows require a public citation ID.
- `draft` and `needs_source` rows can exist, but the app must display uncertainty or hide verified-style claims.
- No unreachable, private, dead, or vague source links should be used for reviewed claims.

### 6. App integration acceptance

Before calling the repo product-ready, test one app ingestion path using either:

- `Food-Ingredient-Analyzer`
- `FoodLabelAnalyzerPic2Facts`

The app should consume:

- SQLite database
- JSON package
- evidence packs
- alias index
- allergen label terms
- color additive label terms
- sweetener label terms
- report sections
- scan badges
- uncertainty flags
- rich ingredient profiles

## Definition of finished for v0.1.0

The repo is finished for v0.1.0 when:

- The PR history is squashed or otherwise clean.
- CI is green on the final commit.
- PR #1 is merged into `main`.
- A `v0.1.0` tag exists.
- Generated package artifacts build successfully.
- Citation policy is documented and enforced by quality gates.
- Draft/unverified content is clearly separated from reviewed content.
- App integration instructions are present and usable.

## Recommended v0.2.0 work

- Replace remaining `needs_source` rows in batches.
- Attach row-level citations for top additives, sweeteners, allergens, colors, preservatives, and compounds.
- Replace templated rich-profile rows with row-specific stories, fun facts, odd uses, and citations.
- Mine Open Food Facts bulk data for frequency and co-occurrence signals.
- Add app-facing tests for real OCR label examples.
