# Project Overview

Quick Search Browser is an Anki add-on that extends Anki's Browser window with a compact second row of quick filter controls. The add-on is intended to make frequent card searches faster without replacing Anki's native search box or Browser behavior.

## Core User Experience

When an Anki Browser window opens, the add-on inserts a filter row under Anki's built-in search controls. The row contains checkbox and menu-style controls for common searches:

- Show or hide suspended cards.
- Restrict results to new cards.
- Restrict results to recently added cards.
- Restrict results to cards due within common day ranges.
- Restrict results to cards studied within common day ranges.
- Restrict results by flag state or specific flag numbers.

The add-on does not maintain its own database or search index. It modifies Anki Browser search text through Anki's search hook system, then asks Anki to run the normal Browser search. This keeps the behavior aligned with Anki's own search syntax and card table.

## Current Source Package

The active add-on package is:

```text
src/quick_search_browser/
```

Important runtime files:

- `__init__.py`: all current add-on runtime logic.
- `manifest.json`: add-on metadata used by Anki and packaging automation.
- `config.json`: default add-on configuration.
- `config.md`: configuration help text shown by Anki.

The package is intentionally small. Runtime code depends on Anki's bundled Python, `aqt`, and Qt bindings exposed through Anki. Automation scripts use only Python's standard library.

## Repository Purpose

This repository has two jobs:

1. Maintain the Quick Search Browser add-on.
2. Act as a reusable starter structure for future Anki add-ons.

Because of that second goal, automation should avoid hardcoding this add-on's name when it can discover metadata from `src/<package>/manifest.json`. Documentation should distinguish between project-specific facts and reusable process guidance.

## Packaging Philosophy

The installable `.ankiaddon` file should contain the add-on package contents at the root of the archive. In other words, `__init__.py`, `manifest.json`, `config.json`, and `config.md` should appear at archive root, not under `src/quick_search_browser/`.

Repository-only files such as workflows, docs, release scripts, and templates should not be copied into Anki's add-on runtime folder unless they are intentionally included as root documentation in the package.

## Publishing Model

GitHub is used for source hosting, CI, issue tracking, and release artifacts. AnkiWeb is used for public add-on distribution to Anki users. The repository supports both:

- `.github/` contains CI and release automation.
- `ankiweb/` contains manual upload templates and preparation scripts.
- `tools/` contains reusable local scripts for validation, packaging, release checks, local install, and GitHub CLI publishing.

AnkiWeb upload remains a manual browser step. The repository prepares the package and listing text, but it does not attempt to automate AnkiWeb credentials or browser upload.
