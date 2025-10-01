# GitHub Actions Workflows

## python-app.yml - Galaxy Wizard CI

This workflow runs automatically on:
- Push to `main` branch
- Pull requests to `main` branch

### What it does:

1. **Sets up Python 3.11** - Matches your development environment
2. **Installs Poetry** - Uses Poetry for dependency management (not pip/requirements.txt)
3. **Caches dependencies** - Speeds up subsequent runs by caching `.venv`
4. **Installs project dependencies** - Runs `poetry install` to get all packages from `poetry.lock`
5. **Lints with flake8** - Checks Python code for syntax errors and style issues
6. **Runs pytest** - Executes all 33 unit tests from the `tests/` directory

### Key differences from standard workflow:

- ✅ Uses **Poetry** instead of pip/requirements.txt
- ✅ Runs tests from `src/` directory (needed for resource file paths)
- ✅ Only lints `src/` directory (not test files)
- ✅ Caches Poetry virtual environment for faster builds

### Test results:

The workflow runs all test suites:
- 7 Unit tests (`test_unit.py`)
- 4 Battle tests (`test_battle.py`)
- 8 AI tests (`test_ai.py`)
- 14 Map tests (`test_map.py`)

**Total: 33 tests** ✅

### Troubleshooting:

If tests fail in CI but pass locally:
1. Check that you committed `poetry.lock` file
2. Verify all data files in `src/data/` are committed
3. Tests need to run from `src/` directory to find resource files

### Local testing:

To run the same checks locally:
```bash
# Lint
poetry run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics

# Test
cd src && poetry run pytest ../tests/ -v
```
