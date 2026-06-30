# Release Checklist

Use this checklist when preparing a GitHub or AnkiWeb release.

1. Bump the version with `python tools/bump_version.py patch`, `minor`, `major`, or an explicit version.
2. Review `CHANGELOG.md` and fill in the generated release section.
3. Run `python tools/prepare_release.py`.
4. Confirm `dist/Quick Search Browser.ankiaddon` contains only add-on files and release docs.
5. Confirm `dist/SHA256SUMS.txt` and `dist/release.json` were generated.
6. Test the add-on in Anki.
7. Commit the release changes.
8. Create the matching Git tag, such as `git tag v0.1.0`.
9. Push to GitHub with `git push origin main --tags`.
10. Let GitHub Actions create the release artifact.
11. Upload the same `.ankiaddon` file to AnkiWeb.

The generated `.ankiaddon` file should not be committed to git.
