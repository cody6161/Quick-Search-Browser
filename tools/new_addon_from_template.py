"""Create a minimal Anki add-on source package in this repository."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from versioning import read_version

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def normalize_package(name: str) -> str:
    package = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip().lower()).strip("_")
    if not package:
        raise SystemExit("Package name cannot be empty.")
    if package[0].isdigit():
        package = "addon_" + package
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold src/<package> for a new add-on.")
    parser.add_argument("name", help="Human-readable add-on name.")
    parser.add_argument("--package", help="Python package folder name. Defaults to normalized name.")
    args = parser.parse_args()

    package = normalize_package(args.package or args.name)
    target = SRC / package
    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing package: {target}")
    version = read_version()
    target.mkdir(parents=True)
    (target / "__init__.py").write_text('"""Anki add-on entry point."""\n', encoding="utf-8")
    (target / "manifest.json").write_text(
        json.dumps({"name": args.name, "package": package, "version": version}, indent=2) + "\n",
        encoding="utf-8",
    )
    (target / "config.json").write_text("{}\n", encoding="utf-8")
    (target / "config.md").write_text(f"# {args.name} Configuration\n\nNo options yet.\n", encoding="utf-8")
    print(f"Created {target}")


if __name__ == "__main__":
    main()
