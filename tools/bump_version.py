"""Bump VERSION, sync manifest.json, and prepare CHANGELOG.md.

Examples:
    python tools/bump_version.py patch
    python tools/bump_version.py minor
    python tools/bump_version.py major
    python tools/bump_version.py 1.2.3
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from versioning import read_version, sync_manifest_version, validate_version, write_version


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"


def bump(current: str, part: str) -> str:
    major, minor, patch = [int(piece) for piece in current.split("-", 1)[0].split("+", 1)[0].split(".")]
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    validate_version(part)
    return part


def update_changelog(version: str) -> None:
    if not CHANGELOG.exists():
        return

    text = CHANGELOG.read_text(encoding="utf-8")
    today = date.today().isoformat()
    released_header = f"## {version} - {today}"

    if released_header in text:
        return

    if "## Unreleased" in text:
        lines = text.splitlines()
        unreleased_index = next(
            index for index, line in enumerate(lines) if line.strip() == "## Unreleased"
        )
        next_release_index = next(
            (
                index
                for index in range(unreleased_index + 1, len(lines))
                if lines[index].startswith("## ")
            ),
            len(lines),
        )
        unreleased_body = "\n".join(lines[unreleased_index + 1 : next_release_index]).strip()
        release_body = unreleased_body if unreleased_body and unreleased_body != "-" else "- "
        new_lines = (
            lines[: unreleased_index + 1]
            + ["", "- ", "", released_header, "", *release_body.splitlines(), ""]
            + lines[next_release_index:]
        )
        text = "\n".join(new_lines).rstrip() + "\n"
    else:
        text = text.rstrip() + f"\n\n## Unreleased\n\n- \n\n{released_header}\n\n- \n"

    CHANGELOG.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump the repository version and sync metadata.")
    parser.add_argument("version", help="major, minor, patch, or an explicit semantic version.")
    parser.add_argument("--no-changelog", action="store_true", help="Do not update CHANGELOG.md.")
    args = parser.parse_args()

    current = read_version()
    new_version = bump(current, args.version)
    write_version(new_version)
    sync_manifest_version(new_version)
    if not args.no_changelog:
        update_changelog(new_version)
    print(f"Bumped version: {current} -> {new_version}")
    print(f"Release tag: v{new_version}")


if __name__ == "__main__":
    main()
