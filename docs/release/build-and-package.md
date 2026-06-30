# Build and Package

`tools/build_ankiaddon.py` discovers the add-on package by finding `src/*/manifest.json`. It packages the contents of that folder at the root of the `.ankiaddon` archive, which is what Anki expects.

## Build

```bash
python tools/build_ankiaddon.py
```

Output goes to `dist/<Add-on Name>.ankiaddon`.

## Release Check

```bash
python tools/release_check.py
```

This validates source files, checks version metadata, builds the package, confirms required package files are present, and writes:

- `dist/SHA256SUMS.txt`
- `dist/release.json`

## Files Excluded from Package

- `__pycache__/`
- `.pyc` and `.pyo` files
- `meta.json`
- local test/cache directories
