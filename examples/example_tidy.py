"""
TidyViz Tidy Module Example

Demonstrates data tidying and wrangling functions for survey data.
"""

import os
import pandas as pd
import tidyviz as tv

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'sample_survey_data.csv')
output_dir = os.path.join(script_dir, 'outputs')

# Create outputs directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("TidyViz Tidy Module Examples")
print("=" * 70)

# Load sample survey data
print("\n[1] Loading survey data...")
df = pd.read_csv(data_path)
print(f"Loaded {len(df)} responses with {len(df.columns)} columns")

# Example 1: Detect missing data patterns
print("\n[2] Detecting missing data patterns...")
missing_info = tv.tidy.detect_missing_patterns(df)
print(f"   Complete rows: {missing_info['complete_rows']}/{len(df)}")
print(f"   Rows with missing data: {missing_info['rows_with_missing']}")
print("\n   Columns with missing data:")
for col, rate in missing_info['missing_rates'].items():
    if rate > 0:
        print(f"   - {col}: {rate:.1%}")

# Example 2: Validate response ranges
print("\n[3] Validating response ranges...")
df_validated, invalid_satisfaction = tv.tidy.check_response_range(
    df, 'satisfaction', 1, 5, handle_invalid='flag'
)
df_validated, invalid_nps = tv.tidy.check_response_range(
    df_validated, 'recommend_score', 0, 10, handle_invalid='flag'
)
print(f"   Invalid satisfaction scores: {invalid_satisfaction.sum()}")
print(f"   Invalid NPS scores: {invalid_nps.sum()}")

# Save validated data
validated_path = os.path.join(output_dir, 'validated_survey_data.csv')
df_validated.to_csv(validated_path, index=False)
print(f"\n    Saved validated data to: {validated_path}")

# Example 3: Expand multiple choice responses
print("\n[4] Expanding multiple choice responses...")
df_expanded = tv.tidy.expand_multiple_choice(
    df, 'favorite_colors', keep_original=True
)
color_columns = [col for col in df_expanded.columns if col.startswith('favorite_colors_')]
print(f"   Created {len(color_columns)} binary columns:")
for col in color_columns:
    count = df_expanded[col].sum()
    print(f"   - {col}: {count} respondents")

# Save expanded data
expanded_path = os.path.join(output_dir, 'expanded_survey_data.csv')
df_expanded.to_csv(expanded_path, index=False)
print(f"\n    Saved expanded data to: {expanded_path}")

# Example 4: Create summary statistics
print("\n[5] Generating summary statistics...")
summary_stats = {
    'total_respondents': len(df),
    'complete_responses': missing_info['complete_rows'],
    'avg_satisfaction': df['satisfaction'].mean(),
    'avg_nps_score': df['recommend_score'].mean(),
    'most_common_contact': df['preferred_contact'].mode()[0],
    'data_completeness_rate': missing_info['complete_rows'] / len(df)
}

summary_df = pd.DataFrame([summary_stats])
summary_path = os.path.join(output_dir, 'summary_statistics.csv')
summary_df.to_csv(summary_path, index=False)
print(f"    Saved summary statistics to: {summary_path}")

print("\n" + "=" * 70)
print("Tidy Module Examples Complete!")
print(f"Check the outputs directory: {output_dir}")
print("=" * 70)
