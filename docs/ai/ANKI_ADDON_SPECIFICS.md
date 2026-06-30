# Anki Add-on Specifics

## Package Layout

Anki expects an add-on package to include `__init__.py` at the root of the installed add-on folder. This repo stores that root under `src/<package>/`.

Required source files:

- `__init__.py`
- `manifest.json`

Recommended source files:

- `config.json`
- `config.md`

## Manifest

Use:

```json
{
  "name": "Human Readable Add-on Name",
  "package": "python_package_folder"
}
```

For AnkiWeb add-ons, Anki may add or manage extra metadata after installation. Keep the source manifest simple unless a release specifically requires more fields.

## Hooks

Use public `aqt.gui_hooks` where possible. Browser UI changes should be attached when the Browser window is shown. Search changes should be applied through Browser search hooks so they compose with Anki's own search behavior.

## Compatibility Notes

Anki's UI internals change over time. Prefer stable hooks and documented Qt APIs. Test layout changes manually in the Browser.
