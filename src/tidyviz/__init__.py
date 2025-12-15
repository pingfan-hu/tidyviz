"""
TidyViz: Tidy and Visualize Survey Data

A Python package for tidying and visualizing survey data.
"""

__version__ = "0.1.0"

# Import submodules
from . import tidy
from . import viz

__all__ = [
    # Version
    "__version__",
    # Submodules
    "tidy",
    "viz",
]
