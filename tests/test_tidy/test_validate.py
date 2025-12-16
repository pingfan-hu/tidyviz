"""
Tests for the validate module.
"""

import pytest
import pandas as pd
import numpy as np
from tidyviz.tidy import validate


class TestCheckResponseRange:
    """Tests for check_response_range function."""

    def test_flag_invalid_responses(self):
        """Test flagging invalid responses."""
        df = pd.DataFrame({"satisfaction": [1, 3, 5, 7, 2]})

        result, invalid_mask = validate.check_response_range(
            df, "satisfaction", 1, 5, handle_invalid="flag"
        )

        assert "satisfaction_valid" in result.columns
        assert result["satisfaction_valid"].sum() == 4  # 4 valid values
        assert invalid_mask.sum() == 1  # 1 invalid value
        assert invalid_mask.iloc[3]  # 7 is invalid

    def test_remove_invalid_responses(self):
        """Test removing invalid responses."""
        df = pd.DataFrame({"satisfaction": [1, 3, 5, 7, 2]})

        result = validate.check_response_range(
            df, "satisfaction", 1, 5, handle_invalid="remove"
        )

        assert len(result) == 4
        assert 7 not in result["satisfaction"].values

    def test_nan_invalid_responses(self):
        """Test replacing invalid with NaN."""
        df = pd.DataFrame({"satisfaction": [1, 3, 5, 7, 2]})

        result = validate.check_response_range(
            df, "satisfaction", 1, 5, handle_invalid="nan"
        )

        assert pd.isna(result.loc[3, "satisfaction"])
        assert result["satisfaction"].notna().sum() == 4

    def test_handle_existing_nan(self):
        """Test that existing NaN values are preserved."""
        df = pd.DataFrame({"satisfaction": [1, np.nan, 5, 3]})

        result, invalid_mask = validate.check_response_range(
            df, "satisfaction", 1, 5, handle_invalid="flag"
        )

        assert result["satisfaction_valid"].iloc[1]  # NaN is valid
        assert invalid_mask.sum() == 0

    def test_float_range(self):
        """Test with float values."""
        df = pd.DataFrame({"rating": [1.5, 2.8, 5.2, 3.0]})

        result, invalid_mask = validate.check_response_range(
            df, "rating", 1.0, 5.0, handle_invalid="flag"
        )

        assert invalid_mask.iloc[2]  # 5.2 is invalid

    def test_column_not_found(self):
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"other": [1, 2, 3]})

        with pytest.raises(ValueError, match="Column 'satisfaction' not found"):
            validate.check_response_range(df, "satisfaction", 1, 5)

    def test_invalid_handle_option(self):
        """Test error with invalid handle_invalid option."""
        df = pd.DataFrame({"satisfaction": [1, 2, 3]})

        with pytest.raises(ValueError, match="Invalid handle_invalid option"):
            validate.check_response_range(
                df, "satisfaction", 1, 5, handle_invalid="invalid_option"
            )


class TestDetectMissingPatterns:
    """Tests for detect_missing_patterns function."""

    def test_basic_missing_detection(self):
        """Test basic missing data detection."""
        df = pd.DataFrame(
            {"Q1": [1, 2, np.nan, 4], "Q2": [1, np.nan, np.nan, 4], "Q3": [1, 2, 3, 4]}
        )

        result = validate.detect_missing_patterns(df)

        assert "missing_counts" in result
        assert "missing_rates" in result
        assert result["missing_counts"]["Q1"] == 1
        assert result["missing_counts"]["Q2"] == 2
        assert result["missing_counts"]["Q3"] == 0

    def test_missing_rates(self):
        """Test missing rate calculation."""
        df = pd.DataFrame({"Q1": [1, np.nan, np.nan, np.nan], "Q2": [1, 2, 3, 4]})

        result = validate.detect_missing_patterns(df)

        assert result["missing_rates"]["Q1"] == 0.75
        assert result["missing_rates"]["Q2"] == 0.0

    def test_high_missing_threshold(self):
        """Test high missing threshold detection."""
        df = pd.DataFrame(
            {"Q1": [1, np.nan, np.nan, 4], "Q2": [1, 2, np.nan, 4], "Q3": [1, 2, 3, 4]}
        )

        result = validate.detect_missing_patterns(df, threshold=0.4)

        assert "Q1" in result["high_missing_cols"]  # 50% missing
        assert "Q2" not in result["high_missing_cols"]  # 25% missing

    def test_row_counts(self):
        """Test row-level missing counts."""
        df = pd.DataFrame({"Q1": [1, np.nan, 3], "Q2": [1, 2, np.nan], "Q3": [1, 2, 3]})

        result = validate.detect_missing_patterns(df)

        assert result["rows_with_missing"] == 2
        assert result["complete_rows"] == 1
        assert result["total_rows"] == 3

    def test_specific_columns(self):
        """Test analyzing specific columns only."""
        df = pd.DataFrame(
            {"Q1": [1, np.nan, 3], "Q2": [1, 2, 3], "Q3": [np.nan, np.nan, np.nan]}
        )

        result = validate.detect_missing_patterns(df, columns=["Q1", "Q2"])

        assert "Q3" not in result["missing_counts"].index


