# Configuration

Anki reads `config.json` as the default config and displays `config.md` as help text in the add-on configuration dialog.

## Conventions

- Keep defaults valid and conservative.
- Document every config key in `config.md`.
- Treat missing config keys as possible; users may carry old config forward.
- Validate type assumptions in code before using config values.

## Current Config

- `recent_added_days`: number of days used by the Recent Added filter.
