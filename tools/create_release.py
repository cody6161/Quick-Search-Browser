"""Create and optionally publish a versioned release.

This is the high-level release automation script. It wraps the existing
version, build, and release-prep tools, then creates the matching Git commit
and tag. With ``--github-release`` it also pushes the release and creates or
updates the GitHub release with the generated .ankiaddon package.

Examples:
    python tools/create_release.py patch
    python tools/create_release.py minor --push
    python tools/create_release.py patch --push --github-release
    python tools/create_release.py 1.2.3 --allow-dirty --push
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from versioning import read_manifest, read_version


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CHANGELOG = ROOT / "CHANGELOG.md"
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


def run(args: list[str], *, capture: bool = False, check: bool = True) -> str:
    print("+ " + " ".join(args))
    completed = subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError(completed.returncode, args)
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


def ensure_github_release_ready(args: argparse.Namespace) -> None:
    if not args.github_release:
        return
    if not args.push:
        raise SystemExit("`--github-release` requires `--push` so the release tag exists on GitHub.")
    try:
        run(["gh", "--version"], capture=True)
        auth_args = ["gh", "auth", "status"]
        if args.repo:
            auth_args.extend(["--hostname", "github.com"])
        run(auth_args, capture=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(
            "GitHub release publishing requires GitHub CLI (`gh`) installed and authenticated. "
            "Run `gh auth login`, then try again."
        ) from exc


def stage_release_files(include_all: bool) -> None:
    if include_all:
        run(["git", "add", "."])
        return

    existing_paths = [path for path in RELEASE_PATHS if (ROOT / path).exists()]
    run(["git", "add", *existing_paths])


def has_staged_changes() -> bool:
    completed = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    return completed.returncode != 0


def release_artifacts() -> list[Path]:
    metadata_path = DIST / "release.json"
    if not metadata_path.exists():
        raise SystemExit("dist/release.json is missing. Run release checks before publishing.")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    package_name = str(metadata.get("artifact", "")).strip()
    package = DIST / package_name
    checksum = DIST / "SHA256SUMS.txt"
    artifacts = [package, checksum, metadata_path]
    missing = [path for path in artifacts if not path.exists()]
    if missing:
        raise SystemExit("Missing release artifact(s): " + ", ".join(str(path) for path in missing))
    return artifacts


def changelog_entry(version: str) -> str:
    if not CHANGELOG.exists():
        return ""

    text = CHANGELOG.read_text(encoding="utf-8")
    header = re.search(rf"^##\s+{re.escape(version)}\s+-\s+.+$", text, re.MULTILINE)
    if not header:
        return ""

    next_header = re.search(r"^##\s+", text[header.end() :], re.MULTILINE)
    end = header.end() + next_header.start() if next_header else len(text)
    body = text[header.end() : end].strip()
    return "" if body == "-" else body


def write_github_release_notes(version: str, tag: str) -> Path:
    manifest = read_manifest()
    addon_name = str(manifest.get("name") or "Release").strip()
    body = changelog_entry(version) or "- Release package and metadata updates."
    notes = (
        f"## {addon_name} {tag}\n\n"
        f"{body}\n\n"
        "## Artifacts\n\n"
        "- `.ankiaddon` package for Anki installation.\n"
        "- `SHA256SUMS.txt` for checksum verification.\n"
        "- `release.json` with package metadata.\n"
    )
    DIST.mkdir(exist_ok=True)
    notes_path = DIST / "github-release-notes.md"
    notes_path.write_text(notes, encoding="utf-8")
    return notes_path


def gh_args(args: argparse.Namespace, command: list[str]) -> list[str]:
    full_command = ["gh", *command]
    if args.repo:
        full_command.extend(["--repo", args.repo])
    return full_command


def github_release_exists(args: argparse.Namespace, tag: str) -> bool:
    completed = subprocess.run(
        gh_args(args, ["release", "view", tag]),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def publish_github_release(args: argparse.Namespace, tag: str, notes_path: Path) -> None:
    artifacts = release_artifacts()
    artifact_args = [str(path) for path in artifacts]

    if github_release_exists(args, tag):
        run(gh_args(args, ["release", "edit", tag, "--title", tag, "--notes-file", str(notes_path)]))
        run(gh_args(args, ["release", "upload", tag, *artifact_args, "--clobber"]))
        return

    create_args = ["release", "create", tag, *artifact_args, "--title", tag, "--notes-file", str(notes_path)]
    if args.draft:
        create_args.append("--draft")
    if args.prerelease:
        create_args.append("--prerelease")
    run(gh_args(args, create_args))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump, build, commit, tag, and optionally publish a GitHub release."
    )
    parser.add_argument("version", help="major, minor, patch, or an explicit semantic version.")
    parser.add_argument("--push", action="store_true", help="Push the release commit and tag to origin.")
    parser.add_argument(
        "--github-release",
        action="store_true",
        help="Create or update the GitHub release with the generated package artifacts. Requires --push.",
    )
    parser.add_argument("--repo", help="GitHub repository for gh commands, such as OWNER/REPO.")
    parser.add_argument("--draft", action="store_true", help="Create the GitHub release as a draft.")
    parser.add_argument("--prerelease", action="store_true", help="Mark the GitHub release as a prerelease.")
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
    ensure_github_release_ready(args)

    bump_args = [sys.executable, "tools/bump_version.py", args.version]
    if args.no_changelog:
        bump_args.append("--no-changelog")
    run(bump_args)

    version = read_version()
    tag = f"v{version}"
    ensure_tag_available(tag)

    run([sys.executable, "tools/prepare_release.py"])
    notes_path = write_github_release_notes(version, tag)
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
        if args.github_release:
            publish_github_release(args, tag, notes_path)
    else:
        print()
        print(f"Created release commit and tag {tag}.")
        print(f"Push with: git push origin {current_branch()}")
        print(f"Push tag with: git push origin {tag}")
    print(f"GitHub release notes: {notes_path}")


if __name__ == "__main__":
    main()
