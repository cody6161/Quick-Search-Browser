"""Generate AnkiWeb release text from templates and current package metadata."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANKIWEB = ROOT / "ankiweb"
GENERATED = ANKIWEB / "generated"
sys.path.insert(0, str(ROOT / "tools"))

from versioning import read_version  # noqa: E402


def manifest() -> dict[str, object]:
    manifests = sorted((ROOT / "src").glob("*/manifest.json"))
    if len(manifests) != 1:
        raise SystemExit("Expected exactly one src/<package>/manifest.json file.")
    return json.loads(manifests[0].read_text(encoding="utf-8"))


def main() -> None:
    GENERATED.mkdir(exist_ok=True)
    info = manifest()
    version = read_version()
    template = (ANKIWEB / "templates" / "ankiweb-description.md").read_text(encoding="utf-8")
    header = (
        f"<!-- Generated for {info.get('name', 'Anki add-on')} "
        f"{version} ({info.get('package', 'unknown package')}) -->\n\n"
    )
    output = GENERATED / "ankiweb-description.md"
    output.write_text(header + template, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
