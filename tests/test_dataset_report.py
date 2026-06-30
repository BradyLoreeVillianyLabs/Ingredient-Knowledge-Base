#!/usr/bin/env python3
"""Tests for the generated dataset report."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "DATASET_REPORT.md"


class DatasetReportTests(unittest.TestCase):
    def test_generated_report_contains_package_summary_sections(self) -> None:
        subprocess.run([sys.executable, "scripts/build_dataset_report.py"], cwd=ROOT, check=True)
        text = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("## Generated package artifacts", text)
        self.assertIn("## Current priorities", text)
        self.assertIn("ingredient_alias_index.csv", text)


if __name__ == "__main__":
    unittest.main()
