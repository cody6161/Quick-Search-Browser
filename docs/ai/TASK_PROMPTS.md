# Useful AI Task Prompts

## Bug Fix

Investigate the reported Anki add-on bug. Read `docs/ai/REPO_CONTEXT.md`, inspect the relevant source, make the smallest safe fix, and run `python tools/validate_addon.py` plus `python tools/build_ankiaddon.py`.

## Release Prep

Prepare this add-on for release. Confirm or bump `VERSION`, update changelog and AnkiWeb text if needed, run `python tools/prepare_release.py`, and summarize the package path, checksum, release metadata, matching Git tag, and manual AnkiWeb upload steps.

## New Add-on From Template

Create a new Anki add-on package using `python tools/new_addon_from_template.py "Add-on Name"`, then update README, docs, AnkiWeb templates, and AI docs for the new behavior.

## Code Review

Review changes for Anki runtime risks, packaging regressions, missing docs, GitHub workflow failures, and AnkiWeb publishing gaps. Put findings first with file and line references.
