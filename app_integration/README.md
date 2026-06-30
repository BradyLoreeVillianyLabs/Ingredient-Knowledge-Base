# App Integration Assets

This folder contains reusable code and instructions for integrating the Ingredient Knowledge Base into app projects such as:

- `BradyLoreeVillianyLabs/Food-Ingredient-Analyzer`
- `BradyLoreeVillianyLabs/FoodLabelAnalyzerPic2Facts`

The integration target is simple:

1. Build this knowledge-base package.
2. Copy generated artifacts into the app project.
3. Load evidence packs and alias indexes in the app.
4. Match OCR ingredient text to canonical ingredient IDs.
5. Show facts only according to review status and display-safety flags.

## Recommended app asset layout

```text
app/
  data/
    ingredient-kb/
      ingredient_knowledge_base.sqlite
      json/
      evidence_packs/
      evidence_packs_index.json
```

## Build source package

```bash
python scripts/build_all.py
```

## Sync to app project

```bash
python app_integration/sync_to_app.py \
  --app-root ../Food-Ingredient-Analyzer \
  --target-subdir app/data/ingredient-kb
```

For another app repo:

```bash
python app_integration/sync_to_app.py \
  --app-root ../FoodLabelAnalyzerPic2Facts \
  --target-subdir app/data/ingredient-kb
```
