# Release Checklist

Use this checklist when preparing a GitHub or AnkiWeb release.

1. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
2. To publish GitHub in the same run, use `python tools/create_release.py patch --push --github-release`.
3. Confirm `dist/Quick Search Browser.ankiaddon` contains only add-on files and release docs.
4. Confirm `dist/SHA256SUMS.txt`, `dist/release.json`, and `dist/github-release-notes.md` were generated.
5. Test the add-on in Anki.
6. Push the printed release commit and tag commands, use `--push`, or use `--push --github-release` for full GitHub publishing.
7. Upload the same `.ankiaddon` file to AnkiWeb.

The generated `.ankiaddon` file should not be committed to git.
