#!/usr/bin/env python3
"""Run the full Ingredient Knowledge Base build pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"

COMMANDS = [
    [sys.executable, "scripts/validate_csvs.py"],
    [sys.executable, "scripts/build_alias_index.py"],
    [sys.executable, "scripts/quality_gate.py"],
    [sys.executable, "scripts/export_json_pack.py"],
    [sys.executable, "scripts/build_evidence_packs.py"],
    [sys.executable, "scripts/build_dataset_report.py"],
]


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sqlite-output",
        default=str(DIST_DIR / "ingredient_knowledge_base.sqlite"),
        help="Where to write the compiled SQLite database.",
    )
    args = parser.parse_args()

    DIST_DIR.mkdir(exist_ok=True)
    for command in COMMANDS:
        run(command)
    run([sys.executable, "scripts/compile_sqlite.py", "--output", args.sqlite_output])
    print("Build complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
