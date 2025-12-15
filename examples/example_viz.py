"""
TidyViz Viz Module Example

Demonstrates visualization functions for survey data.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import tidyviz as tv

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'sample_survey_data.csv')
output_dir = os.path.join(script_dir, 'outputs')

# Create outputs directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("TidyViz Viz Module Examples")
print("=" * 70)

# Load sample survey data
print("\n[1] Loading survey data...")
df = pd.read_csv(data_path)
print(f"Loaded {len(df)} responses")

# Set visualization style
tv.viz.set_survey_style(style='default', palette='categorical')

# Example 1: Single choice visualization - Preferred Contact
print("\n[2] Creating single choice visualizations...")
fig1 = tv.viz.plot_single_choice(
    df,
    'preferred_contact',
    title='Preferred Contact Method',
    show_percentages=True,
    sort_by='count'
)
output_path = os.path.join(output_dir, 'viz_preferred_contact.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

# Example 2: Single choice visualization - Usage Frequency
fig2 = tv.viz.plot_single_choice(
    df,
    'usage_frequency',
    title='Product Usage Frequency',
    show_percentages=True,
    color_palette='sequential'
)
output_path = os.path.join(output_dir, 'viz_usage_frequency.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

# Example 3: Single choice visualization - Gender Demographics
fig3 = tv.viz.plot_single_choice(
    df,
    'gender',
    title='Respondent Demographics',
    show_percentages=True,
    color_palette='default'
)
output_path = os.path.join(output_dir, 'viz_demographics.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

# Example 4: Multiple choice visualization
print("\n[3] Creating multiple choice visualization...")
# First expand the multiple choice column
df_expanded = tv.tidy.expand_multiple_choice(df, 'favorite_colors', keep_original=True)
color_columns = [col for col in df_expanded.columns if col.startswith('favorite_colors_')]

fig4 = tv.viz.plot_multiple_choice(
    df_expanded,
    color_columns,
    title='Favorite Colors (Multiple Selection)',
    show_percentages=True,
    sort_by='count'
)
output_path = os.path.join(output_dir, 'viz_favorite_colors.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

# Example 5: Different color palettes
print("\n[4] Creating visualizations with different palettes...")

# Sequential palette
tv.viz.set_survey_style(palette='sequential')
fig5 = tv.viz.plot_single_choice(
    df,
    'usage_frequency',
    title='Usage Frequency (Sequential Palette)',
    show_percentages=True
)
output_path = os.path.join(output_dir, 'viz_sequential_palette.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

# Diverging palette
tv.viz.set_survey_style(palette='Set2')
fig6 = tv.viz.plot_single_choice(
    df,
    'preferred_contact',
    title='Preferred Contact (Set2 Palette)',
    show_percentages=True
)
output_path = os.path.join(output_dir, 'viz_set2_palette.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"    Saved: {output_path}")

print("\n" + "=" * 70)
print("Viz Module Examples Complete!")
print(f"Check the outputs directory: {output_dir}")
print("=" * 70)
