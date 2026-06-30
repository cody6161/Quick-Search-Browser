# AnkiWeb Release Workspace

This folder holds everything needed to prepare the manual AnkiWeb upload. AnkiWeb does not provide a normal public upload API for add-on maintainers, so the final upload is done in the browser. The scripts and templates here make the package, description, changelog, and checklist consistent.

## Standard Flow

1. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version from the repository root.
2. Confirm `src/<package>/manifest.json` has the correct add-on name, package id, and version.
3. Review `CHANGELOG.md`.
4. Review the generated release commit and tag.
5. Open `ankiweb/generated/ankiweb-description.md` and review the text.
6. Upload `dist/*.ankiaddon` on AnkiWeb.
7. Paste the reviewed description and changelog into the AnkiWeb listing.
8. Save the completed checklist from `ankiweb/templates/upload-checklist.md` with the release notes.

## Folder Map

- `templates/`: reusable text for AnkiWeb description, changelog, support replies, and upload checks.
- `scripts/`: helper scripts for release preparation.
- `generated/`: generated release text. This folder is ignored except for `.gitkeep`.
- `releases/`: optional local copies of packages and checksums. This folder is ignored except for `.gitkeep`.
