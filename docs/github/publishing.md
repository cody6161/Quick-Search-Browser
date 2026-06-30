# GitHub Publishing

## One-Time Setup With GitHub CLI

Install GitHub CLI, authenticate, then run:

```bash
gh auth login
python tools/publish_github.py --repo OWNER/REPO --public
```

Use `--private` instead of `--public` if the repository should start private.

## Manual Setup Without GitHub CLI

```bash
git init
git add .
git commit -m "Initial add-on repository"
git branch -M main
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
```

## GitHub Actions

- CI runs on pushes and pull requests.
- Release automation runs when pushing tags that start with `v`.
- Release artifacts include the `.ankiaddon` package, `SHA256SUMS.txt`, and `release.json`.

## One-Command GitHub Release

After `gh auth login`, the release script can bump the version, build the package,
commit, tag, push, generate changelog-based release notes, and create or update
the GitHub release:

```bash
python tools/create_release.py patch --push --github-release
```

Use `minor`, `major`, or an explicit version instead of `patch` when needed.
Use `--repo OWNER/REPO` if GitHub CLI cannot infer the repository from `origin`.
