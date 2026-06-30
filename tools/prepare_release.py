"""Prepare release artifacts and print the matching Git tag commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from versioning import read_version, require_manifest_version_sync


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> None:
    print("+ " + " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    version = read_version()
    require_manifest_version_sync()
    run([sys.executable, "tools/release_check.py"])
    run([sys.executable, "ankiweb/scripts/prepare_ankiweb_release.py"])
    print()
    print(f"Release version: {version}")
    print(f"Create the matching tag with: git tag v{version}")
    print("Push it with: git push origin main --tags")


if __name__ == "__main__":
    main()
