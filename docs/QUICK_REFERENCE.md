# Quick Reference

Concise reference for all TidyViz functions.

## Import

```python
import tidyviz as tv
import pandas as pd
```

---

## Data Cleaning

### Multiple Choice

```python
# Expand comma-separated to binary columns
df_exp = tv.tidy.expand_multiple_choice(df, 'colors', sep=',')

# Collapse binary columns to comma-separated
df_col = tv.tidy.collapse_multiple_choice(df_exp, 'colors', sep=',')
```

### Validation

```python
# Check response range
df, invalid = tv.tidy.check_response_range(
    df, 'rating', min_val=1, max_val=5,
    handle_invalid='flag'  # or 'remove', 'nan'
)

# Detect missing patterns
info = tv.tidy.detect_missing_patterns(df)
# Returns: {'complete_rows', 'rows_with_missing', 'missing_rates'}
```

### Quality Checks

```python
# Flag straight-liners
flags = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3'], threshold=0)

# Detect speeders
flags = tv.tidy.detect_speeders(
    df, 'time',
    method='iqr'  # or 'median', 'percentile'
)

# Check logical consistency
rules = [{'name': 'rule1', 'condition': lambda r: r['A'] < r['B']}]
df = tv.tidy.check_logical_consistency(df, rules)
```

---

## Visualization

### Setup

```python
import matplotlib.pyplot as plt

# Set style globally
tv.viz.set_survey_style(
    style='default',  # or 'minimal', 'presentation'
    palette='categorical'  # or 'sequential', 'Set2', etc.
)
```

### Plotting

```python
# Single choice bar chart
tv.viz.plot_single_choice(
    df, 'column',
    title='Title',
    show_percentages=True,
    sort_by='count'  # or 'name'
)

# Multiple choice bar chart
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')
cols = [c for c in df_exp.columns if c.startswith('colors_')]
tv.viz.plot_multiple_choice(
    df_exp, cols,
    title='Title',
    show_percentages=True
)

# Show or save
plt.show()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Styling

```python
# Get color palette
colors = tv.viz.get_palette('categorical', n_colors=5)
```

---

## Common Workflows

### Complete Cleaning Pipeline

```python
# Load
df = pd.read_csv('survey.csv')

# Validate
df, invalid = tv.tidy.check_response_range(df, 'rating', 1, 5)

# Quality checks
speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')
straight = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3'])

# Filter
df_clean = df[~invalid & ~speeders & ~straight]

# Transform
df_clean = tv.tidy.expand_multiple_choice(df_clean, 'colors')

# Save
df_clean.to_csv('survey_clean.csv', index=False)
```

### Complete Visualization Pipeline

```python
# Setup
tv.viz.set_survey_style(palette='categorical')

# Plot single choice
tv.viz.plot_single_choice(df, 'satisfaction', title='Satisfaction')
plt.savefig('satisfaction.png', dpi=300)
plt.close()

# Plot multiple choice
df_exp = tv.tidy.expand_multiple_choice(df, 'features')
cols = [c for c in df_exp.columns if c.startswith('features_')]
tv.viz.plot_multiple_choice(df_exp, cols, title='Features')
plt.savefig('features.png', dpi=300)
plt.close()
```

### Multi-Panel Figure

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

plt.sca(axes[0, 0])
tv.viz.plot_single_choice(df, 'Q1')

plt.sca(axes[0, 1])
tv.viz.plot_single_choice(df, 'Q2')

plt.sca(axes[1, 0])
tv.viz.plot_single_choice(df, 'Q3')

plt.sca(axes[1, 1])
tv.viz.plot_single_choice(df, 'Q4')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=300)
```

---

## Function Parameters Quick Lookup

### `expand_multiple_choice()`
- `df` - DataFrame
- `column` - Column name (str)
- `sep` - Separator (str, default: ',')
- `keep_original` - Keep original column (bool, default: False)
- `prefix` - Prefix for new columns (str, optional)

### `collapse_multiple_choice()`
- `df` - DataFrame
- `prefix` - Column prefix (str)
- `sep` - Separator (str, default: ',')
- `drop_binary` - Drop binary columns (bool, default: True)

### `check_response_range()`
- `df` - DataFrame
- `column` - Column name (str)
- `min_val` - Minimum valid value (float)
- `max_val` - Maximum valid value (float)
- `handle_invalid` - Strategy (str: 'flag', 'remove', 'nan')

### `flag_straight_liners()`
- `df` - DataFrame
- `columns` - Columns to check (list)
- `threshold` - Max unique values to flag (int, default: 0)

### `detect_speeders()`
- `df` - DataFrame
- `column` - Time column (str)
- `threshold` - Manual threshold (float, optional)
- `method` - Auto method (str: 'iqr', 'median', 'percentile')

### `plot_single_choice()`
- `df` - DataFrame
- `column` - Column name (str)
- `title` - Plot title (str, optional)
- `show_percentages` - Show percentage labels (bool, default: True)
- `sort_by` - Sort by 'count' or 'name' (str, default: 'count')
- `color_palette` - Palette name (str, optional)

### `plot_multiple_choice()`
- `df` - DataFrame
- `columns` - Binary column names (list)
- `title` - Plot title (str, optional)
- `show_percentages` - Show percentage labels (bool, default: True)
- `sort_by` - Sort by 'count' or 'name' (str, default: 'count')

### `set_survey_style()`
- `style` - Style preset (str: 'default', 'minimal', 'presentation')
- `palette` - Color palette (str: 'categorical', 'sequential', or colormap)

---

## Tips

**Data Cleaning:**
- Always check missing patterns before cleaning
- Use 'flag' for validation to review before removing
- Combine quality flags with `&` and `|` operators
- Keep original data untouched, save cleaned versions separately

**Visualization:**
- Call `set_survey_style()` once at the start
- Always close plots with `plt.close()` after saving
- Use `sort_by='count'` for most common responses
- Save with `dpi=300` for publication quality

**Performance:**
- Process large files in chunks with `pd.read_csv(chunksize=...)`
- Use categorical dtype for categorical columns
- Drop intermediate columns with `keep_original=False`
- Close figures after saving to free memory

---

## Error Handling

```python
# Check column exists
if 'column' not in df.columns:
    raise ValueError(f"Column 'column' not found")

# Handle missing values
df = df.dropna(subset=['column'])

# Validate data types
if not pd.api.types.is_numeric_dtype(df['column']):
    df['column'] = pd.to_numeric(df['column'], errors='coerce')

# Check for empty dataframe
if len(df) == 0:
    raise ValueError("DataFrame is empty")
```

---

## See Also

- [API.md](API.md) - Complete function reference
- [USER_GUIDE.md](USER_GUIDE.md) - Detailed tutorials
- [README.md](../README.md) - Package overview
- `examples/` - Working code examples
