# User Guide

Comprehensive guide to using TidyViz for survey data analysis.

## Contents

1. [Installation](#installation)
2. [Core Concepts](#core-concepts)
3. [Data Cleaning Workflows](#data-cleaning-workflows)
4. [Visualization Best Practices](#visualization-best-practices)
5. [Common Patterns](#common-patterns)
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

### Response Validation

TidyViz provides three strategies for handling invalid responses:

1. **Flag** - Keep data, add validity indicator
2. **Remove** - Drop invalid rows
3. **NaN** - Replace invalid values with NaN

Choose based on your analysis needs and reporting requirements.

---

## Data Cleaning Workflows

### Workflow 1: Basic Cleaning

```python
import pandas as pd
import tidyviz as tv

# Load data
df = pd.read_csv('survey.csv')

# Check missing data
info = tv.tidy.detect_missing_patterns(df)
print(f"Complete responses: {info['complete_rows']}")

# Validate rating scales
df, invalid = tv.tidy.check_response_range(
    df, 'satisfaction', 1, 5, handle_invalid='flag'
)

# Save cleaned data
df.to_csv('survey_clean.csv', index=False)
```

### Workflow 2: Quality Filtering

```python
# Detect data quality issues
straight = tv.tidy.flag_straight_liners(
    df, ['Q1', 'Q2', 'Q3', 'Q4'], threshold=0
)

speeders = tv.tidy.detect_speeders(
    df, 'completion_time', method='iqr'
)

# Create quality flags
df['quality_flag'] = straight | speeders

# Filter high-quality responses
df_filtered = df[~df['quality_flag']]

print(f"Kept {len(df_filtered)}/{len(df)} responses")
```

### Workflow 3: Logical Validation

```python
# Define validation rules
rules = [
    {
        'name': 'age_valid',
        'condition': lambda r: 18 <= r['age'] <= 100
    },
    {
        'name': 'experience_valid',
        'condition': lambda r: r['years_exp'] < r['age'] - 15
    },
    {
        'name': 'scores_consistent',
        'condition': lambda r: r['pre_score'] <= r['post_score']
    }
]

# Check consistency
df = tv.tidy.check_logical_consistency(df, rules)

# Filter consistent responses
consistent_mask = (
    df['consistent_age_valid'] &
    df['consistent_experience_valid'] &
    df['consistent_scores_consistent']
)

df_valid = df[consistent_mask]
```

---

## Visualization Best Practices

### Setting Up Visualizations

```python
import matplotlib.pyplot as plt
import tidyviz as tv

# Set style once at the beginning
tv.viz.set_survey_style(palette='categorical')

# Configure matplotlib for your needs
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'
```

### Single Choice Visualization

```python
# Basic plot
tv.viz.plot_single_choice(df, 'satisfaction')

# With customization
tv.viz.plot_single_choice(
    df, 'satisfaction',
    title='Overall Satisfaction',
    show_percentages=True,
    sort_by='count'
)

# Save
plt.savefig('satisfaction.png', dpi=300)
plt.close()
```

### Multiple Choice Visualization

```python
# Prepare data
df_exp = tv.tidy.expand_multiple_choice(df, 'features')
feature_cols = [c for c in df_exp.columns if c.startswith('features_')]

# Plot
tv.viz.plot_multiple_choice(
    df_exp, feature_cols,
    title='Most Desired Features',
    show_percentages=True,
    sort_by='count'
)

plt.savefig('features.png', dpi=300)
plt.close()
```

### Creating Multi-Panel Figures

```python
# Create figure with multiple plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1
plt.sca(axes[0, 0])
tv.viz.plot_single_choice(df, 'satisfaction')

# Plot 2
plt.sca(axes[0, 1])
tv.viz.plot_single_choice(df, 'likelihood')

# Plot 3
plt.sca(axes[1, 0])
tv.viz.plot_single_choice(df, 'ease_of_use')

# Plot 4
plt.sca(axes[1, 1])
tv.viz.plot_single_choice(df, 'value')

plt.tight_layout()
plt.savefig('survey_dashboard.png', dpi=300)
```

### Color Palette Selection

```python
# Categorical data (nominal categories)
tv.viz.set_survey_style(palette='categorical')

# Ordered/sequential data (ratings, scales)
tv.viz.set_survey_style(palette='sequential')

# Custom matplotlib colormap
tv.viz.set_survey_style(palette='Set2')
```

---

## Common Patterns

### Pattern 1: End-to-End Pipeline

```python
import pandas as pd
import matplotlib.pyplot as plt
import tidyviz as tv

def process_survey(input_path, output_dir):
    """Complete survey processing pipeline."""

    # Load
    df = pd.read_csv(input_path)

    # Clean
    df, _ = tv.tidy.check_response_range(df, 'rating', 1, 5)
    speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')
    df = df[~speeders]

    # Transform
    df = tv.tidy.expand_multiple_choice(df, 'features')

    # Visualize
    tv.viz.set_survey_style(palette='categorical')
    tv.viz.plot_single_choice(df, 'rating')
    plt.savefig(f'{output_dir}/rating.png')
    plt.close()

    # Save
    df.to_csv(f'{output_dir}/cleaned.csv', index=False)

    return df
```

### Pattern 2: Comparison Across Groups

```python
# Split by demographic group
groups = df.groupby('age_group')

# Create comparison plot
fig, axes = plt.subplots(1, len(groups), figsize=(15, 4))

for i, (name, group) in enumerate(groups):
    plt.sca(axes[i])
    tv.viz.plot_single_choice(
        group, 'satisfaction',
        title=f'{name}',
        show_percentages=True
    )

plt.tight_layout()
plt.savefig('satisfaction_by_age.png')
```

### Pattern 3: Report Generation

```python
def generate_report(df, output_path):
    """Generate comprehensive survey report."""

    # Data quality summary
    missing = tv.tidy.detect_missing_patterns(df)
    speeders = tv.tidy.detect_speeders(df, 'time', method='iqr')
    straight = tv.tidy.flag_straight_liners(df, ['Q1', 'Q2', 'Q3'])

    # Create report
    report = {
        'total_responses': len(df),
        'complete_responses': missing['complete_rows'],
        'speeders': speeders.sum(),
        'straight_liners': straight.sum(),
        'quality_rate': (len(df) - speeders.sum() - straight.sum()) / len(df)
    }

    # Save report
    pd.Series(report).to_csv(output_path)

    return report
```

---

## Troubleshooting

### Issue: Multiple Choice Expansion Fails

**Problem:** `expand_multiple_choice()` produces unexpected results

**Solutions:**
```python
# Check separator
df_exp = tv.tidy.expand_multiple_choice(df, 'colors', sep=';')  # Not ','

# Check for whitespace
df['colors'] = df['colors'].str.strip()  # Remove leading/trailing
df_exp = tv.tidy.expand_multiple_choice(df, 'colors')

# Check column exists
print(df.columns.tolist())  # Verify column name
```

### Issue: Validation Removes Too Many Rows

**Problem:** `check_response_range()` flags valid data

**Solutions:**
```python
# Check actual data range
print(df['rating'].describe())

# Use flag instead of remove
df, invalid = tv.tidy.check_response_range(
    df, 'rating', 1, 5,
    handle_invalid='flag'  # Keep data, add flag
)

# Review flagged data
print(df[invalid]['rating'].value_counts())
```

### Issue: Plots Don't Show

**Problem:** Visualizations don't display

**Solutions:**
```python
# Add plt.show() for interactive display
tv.viz.plot_single_choice(df, 'method')
plt.show()

# Or save to file
tv.viz.plot_single_choice(df, 'method')
plt.savefig('plot.png')
plt.close()

# In Jupyter notebooks
%matplotlib inline
```

### Issue: Colors Look Wrong

**Problem:** Color palette doesn't match expectations

**Solutions:**
```python
# Reset style
tv.viz.set_survey_style(palette='categorical')

# Use specific colormap
tv.viz.set_survey_style(palette='Set2')

# Check available palettes
import matplotlib.pyplot as plt
print(plt.colormaps())
```

---

## Performance Tips

### Large Datasets

```python
# Process in chunks for very large files
chunks = pd.read_csv('survey.csv', chunksize=10000)

results = []
for chunk in chunks:
    cleaned = tv.tidy.check_response_range(chunk, 'rating', 1, 5)[0]
    results.append(cleaned)

df_final = pd.concat(results, ignore_index=True)
```

### Memory Optimization

```python
# Use categorical dtype for categorical columns
df['category'] = df['category'].astype('category')

# Drop intermediate columns
df_exp = tv.tidy.expand_multiple_choice(df, 'colors', keep_original=False)

# Use iterator for plotting
for col in ['Q1', 'Q2', 'Q3']:
    tv.viz.plot_single_choice(df, col)
    plt.savefig(f'{col}.png')
    plt.close()  # Free memory
```

---

## Next Steps

- See [API.md](API.md) for complete function reference
- Check `examples/` directory for working code
- Visit GitHub issues for community support
