# Contributing to TidyViz

Thank you for considering contributing to TidyViz! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and constructive in all interactions with the community.

## Getting Started

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/pingfan-hu/tidyviz.git
cd tidyviz
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Verify installation:
```bash
pytest
black --check src/ tests/
flake8 src/ tests/
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

Write code following these guidelines:

**Code Style**
- Format code with Black (88 character line length)
- Follow PEP 8 conventions
- Use type hints for function parameters and returns
- Write clear, concise docstrings

**Testing**
- Add tests for new functionality
- Ensure all tests pass
- Maintain or improve code coverage

**Documentation**
- Update docstrings for modified functions
- Add examples to documentation
- Update CHANGELOG.md

### 3. Test Your Changes

```bash
# Run tests
pytest

# Check code formatting
black src/ tests/

# Check code quality
flake8 src/ tests/

# Run specific tests
pytest tests/test_tidy/test_reshape.py
```

### 4. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add function to detect duplicate responses"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Test results

## Pull Request Process

1. **Ensure tests pass** - All tests must pass before PR review
2. **Update documentation** - Include relevant documentation updates
3. **Add changelog entry** - Document changes in CHANGELOG.md
4. **Request review** - Tag maintainers for review
5. **Address feedback** - Make requested changes promptly

## Coding Standards

### Function Documentation

Use this docstring format:

```python
def example_function(df: pd.DataFrame, column: str, threshold: int = 5) -> pd.Series:
    """
    Brief one-line description.

    More detailed description if needed. Explain what the function does,
    when to use it, and any important considerations.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to process
    threshold : int, optional
        Threshold value, by default 5

    Returns
    -------
    pd.Series
        Boolean series indicating flagged rows

    Examples
    --------
    >>> df = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
    >>> result = example_function(df, 'values', threshold=3)
    >>> result
    0    False
    1    False
    2    False
    3     True
    4     True
    dtype: bool
    """
    # Implementation
    pass
```

### Test Structure

```python
import pytest
import pandas as pd
import tidyviz as tv

class TestFeatureName:
    """Test suite for specific feature."""

    def test_basic_functionality(self):
        """Test basic use case."""
        df = pd.DataFrame({'col': [1, 2, 3]})
        result = tv.tidy.function_name(df, 'col')
        assert len(result) == 3

    def test_edge_case(self):
        """Test edge case behavior."""
        df = pd.DataFrame({'col': []})
        result = tv.tidy.function_name(df, 'col')
        assert len(result) == 0

    def test_error_handling(self):
        """Test proper error handling."""
        df = pd.DataFrame({'col': [1, 2, 3]})
        with pytest.raises(ValueError):
            tv.tidy.function_name(df, 'nonexistent')
```

## Types of Contributions

### Bug Reports

Submit bug reports via GitHub Issues with:
- Clear title describing the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, package version)
- Minimal code example

**Example:**
```
Title: expand_multiple_choice fails with semicolon separator

Description:
When using semicolon as separator, expand_multiple_choice raises
a KeyError.

Steps to reproduce:
1. Create dataframe with semicolon-separated values
2. Call expand_multiple_choice(df, 'col', sep=';')
3. KeyError is raised

Expected: Binary columns created successfully
Actual: KeyError: 'col'

Environment:
- Python 3.10
- tidyviz 0.1.0
- pandas 1.5.0
```

### Feature Requests

Submit feature requests via GitHub Issues with:
- Clear description of proposed feature
- Use case and motivation
- Proposed API (if applicable)
- Example usage

### Code Contributions

**Priority Areas:**
- Bug fixes
- Documentation improvements
- Test coverage improvements
- Performance optimizations
- New validation functions
- New visualization types

**Guidelines:**
- Discuss major changes in an issue first
- Keep PRs focused on single feature/fix
- Include tests and documentation
- Follow existing code patterns

## Documentation Contributions

Improvements to documentation are always welcome:

**README.md** - Quick start and overview
**docs/API.md** - Complete function reference
**docs/USER_GUIDE.md** - Tutorials and workflows
**examples/** - Working code examples

## Questions?

- Open a GitHub Issue for questions
- Check existing documentation first
- Be specific about what you're trying to accomplish

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
