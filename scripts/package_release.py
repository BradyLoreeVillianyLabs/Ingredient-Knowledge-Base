#!/usr/bin/env python3
"""Create local release ZIPs after running the full build pipeline.

Outputs under dist/:
- ingredient-knowledge-base-csv.zip
- ingredient-knowledge-base-json.zip
"""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"


def add_if_exists(zf: zipfile.ZipFile, path: Path, arcname: str | None = None) -> None:
    if path.exists() and path.is_file():
        zf.write(path, arcname or str(path.relative_to(ROOT)))


def zip_tree(zip_path: Path, paths: list[Path]) -> None:
    zip_path.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for base in paths:
            if base.is_file():
                add_if_exists(zf, base)
            elif base.exists():
                for path in base.rglob("*"):
                    if path.is_file():
                        add_if_exists(zf, path)


def main() -> int:
    DIST_DIR.mkdir(exist_ok=True)
    zip_tree(
        DIST_DIR / "ingredient-knowledge-base-csv.zip",
        [ROOT / "data", ROOT / "schema", ROOT / "docs", ROOT / "README.md", ROOT / "CONTRIBUTING.md"],
    )
    zip_tree(
        DIST_DIR / "ingredient-knowledge-base-json.zip",
        [ROOT / "data" / "generated" / "json", ROOT / "data" / "generated" / "evidence_packs", ROOT / "data" / "generated" / "evidence_packs_index.json"],
    )
    print(f"Wrote release ZIPs to {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
