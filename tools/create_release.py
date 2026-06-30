"""Create a versioned release commit and Git tag.

This is the high-level release automation script. It wraps the existing
version, build, and release-prep tools, then creates the matching Git commit
and tag.

Examples:
    python tools/create_release.py patch
    python tools/create_release.py minor --push
    python tools/create_release.py 1.2.3 --allow-dirty --push
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from versioning import read_version


ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATHS = [
    "VERSION",
    "CHANGELOG.md",
    "README.md",
    "RELEASE.md",
    "src",
    "tools",
    "docs",
    "ankiweb",
    ".github",
]


def run(args: list[str], *, capture: bool = False) -> str:
    print("+ " + " ".join(args))
    completed = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture,
    )
    if capture:
        return completed.stdout.strip()
    return ""


def git_output(args: list[str]) -> str:
    return run(["git", *args], capture=True)


def worktree_status() -> str:
    return git_output(["status", "--porcelain"])


def ensure_clean_worktree(allow_dirty: bool) -> None:
    status = worktree_status()
    if status and not allow_dirty:
        raise SystemExit(
            "Working tree has existing changes. Commit/stash them first, or rerun with "
            "`--allow-dirty` to include them in the release commit."
        )


def ensure_tag_available(tag: str) -> None:
    completed = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode == 0:
        raise SystemExit(f"Tag {tag} already exists.")


def current_branch() -> str:
    branch = git_output(["branch", "--show-current"])
    return branch or "main"


def stage_release_files(include_all: bool) -> None:
    if include_all:
        run(["git", "add", "."])
        return

    existing_paths = [path for path in RELEASE_PATHS if (ROOT / path).exists()]
    run(["git", "add", *existing_paths])


def has_staged_changes() -> bool:
    completed = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    return completed.returncode != 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump, build, commit, tag, and optionally push a release.")
    parser.add_argument("version", help="major, minor, patch, or an explicit semantic version.")
    parser.add_argument("--push", action="store_true", help="Push the release commit and tag to origin.")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow existing worktree changes and include them in the release commit.",
    )
    parser.add_argument(
        "--no-changelog",
        action="store_true",
        help="Do not let bump_version.py create a changelog release section.",
    )
    parser.add_argument(
        "--message",
        help="Commit message. Defaults to 'Release v<VERSION>'.",
    )
    args = parser.parse_args()

    ensure_clean_worktree(args.allow_dirty)

    bump_args = [sys.executable, "tools/bump_version.py", args.version]
    if args.no_changelog:
        bump_args.append("--no-changelog")
    run(bump_args)

    version = read_version()
    tag = f"v{version}"
    ensure_tag_available(tag)

    run([sys.executable, "tools/prepare_release.py"])
    stage_release_files(include_all=args.allow_dirty)

    if not has_staged_changes():
        raise SystemExit("No staged release changes found; refusing to create an empty release commit.")

    message = args.message or f"Release {tag}"
    run(["git", "commit", "-m", message])
    run(["git", "tag", tag])

    if args.push:
        branch = current_branch()
        run(["git", "push", "origin", branch])
        run(["git", "push", "origin", tag])
    else:
        print()
        print(f"Created release commit and tag {tag}.")
        print(f"Push with: git push origin {current_branch()}")
        print(f"Push tag with: git push origin {tag}")


if __name__ == "__main__":
    main()
