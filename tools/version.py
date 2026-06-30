"""Print the current repository/add-on version."""

from __future__ import annotations

from versioning import read_manifest, read_version


def main() -> None:
    version = read_version()
    manifest = read_manifest()
    print(f"{manifest.get('name', 'Anki add-on')} {version}")


if __name__ == "__main__":
    main()
