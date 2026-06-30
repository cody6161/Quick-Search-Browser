# Architecture

## Runtime Architecture

The add-on currently lives in one runtime module:

```text
src/quick_search_browser/__init__.py
```

That module performs four main jobs:

1. Defines a custom `_MultiSelectMenu` for checkable menu behavior.
2. Defines `CheckableComboBox`, a button-backed menu control used for compact filters.
3. Builds the quick filter row when an Anki Browser window is shown.
4. Updates Browser search queries when Anki prepares a search.

## Anki Hook Flow

At import time, the add-on registers two hooks:

- `gui_hooks.browser_will_show.append(setup_quick_search_in_browser)`
- `gui_hooks.browser_will_search.append(setup_quick_search)`

The Browser UI hook creates widgets and connects their state changes to `search(browser)`, which calls `browser.onSearchActivated()`. That asks Anki to rerun the Browser search using the current search bar text.

The Browser search hook receives a `SearchContext`. The add-on reads the active widget state, appends Anki search syntax, and writes the final query back to `context.search`.

## Search Query Behavior

The add-on treats Anki search syntax as the source of truth. It builds query fragments such as:

- `-is:suspended`
- `is:new`
- `added:<days>`
- `rated:<days>`
- `prop:due=<n>`
- `flag:<n>`
- `-flag:0`

When combining filters, the code wraps the existing query in parentheses before adding another fragment. This helps preserve the user's original search expression while adding filter constraints.

The code deliberately avoids modifying direct `nid:` and `cid:` lookups, because exact note and card id searches can be disrupted by extra wrapping or filtering.

## UI State Model

The current implementation stores filter widgets in module-level globals:

- `cbSuspended`
- `cbDue`
- `cbStudied`
- `cbNew`
- `cbFlag`
- `cbRecent`

That is simple and matches the current small scope. If future work supports multiple simultaneous Browser windows more rigorously, this state should move to a per-browser object or weak mapping keyed by Browser instance.

## Packaging Architecture

`tools/build_ankiaddon.py` discovers the add-on package by looking for exactly one `src/*/manifest.json`. It then writes all package files into the root of `dist/<Add-on Name>.ankiaddon`.

The build excludes generated Python cache files, local add-on metadata, and common cache folders. Root documentation files such as `README.md`, `CHANGELOG.md`, `LICENSE`, and `ROADMAP.md` are included in the package for user visibility.

## Validation Architecture

`tools/validate_addon.py` checks:

- Exactly one add-on manifest exists under `src/`.
- `manifest.json` has non-empty `name`, `package`, and `version` fields.
- `VERSION` is valid semantic version text.
- `VERSION` and `manifest.json` agree.
- `config.json` is valid JSON when present.
- Runtime and tool Python files compile.
- `__init__.py` exists in the package.

`tools/release_check.py` runs validation, rebuilds the package, checks required archive files, rejects mismatched Git tags in release automation, and writes `dist/SHA256SUMS.txt` plus `dist/release.json`.

## Documentation Architecture

Documentation is organized by audience and task:

- Root `docs/`: project-wide reference and standards.
- `docs/development/`: implementation and local debugging work.
- `docs/release/`: packaging and release procedure.
- `docs/ankiweb/`: AnkiWeb upload process.
- `docs/github/`: GitHub hosting and automation.
- `docs/ai/`: AI assistant operating instructions and context.
