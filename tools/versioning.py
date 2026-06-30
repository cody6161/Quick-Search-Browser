"""Shared version helpers for add-on automation scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
VERSION_FILE = ROOT / "VERSION"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")


def discover_addon_source() -> Path:
    manifests = sorted(SRC_ROOT.glob("*/manifest.json"))
    if not manifests:
        raise SystemExit("No add-on manifest found. Expected src/<package>/manifest.json.")
    if len(manifests) > 1:
        choices = "\n".join(f"- {path}" for path in manifests)
        raise SystemExit(f"Multiple add-on manifests found; keep one per package build.\n{choices}")
    return manifests[0].parent


def read_version() -> str:
    if not VERSION_FILE.exists():
        raise SystemExit("VERSION file is missing.")
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    validate_version(version)
    return version


def validate_version(version: str) -> None:
    if not SEMVER_RE.match(version):
        raise SystemExit(f"Invalid version {version!r}. Use semantic versioning like 1.2.3.")


def write_version(version: str) -> None:
    validate_version(version)
    VERSION_FILE.write_text(version + "\n", encoding="utf-8")


def read_manifest(addon_source: Path | None = None) -> dict[str, object]:
    source = addon_source or discover_addon_source()
    with (source / "manifest.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_manifest(manifest: dict[str, object], addon_source: Path | None = None) -> None:
    source = addon_source or discover_addon_source()
    path = source / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_manifest_version(version: str | None = None) -> None:
    synced_version = version or read_version()
    addon_source = discover_addon_source()
    manifest = read_manifest(addon_source)
    manifest["version"] = synced_version
    write_manifest(manifest, addon_source)


def require_manifest_version_sync() -> None:
    version = read_version()
    manifest = read_manifest()
    manifest_version = str(manifest.get("version", "")).strip()
    if manifest_version != version:
        raise SystemExit(
            f"Version mismatch: VERSION is {version!r}, but manifest.json has {manifest_version!r}. "
            "Run `python tools/sync_version.py`."
        )
