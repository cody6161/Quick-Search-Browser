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
- Moves the current `CHANGELOG.md` Unreleased notes into a matching release section.
- Prints the matching Git tag.

Use `--no-changelog` when you only want metadata changes.

## Prepare Release

```bash
python tools/prepare_release.py
```

This runs release checks, generates AnkiWeb text, and prints the matching Git tag commands.

## Create Release Automatically

Use `tools/create_release.py` when you want the script to bump the version, build artifacts, create the release commit, create the Git tag, and write changelog-based GitHub release notes:

```bash
python tools/create_release.py patch
```

This writes `dist/github-release-notes.md` along with the package artifacts. It does not push by default. After reviewing the commit and tag, push with the commands printed by the script.

To push automatically:

```bash
python tools/create_release.py patch --push
```

To push and create or update the GitHub release in the same run, install and authenticate GitHub CLI, then run:

```bash
gh auth login
python tools/create_release.py patch --push --github-release
```

The GitHub release uses the matching `CHANGELOG.md` section as its description and uploads:

- `dist/<Add-on Name>.ankiaddon`
- `dist/SHA256SUMS.txt`
- `dist/release.json`

Use `--repo OWNER/REPO` if GitHub CLI cannot infer the repository from `origin`.

By default, the script requires a clean working tree before it starts. This keeps unrelated local edits out of the release commit. If you intentionally want to include current local edits in the release commit, use:

```bash
python tools/create_release.py patch --allow-dirty
```

Supported version arguments are `patch`, `minor`, `major`, or an explicit semantic version like `1.2.3`.

## Tag Rule

GitHub release tags must match `VERSION`.

If `VERSION` is `0.1.0`, the tag must be:

```text
v0.1.0
```

`tools/release_check.py` fails in GitHub Actions when `GITHUB_REF_NAME` is a version tag that does not match `VERSION`.
