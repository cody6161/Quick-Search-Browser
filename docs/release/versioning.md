# Versioning

This repository uses a root `VERSION` file as the single source of truth for release versions.

Current version metadata is copied into:

- `VERSION`
- `src/<package>/manifest.json`
- `dist/release.json` during release checks
- Git tags in the form `v<version>`

## Version Format

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Examples:

- `0.1.0`
- `1.0.0`
- `1.2.3`

## Print Current Version

```bash
python tools/version.py
```

## Sync Manifest Metadata

If `VERSION` was edited manually, sync it into the add-on manifest:

```bash
python tools/sync_version.py
```

`python tools/validate_addon.py` fails when `VERSION` and `manifest.json` disagree.

## Bump Version

Use one of:

```bash
python tools/bump_version.py patch
python tools/bump_version.py minor
python tools/bump_version.py major
python tools/bump_version.py 1.2.3
```

The bump script:

- Updates `VERSION`.
- Updates `src/<package>/manifest.json`.
- Creates a matching release section in `CHANGELOG.md`.
- Prints the matching Git tag.

Use `--no-changelog` when you only want metadata changes.

## Prepare Release

```bash
python tools/prepare_release.py
```

This runs release checks, generates AnkiWeb text, and prints the matching Git tag commands.

## Tag Rule

GitHub release tags must match `VERSION`.

If `VERSION` is `0.1.0`, the tag must be:

```text
v0.1.0
```

`tools/release_check.py` fails in GitHub Actions when `GITHUB_REF_NAME` is a version tag that does not match `VERSION`.
