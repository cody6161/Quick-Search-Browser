# Troubleshooting

## Package Does Not Install

- Confirm `manifest.json` and `__init__.py` are at the root of the zip.
- Run `python tools/release_check.py`.
- Try installing in a fresh Anki profile.

## Add-on Does Not Load

- Check Anki's error dialog.
- Run `python tools/validate_addon.py`.
- Confirm imports are available in Anki's bundled Python environment.

## Browser UI Looks Wrong

- Test with other add-ons disabled.
- Check for Anki version-specific Browser layout changes.
- Keep widgets compact and avoid fixed widths unless necessary.

## GitHub Release Does Not Build

- Open the failing workflow log.
- Run the same command locally.
- Check `.github/workflows/release.yml` permissions.
