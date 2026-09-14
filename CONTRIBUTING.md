# Contributing to fyntool

Thanks for your interest! This guide will help you contribute.

## How to contribute
1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Install with uv tool:
   ```bash
   uv tool install --from git+https://github.com/FynChat/fyntool fyntool
   ```
   Or dev install:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```
4. Make changes
5. Run `fyntool doctor --fix`
6. Test your command: `fyntool --help` and `fyntool <command> --help`
7. Commit and push
8. Open a Pull Request

## Code style
- Python 3.12+
- Use clear docstrings for commands
- Keep `run_cmd` consistent
- Add usage examples in factory docstrings

## Issues
Use the issue template in `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`.

## Release
Only maintainers run `fyntool release` to create tags.

## Questions?
Open a discussion or issue.
