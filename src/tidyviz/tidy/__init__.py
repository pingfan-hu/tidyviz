"""
Data cleaning module for survey data.

This module provides functions for reshaping, validating, recoding,
and detecting outliers in survey data.
"""

from .reshape import (
    wide_to_long,
    long_to_wide,
    expand_multiple_choice,
    collapse_multiple_choice,
)

from .validate import (
    check_response_range,
    detect_missing_patterns,
    flag_straight_liners,
    detect_speeders,
    check_logical_consistency,
)

__all__ = [
    # Reshape functions
    "wide_to_long",
    "long_to_wide",
    "expand_multiple_choice",
    "collapse_multiple_choice",
    # Validation functions
    "check_response_range",
    "detect_missing_patterns",
    "flag_straight_liners",
    "detect_speeders",
    "check_logical_consistency",
]
