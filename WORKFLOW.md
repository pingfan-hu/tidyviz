## Setup

1. Create venv (only once)

Run this to create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate venv (not needed for Positron)

```bash
source .venv/bin/activate
```

3. Install packages (only when you need new packages):

```bash
pip install pandas
pip install numpy
# etc.
```

4. Deactivate venv (when you're done working):

```bash
deactivate
```

5. Install this developing package:

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies (pytest, black, flake8, etc.)

## Testing

6. Run tests:

```bash
# Run all tests with coverage
pytest

# Run tests without coverage report (faster)
pytest --no-cov

# Run specific test file
pytest tests/test_tidy/test_reshape.py

# Run specific test class
pytest tests/test_tidy/test_reshape.py::TestExpandMultipleChoice

# Run specific test function
pytest tests/test_tidy/test_reshape.py::TestExpandMultipleChoice::test_basic_expansion
```

7. Code formatting and linting:

```bash
# Format code with Black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Format and lint together
black src/ tests/ && flake8 src/ tests/
```

## Releasing a New Version

### Pre-Release Checklist

8. Before releasing, ensure:

```bash
# All tests pass
pytest

# Code is formatted
black src/ tests/

# Code passes linting
flake8 src/ tests/
```

### Version Bump Process

9. Update version number in **two** files:

**File 1: `pyproject.toml`**
```toml
[project]
version = "0.1.1"  # Update this
```

**File 2: `src/tidyviz/__init__.py`**
```python
__version__ = "0.1.1"  # Update this
```

10. Update `CHANGELOG.md`:

Add a new section at the top with your changes:
```markdown
## [0.1.1] - 2025-01-XX

### Added
- New features you added

### Changed
- Things you modified

### Fixed
- Bugs you fixed
```

11. Commit version bump:

```bash
git add pyproject.toml src/tidyviz/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.1.1"
```

### Building and Publishing

12. Build distribution packages:

```bash
# Clean previous builds (recommended)
rm -rf dist/ build/ src/*.egg-info

# Build both wheel and source distribution
python -m build
```

This creates two files in `dist/`:
- `tidyviz-<version>-py3-none-any.whl` (wheel distribution)
- `tidyviz-<version>.tar.gz` (source distribution)

13. Validate built packages:

```bash
# Check packages for common issues
twine check dist/*
```

14. Upload to PyPI:

```bash
# Option 1: Upload to TestPyPI first (recommended for testing)
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ tidyviz

# Option 2: Upload to PyPI (production)
twine upload dist/*
```

**Note:** You need a PyPI account and API token to upload packages.

### Post-Release

15. Create git tag and push:

```bash
# Create annotated tag
git tag -a v0.1.1 -m "Release version 0.1.1"

# Push commits
git push origin main

# Push tag
git push origin v0.1.1
```

16. Create GitHub release (optional):

Go to GitHub repository → Releases → Create new release
- Tag: v0.1.1
- Title: TidyViz v0.1.1
- Description: Copy from CHANGELOG.md

## Quick Reference

```bash
# Development workflow
source .venv/bin/activate     # Activate venv (macOS/Linux)
pip install -e ".[dev]"       # Install in editable mode
pytest                         # Run tests
black src/ tests/              # Format code
python -m build                # Build package
deactivate                     # Deactivate venv

# Release workflow (compact)
pytest && black src/ tests/ && flake8 src/ tests/  # Pre-release checks
# Update: pyproject.toml, __init__.py, CHANGELOG.md
git add pyproject.toml src/tidyviz/__init__.py CHANGELOG.md
git commit -m "Bump version to X.X.X"
rm -rf dist/ build/ src/*.egg-info && python -m build
twine check dist/*
twine upload dist/*  # Requires PyPI credentials
git tag -a vX.X.X -m "Release version X.X.X"
git push origin main && git push origin vX.X.X
```