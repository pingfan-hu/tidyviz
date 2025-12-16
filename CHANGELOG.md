# Changelog

All notable changes to TidyViz will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added

**Data Cleaning (`tidyviz.tidy`)**
- `expand_multiple_choice()` - Convert comma-separated values to binary columns
- `collapse_multiple_choice()` - Convert binary columns back to comma-separated values
- `check_response_range()` - Validate responses within expected range
- `detect_missing_patterns()` - Analyze missing data patterns
- `flag_straight_liners()` - Detect identical responses across questions
- `detect_speeders()` - Identify unusually fast completion times
- `check_logical_consistency()` - Validate custom logical rules

**Visualization (`tidyviz.viz`)**
- `plot_single_choice()` - Bar charts for single-choice questions
- `plot_multiple_choice()` - Bar charts for multiple-choice questions
- `set_survey_style()` - Apply survey-appropriate styling
- `get_palette()` - Get color palettes for visualizations

**Documentation**
- Comprehensive README with quick start guide
- Detailed API reference documentation
- User guide with workflows and best practices
- Working examples for data cleaning and visualization

**Testing**
- Full test suite with 39 tests
- Code coverage tracking with pytest-cov
- Automated code formatting with Black
- Code quality checks with flake8

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

---

## Release Notes

### [0.1.0] - Initial Release

TidyViz provides essential tools for survey data analysis in Python. This initial release focuses on:

1. **Core data cleaning operations** - Handle the most common survey data preparation tasks including multiple choice expansion, response validation, and quality checks.

2. **Professional visualizations** - Create publication-ready plots for single and multiple choice questions with survey-appropriate styling.

3. **Production-ready code** - Comprehensive test coverage, formatted code, and detailed documentation ensure reliability and maintainability.

**Author:**
- Pingfan Hu (https://pingfanhu.com)

**Target Users:**
- Survey researchers
- Data analysts working with questionnaire data
- Social scientists conducting quantitative research

**Requirements:**
- Python ≥ 3.8
- pandas ≥ 1.3.0
- numpy ≥ 1.20.0
- matplotlib ≥ 3.4.0
- seaborn ≥ 0.11.0

**Known Limitations:**
- Binary columns must follow `{prefix}_{option}` naming convention for `collapse_multiple_choice()`
- Visualization functions return matplotlib figures but don't call `plt.show()` automatically
- Logical consistency rules require lambda functions (not string expressions)

**Future Development:**
Planned features for upcoming releases include:
- Advanced visualizations (Likert scales, distributions, completion funnels)
- Additional data transformations (recoding, text processing)
- Pipeline composition utilities
- Export to common formats (SPSS, Stata)
