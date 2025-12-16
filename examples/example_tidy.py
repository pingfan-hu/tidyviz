"""
TidyViz Data Cleaning Examples

Demonstrates data validation and transformation functions for survey data.
"""

import os
import pandas as pd
import tidyviz as tv

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "sample_survey_data.csv")
output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(data_path)

# ======================
# Missing Data Detection
# ======================

# Analyze missing data patterns across the dataset
missing_info = tv.tidy.detect_missing_patterns(df)
print(f"Missing data: {missing_info['rows_with_missing']}/{len(df)} rows")

# =========================
# Response Range Validation
# =========================

# Validate satisfaction scores (1-5 scale)
df_validated, invalid_satisfaction = tv.tidy.check_response_range(
    df, "satisfaction", min_val=1, max_val=5, handle_invalid="flag"
)

# Validate NPS scores (0-10 scale)
df_validated, invalid_nps = tv.tidy.check_response_range(
    df_validated, "recommend_score", min_val=0, max_val=10, handle_invalid="flag"
)

print(f"Invalid responses found: {invalid_satisfaction.sum() + invalid_nps.sum()}")

# =========================
# Multiple Choice Expansion
# =========================

# Convert comma-separated values to binary indicator columns
df_expanded = tv.tidy.expand_multiple_choice(
    df_validated, "favorite_colors", keep_original=True
)

# Show expanded columns
color_cols = [col for col in df_expanded.columns if col.startswith("favorite_colors_")]
print(f"Expanded to {len(color_cols)} binary columns: {color_cols}")

# ===================
# Export Cleaned Data
# ===================

# Save validated dataset
df_validated.to_csv(os.path.join(output_dir, "validated_data.csv"), index=False)

# Save expanded dataset for analysis
df_expanded.to_csv(os.path.join(output_dir, "expanded_data.csv"), index=False)

print(f"\nCleaned data saved to: {output_dir}")
