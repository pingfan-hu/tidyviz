"""
TidyViz Visualization Examples

Demonstrates core visualization functions for survey data analysis.
"""

import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tidyviz as tv

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "sample_survey_data.csv")
output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(data_path)

# ============================
# Single Choice Visualizations
# ============================

# Basic single choice plot with percentages
tv.viz.set_survey_style(style="default", palette="categorical")
tv.viz.plot_single_choice(
    df,
    "preferred_contact",
    title="Preferred Contact Method",
    show_percentages=True,
    sort_by="count",
)
plt.savefig(
    os.path.join(output_dir, "single_choice_basic.png"), dpi=150, bbox_inches="tight"
)
plt.close()

# Single choice with sequential color palette
tv.viz.set_survey_style(palette="sequential")
tv.viz.plot_single_choice(
    df, "usage_frequency", title="Product Usage Frequency", show_percentages=True
)
plt.savefig(
    os.path.join(output_dir, "single_choice_sequential.png"),
    dpi=150,
    bbox_inches="tight",
)
plt.close()

# =============================
# Multiple Choice Visualization
# =============================

# Expand multiple choice column to binary indicators
df_expanded = tv.tidy.expand_multiple_choice(df, "favorite_colors")
color_cols = [col for col in df_expanded.columns if col.startswith("favorite_colors_")]

# Plot multiple choice responses
tv.viz.set_survey_style(palette="categorical")
tv.viz.plot_multiple_choice(
    df_expanded,
    color_cols,
    title="Favorite Colors (Multiple Selection)",
    show_percentages=True,
    sort_by="count",
)
plt.savefig(
    os.path.join(output_dir, "multiple_choice.png"), dpi=150, bbox_inches="tight"
)
plt.close()

# =====================
# Custom Color Palettes
# =====================

# Using named matplotlib colormap
tv.viz.set_survey_style(palette="Set2")
tv.viz.plot_single_choice(
    df, "gender", title="Demographics (Set2 Palette)", show_percentages=True
)
plt.savefig(
    os.path.join(output_dir, "custom_palette.png"), dpi=150, bbox_inches="tight"
)
plt.close()

print(f"Visualizations saved to: {output_dir}")
