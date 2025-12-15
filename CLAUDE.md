# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TidyViz is a Python package for survey data cleaning and visualization pipelines. It provides specialized tools for handling survey-specific data operations like multiple choice expansion, response validation, and categorical data visualization.

## Development Setup

### Environment Setup
```bash
# Create virtual environment (one time)
python3 -m venv .venv

# Activate environment (macOS/Linux)
source .venv/bin/activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Common Commands

**Testing:**
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_tidy/test_reshape.py

# Run specific test class
pytest tests/test_tidy/test_reshape.py::TestExpandMultipleChoice

# Run specific test
pytest tests/test_tidy/test_reshape.py::TestExpandMultipleChoice::test_basic_expansion

# Run without coverage report
pytest --no-cov
```

**Code Quality:**
```bash
# Format code with Black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Format and lint together
black src/ tests/ && flake8 src/ tests/
```

**Building:**
```bash
# Build distribution packages
python -m build

# Install locally in editable mode
pip install -e .
```

## Architecture

### Package Structure

The package is organized into two main modules under `src/tidyviz/`:

**`tidy/` - Data Cleaning Module:**
- `reshape.py`: Wide-to-long/long-to-wide conversions and multiple choice handling
  - `expand_multiple_choice()`: Converts comma-separated values to binary columns
  - `collapse_multiple_choice()`: Inverse operation, binary columns to comma-separated
  - `wide_to_long()`: Converts wide format to long format (wrapper around pandas)
  - `long_to_wide()`: Converts long format to wide format (wrapper around pandas pivot)

- `validate.py`: Response validation and quality checks
  - `check_response_range()`: Validate responses are within expected ranges
  - `detect_missing_patterns()`: Identify patterns in missing data
  - `flag_straight_liners()`: Detect respondents who select the same answer repeatedly
  - `detect_speeders()`: Identify unusually fast completion times
  - `check_logical_consistency()`: Validate logical relationships between responses

**`viz/` - Visualization Module:**
- `categorical.py`: Survey-specific plotting functions
  - `plot_single_choice()`: Bar charts for single-choice questions
  - `plot_multiple_choice()`: Bar charts for multiple-choice questions (expects binary columns)
  - `plot_top_n()`: Display top N most frequent responses
  - `plot_grouped_bars()`: Compare responses across demographic groups

- `themes.py`: Styling and color palettes
  - `set_survey_style()`: Apply survey-appropriate matplotlib styling
  - `get_palette()`: Get color palettes optimized for survey data
  - `format_percentage_axis()`: Format axes to display percentages
  - `SURVEY_PALETTES`: Predefined color schemes

### API Design Pattern

The package uses a flat, function-based API accessed through module imports:

```python
import tidyviz as tp

# Data cleaning functions
tp.tidy.expand_multiple_choice(df, 'colors')
tp.tidy.check_response_range(df, 'rating', min_val=1, max_val=5)

# Visualization functions
tp.viz.plot_single_choice(df, 'method')
tp.viz.plot_multiple_choice(df, ['colors_Blue', 'colors_Red'])
```

All public functions are explicitly exported via `__all__` in module `__init__.py` files.

### Data Flow Architecture

The typical workflow follows this pattern:

1. **Load Data**: Import survey data (usually CSV) into pandas DataFrame
2. **Clean Data**: Use `tidy.*` functions to reshape, validate, and clean
3. **Visualize**: Use `viz.*` functions to create plots
4. **Pipeline**: Chain operations together for reproducible workflows

Multiple choice questions have a two-representation pattern:
- **Collapsed form**: Single column with comma-separated values (e.g., "Blue,Green,Red")
- **Expanded form**: Binary indicator columns (e.g., `colors_Blue=1`, `colors_Green=1`, `colors_Red=0`)

Use `expand_multiple_choice()` before visualization and analysis, `collapse_multiple_choice()` for export.

## Testing Approach

Tests use pytest with the following structure:
- Tests are organized in `tests/` mirroring the `src/tidyviz/` structure
- Test classes group related tests (e.g., `TestExpandMultipleChoice`)
- Test method names are descriptive (e.g., `test_basic_expansion`, `test_missing_values`)
- Use `pytest.raises()` for exception testing
- Coverage is tracked via pytest-cov and configured in `pyproject.toml`

## Configuration

**pyproject.toml** contains all project configuration:
- Build system: setuptools-based
- Dependencies: pandas, numpy, matplotlib, seaborn
- Dev dependencies: pytest, pytest-cov, black, flake8
- Python support: >=3.8
- Black config: 88 character line length
- Pytest config: coverage enabled by default with `--cov=tidyviz --cov-report=term-missing`

## Important Notes

- The package follows a flat API design - no deep class hierarchies
- All visualization functions return `matplotlib.figure.Figure` objects
- Multiple choice functions expect consistent naming: `{prefix}_{option}` for expanded columns
- The package assumes survey data is in pandas DataFrame format
- Visualization functions use color palettes optimized for survey data (avoiding red/green for accessibility)
