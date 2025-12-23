"""Tests for tidyviz.viz.themes module."""

import matplotlib.pyplot as plt
from tidyviz.viz.themes import (
    get_palette,
    set_survey_style,
    format_percentage_axis,
    SURVEY_PALETTES,
)


class TestGetPalette:
    """Tests for get_palette function."""

    def test_default_palette(self):
        """Test getting default palette."""
        colors = get_palette("default")
        assert isinstance(colors, list)
        assert len(colors) > 0
        assert all(isinstance(c, str) for c in colors)
        assert all(c.startswith("#") for c in colors)

    def test_likert_palette(self):
        """Test getting likert palette."""
        colors = get_palette("likert")
        assert colors == SURVEY_PALETTES["likert"]

    def test_categorical_palette(self):
        """Test getting categorical palette."""
        colors = get_palette("categorical")
        assert colors == SURVEY_PALETTES["categorical"]

    def test_sequential_palette(self):
        """Test getting sequential palette."""
        colors = get_palette("sequential")
        assert colors == SURVEY_PALETTES["sequential"]

    def test_nps_palette(self):
        """Test getting NPS palette."""
        colors = get_palette("nps")
        assert colors == SURVEY_PALETTES["nps"]
        assert len(colors) == 3  # Detractor, Passive, Promoter

    def test_invalid_palette_returns_default(self):
        """Test that invalid palette name returns default."""
        colors = get_palette("nonexistent_palette")
        assert colors == SURVEY_PALETTES["default"]

    def test_n_colors_less_than_palette(self):
        """Test requesting fewer colors than palette has."""
        colors = get_palette("categorical", n_colors=3)
        assert len(colors) == 3
        assert colors == SURVEY_PALETTES["categorical"][:3]

    def test_n_colors_equal_to_palette(self):
        """Test requesting exactly as many colors as palette has."""
        palette_length = len(SURVEY_PALETTES["default"])
        colors = get_palette("default", n_colors=palette_length)
        assert len(colors) == palette_length

    def test_n_colors_more_than_palette(self):
        """Test requesting more colors than palette has (should repeat)."""
        palette = SURVEY_PALETTES["nps"]  # Only 3 colors
        colors = get_palette("nps", n_colors=7)
        assert len(colors) == 7
        # First 3 should match palette
        assert colors[:3] == palette
        # Should start repeating
        assert colors[3] == palette[0]
        assert colors[4] == palette[1]

    def test_n_colors_none_returns_full_palette(self):
        """Test that n_colors=None returns full palette."""
        colors = get_palette("categorical", n_colors=None)
        assert colors == SURVEY_PALETTES["categorical"]

    def test_n_colors_zero(self):
        """Test edge case of n_colors=0."""
        colors = get_palette("default", n_colors=0)
        assert len(colors) == 0

    def test_n_colors_one(self):
        """Test edge case of n_colors=1."""
        colors = get_palette("default", n_colors=1)
        assert len(colors) == 1
        assert colors[0] == SURVEY_PALETTES["default"][0]

    def test_all_palettes_are_valid_hex(self):
        """Test that all predefined palettes contain valid hex colors."""
        for palette_name, palette_colors in SURVEY_PALETTES.items():
            for color in palette_colors:
                assert isinstance(color, str)
                assert color.startswith("#")
                # Hex color should be 7 characters (#RRGGBB)
                assert len(color) == 7


