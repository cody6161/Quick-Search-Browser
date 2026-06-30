# Release Checklist

Use this checklist when preparing a GitHub or AnkiWeb release.

1. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
2. Confirm `dist/Quick Search Browser.ankiaddon` contains only add-on files and release docs.
3. Confirm `dist/SHA256SUMS.txt` and `dist/release.json` were generated.
4. Test the add-on in Anki.
5. Push the printed release commit and tag commands, or use `python tools/create_release.py patch --push`.
6. Let GitHub Actions create the release artifact.
7. Upload the same `.ankiaddon` file to AnkiWeb.

The generated `.ankiaddon` file should not be committed to git.
