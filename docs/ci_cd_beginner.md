# CI/CD for Beginners with fyntool

## What is CI/CD?
CI = Continuous Integration: automatically test your code on push.
CD = Continuous Delivery/Deployment: automatically build and release.

## Simple GitHub Actions workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install uv
        run: pip install uv
      - name: Install deps
        run: uv pip install -e .
      - name: Run doctor
        run: fyntool doctor
      - name: Run env check
        run: fyntool env
```

## Add Docker build
```yaml
      - name: Build Docker
        run: docker compose -f docker-compose.yml build
```

## Add release on tag
Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
```

## Tips
- Start small: just checkout + setup python + run tests
- Use `fyntool doctor` in CI to catch missing tools
- Store secrets in GitHub Secrets, never in repo
- For Crew AI, add secrets `CREW_AI_API_KEY` and use them in workflow

## Next steps
- Add lint with `ruff` / `flake8`
- Add tests with `pytest`
- Use `fyntool build` / `fyntool run` in CI
