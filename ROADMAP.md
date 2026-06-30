# Roadmap and Upgrade Ideas

This is a working list of improvements that could make Quick Search Browser more useful, configurable, and easier to maintain.

## TODO First

- Add a manafest file to the addon src.
- Add required src files to addon.
- add meta.json file to src
- generate a complete codebase that contains everything needed for github repo and ankiweb ready. follow an addon codebase template structure.

## High-Value UI Improvements

- Add a reset button that clears all Quick Search Browser filters at once.
- Show active filter count in the Browser toolbar.
- Add compact labels or icons for smaller browser widths.
- Add tooltips that explain each filter and the Anki search term it applies.
- Add a settings option to choose left, right, or wrapping alignment for the filter row.
- Add a responsive wrap layout so filters move to a new line instead of squeezing the editor/sidebar area.
- Remember the last selected filters per Anki session, with an option to disable persistence.

## Additional Filters

- Add deck filter drop-down for the current collection decks.
- Add note type filter drop-down.
- Add yield tag filter selector with different yield levels (use the yield tags and set to the anking yield by default).
- Add tag filter selector with recent or favorite tags.
- Add card state filters for learning, review, relearning, buried, suspended, and marked.
- Add interval filters such as young, mature, and custom interval ranges.
- Add ease/difficulty filters when supported by the Anki version.
- Add due overdue-only and due today-only shortcuts.
- Add created/modified date filters for notes.
- Add has-media filters for audio, images, or no media.
- Add empty-field or missing-field filters for common cleanup workflows.

## Search Presets

- Let users save current Quick Search Browser selections as named presets.
- Add a preset drop-down for common workflows like New cards, Due this week, Flagged, and Recently added.
- Allow import/export of presets through addon config JSON.
- Add optional keyboard shortcuts for applying saved presets.

## Configuration

- Make due day options configurable instead of fixed to 1, 3, 7, 14, and 30.
- Make studied day options configurable.
- Make recent added days configurable from a simple dialog, not only config JSON.
- Add config validation with friendly error messages.
- Add an option to show suspended cards by default.
- Add an option to choose which filters are visible.
- Add an option to reorder filters.

## Browser Integration

- Update the filter controls when the user manually changes the search text, where practical.
- Avoid modifying exact searches more broadly, including future Anki direct lookup formats.
- Add a visible indicator when Quick Search Browser has modified the search query.
- Consider integrating with Anki saved searches if a stable API path is available.
- Keep compatibility checks for current and upcoming Anki browser layout changes.

## Code Quality

- Split the single addon file into smaller modules under src/quick_search_browser.
- Add unit tests for query-building logic independent of Qt.
- Add a small compatibility layer for Anki/Qt API differences.
- Replace global widget state with browser-attached state so multiple Browser windows behave independently.
- Remove unused imports and narrow wildcard Qt imports.
- Add type hints for helper methods and query construction.
- Add a lightweight lint/format workflow.

## Packaging and Release

- Add a GitHub Actions workflow to run Python syntax checks on pull requests.
- Add a GitHub Actions workflow to build the .ankiaddon artifact on release tags.
- Add version metadata in one place and include it in release notes.
- Add screenshots or a short animated demo to README.md and AnkiWeb.
- Add an AnkiWeb description file or release notes template.

## Nice-to-Have Ideas

- Add per-profile settings if users want different Browser behavior per Anki profile.
- Add a command palette action for toggling common filters.
- Add optional search query preview for advanced users.
- Add localization support for labels and tooltips.
- Add theme-aware spacing or style tweaks for Anki light/dark themes.
