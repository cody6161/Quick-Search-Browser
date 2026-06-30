# Testing

## Automated Checks

```bash
python tools/validate_addon.py
python tools/build_ankiaddon.py
python tools/release_check.py
```

## Manual Smoke Test

- Install the generated `.ankiaddon` into Anki.
- Restart Anki.
- Open the Browser.
- Confirm the quick filter row appears.
- Toggle each checkbox or menu option.
- Confirm Anki search results update.
- Open the add-on config dialog.
- Restart Anki again and confirm no startup errors.

## Regression Notes

For search behavior changes, record the initial query, enabled filters, expected query meaning, and observed result count if relevant.