class TestFlagStraightLiners:
    """Tests for flag_straight_liners function."""

    def test_detect_straight_liner(self):
        """Test detecting straight-lined responses."""
        df = pd.DataFrame({"Q1": [3, 5, 3], "Q2": [3, 4, 3], "Q3": [3, 3, 3]})

        result = validate.flag_straight_liners(df, ["Q1", "Q2", "Q3"])

        assert result.iloc[0]  # All 3s
        assert not result.iloc[1]  # Varied responses
        assert result.iloc[2]  # All 3s - straight-liner

    def test_with_missing_values(self):
        """Test with missing values."""
        df = pd.DataFrame(
            {"Q1": [3, np.nan, 5], "Q2": [3, np.nan, 5], "Q3": [3, np.nan, 5]}
        )

        result = validate.flag_straight_liners(df, ["Q1", "Q2", "Q3"])

        assert result.iloc[0]  # All 3s
        assert result.iloc[2]  # All 5s

    def test_threshold_parameter(self):
        """Test threshold parameter."""
        df = pd.DataFrame({"Q1": [1, 2, 3], "Q2": [1, 2, 4], "Q3": [1, 2, 5]})

        # Default threshold=0 flags only 1 unique value
        result_0 = validate.flag_straight_liners(df, ["Q1", "Q2", "Q3"], threshold=0)
        # Rows 0 and 1 have only 1 unique value (all 1s, all 2s)
        assert result_0.sum() == 2
        assert result_0.iloc[0]  # All 1s
        assert result_0.iloc[1]  # All 2s
        assert not result_0.iloc[2]  # Has 3 unique values

    def test_column_not_found(self):
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"Q1": [1, 2, 3]})

        with pytest.raises(ValueError, match="Columns not found"):
            validate.flag_straight_liners(df, ["Q1", "Q2"])


class TestDetectSpeeders:
    """Tests for detect_speeders function."""

    def test_detect_with_manual_threshold(self):
        """Test speeder detection with manual threshold."""
        df = pd.DataFrame({"completion_time": [120, 45, 300, 30, 180]})

        result = validate.detect_speeders(df, "completion_time", threshold=60)

        assert result.iloc[1]  # 45 < 60
        assert result.iloc[3]  # 30 < 60
        assert not result.iloc[0]  # 120 >= 60

    def test_iqr_method(self):
        """Test IQR method for automatic threshold."""
        df = pd.DataFrame({"completion_time": [100, 110, 120, 130, 140, 30]})

        result = validate.detect_speeders(df, "completion_time", method="iqr")

        assert result.iloc[5]  # 30 is outlier

    def test_median_method(self):
        """Test median method."""
        df = pd.DataFrame({"completion_time": [100, 200, 300, 40]})

        result = validate.detect_speeders(df, "completion_time", method="median")

        # Median is 150, threshold is 75
        assert result.iloc[3]  # 40 < 75

    def test_percentile_method(self):
        """Test percentile method."""
        df = pd.DataFrame({"completion_time": list(range(10, 110, 10))})

        result = validate.detect_speeders(df, "completion_time", method="percentile")

        # 10th percentile should flag the lowest value
        assert result.iloc[0]

    def test_column_not_found(self):
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"other": [1, 2, 3]})

        with pytest.raises(ValueError, match="Column 'time' not found"):
            validate.detect_speeders(df, "time")

    def test_invalid_method(self):
        """Test error with invalid method."""
        df = pd.DataFrame({"time": [100, 200]})

        with pytest.raises(ValueError, match="Invalid method"):
            validate.detect_speeders(df, "time", method="invalid")


class TestCheckLogicalConsistency:
    """Tests for check_logical_consistency function."""

    def test_basic_consistency_check(self):
        """Test basic logical consistency."""
        df = pd.DataFrame({"age": [25, 30, 20], "years_experience": [5, 12, 2]})

        rules = [
            {
                "name": "age_experience",
                "condition": lambda row: row["age"] >= row["years_experience"] + 18,
                "columns": ["age", "years_experience"],
            }
        ]

        result = validate.check_logical_consistency(df, rules)

        assert "consistent_age_experience" in result.columns
        assert result["consistent_age_experience"].iloc[0]  # 25 >= 5+18 (23)
        assert result["consistent_age_experience"].iloc[1]  # 30 >= 12+18 (30)
        assert result["consistent_age_experience"].iloc[2]  # 20 >= 2+18 (20)

    def test_multiple_rules(self):
        """Test multiple consistency rules."""
        df = pd.DataFrame(
            {"min_val": [10, 20], "max_val": [20, 15], "avg_val": [15, 18]}
        )

        rules = [
            {
                "name": "min_max",
                "condition": lambda row: row["min_val"] <= row["max_val"],
                "columns": ["min_val", "max_val"],
            },
            {
                "name": "avg_in_range",
                "condition": lambda row: (
                    row["min_val"] <= row["avg_val"] <= row["max_val"]
                ),
                "columns": ["min_val", "avg_val", "max_val"],
            },
        ]

        result = validate.check_logical_consistency(df, rules)

        assert "consistent_min_max" in result.columns
        assert "consistent_avg_in_range" in result.columns
        assert result["consistent_min_max"].iloc[0]
        assert not result["consistent_min_max"].iloc[1]

    def test_missing_condition(self):
        """Test error when rule has no condition."""
        df = pd.DataFrame({"a": [1, 2]})

        rules = [{"name": "test_rule"}]

        with pytest.raises(ValueError, match="must have a 'condition' function"):
            validate.check_logical_consistency(df, rules)
