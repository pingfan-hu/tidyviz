"""
Validation functions for survey data.

This module provides functions to validate survey responses, detect missing
data patterns, and identify data quality issues.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Optional, Tuple, Dict


def check_response_range(
    df: pd.DataFrame,
    column: str,
    min_val: Union[int, float],
    max_val: Union[int, float],
    handle_invalid: str = "flag",
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.Series]]:
    """
    Validate that responses fall within an expected range.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to validate
    min_val : int or float
        Minimum valid value (inclusive)
    max_val : int or float
        Maximum valid value (inclusive)
    handle_invalid : str, default 'flag'
        How to handle invalid values:
        - 'flag': Return dataframe with additional '_valid' column
        - 'remove': Remove rows with invalid values
        - 'nan': Replace invalid values with NaN

    Returns
    -------
    pd.DataFrame or tuple of (pd.DataFrame, pd.Series)
        If handle_invalid='flag', returns (dataframe, invalid_mask)
        Otherwise returns modified dataframe

    Examples
    --------
    >>> df = pd.DataFrame({'satisfaction': [1, 3, 5, 7, 2]})
    >>> check_response_range(df, 'satisfaction', 1, 5, handle_invalid='flag')
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe")

    result_df = df.copy()

    # Create mask for valid values (accounting for NaN)
    valid_mask = (
        (result_df[column].isna()) |
        ((result_df[column] >= min_val) & (result_df[column] <= max_val))
    )
    invalid_mask = ~valid_mask

    if handle_invalid == "flag":
        result_df[f"{column}_valid"] = valid_mask
        return result_df, invalid_mask

    elif handle_invalid == "remove":
        return result_df[valid_mask].reset_index(drop=True)

    elif handle_invalid == "nan":
        result_df.loc[invalid_mask, column] = np.nan
        return result_df

    else:
        raise ValueError(
            f"Invalid handle_invalid option: {handle_invalid}. "
            "Must be 'flag', 'remove', or 'nan'"
        )


def detect_missing_patterns(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    threshold: float = 0.5,
) -> Dict[str, any]:
    """
    Identify missing data patterns in survey responses.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    columns : list of str, optional
        Columns to analyze. If None, analyzes all columns
    threshold : float, default 0.5
        Threshold for flagging high missing rate (0 to 1)

    Returns
    -------
    dict
        Dictionary containing:
        - 'missing_counts': Series of missing value counts per column
        - 'missing_rates': Series of missing value rates per column
        - 'high_missing_cols': List of columns exceeding threshold
        - 'rows_with_missing': Number of rows with any missing values
        - 'complete_rows': Number of rows with no missing values

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'Q1': [1, 2, np.nan, 4],
    ...     'Q2': [1, np.nan, np.nan, 4]
    ... })
    >>> detect_missing_patterns(df)
    """
    if columns is None:
        columns = df.columns.tolist()

    analysis_df = df[columns]

    missing_counts = analysis_df.isna().sum()
    missing_rates = missing_counts / len(analysis_df)

    high_missing_cols = missing_rates[missing_rates > threshold].index.tolist()

    rows_with_missing = analysis_df.isna().any(axis=1).sum()
    complete_rows = len(analysis_df) - rows_with_missing

    return {
        "missing_counts": missing_counts,
        "missing_rates": missing_rates,
        "high_missing_cols": high_missing_cols,
        "rows_with_missing": rows_with_missing,
        "complete_rows": complete_rows,
        "total_rows": len(analysis_df),
    }


def flag_straight_liners(
    df: pd.DataFrame,
    columns: List[str],
    threshold: int = 0,
) -> pd.Series:
    """
    Detect respondents who gave the same answer to all questions (straight-lining).

    This is a common data quality issue in surveys where respondents
    don't engage thoughtfully with the questions.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    columns : list of str
        List of columns to check for straight-lining
    threshold : int, default 0
        Number of unique values threshold. If 0, flags rows with only 1 unique value.
        If 1, flags rows with 1 or fewer unique values, etc.

    Returns
    -------
    pd.Series
        Boolean series indicating straight-lined responses (True = straight-liner)

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'Q1': [3, 5, 3],
    ...     'Q2': [3, 4, 3],
    ...     'Q3': [3, 3, 3]
    ... })
    >>> flag_straight_liners(df, ['Q1', 'Q2', 'Q3'])
    """
    # Check that all columns exist
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns not found in dataframe: {missing_cols}")

    # Count unique non-null values per row
    def count_unique(row):
        values = row.dropna()
        return len(values.unique()) if len(values) > 0 else 0

    unique_counts = df[columns].apply(count_unique, axis=1)

    # Flag rows with unique count <= threshold
    return unique_counts <= max(1, threshold)


def detect_speeders(
    df: pd.DataFrame,
    time_column: str,
    threshold: Optional[float] = None,
    method: str = "iqr",
) -> pd.Series:
    """
    Identify respondents who completed the survey too quickly (speeders).

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    time_column : str
        Column containing completion time (in seconds or minutes)
    threshold : float, optional
        Time threshold in same units as time_column. If None, calculates
        automatically based on method
    method : str, default 'iqr'
        Method for automatic threshold:
        - 'iqr': Q1 - 1.5*IQR
        - 'median': 0.5 * median
        - 'percentile': 10th percentile

    Returns
    -------
    pd.Series
        Boolean series indicating speeders (True = speeder)

    Examples
    --------
    >>> df = pd.DataFrame({'completion_time': [120, 45, 300, 30, 180]})
    >>> detect_speeders(df, 'completion_time', method='median')
    """
    if time_column not in df.columns:
        raise ValueError(f"Column '{time_column}' not found in dataframe")

    times = df[time_column].dropna()

    if threshold is None:
        if method == "iqr":
            q1 = times.quantile(0.25)
            q3 = times.quantile(0.75)
            iqr = q3 - q1
            threshold = q1 - 1.5 * iqr
        elif method == "median":
            threshold = times.median() * 0.5
        elif method == "percentile":
            threshold = times.quantile(0.10)
        else:
            raise ValueError(
                f"Invalid method: {method}. Must be 'iqr', 'median', or 'percentile'"
            )

    # Ensure threshold is non-negative
    threshold = max(0, threshold)

    return df[time_column] < threshold


def check_logical_consistency(
    df: pd.DataFrame,
    rules: List[Dict[str, any]],
) -> pd.DataFrame:
    """
    Check logical consistency between survey responses.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    rules : list of dict
        List of consistency rules. Each rule is a dict with:
        - 'condition': lambda function that returns True if consistent
        - 'name': descriptive name for the rule
        - 'columns': list of columns involved

    Returns
    -------
    pd.DataFrame
        Original dataframe with additional columns for each rule
        showing consistency (True = consistent, False = inconsistent)

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'age': [25, 30, 20],
    ...     'years_experience': [8, 12, 2]
    ... })
    >>> rules = [{
    ...     'name': 'age_experience',
    ...     'condition': lambda row: row['age'] >= row['years_experience'] + 18,
    ...     'columns': ['age', 'years_experience']
    ... }]
    >>> check_logical_consistency(df, rules)
    """
    result_df = df.copy()

    for rule in rules:
        rule_name = rule.get("name", "unnamed_rule")
        condition = rule.get("condition")
        columns = rule.get("columns", [])

        if condition is None:
            raise ValueError(f"Rule '{rule_name}' must have a 'condition' function")

        # Apply condition to each row
        try:
            result_df[f"consistent_{rule_name}"] = df.apply(condition, axis=1)
        except Exception as e:
            raise ValueError(
                f"Error applying rule '{rule_name}': {str(e)}"
            )

    return result_df
