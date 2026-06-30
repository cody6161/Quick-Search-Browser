# AnkiWeb Publishing

AnkiWeb upload is a manual browser step. Use `ankiweb/` to make that manual step repeatable.

## Before Upload

Run:

```bash
python tools/release_check.py
python ankiweb/scripts/prepare_ankiweb_release.py
```

Review:

- `dist/*.ankiaddon`
- `dist/SHA256SUMS.txt`
- `ankiweb/generated/ankiweb-description.md`
- `ankiweb/templates/upload-checklist.md`

## Upload

1. Sign in to AnkiWeb.
2. Open the add-on management page.
3. Upload the generated `.ankiaddon` package.
4. Paste the reviewed description and changelog.
5. Save the listing.
6. Download and test the published package.

## Listing Rules

- Mention compatibility honestly.
- Keep feature lists current.
- Include support instructions.
- Do not promise behavior that is not tested.
