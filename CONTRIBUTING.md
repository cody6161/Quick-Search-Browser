# Contributing

Thanks for helping improve Quick Search Browser. This is a small Anki add-on, so changes should stay focused and easy to review.

## Local setup

1. Clone the repository.
2. Copy or symlink `src/quick_search_browser` into Anki's `addons21` folder.
3. Restart Anki after code changes so the add-on is reloaded.

## Checks before opening a pull request

Run:

```bash
python -m py_compile src/quick_search_browser/__init__.py tools/build_ankiaddon.py
python tools/build_ankiaddon.py
```

Then test the Browser window in Anki and confirm the quick filters still update searches correctly.

## Pull request guidance

- Keep UI behavior changes small and described clearly.
- Do not commit `meta.json`, `dist/`, `.ankiaddon` files, `.vscode/`, or `__pycache__/`.
- Update `README.md` or `CHANGELOG.md` when behavior changes.
