# AnkiWeb Upload Checklist

- [ ] `python tools/validate_addon.py` passes.
- [ ] `VERSION` matches `src/<package>/manifest.json`.
- [ ] `python tools/build_ankiaddon.py` builds the package.
- [ ] `python tools/release_check.py` writes `dist/SHA256SUMS.txt` and `dist/release.json`.
- [ ] Package installs from file in Anki.
- [ ] Browser opens without errors.
- [ ] Main workflow was tested manually.
- [ ] Configuration dialog opens, if the add-on has config.
- [ ] AnkiWeb description was reviewed for current behavior.
- [ ] Changelog entry was reviewed.
- [ ] Git tag matches `VERSION`.
- [ ] GitHub release was created or updated.
- [ ] Uploaded `.ankiaddon` to AnkiWeb.
- [ ] Downloaded from AnkiWeb and smoke tested after upload.
