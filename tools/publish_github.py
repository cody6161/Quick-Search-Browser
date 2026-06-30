"""Publish the local repository to GitHub using GitHub CLI when available.

This script intentionally does not invent credentials. Install and authenticate
GitHub CLI first:

    gh auth login

Then run:

    python tools/publish_github.py --repo OWNER/REPO --public
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> str:
    completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)
    if completed.stdout.strip():
        print(completed.stdout.strip())
    return completed.stdout


def has_origin() -> bool:
    remotes = run(["git", "remote"])
    return "origin" in {line.strip() for line in remotes.splitlines()}


def current_branch() -> str:
    return run(["git", "branch", "--show-current"]).strip() or "main"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or push this repo to GitHub with gh.")
    parser.add_argument("--repo", required=True, help="GitHub repository as owner/name.")
    visibility = parser.add_mutually_exclusive_group()
    visibility.add_argument("--public", action="store_true", help="Create a public repository.")
    visibility.add_argument("--private", action="store_true", help="Create a private repository.")
    args = parser.parse_args()

    if shutil.which("gh") is None:
        raise SystemExit("GitHub CLI is not installed. Install gh and run `gh auth login` first.")

    if not has_origin():
        flag = "--private" if args.private else "--public"
        run(["gh", "repo", "create", args.repo, flag, "--source", ".", "--remote", "origin", "--push"])
    else:
        run(["git", "push", "-u", "origin", current_branch()])


if __name__ == "__main__":
    main()
