# Release Assistant Checklist

For release work:

1. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
2. Use `python tools/create_release.py patch --push --github-release` when the maintainer wants GitHub publishing in the same run.
3. Review `CHANGELOG.md`.
4. Confirm `dist/*.ankiaddon` exists.
5. Confirm `dist/SHA256SUMS.txt`, `dist/release.json`, and `dist/github-release-notes.md` exist.
6. Confirm the created Git tag is `v<VERSION>`.
7. Review generated AnkiWeb text.
8. Confirm GitHub release workflow exists or that `--github-release` published the release.
9. Remind the maintainer that AnkiWeb upload is manual.
