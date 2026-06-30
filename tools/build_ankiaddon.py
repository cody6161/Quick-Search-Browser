"""Build an Anki .ankiaddon package from the add-on source folder.

The script discovers the add-on package by looking for exactly one
``src/*/manifest.json`` file. That keeps it reusable for future add-ons:
create ``src/<package_name>/manifest.json`` and the package name will be
picked up automatically.
"""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
DIST = ROOT / "dist"

ROOT_FILES = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "ROADMAP.md",
]

SKIP_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_FILES = {"meta.json"}


def discover_addon_source() -> Path:
    manifests = sorted(SRC_ROOT.glob("*/manifest.json"))
    if not manifests:
        raise SystemExit("No add-on manifest found. Expected src/<package>/manifest.json.")
    if len(manifests) > 1:
        choices = "\n".join(f"- {path}" for path in manifests)
        raise SystemExit(f"Multiple add-on manifests found; keep one per package build.\n{choices}")
    return manifests[0].parent


def read_manifest(addon_source: Path) -> dict[str, object]:
    with (addon_source / "manifest.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def package_name(manifest: dict[str, object], addon_source: Path) -> str:
    name = manifest.get("name") or addon_source.name
    return str(name).strip() or addon_source.name


def should_package(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name in SKIP_FILES:
        return False
    if path.suffix in SKIP_SUFFIXES:
        return False
    return path.is_file()


def addon_files(addon_source: Path) -> list[Path]:
    return sorted(path for path in addon_source.rglob("*") if should_package(path))


def build() -> Path:
    addon_source = discover_addon_source()
    manifest = read_manifest(addon_source)
    output = DIST / f"{package_name(manifest, addon_source)}.ankiaddon"
    DIST.mkdir(exist_ok=True)

    if output.exists():
        output.unlink()

    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in addon_files(addon_source):
            archive.write(path, path.relative_to(addon_source).as_posix())

        for relative_name in ROOT_FILES:
            path = ROOT / relative_name
            if path.exists():
                archive.write(path, relative_name)

    return output


def main() -> None:
    output = build()
    print(f"Built {output}")


if __name__ == "__main__":
    main()
