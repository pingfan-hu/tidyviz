"""
Reshaping functions for survey data.

This module provides functions to convert between wide and long formats,
and to handle multiple choice questions.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union


def wide_to_long(
    df: pd.DataFrame,
    stub: str,
    i: Union[str, List[str]],
    j: str = "variable",
    sep: str = "_",
    suffix: str = r"\w+",
) -> pd.DataFrame:
    """
    Convert wide format survey data to long format.

    Useful for converting questions like Q1_option1, Q1_option2, Q1_option3
    into a long format with a single value column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe in wide format
    stub : str
        The prefix of columns to convert (e.g., 'Q1' for Q1_option1, Q1_option2)
    i : str or list of str
        Column(s) to use as identifier variable(s)
    j : str, default 'variable'
        Name for the new variable column
    sep : str, default '_'
        Separator between stub and suffix in column names
    suffix : str, default r'\\w+'
        Regular expression for the suffix pattern

    Returns
    -------
    pd.DataFrame
        Dataframe in long format

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'id': [1, 2],
    ...     'Q1_A': [1, 0],
    ...     'Q1_B': [0, 1],
    ...     'Q1_C': [1, 1]
    ... })
    >>> wide_to_long(df, stub='Q1', i='id')
    """
    return pd.wide_to_long(
        df, stubnames=stub, i=i, j=j, sep=sep, suffix=suffix
    ).reset_index()


def long_to_wide(
    df: pd.DataFrame,
    index: Union[str, List[str]],
    columns: str,
    values: str,
    fill_value: Optional[any] = None,
) -> pd.DataFrame:
    """
    Convert long format survey data to wide format.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe in long format
    index : str or list of str
        Column(s) to use as row identifiers
    columns : str
        Column to use for creating new column names
    values : str
        Column to use for values in the new columns
    fill_value : optional
        Value to replace missing values with

    Returns
    -------
    pd.DataFrame
        Dataframe in wide format

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'id': [1, 1, 2, 2],
    ...     'question': ['Q1', 'Q2', 'Q1', 'Q2'],
    ...     'response': [5, 4, 3, 5]
    ... })
    >>> long_to_wide(df, index='id', columns='question', values='response')
    """
    result = df.pivot(index=index, columns=columns, values=values)

    if fill_value is not None:
        result = result.fillna(fill_value)

    # Flatten column names if they're multi-level
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = ['_'.join(map(str, col)).strip() for col in result.columns.values]

    return result.reset_index()


def expand_multiple_choice(
    df: pd.DataFrame,
    column: str,
    sep: str = ",",
    prefix: Optional[str] = None,
    keep_original: bool = False,
) -> pd.DataFrame:
    """
    Expand a multiple choice column into binary indicator columns.

    Converts a column with comma-separated values (e.g., "Blue,Green,Red")
    into separate binary columns for each option.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Name of the column containing comma-separated values
    sep : str, default ','
        Separator used in the multiple choice column
    prefix : str, optional
        Prefix for new column names. If None, uses the original column name
    keep_original : bool, default False
        Whether to keep the original column

    Returns
    -------
    pd.DataFrame
        Dataframe with expanded binary columns

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'id': [1, 2, 3],
    ...     'colors': ['Blue,Green', 'Red', 'Blue,Red,Yellow']
    ... })
    >>> expand_multiple_choice(df, 'colors')
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe")

    # Get unique values across all responses
    all_values = set()
    for val in df[column].dropna():
        if pd.notna(val) and str(val).strip():
            values = [v.strip() for v in str(val).split(sep)]
            all_values.update(values)

    all_values = sorted(all_values)

    # Create prefix for new columns
    col_prefix = prefix if prefix is not None else column

    # Create binary columns for each unique value
    result_df = df.copy()
    for value in all_values:
        new_col = f"{col_prefix}_{value}"
        result_df[new_col] = df[column].apply(
            lambda x: 1 if pd.notna(x) and value in str(x).split(sep) else 0
        )

    # Remove original column if requested
    if not keep_original:
        result_df = result_df.drop(columns=[column])

    return result_df


def collapse_multiple_choice(
    df: pd.DataFrame,
    columns: List[str],
    new_column: str,
    sep: str = ",",
    drop_original: bool = True,
) -> pd.DataFrame:
    """
    Collapse binary indicator columns into a single multiple choice column.

    Inverse operation of expand_multiple_choice. Combines binary columns
    into a comma-separated string.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    columns : list of str
        List of binary column names to collapse
    new_column : str
        Name for the new collapsed column
    sep : str, default ','
        Separator to use in the output
    drop_original : bool, default True
        Whether to drop the original binary columns

    Returns
    -------
    pd.DataFrame
        Dataframe with collapsed column

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'id': [1, 2],
    ...     'colors_Blue': [1, 0],
    ...     'colors_Red': [0, 1],
    ...     'colors_Green': [1, 0]
    ... })
    >>> collapse_multiple_choice(df, ['colors_Blue', 'colors_Red', 'colors_Green'],
    ...                          'colors')
    """
    result_df = df.copy()

    # Extract option names from column names (remove common prefix)
    def get_option_name(col):
        # Try to extract the part after the last underscore
        parts = col.split('_')
        return parts[-1] if len(parts) > 1 else col

    option_names = [get_option_name(col) for col in columns]

    # Create the collapsed column
    def collapse_row(row):
        selected = [
            option_names[i]
            for i, col in enumerate(columns)
            if row[col] == 1
        ]
        return sep.join(selected) if selected else np.nan

    result_df[new_column] = df.apply(collapse_row, axis=1)

    # Drop original columns if requested
    if drop_original:
        result_df = result_df.drop(columns=columns)

    return result_df
