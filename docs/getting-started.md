# Getting Started

## Requirements

- Python 3.10 or newer. GitHub Actions uses Python 3.12.
- Anki installed locally for manual testing.
- Git for version control.
- Optional: GitHub CLI (`gh`) for one-command repository publishing.

## Local Validation

Run these from the repository root:

```bash
python tools/validate_addon.py
python tools/build_ankiaddon.py
python tools/release_check.py
```

## Install in Anki for Testing

Build the package and install `dist/*.ankiaddon` with Anki's install-from-file add-on option.

For source development, copy or symlink `src/<package>` into Anki's `addons21` directory, or run:

```bash
python tools/install_local.py --addons-dir "path/to/addons21"
```

Restart Anki after changing add-on source files.
