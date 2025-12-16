"""
Visualization functions for categorical survey data.

This module provides plotting functions for single-choice and multiple-choice
survey questions.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple
from .themes import get_palette


def plot_single_choice(
    df: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
    show_percentages: bool = True,
    sort_by: str = "count",
    top_n: Optional[int] = None,
    figsize: Tuple[int, int] = (10, 6),
    color_palette: str = "default",
) -> plt.Figure:
    """
    Create a bar chart for single-choice survey questions.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to visualize
    title : str, optional
        Chart title. If None, uses column name
    show_percentages : bool, default True
        Whether to show percentage labels on bars
    sort_by : str, default 'count'
        How to sort bars: 'count', 'alphabetical', or 'none'
    top_n : int, optional
        Show only top N categories
    figsize : tuple, default (10, 6)
        Figure size (width, height)
    color_palette : str, default 'default'
        Color palette name

    Returns
    -------
    matplotlib.figure.Figure
        The created figure

    Examples
    --------
    >>> df = pd.DataFrame({'method': ['Email', 'Phone', 'Email', 'Text']})
    >>> fig = plot_single_choice(df, 'method', title='Preferred Contact Method')
    >>> plt.show()
    """
    # Count values
    counts = df[column].value_counts()

    # Sort if requested
    if sort_by == "count":
        counts = counts.sort_values(ascending=False)
    elif sort_by == "alphabetical":
        counts = counts.sort_index()

    # Limit to top N if specified
    if top_n is not None:
        counts = counts.head(top_n)

    # Calculate percentages
    percentages = counts / counts.sum()

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Get colors
    colors = get_palette(color_palette, n_colors=len(counts))

    # Create bar chart
    bars = ax.bar(range(len(counts)), counts.values, color=colors)

    # Set labels
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=45, ha="right")
    ax.set_ylabel("Count")
    ax.set_title(title or f"{column} Distribution")

    # Add percentage labels if requested
    if show_percentages:
        for i, (bar, pct) in enumerate(zip(bars, percentages.values)):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{pct:.1%}\n(n={int(height)})",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    # Add grid
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def plot_multiple_choice(
    df: pd.DataFrame,
    columns: List[str],
    title: Optional[str] = None,
    show_percentages: bool = True,
    sort_by: str = "count",
    top_n: Optional[int] = None,
    figsize: Tuple[int, int] = (10, 6),
    color_palette: str = "default",
) -> plt.Figure:
    """
    Create a bar chart for multiple-choice survey questions.

    Expects binary columns (0/1) for each choice option.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with binary columns
    columns : list of str
        List of binary column names representing choices
    title : str, optional
        Chart title
    show_percentages : bool, default True
        Whether to show percentage labels
    sort_by : str, default 'count'
        How to sort bars: 'count', 'alphabetical', or 'none'
    top_n : int, optional
        Show only top N categories
    figsize : tuple, default (10, 6)
        Figure size
    color_palette : str, default 'default'
        Color palette name

    Returns
    -------
    matplotlib.figure.Figure
        The created figure

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'colors_Blue': [1, 0, 1],
    ...     'colors_Red': [0, 1, 1],
    ...     'colors_Green': [1, 1, 0]
    ... })
    >>> fig = plot_multiple_choice(df, ['colors_Blue', 'colors_Red', 'colors_Green'])
    >>> plt.show()
    """
    # Count selections for each option
    counts = {}
    for col in columns:
        # Extract option name (last part after underscore)
        option_name = col.split("_")[-1] if "_" in col else col
        counts[option_name] = df[col].sum()

    counts = pd.Series(counts)

    # Sort if requested
    if sort_by == "count":
        counts = counts.sort_values(ascending=False)
    elif sort_by == "alphabetical":
        counts = counts.sort_index()

    # Limit to top N
    if top_n is not None:
        counts = counts.head(top_n)

    # Calculate percentages (of total respondents)
    total_respondents = len(df)
    percentages = counts / total_respondents

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Get colors
    colors = get_palette(color_palette, n_colors=len(counts))

    # Create bar chart
    bars = ax.bar(range(len(counts)), counts.values, color=colors)

    # Set labels
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=45, ha="right")
    ax.set_ylabel("Number of Selections")
    ax.set_title(title or "Multiple Choice Responses")

    # Add percentage labels
    if show_percentages:
        for i, (bar, pct) in enumerate(zip(bars, percentages.values)):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{pct:.1%}\n(n={int(height)})",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    # Add grid
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    # Add note about multiple selections
    fig.text(
        0.99,
        0.01,
        f"Note: Percentages based on {total_respondents} total respondents. "
        "Multiple selections allowed.",
        ha="right",
        va="bottom",
        fontsize=8,
        style="italic",
        color="gray",
    )

    plt.tight_layout()
    return fig


def plot_top_n(
    df: pd.DataFrame,
    column: str,
    n: int = 10,
    title: Optional[str] = None,
    show_percentages: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    color_palette: str = "default",
) -> plt.Figure:
    """
    Plot the top N most frequent responses.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to visualize
    n : int, default 10
        Number of top categories to show
    title : str, optional
        Chart title
    show_percentages : bool, default True
        Whether to show percentage labels
    figsize : tuple, default (10, 6)
        Figure size
    color_palette : str, default 'default'
        Color palette name

    Returns
    -------
    matplotlib.figure.Figure
        The created figure

    Examples
    --------
    >>> df = pd.DataFrame({'product': ['A', 'B', 'A', 'C', 'A', 'B']})
    >>> fig = plot_top_n(df, 'product', n=2)
    >>> plt.show()
    """
    return plot_single_choice(
        df=df,
        column=column,
        title=title or f"Top {n} {column}",
        show_percentages=show_percentages,
        sort_by="count",
        top_n=n,
        figsize=figsize,
        color_palette=color_palette,
    )


def plot_grouped_bars(
    df: pd.DataFrame,
    category_column: str,
    value_column: str,
    group_column: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    color_palette: str = "default",
) -> plt.Figure:
    """
    Create grouped bar chart for comparing responses across groups.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    category_column : str
        Column with categories to plot
    value_column : str
        Column with values (usually counts or percentages)
    group_column : str
        Column to group by (e.g., demographic)
    title : str, optional
        Chart title
    figsize : tuple, default (12, 6)
        Figure size
    color_palette : str, default 'default'
        Color palette name

    Returns
    -------
    matplotlib.figure.Figure
        The created figure

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'response': ['Yes', 'No', 'Yes', 'No'],
    ...     'count': [10, 5, 8, 12],
    ...     'gender': ['Male', 'Male', 'Female', 'Female']
    ... })
    >>> fig = plot_grouped_bars(df, 'response', 'count', 'gender')
    >>> plt.show()
    """
    # Pivot data for grouped bar chart
    pivot_df = df.pivot(
        index=category_column, columns=group_column, values=value_column
    )

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Get colors
    colors = get_palette(color_palette, n_colors=len(pivot_df.columns))

    # Create grouped bar chart
    pivot_df.plot(kind="bar", ax=ax, color=colors, width=0.8)

    # Set labels
    ax.set_xlabel(category_column.replace("_", " ").title())
    ax.set_ylabel(value_column.replace("_", " ").title())
    ax.set_title(title or f"{category_column} by {group_column}")
    ax.legend(title=group_column.replace("_", " ").title())

    # Rotate x labels
    plt.xticks(rotation=45, ha="right")

    # Add grid
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig
