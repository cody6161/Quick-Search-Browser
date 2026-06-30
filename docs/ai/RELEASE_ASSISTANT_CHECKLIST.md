# Release Assistant Checklist

For release work:

1. Confirm or bump `VERSION` with `python tools/bump_version.py patch`, `minor`, `major`, or an explicit version.
2. Review `CHANGELOG.md`.
3. Run `python tools/prepare_release.py`.
4. Confirm `dist/*.ankiaddon` exists.
5. Confirm `dist/SHA256SUMS.txt` and `dist/release.json` exist.
6. Confirm the intended Git tag is `v<VERSION>`.
7. Review generated AnkiWeb text.
8. Confirm GitHub release workflow exists.
9. Remind the maintainer that AnkiWeb upload is manual.
