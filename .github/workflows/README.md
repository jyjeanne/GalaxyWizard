# GitHub Actions Workflows

## python-app.yml - Galaxy Wizard CI

This workflow runs automatically on:
- Push to `main` branch
- Pull requests to `main` branch

### What it does:

The workflow consists of **3 parallel jobs**:

#### Job 1: Test (Ubuntu)
1. **Sets up Python 3.11** - Matches your development environment
2. **Installs Poetry** - Uses Poetry for dependency management (not pip/requirements.txt)
3. **Caches dependencies** - Speeds up subsequent runs by caching `.venv`
4. **Installs system dependencies** - xvfb, libgl1-mesa-dev, libglu1-mesa-dev (for headless OpenGL)
5. **Installs project dependencies** - Runs `poetry install` to get all packages from `poetry.lock`
6. **Lints with flake8** - Checks Python code for syntax errors and style issues
7. **Runs pytest with xvfb** - Executes all 33 unit tests using virtual display (OpenGL requires graphics context)

#### Job 2: Build Windows Executable (requires test job to pass)
1. **Sets up Python 3.11 on Windows**
2. **Installs Poetry** - Windows-specific installation
3. **Installs dependencies** - Including PyInstaller
4. **Builds standalone .exe** - Uses `main.spec` to create `GalaxyWizard.exe`
5. **Uploads artifact** - Executable available for download (30 days retention)

#### Job 3: Build Linux Executable (requires test job to pass)
1. **Sets up Python 3.11 on Ubuntu**
2. **Installs Poetry**
3. **Installs system dependencies** - xvfb, OpenGL libraries
4. **Installs dependencies** - Including PyInstaller
5. **Builds standalone binary** - Uses `main.spec` to create `GalaxyWizard` binary
6. **Uploads artifact** - Executable available for download (30 days retention)

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

### Downloading Built Executables:

After a successful workflow run:
1. Go to the **Actions** tab in GitHub
2. Click on the workflow run
3. Scroll to **Artifacts** section
4. Download `GalaxyWizard-Windows.zip` or `GalaxyWizard-Linux.zip`
5. Extract and run the standalone executable

**Note:** Executables are kept for 30 days

### Troubleshooting:

If tests fail in CI but pass locally:
1. Check that you committed `poetry.lock` file
2. Verify all data files in `src/data/` are committed
3. Tests need to run from `src/` directory to find resource files

If build jobs fail:
1. Check that `main.spec` is committed
2. Verify Python version is 3.11 (PyInstaller compatibility)
3. Windows builds may fail if PyOpenGL-accelerate requires C++ build tools (this is optional)

### Local testing:

To run the same checks locally:
```bash
# Lint
poetry run flake8 src --exclude=src/data,src/test/data --count --select=E9,F63,F7,F82 --ignore=F824 --show-source --statistics

# Test (with display)
cd src && poetry run pytest ../tests/ -v

# Test (headless Linux - requires xvfb)
cd src && xvfb-run -a poetry run pytest ../tests/ -v
```
