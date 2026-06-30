# AI Review Checklist

Before finalizing changes, check:

- Does the add-on still have `__init__.py` and `manifest.json` packaged at archive root?
- Does `python tools/validate_addon.py` pass?
- Does `python tools/build_ankiaddon.py` pass?
- Does `VERSION` match `manifest.json`?
- Do docs match the changed behavior?
- Are AnkiWeb templates still accurate?
- Are GitHub workflow commands still valid on Ubuntu runners?
- Did the change avoid touching unrelated user work?
