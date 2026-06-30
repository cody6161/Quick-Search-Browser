"""Run local release checks and produce a SHA256 checksum for the package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from versioning import read_manifest, read_version, require_manifest_version_sync


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def run(args: list[str]) -> None:
    print("+ " + " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def latest_package() -> Path:
    packages = sorted(DIST.glob("*.ankiaddon"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not packages:
        raise SystemExit("No .ankiaddon package found in dist/.")
    return packages[0]


def write_checksum(path: Path) -> Path:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksum_path = DIST / "SHA256SUMS.txt"
    checksum_path.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    return checksum_path


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_tag_matches_version(version: str) -> None:
    tag = os.environ.get("GITHUB_REF_NAME") or os.environ.get("TAG_NAME")
    if tag and tag.startswith("v") and tag != f"v{version}":
        raise SystemExit(f"Release tag {tag!r} does not match VERSION {version!r}.")


def write_release_metadata(path: Path, version: str) -> Path:
    manifest = read_manifest()
    metadata = {
        "name": manifest.get("name"),
        "package": manifest.get("package"),
        "version": version,
        "tag": f"v{version}",
        "artifact": path.name,
        "sha256": checksum(path),
    }
    metadata_path = DIST / "release.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata_path


def main() -> None:
    version = read_version()
    require_manifest_version_sync()
    check_tag_matches_version(version)
    run([sys.executable, "tools/validate_addon.py"])
    run([sys.executable, "tools/build_ankiaddon.py"])
    package = latest_package()
    with ZipFile(package) as archive:
        names = set(archive.namelist())
    for required in ("__init__.py", "manifest.json"):
        if required not in names:
            raise SystemExit(f"Package is missing {required}.")
    checksum_path = write_checksum(package)
    metadata_path = write_release_metadata(package, version)
    print(f"Release version: {version}")
    print(f"Release package: {package}")
    print(f"Checksum file: {checksum_path}")
    print(f"Metadata file: {metadata_path}")


if __name__ == "__main__":
    main()
