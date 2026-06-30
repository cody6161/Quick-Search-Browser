# Release Process

1. Finish code and documentation changes.
2. Bump the version with `python tools/bump_version.py patch`, `minor`, `major`, or an explicit version.
3. Review `CHANGELOG.md` and fill in the generated release section.
4. Run `python tools/prepare_release.py`.
5. Install the generated package into Anki and smoke test.
6. Commit changes.
7. Push to GitHub.
8. Create the matching version tag, such as `v1.0.0`.
9. Let `.github/workflows/release.yml` create the GitHub release artifact.
10. Review `ankiweb/generated/ankiweb-description.md`.
11. Upload the `.ankiaddon` package manually to AnkiWeb.
12. Download from AnkiWeb and smoke test the published package.

Keep GitHub releases and AnkiWeb uploads aligned. If one fails, fix it before announcing the release.

The Git tag must match `VERSION`. For example, `VERSION` value `0.1.0` must use tag `v0.1.0`.
