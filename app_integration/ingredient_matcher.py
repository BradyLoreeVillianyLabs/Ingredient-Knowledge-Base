#!/usr/bin/env python3
"""Portable ingredient matcher for app prototypes.

This module loads generated aliases and evidence packs from an app asset folder.
It is intentionally dependency-free so it can be translated into TypeScript,
Dart, Swift, Kotlin, or kept as a Python backend reference.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

SPACE_RE = re.compile(r"\s+")
SPLIT_RE = re.compile(r",|;|\n|\u2022")


def normalize(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9+\- ]+", " ", value)
    value = SPACE_RE.sub(" ", value)
    return value.strip()


@dataclass
class MatchResult:
    raw_term: str
    normalized_term: str
    ingredient_id: str
    canonical_name: str
    match_type: str
    confidence: float
    review_status: str


class IngredientMatcher:
    def __init__(self, asset_root: Path):
        self.asset_root = Path(asset_root)
        self.alias_index = self._load_alias_index()
        self.ocr_aliases = self._load_ocr_aliases()
        self.pack_index = self._load_pack_index()

    def _load_alias_index(self) -> dict[str, dict[str, str]]:
        path = self.asset_root / "ingredient_alias_index.csv"
        aliases: dict[str, dict[str, str]] = {}
        if not path.exists():
            return aliases
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                normalized = normalize(row.get("normalized_alias") or row.get("alias") or "")
                if normalized and normalized not in aliases:
                    aliases[normalized] = row
        return aliases

    def _load_ocr_aliases(self) -> dict[str, dict[str, str]]:
        # Optional: apps may copy this metadata file too. If absent, exact alias
        # matching still works.
        candidates = [
            self.asset_root / "14_ocr_aliases.csv",
            self.asset_root / "metadata" / "14_ocr_aliases.csv",
        ]
        rows: dict[str, dict[str, str]] = {}
        for path in candidates:
            if not path.exists():
                continue
            with path.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    raw = normalize(row.get("raw_ocr_text") or "")
                    if raw:
                        rows[raw] = row
        return rows

    def _load_pack_index(self) -> dict[str, dict[str, str]]:
        path = self.asset_root / "evidence_packs_index.json"
        if not path.exists():
            return {}
        rows = json.loads(path.read_text(encoding="utf-8"))
        return {row["ingredient_id"]: row for row in rows if row.get("ingredient_id")}

    def split_label(self, raw_text: str) -> list[str]:
        text = raw_text.replace("INGREDIENTS:", "").replace("Ingredients:", "")
        return [term.strip() for term in SPLIT_RE.split(text) if term.strip()]

    def match_term(self, raw_term: str) -> MatchResult | None:
        normalized = normalize(raw_term)
        if not normalized:
            return None

        exact = self.alias_index.get(normalized)
        if exact:
            ingredient_id = exact.get("ingredient_id", "")
            return MatchResult(
                raw_term=raw_term,
                normalized_term=normalized,
                ingredient_id=ingredient_id,
                canonical_name=exact.get("canonical_name", ""),
                match_type="exact_alias",
                confidence=1.0,
                review_status=self.pack_index.get(ingredient_id, {}).get("review_status", "unknown"),
            )

        ocr = self.ocr_aliases.get(normalized)
        if ocr:
            corrected = normalize(ocr.get("normalized_text") or "")
            alias = self.alias_index.get(corrected)
            ingredient_id = ocr.get("ingredient_id") or (alias or {}).get("ingredient_id", "")
            canonical_name = (alias or {}).get("canonical_name", ocr.get("normalized_text", ""))
            return MatchResult(
                raw_term=raw_term,
                normalized_term=corrected or normalized,
                ingredient_id=ingredient_id,
                canonical_name=canonical_name,
                match_type="ocr_alias",
                confidence=float(ocr.get("confidence") or 0.85),
                review_status=self.pack_index.get(ingredient_id, {}).get("review_status", "unknown"),
            )
        return None

    def analyze_label(self, raw_text: str, jurisdiction: str = "Canada") -> dict[str, object]:
        terms = self.split_label(raw_text)
        matches = []
        unmatched = []
        uncertainty_notes = []

        for term in terms:
            result = self.match_term(term)
            if result is None:
                unmatched.append(term)
                continue
            matches.append(result.__dict__)
            if result.review_status in {"draft", "needs_source", "unknown"}:
                uncertainty_notes.append(
                    f"{result.canonical_name or result.raw_term}: matched but not fully source-reviewed."
                )

        return {
            "original_text": raw_text,
            "jurisdiction": jurisdiction,
            "matched_ingredients": matches,
            "unmatched_terms": unmatched,
            "uncertainty_notes": uncertainty_notes,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-root", required=True, type=Path)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()

    matcher = IngredientMatcher(args.asset_root)
    print(json.dumps(matcher.analyze_label(args.label), indent=2))
