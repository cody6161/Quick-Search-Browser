# Repository Context

This repository contains Quick Search Browser, an Anki add-on that adds quick filters to Anki's Browser window.

## Current Add-on Package

- Source folder: `src/quick_search_browser/`
- Entry point: `src/quick_search_browser/__init__.py`
- Manifest: `src/quick_search_browser/manifest.json`
- Default config: `src/quick_search_browser/config.json`
- Config help: `src/quick_search_browser/config.md`

## User-Facing Behavior

The add-on adds a second row of controls below Anki's normal Browser search controls. These controls modify Browser search queries through Anki hooks.

## Maintenance Goal

The repo should also work as a reusable starting point for future Anki add-ons. Automation should discover package metadata from `src/<package>/manifest.json` instead of hardcoding one add-on name whenever practical.
