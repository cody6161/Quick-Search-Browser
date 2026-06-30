# Release Process

1. Finish code and documentation changes.
2. Run `python tools/create_release.py patch`, `minor`, `major`, or an explicit version.
3. Review `CHANGELOG.md`, the generated release commit, and the generated tag.
4. Install the generated package into Anki and smoke test.
5. Push the release commit and matching tag, or rerun the script with `--push` next time.
6. Let `.github/workflows/release.yml` create the GitHub release artifact.
7. Review `ankiweb/generated/ankiweb-description.md`.
8. Upload the `.ankiaddon` package manually to AnkiWeb.
9. Download from AnkiWeb and smoke test the published package.

Keep GitHub releases and AnkiWeb uploads aligned. If one fails, fix it before announcing the release.

The Git tag must match `VERSION`. For example, `VERSION` value `0.1.0` must use tag `v0.1.0`.

If you want the manual release flow instead of the automatic commit/tag flow, run `python tools/bump_version.py patch`, review the changelog, then run `python tools/prepare_release.py`.
