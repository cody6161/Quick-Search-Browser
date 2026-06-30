# Overview

Anki addon was forked and inspired by the QuickSearch addon, found at this ankiweb link: https://ankiweb.net/shared/info/1286588198


# Quick Search Browser

Quick Search Browser is an Anki add-on that adds quick filter controls to the Browser window. The filters appear on a second row below Anki's normal search controls, with checkbox filters grouped first and drop-down filters after them.

## Features

- Hide suspended cards by default, with a toggle to show them.
- Filter new cards.
- Filter recently added cards.
- Filter cards due in 1, 3, 7, 14, or 30 days.
- Filter cards studied in 1, 3, 7, 14, or 30 days.
- Filter cards by configured yield tags: High Yield, Relatively High Yield, High Yield Temporary, Lower Yield, and Low Yield.
- Filter cards by any flag or by specific flag numbers.

## Source Layout

The Anki add-on source lives in `src/quick_search_browser/`. Repository documentation, release helpers, and GitHub templates live outside `src/`.

- `src/quick_search_browser/__init__.py`: Anki add-on entry point.
- `src/quick_search_browser/manifest.json`: Add-on metadata used by Anki and packaging automation.
- `src/quick_search_browser/config.json`: Default add-on configuration.
- `src/quick_search_browser/config.md`: Help text shown in Anki's config dialog.
- `tools/build_ankiaddon.py`: Builds `dist/Quick Search Browser.ankiaddon`.
- `tools/validate_addon.py`: Validates manifest, config, and Python syntax.
- `tools/release_check.py`: Runs validation, builds the package, and writes checksums.
- `tools/create_release.py`: Bumps, builds, commits, tags, and optionally pushes a release.
- `tools/bump_version.py`: Lower-level script that bumps `VERSION`, syncs `manifest.json`, and prepares `CHANGELOG.md`.
- `tools/prepare_release.py`: Lower-level script that runs release checks and generates AnkiWeb release text.
- `ankiweb/`: AnkiWeb upload templates, scripts, and checklist.
- `docs/`: Maintainer documentation.
- `docs/ai/`: AI assistant instructions and Anki add-on context.
- `.github/`: GitHub workflows, issue templates, pull request template, Dependabot config, and label definitions.
- `CHANGELOG.md`, `CONTRIBUTING.md`, `RELEASE.md`, `ROADMAP.md`, and `SUPPORT.md`: Project documentation.

## Documentation

Maintainer documentation lives in `docs/`. AnkiWeb release templates and scripts live in `ankiweb/`. AI assistant operating instructions live in `docs/ai/`.

## Installation from Source

For normal source installation, build the `.ankiaddon` package and install it with Anki:

```bash
python tools/build_ankiaddon.py
```

Then install `dist/Quick Search Browser.ankiaddon` using Anki's install-from-file add-on option.

For local development, copy or symlink `src/quick_search_browser` into Anki's `addons21` folder, then restart Anki after code changes.

## AnkiWeb Packaging

Run:

```bash
python tools/build_ankiaddon.py
```

The upload package will be created at:

```text
dist/Quick Search Browser.ankiaddon
```

Upload that `.ankiaddon` file to AnkiWeb. Do not upload the whole GitHub repo zip, because that includes development files that AnkiWeb users do not need.

## Configuration

The `recent_added_days` option in `src/quick_search_browser/config.json` controls how many days are included by the `Recent Added` checkbox. The default is `10`.

The `yield_tags` option maps each `Yield` dropdown label to the Anki tag searched when that option is selected. Change the tag values if your collection uses different tag names.

## Roadmap

See `ROADMAP.md` for planned upgrades and additional feature ideas.

## GitHub Publishing

This repository is ready to publish after making the first commit. Generated and local files are ignored by `.gitignore`, including `meta.json`, `dist/`, `.ankiaddon` files, AnkiWeb generated release text, `.vscode/`, and `__pycache__/`.

Recommended first-time commands:

```bash
git add .
git commit -m "Initial Quick Search Browser release"
```

If GitHub CLI is installed and authenticated, create or push the hosted repository with:

```bash
python tools/publish_github.py --repo OWNER/REPO --public
```

Use `--private` instead of `--public` if needed. Do not commit the generated `dist/Quick Search Browser.ankiaddon` file. Attach it to GitHub releases and upload it to AnkiWeb instead.

Version releases are managed from the root `VERSION` file:

```bash
python tools/create_release.py patch
```

Add `--push` if you want the script to push the release commit and tag automatically.

## License

Quick Search Browser is free and open source software licensed under the MIT License. See `LICENSE` for details.
