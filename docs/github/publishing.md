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
- Release artifacts include the `.ankiaddon` package and `SHA256SUMS.txt`.
