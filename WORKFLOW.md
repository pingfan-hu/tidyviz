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

## Building and Publishing

8. Build distribution packages:

```bash
# Clean previous builds (optional but recommended)
rm -rf dist/ build/ src/*.egg-info

# Build both wheel and source distribution
python -m build
```

This creates two files in `dist/`:
- `tidyviz-0.1.0-py3-none-any.whl` (wheel distribution)
- `tidyviz-0.1.0.tar.gz` (source distribution)

9. Validate built packages:

```bash
# Check packages for common issues
twine check dist/*
```

10. Upload to PyPI:

```bash
# Upload to TestPyPI first (recommended for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

**Note:** You need a PyPI account and API token to upload packages.

## Quick Reference

```bash
# Development workflow
source .venv/bin/activate     # Activate venv (macOS/Linux)
pip install -e ".[dev]"       # Install in editable mode
pytest                         # Run tests
black src/ tests/              # Format code
python -m build                # Build package
deactivate                     # Deactivate venv
```