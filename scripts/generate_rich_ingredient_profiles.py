#!/usr/bin/env python3
"""Generate the first 500 rich ingredient profiles for app use.

Output:
  data/generated/rich_ingredient_profiles.csv

These rows are intentionally `draft` unless a row-level public citation is added.
They are app-friendly enrichment rows: health-conscious context, feel-good story,
fun fact, odd use, and quip. They are not medical or regulatory advice.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "generated" / "rich_ingredient_profiles.csv"

GROUPS = {
"core_staple": "Water|Salt|Sugar|Wheat Flour|Whole Wheat Flour|Bread Flour|Cake Flour|All-Purpose Flour|Rice Flour|Brown Rice Flour|Corn Flour|Cornmeal|Cornstarch|Potato Starch|Tapioca Starch|Arrowroot Starch|Oat Flour|Barley Flour|Rye Flour|Buckwheat Flour|Sorghum Flour|Millet Flour|Quinoa Flour|Chickpea Flour|Almond Flour|Coconut Flour|Cassava Flour|Semolina|Durum Wheat|Bulgur|Couscous|Rolled Oats|Steel-Cut Oats|White Rice|Brown Rice|Wild Rice|Jasmine Rice|Basmati Rice|Arborio Rice|Black Rice|Red Rice|Corn|Popcorn|Hominy|Masa Harina|Quinoa|Amaranth|Teff|Farro|Spelt|Freekeh|Wheat Germ|Wheat Bran|Oat Bran|Rice Bran",
"oil_fat": "Olive Oil|Extra Virgin Olive Oil|Canola Oil|Soybean Oil|Corn Oil|Sunflower Oil|Safflower Oil|Peanut Oil|Sesame Oil|Avocado Oil|Coconut Oil|Palm Oil|Palm Kernel Oil|Cottonseed Oil|Grapeseed Oil|Rice Bran Oil|Flaxseed Oil|Walnut Oil|Almond Oil|MCT Oil|Butter|Ghee|Cream|Lard|Beef Tallow|Chicken Fat|Duck Fat|Shortening|Margarine|Cocoa Butter|Shea Butter|Vegetable Oil|Hydrogenated Vegetable Oil|Interesterified Oil|High-Oleic Sunflower Oil|High-Oleic Canola Oil",
"sweetener": "Honey|Maple Syrup|Molasses|Brown Sugar|Cane Sugar|Coconut Sugar|Date Sugar|Agave Syrup|Corn Syrup|High Fructose Corn Syrup|Glucose Syrup|Dextrose|Fructose|Maltose|Lactose|Invert Sugar|Golden Syrup|Rice Syrup|Barley Malt Syrup|Sorghum Syrup|Stevia|Steviol Glycosides|Monk Fruit Extract|Erythritol|Xylitol|Sorbitol|Mannitol|Maltitol|Isomalt|Lactitol|Allulose|Aspartame|Sucralose|Saccharin|Acesulfame Potassium|Neotame|Advantame|Thaumatin|Tagatose|Isomaltulose",
"protein_dairy_animal": "Milk|Skim Milk|Whole Milk|Buttermilk|Cream Cheese|Cheddar Cheese|Mozzarella Cheese|Parmesan Cheese|Whey Protein|Whey Protein Isolate|Casein|Caseinate|Greek Yogurt|Yogurt|Kefir|Egg|Egg White|Egg Yolk|Gelatin|Collagen Peptides|Beef|Pork|Chicken|Turkey|Duck|Lamb|Salmon|Tuna|Cod|Pollock|Anchovy|Sardine|Shrimp|Crab|Lobster|Clam|Oyster|Mussel|Scallop|Fish Sauce|Bone Broth|Chicken Broth|Beef Broth",
"plant_protein_legume": "Soy Protein Isolate|Soy Protein Concentrate|Textured Vegetable Protein|Pea Protein|Pea Protein Isolate|Brown Rice Protein|Hemp Protein|Pumpkin Seed Protein|Sunflower Protein|Lentils|Red Lentils|Green Lentils|Chickpeas|Black Beans|Kidney Beans|Pinto Beans|Navy Beans|Cannellini Beans|Great Northern Beans|Lima Beans|Fava Beans|Mung Beans|Adzuki Beans|Black-Eyed Peas|Split Peas|Edamame|Soybeans|Tofu|Tempeh|Miso|Natto|Hummus|Bean Flour|Lupin Flour",
"fruit": "Apple|Applesauce|Apple Juice|Banana|Strawberry|Blueberry|Raspberry|Blackberry|Cranberry|Cherry|Peach|Pear|Plum|Apricot|Mango|Pineapple|Papaya|Guava|Passion Fruit|Kiwi|Orange|Mandarin|Lemon|Lime|Grapefruit|Grape|Raisin|Date|Fig|Prune|Coconut|Coconut Milk|Coconut Cream|Coconut Water|Watermelon|Cantaloupe|Honeydew|Pomegranate|Acai|Goji Berry",
"vegetable": "Tomato|Tomato Paste|Tomato Puree|Carrot|Celery|Onion|Garlic|Potato|Sweet Potato|Yam|Beet|Spinach|Kale|Swiss Chard|Collard Greens|Lettuce|Cabbage|Red Cabbage|Broccoli|Cauliflower|Brussels Sprouts|Asparagus|Green Bean|Pea|Zucchini|Cucumber|Eggplant|Bell Pepper|Jalapeno|Chili Pepper|Mushroom|Shiitake Mushroom|Portobello Mushroom|Pumpkin|Squash|Butternut Squash|Artichoke|Okra|Radish|Turnip|Parsnip|Leek|Scallion|Shallot|Seaweed|Kelp|Nori|Dulse",
"herb_spice": "Black Pepper|White Pepper|Cayenne Pepper|Paprika|Smoked Paprika|Chili Powder|Cumin|Coriander Seed|Cilantro|Parsley|Basil|Oregano|Thyme|Rosemary|Sage|Dill|Mint|Bay Leaf|Fennel Seed|Cardamom|Star Anise|Saffron|Vanilla|Vanilla Extract|Cinnamon|Nutmeg|Mace|Clove|Allspice|Ginger|Turmeric|Mustard Seed|Fenugreek|Caraway Seed|Celery Seed|Poppy Seed|Sesame Seed|Nigella Seed|Sumac|Tarragon|Marjoram|Chives|Lemongrass|Curry Leaf|Wasabi|Horseradish",
"preservative_acid": "Citric Acid|Ascorbic Acid|Acetic Acid|Lactic Acid|Malic Acid|Tartaric Acid|Fumaric Acid|Phosphoric Acid|Sodium Benzoate|Potassium Benzoate|Benzoic Acid|Potassium Sorbate|Sorbic Acid|Calcium Propionate|Sodium Propionate|Propionic Acid|Sodium Nitrite|Sodium Nitrate|Potassium Nitrate|Sulfur Dioxide|Sodium Metabisulfite|Potassium Metabisulfite|Sodium Bisulfite|Calcium Disodium EDTA|BHA|BHT|TBHQ|Natamycin|Nisin|Dimethyl Dicarbonate",
"texture_emulsifier": "Soy Lecithin|Sunflower Lecithin|Mono- and Diglycerides|Distilled Monoglycerides|DATEM|SSL|Calcium Stearoyl Lactylate|Polysorbate 80|Polysorbate 60|Propylene Glycol Esters|Xanthan Gum|Guar Gum|Locust Bean Gum|Gum Arabic|Pectin|Agar|Carrageenan|Konjac Gum|Gellan Gum|Cellulose Gum|Methylcellulose|Hydroxypropyl Methylcellulose|Microcrystalline Cellulose|Modified Food Starch|Pregelatinized Starch|Tara Gum|Karaya Gum|Tragacanth Gum|Sodium Alginate|Calcium Alginate|Propylene Glycol Alginate",
"color": "Red 40|Yellow 5|Yellow 6|Blue 1|Blue 2|Green 3|Red 3|Titanium Dioxide|Caramel Color|Annatto|Beta-Carotene|Paprika Extract|Turmeric Color|Beet Juice Color|Spirulina Extract|Chlorophyll|Carmine|Cochineal Extract|Anthocyanins|Fruit Juice Color|Vegetable Juice Color|Iron Oxides",
"flavor_enhancer": "Monosodium Glutamate|Disodium Inosinate|Disodium Guanylate|Disodium Ribonucleotides|Yeast Extract|Autolyzed Yeast Extract|Hydrolyzed Vegetable Protein|Hydrolyzed Soy Protein|Hydrolyzed Corn Protein|Natural Flavors|Artificial Flavors|Smoke Flavor|Maltol|Ethyl Maltol|Vanillin|Ethyl Vanillin|Soy Sauce Powder|Mushroom Extract|Kombu Extract|Torula Yeast|Worcestershire Sauce|Vinegar Powder|Cheese Powder|Butter Flavor|Chicken Flavor|Beef Flavor",
"vitamin_mineral": "Vitamin A|Vitamin D|Vitamin E|Vitamin K|Vitamin C|Thiamin|Riboflavin|Niacin|Pantothenic Acid|Vitamin B6|Biotin|Folate|Folic Acid|Vitamin B12|Choline|Calcium|Iron|Potassium|Sodium|Magnesium|Zinc|Iodine|Selenium|Copper|Manganese|Chromium|Molybdenum|Phosphorus|Chloride|Fluoride",
"amino_compound": "Alanine|Arginine|Asparagine|Aspartic Acid|Cysteine|Glutamic Acid|Glutamine|Glycine|Histidine|Isoleucine|Leucine|Lysine|Methionine|Phenylalanine|Proline|Serine|Threonine|Tryptophan|Tyrosine",
}

TEMPLATES = {
"core_staple": ("Check refinement level, fiber context, sodium or added sugar around it, and serving size.", "Staples are the quiet backbone of family recipes and local food traditions.", "This ingredient helps form the pantry architecture behind many everyday foods.", "Pantry staples often appear in crafts, cleaning experiments, or kitchen science demos.", "{name} keeps the food world from falling over."),
"oil_fat": ("Check fat source, processing level, smoke point, and saturated versus unsaturated fat context.", "Traditional fats carry stories about groves, farms, dairies, kitchens, and preservation.", "Fats carry aroma compounds, which is why a little can change the whole personality of a dish.", "Oils and fats are also used for seasoning pans, polishing wood, or making soaps.", "{name} is where flavor goes to get a smoother ride."),
"sweetener": ("Check sweetness intensity, added-sugar contribution, sugar-alcohol tolerance, and whether it is used in tiny amounts.", "Sweet ingredients often show up in celebrations, baking rituals, and comfort foods.", "Sweetness can affect browning, moisture, texture, and preservation, not just taste.", "Some sweeteners are used in fermentation, browning tests, or homemade syrups.", "{name} showed up and the label immediately got sweeter."),
"protein_dairy_animal": ("Check protein, allergens, sodium, saturated fat, and degree of processing.", "Protein foods connect to farming, fishing, fermentation, and preservation traditions.", "Protein ingredients can change texture as much as nutrition.", "Some protein ingredients are used in binding, foams, clarification, or traditional craft processes.", "{name} brings the protein and expects a little respect."),
"plant_protein_legume": ("Check fiber, protein, allergen context, sodium, and whether it is an isolate or whole-food ingredient.", "Legumes and plant proteins have fed communities for thousands of years in affordable meals.", "Many plant proteins double as texture builders in modern foods.", "Beans and seeds appear in gardening, fermentation, and craft food projects.", "{name} is plant-powered and not here to whisper."),
"fruit": ("Check added sugar, juice concentration, fiber loss, and whether it is whole, dried, or flavored.", "Fruit ingredients carry orchard, harvest, and seasonal food memories.", "Fruit can bring sweetness, acidity, color, aroma, and moisture all at once.", "Fruit peels, juices, and powders can be used for natural dyes, aromas, or fermentation starters.", "{name} brings snack energy and a little sunshine."),
"vegetable": ("Check whole-food context, added sodium or oil, fiber, and whether it is fresh, dried, powdered, or concentrated.", "Vegetables tell stories of gardens, markets, soups, stews, and family cooking.", "Vegetables can act as flavor bases, colors, thickeners, or texture builders.", "Vegetable scraps and peels are often used for stocks, compost, natural dyes, or garden projects.", "{name} is doing more work than it gets credit for."),
"herb_spice": ("Treat wellness claims cautiously; focus on flavor, sodium replacement, and serving size.", "Herbs and spices are some of the oldest global food storytellers.", "Tiny amounts of aromatic plants can change an entire dish.", "Herbs and spices are often used in sachets, natural dyes, aromas, and companion planting.", "{name} arrived with flavor and absolutely no chill."),
"preservative_acid": ("Check why it is present: acidity, preservation, color protection, oxidation control, or texture.", "Preservation ingredients connect to the long human story of keeping food usable longer.", "Acids and preservatives often work behind the scenes to manage microbes, browning, or shelf life.", "Acids are common in cleaning demos, pH experiments, and kitchen science.", "{name} is the label's tiny shelf-life manager."),
"texture_emulsifier": ("Check whether it modifies texture, keeps mixtures stable, or replaces fat or gluten structure.", "Texture ingredients help foods become consistent, scoopable, spreadable, pourable, or creamy.", "A small amount can dramatically change thickness or mouthfeel.", "Gums and emulsifiers appear in science demos about gels, viscosity, and oil-water mixtures.", "{name} keeps the texture from starting drama."),
"color": ("Check whether the color is certified, exempt from certification, naturally derived, and jurisdiction-specific.", "Color ingredients show how strongly people eat with their eyes.", "Some colors shift with pH, light, or processing.", "Food colors are also used in crafts, staining experiments, and visual kitchen science.", "{name} did not come here to be subtle."),
"flavor_enhancer": ("Check transparency around broad flavor terms, sodium contribution, allergens, and flavor purpose.", "Flavor systems tell how food makers recreate roasted, savory, smoky, fruity, or creamy notes.", "Flavor enhancers can make existing flavors seem louder rather than adding a brand-new taste.", "Flavor extracts and powders are common in aroma experiments and seasoning blends.", "{name} is basically the label's hype person."),
"vitamin_mineral": ("Check whether it is naturally present or added for fortification; avoid supplement-like assumptions.", "Fortification has been used in many places to address population nutrition gaps.", "Tiny nutrient amounts can matter on labels, but dose and context matter.", "Vitamins and minerals often appear in educational chemistry and nutrition demonstrations.", "{name} brought a lab coat to the grocery aisle."),
"amino_compound": ("Distinguish normal food chemistry from supplement claims and dose-dependent effects.", "Food compounds are the hidden chemistry behind aroma, color, taste, and nutrition curiosity.", "Many compounds are famous because they create recognizable sensations like heat, bitterness, aroma, or color.", "Compounds are useful in kitchen science, sensory demos, and fermentation experiments.", "{name} sounds like science because it is."),
}


def slug(name: str) -> str:
    return "ing_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def iter_ingredients(limit: int = 500):
    count = 0
    for category, names in GROUPS.items():
        for name in names.split("|"):
            count += 1
            if count > limit:
                return
            yield count, category, name


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "profile_id", "ingredient_id", "canonical_name", "category",
            "health_conscious_note", "feel_good_story", "fun_fact", "odd_use",
            "quip", "citation_id", "review_status", "source_strategy"
        ])
        for i, category, name in iter_ingredients(500):
            note, story, fact, odd, quip = TEMPLATES[category]
            writer.writerow([
                f"profile_{i:04d}", slug(name), name, category, note, story, fact, odd,
                quip.format(name=name), "", "draft",
                "Needs row-level public source review before verified health/regulatory display; safe for draft educational/fun app content only."
            ])
    print(f"Wrote 500 rich ingredient profiles to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
