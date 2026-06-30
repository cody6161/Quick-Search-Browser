# Development Workflow

## Normal Loop

1. Edit files in `src/<package>`.
2. Run `python tools/validate_addon.py`.
3. Install into Anki or rebuild the `.ankiaddon` package.
4. Restart Anki.
5. Test the affected Browser workflow.

## Anki Hook Guidelines

- Register hooks once at import time.
- Keep UI setup idempotent for each Browser window.
- Avoid slow work in UI hooks.
- Avoid mutating Anki internals unless there is no public hook or API.
- Treat search query generation as user-visible behavior and test it manually.

## Compatibility

Anki add-ons run inside Anki's bundled Python and Qt environment. Avoid dependencies unless they are vendored and small. Prefer standard library code for packaging and validation scripts.
