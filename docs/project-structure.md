# Project Structure

This repository separates runtime add-on code from maintenance infrastructure. The `src/` tree is what Anki needs to run the add-on. The surrounding folders support packaging, publishing, documentation, GitHub hosting, AnkiWeb upload, and AI-assisted maintenance.

## Root Files

- `README.md`: public overview.
- `CHANGELOG.md`: user-facing release history.
- `VERSION`: canonical semantic version for the add-on and release automation.
- `LICENSE`: license text.
- `ROADMAP.md`: planned work.
- `RELEASE.md`: concise release notes or release commands.
- `CONTRIBUTING.md`: contributor expectations.
- `SUPPORT.md`: support request guidance.
- `.gitignore`: ignores generated packages, local Anki metadata, generated AnkiWeb text, caches, and editor files.
- `.gitattributes`: normalizes text files and line endings.

## Source

Current package:

```text
src/quick_search_browser/
```

Files:

- `__init__.py`: Anki add-on entry point and current runtime implementation.
- `manifest.json`: add-on metadata used by Anki and packaging tools.
- `config.json`: default configuration shown in Anki's add-on config UI.
- `config.md`: configuration help text.

The package folder name should match the `package` field in `manifest.json`. The packaging tools discover the add-on by finding exactly one `src/*/manifest.json`.

## Automation

- `tools/build_ankiaddon.py`: builds `dist/<Add-on Name>.ankiaddon`.
- `tools/validate_addon.py`: validates manifest, config JSON, required source files, and Python syntax.
- `tools/release_check.py`: runs validation, rebuilds the package, verifies archive contents, and writes `dist/SHA256SUMS.txt`.
- `tools/version.py`: prints the current add-on version.
- `tools/sync_version.py`: syncs `VERSION` into `manifest.json`.
- `tools/bump_version.py`: bumps `VERSION`, syncs `manifest.json`, and prepares `CHANGELOG.md`.
- `tools/prepare_release.py`: runs release checks, generates AnkiWeb text, and prints matching tag commands.
- `tools/install_local.py`: copies the source package into a local Anki `addons21` folder for development testing.
- `tools/new_addon_from_template.py`: scaffolds a new `src/<package>` package for future add-ons.
- `tools/publish_github.py`: uses GitHub CLI to create or push a hosted repository when `gh` is installed.

## GitHub Infrastructure

- `.github/workflows/ci.yml`: validates and builds on pushes and pull requests.
- `.github/workflows/release.yml`: creates or updates GitHub releases for `v*` tags.
- `.github/ISSUE_TEMPLATE/`: issue forms for bugs and feature requests.
- `.github/pull_request_template.md`: validation and release-impact checklist for PRs.
- `.github/dependabot.yml`: GitHub Actions dependency update checks.
- `.github/labels.yml`: reusable label definitions.

## AnkiWeb Infrastructure

- `ankiweb/README.md`: AnkiWeb workspace guide.
- `ankiweb/templates/`: listing, changelog, support, and upload checklist templates.
- `ankiweb/scripts/prepare_ankiweb_release.py`: generates reviewable AnkiWeb description text.
- `ankiweb/generated/`: generated release text, ignored except for `.gitkeep`.
- `ankiweb/releases/`: optional local release copies, ignored except for `.gitkeep`.

## Documentation

- `docs/`: human maintainer documentation.
- `docs/development/`: local development workflow, testing, configuration, and troubleshooting.
- `docs/release/`: build, package, and release process.
- `docs/ankiweb/`: AnkiWeb-specific publishing docs.
- `docs/github/`: GitHub-specific publishing docs.
- `docs/ai/`: AI assistant operating context and instructions.

## Generated Files

Generated files should not be committed unless they are intentional placeholders or templates.

- `dist/`: built `.ankiaddon` packages and checksums.
- `dist/release.json`: generated release metadata for GitHub release artifacts.
- `ankiweb/generated/ankiweb-description.md`: generated AnkiWeb listing text.
- `__pycache__/`: Python bytecode cache folders.
- `meta.json`: local Anki add-on metadata.
