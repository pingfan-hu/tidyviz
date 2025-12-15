"""
Visualization module for survey data.

This module provides plotting functions for categorical data, scales,
distributions, and custom theming.
"""

from .categorical import (
    plot_single_choice,
    plot_multiple_choice,
    plot_top_n,
    plot_grouped_bars,
)

from .themes import (
    set_survey_style,
    get_palette,
    format_percentage_axis,
    SURVEY_PALETTES,
)

__all__ = [
    # Categorical plots
    "plot_single_choice",
    "plot_multiple_choice",
    "plot_top_n",
    "plot_grouped_bars",
    # Theming
    "set_survey_style",
    "get_palette",
    "format_percentage_axis",
    "SURVEY_PALETTES",
]
