# AI Instructions

## Mission

Help maintain an Anki add-on repository that can be built, tested, hosted on GitHub, and manually published to AnkiWeb.

## Ground Rules

- Read the existing code before editing.
- Keep changes scoped to the user request.
- Do not remove user changes unless explicitly asked.
- Prefer standard library scripts for automation.
- Keep add-on runtime dependencies minimal.
- Run validation after edits when possible.
- Update docs when workflow, packaging, configuration, or release behavior changes.

## Required Checks

For normal code or packaging changes, run:

```bash
python tools/validate_addon.py
python tools/build_ankiaddon.py
```

For release-related changes, also run:

```bash
python tools/release_check.py
```
