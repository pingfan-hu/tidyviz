"""
Theme and styling for survey visualizations.

This module provides survey-appropriate color palettes and styling functions.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List


# Survey-friendly color palettes
SURVEY_PALETTES = {
    "default": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E"],
    "likert": ["#D7191C", "#FDAE61", "#FFFFBF", "#A6D96A", "#1A9641"],
    "categorical": [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14F",
        "#EDC948",
        "#B07AA1",
        "#FF9DA7",
        "#9C755F",
        "#BAB0AC",
    ],
    "sequential": [
        "#FFF5EB",
        "#FEE6CE",
        "#FDD0A2",
        "#FDAE6B",
        "#FD8D3C",
        "#F16913",
        "#D94801",
        "#8C2D04",
    ],
    "nps": ["#D7191C", "#FDAE61", "#1A9641"],  # Detractor, Passive, Promoter
}


def set_survey_style(style: str = "default", palette: str = "default") -> None:
    """
    Set matplotlib style for survey visualizations.

    Parameters
    ----------
    style : str, default 'default'
        Style preset: 'default', 'minimal', or 'presentation'
    palette : str, default 'default'
        Color palette name from SURVEY_PALETTES

    Examples
    --------
    >>> set_survey_style('presentation', 'categorical')
    """
    # Base seaborn style
    if style == "minimal":
        sns.set_style(
            "whitegrid",
            {
                "axes.edgecolor": "0.8",
                "grid.color": "0.9",
                "axes.spines.top": False,
                "axes.spines.right": False,
            },
        )
    elif style == "presentation":
        sns.set_style("white")
        plt.rcParams.update(
            {
                "font.size": 12,
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
            }
        )
    else:  # default
        sns.set_style("whitegrid")

    # Set color palette
    if palette in SURVEY_PALETTES:
        sns.set_palette(SURVEY_PALETTES[palette])
    else:
        sns.set_palette(palette)

    # Common settings for survey charts
    plt.rcParams.update(
        {
            "figure.figsize": (10, 6),
            "axes.grid": True,
            "grid.alpha": 0.3,
        }
    )


def get_palette(
    palette_name: str = "default", n_colors: Optional[int] = None
) -> List[str]:
    """
    Get a color palette for survey visualizations.

    Parameters
    ----------
    palette_name : str, default 'default'
        Name of the palette from SURVEY_PALETTES
    n_colors : int, optional
        Number of colors to return. If None, returns all colors in palette

    Returns
    -------
    list of str
        List of hex color codes

    Examples
    --------
    >>> colors = get_palette('categorical', n_colors=3)
    """
    palette = SURVEY_PALETTES.get(palette_name, SURVEY_PALETTES["default"])

    if n_colors is not None:
        if n_colors <= len(palette):
            return palette[:n_colors]
        else:
            # Repeat palette if needed
            return (palette * (n_colors // len(palette) + 1))[:n_colors]

    return palette


def format_percentage_axis(ax, axis: str = "y") -> None:
    """
    Format axis to display percentages.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object to format
    axis : str, default 'y'
        Which axis to format ('x' or 'y')

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> # ... plot data ...
    >>> format_percentage_axis(ax, 'y')
    """
    from matplotlib.ticker import FuncFormatter

    def to_percent(y, position):
        return f"{100 * y:.0f}%"

    formatter = FuncFormatter(to_percent)

    if axis.lower() == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)
