"""Sync the root VERSION value into the add-on manifest."""

from __future__ import annotations

from versioning import read_version, sync_manifest_version


def main() -> None:
    version = read_version()
    sync_manifest_version(version)
    print(f"Synced manifest.json to version {version}")


if __name__ == "__main__":
    main()
