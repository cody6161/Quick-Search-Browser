# File Map

## Runtime

- `src/quick_search_browser/__init__.py`: add-on runtime code.
- `src/quick_search_browser/config.json`: default settings.
- `src/quick_search_browser/config.md`: config help.
- `src/quick_search_browser/manifest.json`: add-on metadata.
- `VERSION`: canonical release version.

## Automation

- `tools/build_ankiaddon.py`: creates the installable package.
- `tools/validate_addon.py`: validates manifest, config, and Python syntax.
- `tools/release_check.py`: runs release checks and writes checksums.
- `tools/version.py`: prints the current version.
- `tools/sync_version.py`: syncs `VERSION` into the manifest.
- `tools/bump_version.py`: bumps version metadata and prepares the changelog.
- `tools/prepare_release.py`: runs release checks and AnkiWeb text generation.
- `tools/create_release.py`: automates version bump, release prep, commit, tag, and optional push.
- `tools/install_local.py`: copies source into a local Anki addons folder.
- `tools/new_addon_from_template.py`: scaffolds a new source package.
- `tools/publish_github.py`: uses GitHub CLI to create or push the repository.

## Publishing

- `.github/workflows/ci.yml`: validation on pushes and PRs.
- `.github/workflows/release.yml`: GitHub release artifact build.
- `ankiweb/`: AnkiWeb templates and preparation script.