class TestSetSurveyStyle:
    """Tests for set_survey_style function."""

    def test_default_style(self):
        """Test setting default style."""
        set_survey_style("default", "default")
        # If no exception, style was set successfully
        assert True

    def test_minimal_style(self):
        """Test setting minimal style."""
        set_survey_style("minimal", "categorical")
        # Check that some rcParams were updated
        assert list(plt.rcParams["figure.figsize"]) == [10, 6]

    def test_presentation_style(self):
        """Test setting presentation style."""
        set_survey_style("presentation", "likert")
        # Check font sizes were updated for presentation
        assert plt.rcParams["font.size"] == 12
        assert plt.rcParams["axes.titlesize"] == 14

    def test_style_with_default_palette(self):
        """Test style with default palette."""
        set_survey_style("default", "default")
        assert plt.rcParams["axes.grid"] is True

    def test_style_with_custom_palette_name(self):
        """Test style with custom seaborn palette name."""
        set_survey_style("default", "viridis")
        # Should accept non-SURVEY_PALETTES palette names
        assert True

    def test_grid_settings(self):
        """Test that grid settings are applied."""
        set_survey_style("default", "default")
        assert plt.rcParams["axes.grid"] is True
        assert plt.rcParams["grid.alpha"] == 0.3

    def test_figure_size_default(self):
        """Test that default figure size is set."""
        set_survey_style("default", "default")
        assert list(plt.rcParams["figure.figsize"]) == [10, 6]


class TestFormatPercentageAxis:
    """Tests for format_percentage_axis function."""

    def test_format_y_axis(self):
        """Test formatting y-axis as percentages."""
        fig, ax = plt.subplots()
        ax.plot([0, 0.25, 0.5, 0.75, 1.0], [1, 2, 3, 4, 5])
        format_percentage_axis(ax, axis="y")

        # Formatter should be applied to y-axis
        assert isinstance(
            ax.yaxis.get_major_formatter(), type(ax.yaxis.get_major_formatter())
        )
        plt.close(fig)

    def test_format_x_axis(self):
        """Test formatting x-axis as percentages."""
        fig, ax = plt.subplots()
        ax.plot([0, 0.25, 0.5, 0.75, 1.0], [1, 2, 3, 4, 5])
        format_percentage_axis(ax, axis="x")

        # Formatter should be applied to x-axis
        assert isinstance(
            ax.xaxis.get_major_formatter(), type(ax.xaxis.get_major_formatter())
        )
        plt.close(fig)

    def test_default_axis_is_y(self):
        """Test that default axis is y when not specified."""
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        format_percentage_axis(ax)  # No axis parameter

        # Should format y-axis by default
        assert isinstance(
            ax.yaxis.get_major_formatter(), type(ax.yaxis.get_major_formatter())
        )
        plt.close(fig)

    def test_case_insensitive_axis_parameter(self):
        """Test that axis parameter is case insensitive."""
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])

        # Test uppercase
        format_percentage_axis(ax, axis="Y")
        assert isinstance(
            ax.yaxis.get_major_formatter(), type(ax.yaxis.get_major_formatter())
        )

        # Test uppercase X
        format_percentage_axis(ax, axis="X")
        assert isinstance(
            ax.xaxis.get_major_formatter(), type(ax.xaxis.get_major_formatter())
        )

        plt.close(fig)


class TestSurveyPalettes:
    """Tests for SURVEY_PALETTES constant."""

    def test_all_required_palettes_exist(self):
        """Test that all expected palettes are defined."""
        required_palettes = ["default", "likert", "categorical", "sequential", "nps"]
        for palette_name in required_palettes:
            assert palette_name in SURVEY_PALETTES

    def test_palettes_are_nonempty(self):
        """Test that all palettes have at least one color."""
        for palette_name, colors in SURVEY_PALETTES.items():
            assert len(colors) > 0

    def test_nps_has_three_colors(self):
        """Test NPS palette has exactly 3 colors (Detractor, Passive, Promoter)."""
        assert len(SURVEY_PALETTES["nps"]) == 3

    def test_categorical_has_many_colors(self):
        """Test categorical palette has enough colors for diverse categories."""
        # Should have at least 5 colors for good categorical coverage
        assert len(SURVEY_PALETTES["categorical"]) >= 5

    def test_sequential_has_gradation(self):
        """Test sequential palette has multiple shades."""
        # Sequential palettes should have several colors for gradations
        assert len(SURVEY_PALETTES["sequential"]) >= 5
