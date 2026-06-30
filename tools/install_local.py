"""Copy the add-on source package into a local Anki addons21 folder.

Example:
    python tools/install_local.py --addons-dir "%APPDATA%/Anki2/addons21"
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"


def discover_addon_source() -> Path:
    manifests = sorted(SRC_ROOT.glob("*/manifest.json"))
    if len(manifests) != 1:
        raise SystemExit("Expected exactly one src/<package>/manifest.json file.")
    return manifests[0].parent


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "meta.json")
    shutil.copytree(src, dst, ignore=ignore)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install this add-on source into Anki addons21.")
    parser.add_argument("--addons-dir", required=True, help="Path to Anki's addons21 directory.")
    args = parser.parse_args()

    addon_source = discover_addon_source()
    addons_dir = Path(args.addons_dir).expanduser().resolve()
    if addons_dir.name != "addons21":
        raise SystemExit("--addons-dir should point directly to an addons21 folder.")
    target = addons_dir / addon_source.name
    copytree(addon_source, target)
    print(f"Installed {addon_source.name} to {target}")


if __name__ == "__main__":
    main()
