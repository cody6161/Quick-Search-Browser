# Release Process

1. Finish code and documentation changes.
2. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
3. For a full GitHub publish in the same command, run `python tools/create_release.py patch --push --github-release`.
4. Review `CHANGELOG.md`, the generated release commit, the generated tag, and `dist/github-release-notes.md`.
5. Install the generated package into Anki and smoke test.
6. Push the release commit and matching tag if they were not already pushed.
7. Confirm the GitHub release contains the `.ankiaddon`, `SHA256SUMS.txt`, and `release.json` assets.
8. Review `ankiweb/generated/ankiweb-description.md`.
9. Upload the `.ankiaddon` package manually to AnkiWeb.
10. Download from AnkiWeb and smoke test the published package.

Keep GitHub releases and AnkiWeb uploads aligned. If one fails, fix it before announcing the release.

The Git tag must match `VERSION`. For example, `VERSION` value `0.1.0` must use tag `v0.1.0`.

If GitHub CLI is installed and authenticated with `gh auth login`, `--github-release` creates or updates the release notes from `CHANGELOG.md` and uploads the generated artifacts. If you skip `--github-release`, pushing a `v*` tag still lets `.github/workflows/release.yml` create or update release artifacts.

If you want the manual release flow instead of the automatic commit/tag flow, run `python tools/bump_version.py patch`, review the changelog, then run `python tools/prepare_release.py`.
