"""
Tests for the reshape module.
"""

import pytest
import pandas as pd
import numpy as np
from tidyviz.tidy import reshape


class TestExpandMultipleChoice:
    """Tests for expand_multiple_choice function."""

    def test_basic_expansion(self):
        """Test basic multiple choice expansion."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'colors': ['Blue,Green', 'Red', 'Blue,Red,Yellow']
        })

        result = reshape.expand_multiple_choice(df, 'colors')

        assert 'colors_Blue' in result.columns
        assert 'colors_Green' in result.columns
        assert 'colors_Red' in result.columns
        assert 'colors_Yellow' in result.columns
        assert 'colors' not in result.columns  # Original removed by default

        # Check values
        assert result.loc[0, 'colors_Blue'] == 1
        assert result.loc[0, 'colors_Green'] == 1
        assert result.loc[0, 'colors_Red'] == 0
        assert result.loc[2, 'colors_Yellow'] == 1

    def test_keep_original(self):
        """Test keeping original column."""
        df = pd.DataFrame({
            'id': [1, 2],
            'colors': ['Blue', 'Red']
        })

        result = reshape.expand_multiple_choice(df, 'colors', keep_original=True)

        assert 'colors' in result.columns
        assert 'colors_Blue' in result.columns

    def test_custom_separator(self):
        """Test custom separator."""
        df = pd.DataFrame({
            'id': [1, 2],
            'items': ['A;B', 'C']
        })

        result = reshape.expand_multiple_choice(df, 'items', sep=';')

        assert 'items_A' in result.columns
        assert 'items_B' in result.columns
        assert result.loc[0, 'items_A'] == 1

    def test_custom_prefix(self):
        """Test custom prefix for new columns."""
        df = pd.DataFrame({
            'id': [1],
            'colors': ['Blue']
        })

        result = reshape.expand_multiple_choice(df, 'colors', prefix='choice')

        assert 'choice_Blue' in result.columns
        assert 'colors_Blue' not in result.columns

    def test_missing_values(self):
        """Test handling of missing values."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'colors': ['Blue', np.nan, 'Red']
        })

        result = reshape.expand_multiple_choice(df, 'colors')

        assert result.loc[1, 'colors_Blue'] == 0
        assert result.loc[1, 'colors_Red'] == 0

    def test_column_not_found(self):
        """Test error when column doesn't exist."""
        df = pd.DataFrame({'id': [1, 2]})

        with pytest.raises(ValueError, match="Column 'colors' not found"):
            reshape.expand_multiple_choice(df, 'colors')


class TestCollapseMultipleChoice:
    """Tests for collapse_multiple_choice function."""

    def test_basic_collapse(self):
        """Test basic collapse of binary columns."""
        df = pd.DataFrame({
            'id': [1, 2],
            'colors_Blue': [1, 0],
            'colors_Red': [0, 1],
            'colors_Green': [1, 0]
        })

        result = reshape.collapse_multiple_choice(
            df,
            ['colors_Blue', 'colors_Red', 'colors_Green'],
            'colors'
        )

        assert 'colors' in result.columns
        assert result.loc[0, 'colors'] == 'Blue,Green'
        assert result.loc[1, 'colors'] == 'Red'

    def test_keep_original_columns(self):
        """Test keeping original binary columns."""
        df = pd.DataFrame({
            'id': [1],
            'opt_A': [1],
            'opt_B': [0]
        })

        result = reshape.collapse_multiple_choice(
            df,
            ['opt_A', 'opt_B'],
            'options',
            drop_original=False
        )

        assert 'options' in result.columns
        assert 'opt_A' in result.columns
        assert 'opt_B' in result.columns

    def test_no_selection(self):
        """Test row with no selections."""
        df = pd.DataFrame({
            'id': [1],
            'colors_Blue': [0],
            'colors_Red': [0]
        })

        result = reshape.collapse_multiple_choice(
            df,
            ['colors_Blue', 'colors_Red'],
            'colors'
        )

        assert pd.isna(result.loc[0, 'colors'])

    def test_custom_separator(self):
        """Test custom separator."""
        df = pd.DataFrame({
            'id': [1],
            'opt_A': [1],
            'opt_B': [1]
        })

        result = reshape.collapse_multiple_choice(
            df,
            ['opt_A', 'opt_B'],
            'options',
            sep=';'
        )

        assert result.loc[0, 'options'] == 'A;B'


class TestWideToLong:
    """Tests for wide_to_long function."""

    def test_basic_wide_to_long(self):
        """Test basic wide to long conversion."""
        df = pd.DataFrame({
            'id': [1, 2],
            'Q1_A': [1, 0],
            'Q1_B': [0, 1]
        })

        result = reshape.wide_to_long(df, stub='Q1', i='id')

        assert 'variable' in result.columns
        assert len(result) == 4  # 2 rows * 2 variables

    def test_custom_column_names(self):
        """Test custom j parameter."""
        df = pd.DataFrame({
            'id': [1, 2],
            'score_math': [90, 85],
            'score_reading': [88, 92]
        })

        result = reshape.wide_to_long(
            df,
            stub='score',
            i='id',
            j='subject'
        )

        assert 'subject' in result.columns


class TestLongToWide:
    """Tests for long_to_wide function."""

    def test_basic_long_to_wide(self):
        """Test basic long to wide conversion."""
        df = pd.DataFrame({
            'id': [1, 1, 2, 2],
            'question': ['Q1', 'Q2', 'Q1', 'Q2'],
            'response': [5, 4, 3, 5]
        })

        result = reshape.long_to_wide(
            df,
            index='id',
            columns='question',
            values='response'
        )

        assert 'Q1' in result.columns
        assert 'Q2' in result.columns
        assert len(result) == 2  # 2 unique ids

    def test_fill_missing_values(self):
        """Test filling missing values."""
        df = pd.DataFrame({
            'id': [1, 2, 2],
            'question': ['Q1', 'Q1', 'Q2'],
            'response': [5, 3, 4]
        })

        result = reshape.long_to_wide(
            df,
            index='id',
            columns='question',
            values='response',
            fill_value=0
        )

        assert result.loc[0, 'Q2'] == 0  # Filled missing value
