# Quick Start Guide

Get started with TidyViz in minutes.

## Installation

```bash
pip install tidyviz
```

## Basic Setup

```python
import pandas as pd
import matplotlib.pyplot as plt
import tidyviz as tv
```

## Your First Analysis

### 1. Load Survey Data

```python
# Load your survey data
df = pd.read_csv('survey.csv')

# Quick look at the data
print(df.head())
print(df.columns.tolist())
```

### 2. Clean the Data

```python
# Check for missing data
missing_info = tv.tidy.detect_missing_patterns(df)
print(f"Complete responses: {missing_info['complete_rows']}/{len(df)}")

# Validate rating scales (e.g., 1-5 scale)
df_clean, invalid = tv.tidy.check_response_range(
    df, 'satisfaction',
    min_val=1, max_val=5,
    handle_invalid='flag'
)

# Filter out invalid responses
df_clean = df_clean[~invalid]
```

### 3. Visualize Results

```python
# Set visualization style
tv.viz.set_survey_style(palette='categorical')

# Plot single choice question
tv.viz.plot_single_choice(
    df_clean, 'satisfaction',
    title='Customer Satisfaction',
    show_percentages=True
)
plt.savefig('satisfaction.png', dpi=300)
plt.show()
```

## Common Tasks

### Handle Multiple Choice Questions

```python
# Your data has: "Red,Blue,Green" format
df_expanded = tv.tidy.expand_multiple_choice(df, 'colors')

# Now you have: colors_Red, colors_Blue, colors_Green columns
color_cols = [c for c in df_expanded.columns if c.startswith('colors_')]

# Plot the results
tv.viz.plot_multiple_choice(
    df_expanded, color_cols,
    title='Favorite Colors',
    show_percentages=True
)
plt.savefig('colors.png', dpi=300)
plt.show()
```

### Detect Data Quality Issues

```python
# Find speeders (too fast completion)
speeders = tv.tidy.detect_speeders(
    df, 'completion_time',
    method='iqr'  # Uses statistical method
)
print(f"Speeders detected: {speeders.sum()}")

# Find straight-liners (same answer for all questions)
straight = tv.tidy.flag_straight_liners(
    df, ['Q1', 'Q2', 'Q3', 'Q4']
)
print(f"Straight-liners: {straight.sum()}")

# Remove low-quality responses
df_quality = df[~speeders & ~straight]
```

### Create Multiple Plots

```python
# Set style once
tv.viz.set_survey_style(palette='categorical')

# Create dashboard with multiple plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

plt.sca(axes[0, 0])
tv.viz.plot_single_choice(df, 'satisfaction')

plt.sca(axes[0, 1])
tv.viz.plot_single_choice(df, 'likelihood')

plt.sca(axes[1, 0])
tv.viz.plot_single_choice(df, 'ease_of_use')

plt.sca(axes[1, 1])
tv.viz.plot_single_choice(df, 'value')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=300)
plt.show()
```

## Complete Example Workflow

```python
import pandas as pd
import matplotlib.pyplot as plt
import tidyviz as tv

# 1. Load data
df = pd.read_csv('survey_data.csv')

# 2. Clean and validate
df, invalid = tv.tidy.check_response_range(df, 'rating', 1, 5)
speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')
df_clean = df[~invalid & ~speeders]

# 3. Transform multiple choice
df_clean = tv.tidy.expand_multiple_choice(df_clean, 'features')

# 4. Visualize
tv.viz.set_survey_style(palette='categorical')

tv.viz.plot_single_choice(
    df_clean, 'rating',
    title='Overall Rating'
)
plt.savefig('rating.png', dpi=300)
plt.close()

# 5. Save cleaned data
df_clean.to_csv('survey_clean.csv', index=False)

print("Analysis complete!")
```

## Quick Reference

### Data Cleaning

```python
# Expand multiple choice
df_exp = tv.tidy.expand_multiple_choice(df, 'column', sep=',')

# Collapse back
df_col = tv.tidy.collapse_multiple_choice(df_exp, 'prefix')

# Validate range
df, invalid = tv.tidy.check_response_range(df, 'col', 1, 5)

# Detect issues
speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')
straight = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3'])
```

### Visualization

```python
# Set style (do this once)
tv.viz.set_survey_style(palette='categorical')

# Single choice plot
tv.viz.plot_single_choice(df, 'column', title='Title')

# Multiple choice plot
tv.viz.plot_multiple_choice(df, ['col1', 'col2'], title='Title')

# Save
plt.savefig('plot.png', dpi=300)
plt.show()
```

## Next Steps

- **Read the [User Manual](USER_MANUAL.md)** for comprehensive documentation
- **Check the examples folder** for more complete workflows
- **Visit the [GitHub repository](https://github.com/pingfan-hu/tidyviz)** for support

## Tips

- Always call `tv.viz.set_survey_style()` before creating plots
- Use `handle_invalid='flag'` to review data before removing it
- Close plots with `plt.close()` after saving to free memory
- Save high-quality images with `dpi=300`
- Keep original data files unchanged, save cleaned versions separately
