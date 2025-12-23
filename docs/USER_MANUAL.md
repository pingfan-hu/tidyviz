# TidyViz User Manual

Complete documentation for survey data cleaning and visualization with TidyViz.

## Table of Contents

1. [Installation](#installation)
2. [Core Concepts](#core-concepts)
3. [Data Cleaning API](#data-cleaning-api)
4. [Visualization API](#visualization-api)
5. [Workflows & Patterns](#workflows--patterns)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Standard Installation

```bash
pip install tidyviz
```

### Development Installation

```bash
git clone https://github.com/pingfan-hu/tidyviz.git
cd tidyviz
pip install -e ".[dev]"
```

### Requirements

- Python ≥ 3.8
- pandas ≥ 1.3.0
- numpy ≥ 1.20.0
- matplotlib ≥ 3.4.0
- seaborn ≥ 0.11.0

### Verify Installation

```python
import tidyviz as tv
print(tv.__version__)
```

---

## Core Concepts

### Multiple Choice Data Representation

TidyViz handles multiple choice questions in two formats:

**Collapsed Format** (storage-efficient)
```
| respondent | colors        |
|------------|---------------|
| 1          | Red,Blue      |
| 2          | Green         |
| 3          | Blue,Green    |
```

**Expanded Format** (analysis-ready)
```
| respondent | colors_Red | colors_Blue | colors_Green |
|------------|------------|-------------|--------------|
| 1          | 1          | 1           | 0            |
| 2          | 0          | 0           | 1            |
| 3          | 0          | 1           | 1            |
```

Use `expand_multiple_choice()` for analysis and visualization, `collapse_multiple_choice()` for storage.

### Response Validation Strategies

TidyViz provides three strategies for handling invalid responses:

1. **Flag** (`handle_invalid='flag'`) - Keep data, add validity indicator column
2. **Remove** (`handle_invalid='remove'`) - Drop invalid rows from dataframe
3. **NaN** (`handle_invalid='nan'`) - Replace invalid values with NaN

Choose based on your analysis needs and reporting requirements.

---

## Data Cleaning API

### Multiple Choice Functions

#### `expand_multiple_choice()`

Convert comma-separated multiple choice responses into binary indicator columns.

**Signature:**
```python
expand_multiple_choice(
    df: pd.DataFrame,
    column: str,
    sep: str = ',',
    keep_original: bool = False,
    prefix: str = None
) -> pd.DataFrame
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name containing comma-separated values
- `sep` (str, optional): Separator character. Default: `','`
- `keep_original` (bool, optional): Keep original column. Default: `False`
- `prefix` (str, optional): Prefix for new columns. Default: column name

**Returns:**
- DataFrame: New dataframe with binary indicator columns

**Example:**
```python
import pandas as pd
import tidyviz as tv

df = pd.DataFrame({
    'id': [1, 2, 3],
    'colors': ['Red,Blue', 'Green', 'Blue,Green']
})

df_expanded = tv.tidy.expand_multiple_choice(df, 'colors')
print(df_expanded)
# Creates columns: colors_Red, colors_Blue, colors_Green
```

**Advanced Usage:**
```python
# Keep original column
df_exp = tv.tidy.expand_multiple_choice(
    df, 'colors',
    keep_original=True
)

# Custom separator
df_exp = tv.tidy.expand_multiple_choice(
    df, 'colors',
    sep=';'
)

# Custom prefix
df_exp = tv.tidy.expand_multiple_choice(
    df, 'colors',
    prefix='fav_color'
)
# Creates: fav_color_Red, fav_color_Blue, etc.
```

---

#### `collapse_multiple_choice()`

Convert binary indicator columns back to comma-separated values.

**Signature:**
```python
collapse_multiple_choice(
    df: pd.DataFrame,
    prefix: str,
    sep: str = ',',
    drop_binary: bool = True
) -> pd.DataFrame
```

**Parameters:**
- `df` (DataFrame): Input dataframe with binary columns
- `prefix` (str): Common prefix of binary columns to collapse
- `sep` (str, optional): Separator for output. Default: `','`
- `drop_binary` (bool, optional): Drop binary columns after collapse. Default: `True`

**Returns:**
- DataFrame: Dataframe with collapsed column

**Example:**
```python
# Collapse expanded columns back
df_collapsed = tv.tidy.collapse_multiple_choice(df_expanded, 'colors')
# Recreates original 'colors' column

# Keep binary columns
df_both = tv.tidy.collapse_multiple_choice(
    df_expanded, 'colors',
    drop_binary=False
)
```

---

### Validation Functions

#### `check_response_range()`

Validate that responses fall within expected range.

**Signature:**
```python
check_response_range(
    df: pd.DataFrame,
    column: str,
    min_val: float,
    max_val: float,
    handle_invalid: str = 'flag'
) -> tuple[pd.DataFrame, pd.Series]
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name to validate
- `min_val` (float): Minimum valid value
- `max_val` (float): Maximum valid value
- `handle_invalid` (str, optional): How to handle invalid values:
  - `'flag'`: Add `{column}_valid` column, keep invalid values
  - `'remove'`: Remove rows with invalid values
  - `'nan'`: Replace invalid values with NaN
  - Default: `'flag'`

**Returns:**
- `tuple`: (validated_df, invalid_mask)
  - `validated_df`: Processed dataframe
  - `invalid_mask`: Boolean series indicating invalid rows

**Example:**
```python
# Flag invalid responses
df_valid, invalid = tv.tidy.check_response_range(
    df, 'rating',
    min_val=1, max_val=5,
    handle_invalid='flag'
)
print(f"Invalid responses: {invalid.sum()}")
print(f"Invalid rows: {df_valid[invalid]}")

# Remove invalid responses
df_clean, _ = tv.tidy.check_response_range(
    df, 'rating',
    min_val=1, max_val=5,
    handle_invalid='remove'
)

# Replace with NaN
df_nan, _ = tv.tidy.check_response_range(
    df, 'rating',
    min_val=1, max_val=5,
    handle_invalid='nan'
)
```

---

#### `detect_missing_patterns()`

Analyze missing data patterns across the dataset.

**Signature:**
```python
detect_missing_patterns(
    df: pd.DataFrame,
    columns: list = None
) -> dict
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `columns` (list, optional): Specific columns to analyze. Default: all columns

**Returns:**
- `dict`: Dictionary containing:
  - `complete_rows` (int): Number of rows with no missing values
  - `rows_with_missing` (int): Number of rows with any missing values
  - `missing_rates` (dict): Missing rate per column (0.0 to 1.0)

**Example:**
```python
info = tv.tidy.detect_missing_patterns(df)

print(f"Complete responses: {info['complete_rows']}/{len(df)}")
print(f"Responses with missing: {info['rows_with_missing']}")
print(f"Missing rates by column:")
for col, rate in info['missing_rates'].items():
    print(f"  {col}: {rate:.1%}")

# Analyze specific columns
info = tv.tidy.detect_missing_patterns(
    df,
    columns=['Q1', 'Q2', 'Q3']
)
```

---

### Quality Check Functions

#### `flag_straight_liners()`

Detect respondents who select identical answers across questions.

**Signature:**
```python
flag_straight_liners(
    df: pd.DataFrame,
    columns: list,
    threshold: int = 0
) -> pd.Series
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `columns` (list): List of column names to check
- `threshold` (int, optional): Maximum unique values to flag as straight-lining. Default: `0` (only identical responses)

**Returns:**
- Series: Boolean series indicating straight-lining rows (True = straight-liner)

**Example:**
```python
# Flag respondents with identical answers
flags = tv.tidy.flag_straight_liners(
    df,
    columns=['Q1', 'Q2', 'Q3', 'Q4']
)
print(f"Straight-liners: {flags.sum()}")

# Review flagged responses
print(df[flags][['Q1', 'Q2', 'Q3', 'Q4']])

# Flag if 1 or fewer unique values
flags = tv.tidy.flag_straight_liners(
    df,
    columns=['Q1', 'Q2', 'Q3', 'Q4'],
    threshold=1
)
```

---

#### `detect_speeders()`

Identify respondents with unusually fast completion times.

**Signature:**
```python
detect_speeders(
    df: pd.DataFrame,
    column: str,
    threshold: float = None,
    method: str = 'iqr'
) -> pd.Series
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name containing completion times
- `threshold` (float, optional): Manual threshold (in same units as data). If provided, `method` is ignored.
- `method` (str, optional): Automatic threshold method (when `threshold` is None):
  - `'iqr'`: Uses Q1 - 1.5*IQR as cutoff
  - `'median'`: Uses 50% of median as cutoff
  - `'percentile'`: Uses 5th percentile as cutoff
  - Default: `'iqr'`

**Returns:**
- Series: Boolean series indicating speeders (True = speeder)

**Example:**
```python
# Auto-detect using IQR method
speeders = tv.tidy.detect_speeders(df, 'completion_time', method='iqr')
print(f"Speeders: {speeders.sum()}")

# Use manual threshold (e.g., < 60 seconds)
speeders = tv.tidy.detect_speeders(df, 'completion_time', threshold=60)

# Use median method
speeders = tv.tidy.detect_speeders(df, 'completion_time', method='median')

# Review speeder times
print(df[speeders]['completion_time'].describe())
```

---

#### `check_logical_consistency()`

Validate custom logical rules across rows.

**Signature:**
```python
check_logical_consistency(
    df: pd.DataFrame,
    rules: list
) -> pd.DataFrame
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `rules` (list): List of rule dictionaries, each containing:
  - `name` (str): Rule identifier (used for column name)
  - `condition` (callable): Function that takes a row and returns boolean (True = consistent)

**Returns:**
- DataFrame: Dataframe with `consistent_{name}` columns added for each rule

**Example:**
```python
# Define validation rules
rules = [
    {
        'name': 'age_experience',
        'condition': lambda row: row['age'] >= row['years_exp'] + 18
    },
    {
        'name': 'score_range',
        'condition': lambda row: row['min_score'] <= row['max_score']
    },
    {
        'name': 'budget_realistic',
        'condition': lambda row: row['budget'] >= row['min_budget']
    }
]

# Check consistency
df_checked = tv.tidy.check_logical_consistency(df, rules)

# Columns added:
# - consistent_age_experience
# - consistent_score_range
# - consistent_budget_realistic

# Filter to only consistent rows
all_consistent = (
    df_checked['consistent_age_experience'] &
    df_checked['consistent_score_range'] &
    df_checked['consistent_budget_realistic']
)
df_valid = df_checked[all_consistent]

# Review inconsistencies
print(df_checked[~df_checked['consistent_age_experience']])
```

---

## Visualization API

### Plotting Functions

#### `plot_single_choice()`

Create bar chart for single-choice survey questions.

**Signature:**
```python
plot_single_choice(
    df: pd.DataFrame,
    column: str,
    title: str = None,
    show_percentages: bool = True,
    sort_by: str = 'count',
    top_n: int = None,
    figsize: tuple = (10, 6),
    color_palette: str = 'default'
) -> plt.Figure
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name to plot
- `title` (str, optional): Plot title. If None, uses column name
- `show_percentages` (bool, optional): Show percentage labels on bars. Default: `True`
- `sort_by` (str, optional): Sort bars by `'count'`, `'alphabetical'`, or `'none'`. Default: `'count'`
- `top_n` (int, optional): Show only top N categories
- `figsize` (tuple, optional): Figure size (width, height). Default: `(10, 6)`
- `color_palette` (str, optional): Color palette name. Default: `'default'`

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
import matplotlib.pyplot as plt

# Basic plot
fig = tv.viz.plot_single_choice(df, 'satisfaction')
plt.show()

# With customization
fig = tv.viz.plot_single_choice(
    df, 'satisfaction',
    title='Customer Satisfaction Ratings',
    show_percentages=True,
    sort_by='count'
)
plt.savefig('satisfaction.png', dpi=300, bbox_inches='tight')
plt.close()

# Top 10 categories
fig = tv.viz.plot_single_choice(
    df, 'product',
    title='Top 10 Products',
    top_n=10,
    sort_by='count'
)
plt.show()
```

---

#### `plot_multiple_choice()`

Create bar chart for multiple-choice survey questions.

**Signature:**
```python
plot_multiple_choice(
    df: pd.DataFrame,
    columns: list,
    title: str = None,
    show_percentages: bool = True,
    sort_by: str = 'count',
    top_n: int = None,
    figsize: tuple = (10, 6),
    color_palette: str = 'default'
) -> plt.Figure
```

**Parameters:**
- `df` (DataFrame): Input dataframe with binary indicator columns
- `columns` (list): List of binary column names to plot
- `title` (str, optional): Plot title
- `show_percentages` (bool, optional): Show percentage labels. Default: `True`
- `sort_by` (str, optional): Sort bars by `'count'`, `'alphabetical'`, or `'none'`. Default: `'count'`
- `top_n` (int, optional): Show only top N options
- `figsize` (tuple, optional): Figure size. Default: `(10, 6)`
- `color_palette` (str, optional): Color palette name. Default: `'default'`

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
# First expand multiple choice data
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')
color_cols = [c for c in df_exp.columns if c.startswith('colors_')]

# Plot
fig = tv.viz.plot_multiple_choice(
    df_exp, color_cols,
    title='Favorite Colors',
    show_percentages=True
)
plt.show()

# Top 5 most selected
fig = tv.viz.plot_multiple_choice(
    df_exp, color_cols,
    title='Top 5 Colors',
    top_n=5,
    sort_by='count'
)
plt.savefig('top_colors.png', dpi=300)
plt.close()
```

---

#### `plot_top_n()`

Plot the top N most frequent responses (convenience wrapper for `plot_single_choice`).

**Signature:**
```python
plot_top_n(
    df: pd.DataFrame,
    column: str,
    n: int = 10,
    title: str = None,
    show_percentages: bool = True,
    figsize: tuple = (10, 6),
    color_palette: str = 'default'
) -> plt.Figure
```

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name to visualize
- `n` (int, optional): Number of top categories to show. Default: `10`
- `title` (str, optional): Chart title
- `show_percentages` (bool, optional): Whether to show percentage labels. Default: `True`
- `figsize` (tuple, optional): Figure size. Default: `(10, 6)`
- `color_palette` (str, optional): Color palette name. Default: `'default'`

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
# Top 10 products
fig = tv.viz.plot_top_n(df, 'product', n=10)
plt.show()

# Top 5 with custom title
fig = tv.viz.plot_top_n(
    df, 'city',
    n=5,
    title='Top 5 Cities by Respondents'
)
plt.savefig('top_cities.png', dpi=300)
plt.close()
```

---

#### `plot_grouped_bars()`

Create grouped bar chart for comparing responses across groups.

**Signature:**
```python
plot_grouped_bars(
    df: pd.DataFrame,
    category_column: str,
    value_column: str,
    group_column: str,
    title: str = None,
    figsize: tuple = (12, 6),
    color_palette: str = 'default'
) -> plt.Figure
```

**Parameters:**
- `df` (DataFrame): Input dataframe (should be in long format)
- `category_column` (str): Column with categories to plot on x-axis
- `value_column` (str): Column with values (usually counts or percentages)
- `group_column` (str): Column to group by (e.g., demographic)
- `title` (str, optional): Chart title
- `figsize` (tuple, optional): Figure size. Default: `(12, 6)`
- `color_palette` (str, optional): Color palette name. Default: `'default'`

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
# Compare satisfaction across age groups
# Data should be structured like:
# response | count | age_group
# Yes      | 10    | 18-25
# No       | 5     | 18-25
# Yes      | 8     | 26-35
# No       | 12    | 26-35

fig = tv.viz.plot_grouped_bars(
    df_summary,
    category_column='response',
    value_column='count',
    group_column='age_group',
    title='Responses by Age Group'
)
plt.show()
```

---

### Styling Functions

#### `set_survey_style()`

Apply survey-appropriate styling to all plots.

**Signature:**
```python
set_survey_style(
    style: str = 'default',
    palette: str = 'default'
) -> None
```

**Parameters:**
- `style` (str, optional): Style preset:
  - `'default'`: Standard survey style with gridlines
  - `'minimal'`: Clean, minimal design
  - `'presentation'`: High-contrast for presentations with larger fonts
  - Default: `'default'`
- `palette` (str, optional): Color palette:
  - `'default'`: Balanced categorical colors
  - `'categorical'`: Distinct colors for categories
  - `'sequential'`: Sequential color scale
  - `'likert'`: Diverging scale for Likert-type questions
  - `'nps'`: NPS colors (Detractor, Passive, Promoter)
  - Any matplotlib colormap name (e.g., `'Set2'`, `'viridis'`)
  - Default: `'default'`

**Returns:**
- None (applies styling globally to matplotlib)

**Example:**
```python
# Default style
tv.viz.set_survey_style()

# Minimal style with categorical colors
tv.viz.set_survey_style(style='minimal', palette='categorical')

# Presentation style with custom colormap
tv.viz.set_survey_style(style='presentation', palette='Set2')

# For Likert scale questions
tv.viz.set_survey_style(palette='likert')

# All subsequent plots will use this style
tv.viz.plot_single_choice(df, 'satisfaction')
```

---

#### `get_palette()`

Get color palette as list of colors.

**Signature:**
```python
get_palette(
    palette_name: str = 'default',
    n_colors: int = None
) -> list
```

**Parameters:**
- `palette_name` (str, optional): Palette name. Default: `'default'`
- `n_colors` (int, optional): Number of colors to return. If None, returns all colors in palette. If more than palette size, repeats colors.

**Returns:**
- list: List of hex color codes

**Example:**
```python
# Get 5 categorical colors
colors = tv.viz.get_palette('categorical', n_colors=5)

# Use in custom matplotlib plot
import matplotlib.pyplot as plt
plt.bar(x, y, color=colors)

# Get all colors in palette
all_colors = tv.viz.get_palette('sequential')
print(f"Palette has {len(all_colors)} colors")
```

---

#### `format_percentage_axis()`

Format axis to display percentages.

**Signature:**
```python
format_percentage_axis(
    ax: plt.Axes,
    axis: str = 'y'
) -> None
```

**Parameters:**
- `ax` (Axes): The matplotlib axes object to format
- `axis` (str, optional): Which axis to format (`'x'` or `'y'`). Default: `'y'`

**Returns:**
- None (modifies axes in-place)

**Example:**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C'], [0.25, 0.50, 0.75])

# Format y-axis to show percentages
tv.viz.format_percentage_axis(ax, axis='y')
plt.show()
```

---

## Workflows & Patterns

### Complete Data Cleaning Pipeline

```python
import pandas as pd
import tidyviz as tv

def clean_survey_data(input_path, output_path):
    """Complete data cleaning pipeline."""

    # 1. Load data
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} responses")

    # 2. Detect missing patterns
    missing_info = tv.tidy.detect_missing_patterns(df)
    print(f"Complete responses: {missing_info['complete_rows']}")
    print(f"Missing rates: {missing_info['missing_rates']}")

    # 3. Validate ranges
    df, invalid = tv.tidy.check_response_range(
        df, 'satisfaction',
        min_val=1, max_val=5,
        handle_invalid='flag'
    )
    print(f"Invalid satisfaction scores: {invalid.sum()}")

    # 4. Quality checks
    straight = tv.tidy.flag_straight_liners(
        df, ['Q1', 'Q2', 'Q3', 'Q4']
    )
    print(f"Straight-liners: {straight.sum()}")

    speeders = tv.tidy.detect_speeders(
        df, 'completion_time',
        method='iqr'
    )
    print(f"Speeders: {speeders.sum()}")

    # 5. Remove flagged respondents
    quality_mask = ~invalid & ~straight & ~speeders
    df_clean = df[quality_mask]
    print(f"Cleaned data: {len(df_clean)} responses")

    # 6. Expand multiple choice
    df_clean = tv.tidy.expand_multiple_choice(df_clean, 'features')

    # 7. Save
    df_clean.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

    return df_clean
```

---

### Complete Visualization Pipeline

```python
import matplotlib.pyplot as plt
import tidyviz as tv

def create_survey_dashboard(df, output_dir):
    """Create comprehensive survey visualizations."""

    # Set global style
    tv.viz.set_survey_style(style='presentation', palette='categorical')

    # Single choice plots
    for question in ['satisfaction', 'likelihood', 'ease_of_use']:
        fig = tv.viz.plot_single_choice(
            df, question,
            title=question.replace('_', ' ').title(),
            show_percentages=True,
            sort_by='count'
        )
        plt.savefig(
            f'{output_dir}/{question}.png',
            dpi=300,
            bbox_inches='tight'
        )
        plt.close()

    # Multiple choice plot
    df_exp = tv.tidy.expand_multiple_choice(df, 'features')
    feature_cols = [c for c in df_exp.columns if c.startswith('features_')]

    fig = tv.viz.plot_multiple_choice(
        df_exp, feature_cols,
        title='Desired Features',
        show_percentages=True,
        top_n=10
    )
    plt.savefig(f'{output_dir}/features.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Multi-panel dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    plt.sca(axes[0, 0])
    tv.viz.plot_single_choice(df, 'satisfaction', title='Satisfaction')

    plt.sca(axes[0, 1])
    tv.viz.plot_single_choice(df, 'likelihood', title='Likelihood to Recommend')

    plt.sca(axes[1, 0])
    tv.viz.plot_single_choice(df, 'ease_of_use', title='Ease of Use')

    plt.sca(axes[1, 1])
    tv.viz.plot_single_choice(df, 'value', title='Value for Money')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Visualizations saved to {output_dir}")
```

---

### Comparison Across Groups

```python
def compare_by_demographic(df, question, demographic):
    """Compare question responses across demographic groups."""

    tv.viz.set_survey_style(palette='categorical')

    # Get unique groups
    groups = df[demographic].unique()
    n_groups = len(groups)

    # Create subplots
    fig, axes = plt.subplots(1, n_groups, figsize=(5*n_groups, 5))

    # Ensure axes is iterable
    if n_groups == 1:
        axes = [axes]

    # Plot each group
    for ax, group in zip(axes, groups):
        plt.sca(ax)
        group_data = df[df[demographic] == group]

        tv.viz.plot_single_choice(
            group_data, question,
            title=f'{group}\n(n={len(group_data)})',
            show_percentages=True
        )

    fig.suptitle(f'{question} by {demographic}', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f'{question}_by_{demographic}.png', dpi=300, bbox_inches='tight')
    plt.close()
```

---

### Report Generation

```python
def generate_quality_report(df, output_path):
    """Generate data quality report."""

    # Missing data analysis
    missing = tv.tidy.detect_missing_patterns(df)

    # Quality flags
    speeders = tv.tidy.detect_speeders(df, 'completion_time', method='iqr')
    straight = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3', 'Q4'])

    # Response validation
    _, invalid = tv.tidy.check_response_range(
        df, 'rating',
        min_val=1, max_val=5,
        handle_invalid='flag'
    )

    # Compile report
    report = {
        'total_responses': len(df),
        'complete_responses': missing['complete_rows'],
        'completeness_rate': missing['complete_rows'] / len(df),
        'speeders': speeders.sum(),
        'speeder_rate': speeders.sum() / len(df),
        'straight_liners': straight.sum(),
        'straight_liner_rate': straight.sum() / len(df),
        'invalid_ratings': invalid.sum(),
        'invalid_rate': invalid.sum() / len(df),
        'high_quality_responses': (len(df) - speeders.sum() - straight.sum() - invalid.sum()),
        'quality_rate': (len(df) - speeders.sum() - straight.sum() - invalid.sum()) / len(df)
    }

    # Save report
    report_df = pd.Series(report).to_frame('value')
    report_df.to_csv(output_path)

    print("Quality Report:")
    print(f"  Total responses: {report['total_responses']}")
    print(f"  High quality: {report['high_quality_responses']} ({report['quality_rate']:.1%})")
    print(f"  Speeders: {report['speeders']} ({report['speeder_rate']:.1%})")
    print(f"  Straight-liners: {report['straight_liners']} ({report['straight_liner_rate']:.1%})")

    return report
```

---

### End-to-End Pipeline

```python
def process_survey_end_to_end(input_path, output_dir):
    """Complete survey processing from raw data to visualizations."""

    import os
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load data
    print("Loading data...")
    df = pd.read_csv(input_path)

    # 2. Generate quality report
    print("Generating quality report...")
    report = generate_quality_report(df, f'{output_dir}/quality_report.csv')

    # 3. Clean data
    print("Cleaning data...")
    df_clean = clean_survey_data(input_path, f'{output_dir}/survey_clean.csv')

    # 4. Create visualizations
    print("Creating visualizations...")
    create_survey_dashboard(df_clean, output_dir)

    print(f"\nProcessing complete! Output saved to {output_dir}")
    return df_clean, report

# Use it
df_final, report = process_survey_end_to_end(
    'raw_survey.csv',
    'output/'
)
```

---

## Troubleshooting

### Issue: Multiple Choice Expansion Fails

**Problem:** `expand_multiple_choice()` produces unexpected results or errors.

**Solutions:**

```python
# Check separator - your data might use semicolons or pipes
df_exp = tv.tidy.expand_multiple_choice(df, 'colors', sep=';')

# Check for whitespace around values
df['colors'] = df['colors'].str.strip()
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')

# Verify column exists
print("Available columns:", df.columns.tolist())

# Check data format
print(df['colors'].head())
print(df['colors'].value_counts())
```

---

### Issue: Validation Removes Too Many Rows

**Problem:** `check_response_range()` flags or removes valid data.

**Solutions:**

```python
# Inspect actual data range
print(df['rating'].describe())
print(df['rating'].value_counts())

# Use 'flag' to review before removing
df, invalid = tv.tidy.check_response_range(
    df, 'rating', 1, 5,
    handle_invalid='flag'
)

# Review flagged data
print("Flagged values:")
print(df[invalid]['rating'].value_counts())

# Check for data type issues
print(df['rating'].dtype)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
```

---

### Issue: Plots Don't Show

**Problem:** Visualizations don't display in your environment.

**Solutions:**

```python
# For interactive environments (Python scripts)
tv.viz.plot_single_choice(df, 'method')
plt.show()  # Add this

# For saving to files
tv.viz.plot_single_choice(df, 'method')
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.close()

# In Jupyter notebooks
%matplotlib inline
tv.viz.plot_single_choice(df, 'method')

# Check if figure was created
fig = tv.viz.plot_single_choice(df, 'method')
print(f"Figure created: {fig is not None}")
```

---

### Issue: Colors Look Wrong

**Problem:** Color palette doesn't match expectations.

**Solutions:**

```python
# Reset to default style
tv.viz.set_survey_style()

# Try different palettes
tv.viz.set_survey_style(palette='categorical')  # Distinct colors
tv.viz.set_survey_style(palette='sequential')   # Sequential scale

# Use matplotlib colormap
tv.viz.set_survey_style(palette='Set2')
tv.viz.set_survey_style(palette='viridis')

# List available colormaps
import matplotlib.pyplot as plt
print(sorted(plt.colormaps()))
```

---

### Issue: Memory Problems with Large Datasets

**Problem:** Running out of memory with large survey datasets.

**Solutions:**

```python
# Process in chunks
chunks = pd.read_csv('large_survey.csv', chunksize=10000)

results = []
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i}...")
    cleaned = tv.tidy.check_response_range(chunk, 'rating', 1, 5)[0]
    results.append(cleaned)

df_final = pd.concat(results, ignore_index=True)

# Use categorical dtypes
df['category_col'] = df['category_col'].astype('category')

# Drop intermediate columns
df_exp = tv.tidy.expand_multiple_choice(df, 'colors', keep_original=False)

# Process and save plots individually
for col in ['Q1', 'Q2', 'Q3']:
    tv.viz.plot_single_choice(df, col)
    plt.savefig(f'{col}.png', dpi=300)
    plt.close()  # Free memory immediately
```

---

### Issue: Logical Consistency Rules Failing

**Problem:** `check_logical_consistency()` produces unexpected results.

**Solutions:**

```python
# Test rules individually
def test_rule(df, condition, name):
    try:
        result = df.apply(condition, axis=1)
        print(f"{name}: {result.sum()} valid, {(~result).sum()} invalid")
        return result
    except Exception as e:
        print(f"{name} failed: {e}")
        return None

# Test each condition
test_rule(df, lambda r: r['age'] >= 18, 'age_valid')
test_rule(df, lambda r: r['years_exp'] < r['age'], 'experience_valid')

# Handle missing values in conditions
rules = [
    {
        'name': 'age_valid',
        'condition': lambda r: pd.notna(r['age']) and r['age'] >= 18
    }
]

# Review which rows fail
df_checked = tv.tidy.check_logical_consistency(df, rules)
failed = df_checked[~df_checked['consistent_age_valid']]
print(failed[['age', 'years_exp']])
```

---

## Performance Tips

### Large Datasets

```python
# Use dtype specifications when reading
dtypes = {
    'id': 'int32',
    'age': 'int8',
    'satisfaction': 'int8'
}
df = pd.read_csv('survey.csv', dtype=dtypes)

# Sample for exploration
df_sample = df.sample(n=1000, random_state=42)

# Process in parallel (for advanced users)
from multiprocessing import Pool

def process_chunk(chunk):
    return tv.tidy.check_response_range(chunk, 'rating', 1, 5)[0]

with Pool(4) as pool:
    results = pool.map(process_chunk, chunks)
```

---

### Visualization Optimization

```python
# Reduce DPI for faster preview
tv.viz.plot_single_choice(df, 'method')
plt.savefig('preview.png', dpi=100)  # Fast
plt.close()

# High DPI for final output
tv.viz.plot_single_choice(df, 'method')
plt.savefig('final.png', dpi=300)  # High quality
plt.close()

# Batch save plots
def save_all_plots(df, questions, output_dir):
    tv.viz.set_survey_style()  # Set once

    for q in questions:
        tv.viz.plot_single_choice(df, q, title=q)
        plt.savefig(f'{output_dir}/{q}.png', dpi=300)
        plt.close()
```

---

## Additional Resources

- **GitHub Repository:** [github.com/pingfan-hu/tidyviz](https://github.com/pingfan-hu/tidyviz)
- **Quick Start Guide:** See [QUICK_START.md](QUICK_START.md) for rapid introduction
- **Examples:** Check the `examples/` directory for complete working code
- **Issues:** Report bugs or request features on GitHub Issues

---

## License

TidyViz is released under the MIT License. See [LICENSE](../LICENSE) for details.

---

## Citation

```bibtex
@software{tidyviz2025,
  title = {TidyViz: Survey Data Analysis for Python},
  author = {Hu, Pingfan},
  year = {2025},
  url = {https://github.com/pingfan-hu/tidyviz}
}
```
