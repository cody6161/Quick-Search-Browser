# Project Standards

## Runtime Code Standards

- Prefer Anki public APIs and `aqt.gui_hooks`.
- Keep UI code compact and focused on Browser workflows.
- Avoid long-running work in Anki UI hooks.
- Treat Browser search text as user-visible behavior.
- Avoid external runtime dependencies unless there is a strong reason.
- Keep config handling tolerant of missing keys, because users may carry older config forward.

## Automation Standards

- Tooling scripts should run from the repository root.
- Tooling scripts should use the Python standard library by default.
- Scripts should discover the add-on package from `src/<package>/manifest.json` when practical.
- Release checks should fail loudly when required package files are missing.
- `VERSION` is the canonical release version and must match `manifest.json`.
- Git release tags must use `v<version>`, such as `v0.1.0`.
- Generated release artifacts belong in ignored folders such as `dist/` and `ankiweb/generated/`.

## Documentation Standards

- Root `docs/` files should explain the codebase as a whole.
- Subfolder docs should stay task-specific.
- Update docs when changing packaging, publishing, configuration, or AI instructions.
- Keep AnkiWeb listing templates aligned with actual add-on behavior.
- Keep AI docs explicit enough that a future assistant can work without guessing.

## GitHub Standards

- CI should validate and build the add-on on every push and pull request.
- Release workflow should attach `.ankiaddon` files, checksums, and `release.json` to version tags.
- Issue templates should request Anki version, operating system, steps to reproduce, and error text.
- Pull requests should state validation commands and release impact.

## AnkiWeb Standards

- Always run release checks before upload.
- Always review generated AnkiWeb description text before pasting it into AnkiWeb.
- Keep compatibility statements honest and current.
- Download and smoke test the published package after upload.

## Reuse Standards For Future Add-ons

When using this repository as a template for another add-on, update:

- `src/<package>/manifest.json`
- Runtime package folder name.
- `README.md`
- `docs/project-overview.md`
- `docs/architecture.md`
- `docs/development/configuration.md`
- `docs/ankiweb/publishing.md`
- `ankiweb/templates/ankiweb-description.md`
- `docs/ai/REPO_CONTEXT.md`
- `docs/ai/FILE_MAP.md`
