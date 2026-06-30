"""Validate the local Anki add-on source before packaging or release."""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

from versioning import read_version, require_manifest_version_sync


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def discover_addon_source() -> Path:
    manifests = sorted(SRC_ROOT.glob("*/manifest.json"))
    if not manifests:
        fail("Expected one manifest at src/<package>/manifest.json.")
    if len(manifests) > 1:
        fail("Expected one add-on package per build; found: " + ", ".join(str(p) for p in manifests))
    return manifests[0].parent


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def validate_manifest(addon_source: Path) -> None:
    manifest = load_json(addon_source / "manifest.json")
    for key in ("name", "package", "version"):
        value = str(manifest.get(key, "")).strip()
        if not value:
            fail(f"manifest.json must include a non-empty {key!r} field.")
    if manifest["package"] != addon_source.name:
        print(
            f"WARNING: manifest package {manifest['package']!r} does not match folder {addon_source.name!r}.",
            file=sys.stderr,
        )


def validate_config(addon_source: Path) -> None:
    config_path = addon_source / "config.json"
    if config_path.exists():
        load_json(config_path)


def compile_python(paths: list[Path]) -> None:
    for path in paths:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(str(exc))


def main() -> None:
    addon_source = discover_addon_source()
    if not (addon_source / "__init__.py").exists():
        fail("Anki add-on package must include __init__.py.")
    read_version()
    validate_manifest(addon_source)
    require_manifest_version_sync()
    validate_config(addon_source)
    compile_python(sorted(addon_source.rglob("*.py")) + sorted((ROOT / "tools").glob("*.py")))
    print(f"Validated {addon_source}")


if __name__ == "__main__":
    main()
