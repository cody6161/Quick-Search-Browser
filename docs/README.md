# Documentation Index

This folder is the canonical maintainer manual for Quick Search Browser and the reusable Anki add-on repository template around it.

The root of `docs/` is reserved for project-wide reference material: what this codebase is, how it is shaped, what standards it follows, and how future add-ons should adapt it. Focused process docs live in subfolders.

## Root Reference

- `project-overview.md`: detailed description of this add-on, its behavior, and the repository goals.
- `architecture.md`: runtime architecture, Anki hook flow, packaging model, and automation architecture.
- `project-structure.md`: file and folder map for the repository.
- `standards.md`: coding, documentation, release, and repository standards.
- `getting-started.md`: first-run setup and local validation.
- `maintenance.md`: ongoing maintainer checklist.

## Subfolders

- `development/`: local development workflow, testing, configuration, and troubleshooting.
- `release/`: package building, release checks, and release process.
- `ankiweb/`: AnkiWeb-specific publishing instructions and listing guidance.
- `github/`: GitHub hosting, workflows, release artifacts, and repository publishing.
- `ai/`: AI assistant instructions, codebase context, Anki add-on rules, and task checklists.

## Recommended Reading Paths

For a new human maintainer:

1. `project-overview.md`
2. `architecture.md`
3. `getting-started.md`
4. `development/workflow.md`
5. `release/process.md`

For release work:

1. `release/process.md`
2. `release/build-and-package.md`
3. `ankiweb/publishing.md`
4. `github/publishing.md`

For AI-assisted work:

1. `ai/README.md`
2. `ai/AI_INSTRUCTIONS.md`
3. `ai/REPO_CONTEXT.md`
4. `ai/ANKI_ADDON_SPECIFICS.md`
5. `ai/REVIEW_CHECKLIST.md`
