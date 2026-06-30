# Configuration

Anki reads `config.json` as the default config and displays `config.md` as help text in the add-on configuration dialog.

## Conventions

- Keep defaults valid and conservative.
- Document every config key in `config.md`.
- Treat missing config keys as possible; users may carry old config forward.
- Validate type assumptions in code before using config values.

## Current Config

- `recent_added_days`: number of days used by the Recent Added filter.
- `yield_tags`: mapping of Yield dropdown labels to Anki tags.

Default yield tag mapping:

```json
{
  "yield_tags": {
    "High Yield": "#AK_Step1_v12::#Low/HighYield::1-HighYield",
    "Relatively High Yield": "#AK_Step1_v12::#Low/HighYield::2-RelativelyHighYield",
    "High Yield Temporary": "#AK_Step1_v12::#Low/HighYield::3-HighYield-temporary",
    "Lower Yield": "#AK_Step1_v12::#Low/HighYield::4-LowerYield",
    "Low Yield": "#AK_Step1_v12::#Low/HighYield::5-LowYield"
  }
}
```

The dropdown labels should stay stable because they are the user-facing menu options. Change the tag values when a collection uses different tag names.
