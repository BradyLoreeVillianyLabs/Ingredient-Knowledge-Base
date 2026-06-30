#!/usr/bin/env python3
"""Compile all Python scripts and tests to catch syntax errors early in CI."""

from __future__ import annotations

import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK_DIRS = [ROOT / "scripts", ROOT / "tests", ROOT / "app_integration"]


def main() -> int:
    errors: list[str] = []
    for directory in CHECK_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.py")):
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc.msg}")
    if errors:
        print("Python syntax check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Python syntax check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
