# API Reference

Complete reference for TidyViz functions and parameters.

## Table of Contents

- [Data Cleaning (`tidyviz.tidy`)](#data-cleaning-tidyviztidy)
  - [Multiple Choice Functions](#multiple-choice-functions)
  - [Validation Functions](#validation-functions)
  - [Quality Check Functions](#quality-check-functions)
- [Visualization (`tidyviz.viz`)](#visualization-tidyvizviz)
  - [Plotting Functions](#plotting-functions)
  - [Styling Functions](#styling-functions)

---

## Data Cleaning (`tidyviz.tidy`)

### Multiple Choice Functions

#### `expand_multiple_choice()`

Convert comma-separated multiple choice responses into binary indicator columns.

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
df = pd.DataFrame({'colors': ['Red,Blue', 'Green', 'Blue,Green']})
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')
# Creates: colors_Red, colors_Blue, colors_Green
```

#### `collapse_multiple_choice()`

Convert binary indicator columns back to comma-separated values.

**Parameters:**
- `df` (DataFrame): Input dataframe with binary columns
- `prefix` (str): Common prefix of binary columns to collapse
- `sep` (str, optional): Separator for output. Default: `','`
- `drop_binary` (bool, optional): Drop binary columns. Default: `True`

**Returns:**
- DataFrame: Dataframe with collapsed column

**Example:**
```python
df_collapsed = tv.tidy.collapse_multiple_choice(df_exp, 'colors')
# Recreates original 'colors' column
```

---

### Validation Functions

#### `check_response_range()`

Validate that responses fall within expected range.

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name to validate
- `min_val` (float): Minimum valid value
- `max_val` (float): Maximum valid value
- `handle_invalid` (str, optional): How to handle invalid values:
  - `'flag'`: Add validity column, keep invalid values
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
    df, 'rating', min_val=1, max_val=5,
    handle_invalid='flag'
)
print(f"Found {invalid.sum()} invalid responses")
```

#### `detect_missing_patterns()`

Analyze missing data patterns across the dataset.

**Parameters:**
- `df` (DataFrame): Input dataframe

**Returns:**
- `dict`: Dictionary containing:
  - `complete_rows` (int): Number of rows with no missing values
  - `rows_with_missing` (int): Number of rows with any missing values
  - `missing_rates` (dict): Missing rate per column

**Example:**
```python
info = tv.tidy.detect_missing_patterns(df)
print(f"Complete: {info['complete_rows']}/{len(df)}")
print(f"Missing rates: {info['missing_rates']}")
```

---

### Quality Check Functions

#### `flag_straight_liners()`

Detect respondents who select identical answers across questions.

**Parameters:**
- `df` (DataFrame): Input dataframe
- `columns` (list): List of column names to check
- `threshold` (int, optional): Maximum unique values to flag. Default: `0` (flags only identical responses)

**Returns:**
- Series: Boolean series indicating straight-lining rows

**Example:**
```python
# Flag respondents with identical answers
flags = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3', 'Q4'])
print(f"Straight-liners: {flags.sum()}")
```

#### `detect_speeders()`

Identify respondents with unusually fast completion times.

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name containing completion times
- `threshold` (float, optional): Manual threshold (in same units as data)
- `method` (str, optional): Automatic threshold method:
  - `'iqr'`: Interquartile range method
  - `'median'`: Percentage of median
  - `'percentile'`: Percentile cutoff
  - Default: `'iqr'`

**Returns:**
- Series: Boolean series indicating speeders

**Example:**
```python
# Detect speeders using IQR method
speeders = tv.tidy.detect_speeders(df, 'completion_time', method='iqr')
print(f"Speeders: {speeders.sum()}")

# Or use manual threshold
speeders = tv.tidy.detect_speeders(df, 'completion_time', threshold=60)
```

#### `check_logical_consistency()`

Validate custom logical rules across rows.

**Parameters:**
- `df` (DataFrame): Input dataframe
- `rules` (list): List of rule dictionaries, each containing:
  - `name` (str): Rule identifier
  - `condition` (callable): Function that takes a row and returns boolean

**Returns:**
- DataFrame: Dataframe with consistency columns added

**Example:**
```python
rules = [
    {
        'name': 'age_experience',
        'condition': lambda row: row['age'] >= row['years_exp'] + 18
    },
    {
        'name': 'score_range',
        'condition': lambda row: row['min_score'] <= row['max_score']
    }
]
df_checked = tv.tidy.check_logical_consistency(df, rules)
# Adds: consistent_age_experience, consistent_score_range columns
```

---

## Visualization (`tidyviz.viz`)

### Plotting Functions

#### `plot_single_choice()`

Create bar chart for single-choice survey questions.

**Parameters:**
- `df` (DataFrame): Input dataframe
- `column` (str): Column name to plot
- `title` (str, optional): Plot title
- `show_percentages` (bool, optional): Show percentage labels. Default: `True`
- `sort_by` (str, optional): Sort bars by `'count'` or `'name'`. Default: `'count'`
- `color_palette` (str, optional): Color palette name. Default: `None` (uses current style)

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
fig = tv.viz.plot_single_choice(
    df, 'satisfaction',
    title='Satisfaction Ratings',
    show_percentages=True,
    sort_by='count'
)
plt.show()
```

#### `plot_multiple_choice()`

Create bar chart for multiple-choice survey questions.

**Parameters:**
- `df` (DataFrame): Input dataframe with binary indicator columns
- `columns` (list): List of binary column names to plot
- `title` (str, optional): Plot title
- `show_percentages` (bool, optional): Show percentage labels. Default: `True`
- `sort_by` (str, optional): Sort bars by `'count'` or `'name'`. Default: `'count'`

**Returns:**
- Figure: Matplotlib figure object

**Example:**
```python
# First expand multiple choice data
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')
cols = [c for c in df_exp.columns if c.startswith('colors_')]

# Then plot
fig = tv.viz.plot_multiple_choice(
    df_exp, cols,
    title='Favorite Colors',
    show_percentages=True
)
plt.show()
```

---

### Styling Functions

#### `set_survey_style()`

Apply survey-appropriate styling to all plots.

**Parameters:**
- `style` (str, optional): Style preset:
  - `'default'`: Standard survey style
  - `'minimal'`: Clean, minimal design
  - `'presentation'`: High-contrast for presentations
  - Default: `'default'`
- `palette` (str, optional): Color palette:
  - `'categorical'`: Distinct colors for categories
  - `'sequential'`: Sequential color scale
  - Any matplotlib colormap name (e.g., `'Set2'`, `'viridis'`)
  - Default: `'categorical'`

**Returns:**
- None (applies styling globally)

**Example:**
```python
# Set style for all subsequent plots
tv.viz.set_survey_style(style='presentation', palette='Set2')

# Now all plots will use this style
tv.viz.plot_single_choice(df, 'method')
```

#### `get_palette()`

Get color palette as list of colors.

**Parameters:**
- `name` (str): Palette name
- `n_colors` (int, optional): Number of colors to return

**Returns:**
- list: List of color values (hex strings or RGB tuples)

**Example:**
```python
# Get 5 categorical colors
colors = tv.viz.get_palette('categorical', n_colors=5)

# Use in custom plot
plt.bar(x, y, color=colors)
```

---

## Common Workflows

### Complete Data Cleaning Pipeline

```python
import pandas as pd
import tidyviz as tv

# Load data
df = pd.read_csv('survey.csv')

# 1. Detect missing patterns
missing_info = tv.tidy.detect_missing_patterns(df)
print(f"Completeness: {missing_info['complete_rows']/len(df):.1%}")

# 2. Validate ranges
df, invalid = tv.tidy.check_response_range(
    df, 'satisfaction', 1, 5, handle_invalid='flag'
)

# 3. Flag quality issues
straight = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3'])
speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')

# 4. Remove flagged respondents
df_clean = df[~straight & ~speeders & ~invalid]

# 5. Expand multiple choice
df_clean = tv.tidy.expand_multiple_choice(df_clean, 'colors')
```

### Complete Visualization Pipeline

```python
import matplotlib.pyplot as plt
import tidyviz as tv

# Set global style
tv.viz.set_survey_style(palette='categorical')

# Create multiple plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Single choice
plt.sca(axes[0, 0])
tv.viz.plot_single_choice(df, 'satisfaction',
                          title='Satisfaction')

# Plot 2: Multiple choice
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')
cols = [c for c in df_exp.columns if c.startswith('colors_')]
plt.sca(axes[0, 1])
tv.viz.plot_multiple_choice(df_exp, cols, title='Colors')

plt.tight_layout()
plt.savefig('survey_results.png', dpi=300)
```
