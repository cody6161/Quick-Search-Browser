# Release Assistant Checklist

For release work:

1. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
2. Review `CHANGELOG.md`.
3. Confirm `dist/*.ankiaddon` exists.
4. Confirm `dist/SHA256SUMS.txt` and `dist/release.json` exist.
5. Confirm the created Git tag is `v<VERSION>`.
6. Review generated AnkiWeb text.
7. Confirm GitHub release workflow exists.
8. Remind the maintainer that AnkiWeb upload is manual.
