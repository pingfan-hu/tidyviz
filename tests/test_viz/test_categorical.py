"""Tests for tidyviz.viz.categorical module."""

import pandas as pd
import matplotlib.pyplot as plt
from tidyviz.viz.categorical import (
    plot_single_choice,
    plot_multiple_choice,
    plot_top_n,
    plot_grouped_bars,
)


class TestPlotSingleChoice:
    """Tests for plot_single_choice function."""

    def test_basic_plot(self):
        """Test basic single choice plot creation."""
        df = pd.DataFrame({"method": ["Email", "Phone", "Email", "Text", "Phone"]})
        fig = plot_single_choice(df, "method")

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_sort_by_count(self):
        """Test sorting by count (descending)."""
        df = pd.DataFrame({"choice": ["A"] * 5 + ["B"] * 3 + ["C"] * 7})
        fig = plot_single_choice(df, "choice", sort_by="count")

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        # C should be first (7), then A (5), then B (3)
        assert labels[0] == "C"
        assert labels[1] == "A"
        assert labels[2] == "B"
        plt.close(fig)

    def test_sort_by_alphabetical(self):
        """Test alphabetical sorting."""
        df = pd.DataFrame({"choice": ["C", "A", "B", "C", "A"]})
        fig = plot_single_choice(df, "choice", sort_by="alphabetical")

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert labels == ["A", "B", "C"]
        plt.close(fig)

    def test_sort_by_none(self):
        """Test no sorting (value_counts default order)."""
        df = pd.DataFrame({"choice": ["B", "A", "C", "A"]})
        fig = plot_single_choice(df, "choice", sort_by="none")

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_top_n_filter(self):
        """Test filtering to top N categories."""
        df = pd.DataFrame({"choice": ["A"] * 10 + ["B"] * 5 + ["C"] * 3 + ["D"] * 1})
        fig = plot_single_choice(df, "choice", top_n=2)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert len(labels) == 2
        assert "A" in labels
        assert "B" in labels
        plt.close(fig)

    def test_custom_title(self):
        """Test custom title."""
        df = pd.DataFrame({"method": ["Email", "Phone"]})
        fig = plot_single_choice(df, "method", title="Contact Preferences")

        ax = fig.axes[0]
        assert ax.get_title() == "Contact Preferences"
        plt.close(fig)

    def test_default_title(self):
        """Test default title uses column name."""
        df = pd.DataFrame({"method": ["Email", "Phone"]})
        fig = plot_single_choice(df, "method")

        ax = fig.axes[0]
        assert "method" in ax.get_title()
        plt.close(fig)

    def test_show_percentages_true(self):
        """Test that percentage labels are shown when enabled."""
        df = pd.DataFrame({"choice": ["A", "B", "A"]})
        fig = plot_single_choice(df, "choice", show_percentages=True)

        ax = fig.axes[0]
        # Check that there are text annotations (percentage labels)
        texts = [t for t in ax.texts]
        assert len(texts) > 0
        plt.close(fig)

    def test_show_percentages_false(self):
        """Test that percentage labels are hidden when disabled."""
        df = pd.DataFrame({"choice": ["A", "B", "A"]})
        fig = plot_single_choice(df, "choice", show_percentages=False)

        ax = fig.axes[0]
        # Check that there are no text annotations
        texts = [t for t in ax.texts]
        assert len(texts) == 0
        plt.close(fig)

    def test_custom_figsize(self):
        """Test custom figure size."""
        df = pd.DataFrame({"choice": ["A", "B"]})
        fig = plot_single_choice(df, "choice", figsize=(8, 4))

        assert fig.get_size_inches()[0] == 8
        assert fig.get_size_inches()[1] == 4
        plt.close(fig)

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame({"choice": []})
        fig = plot_single_choice(df, "choice")

        ax = fig.axes[0]
        assert len(ax.patches) == 0  # No bars
        plt.close(fig)

    def test_single_value(self):
        """Test with only one category."""
        df = pd.DataFrame({"choice": ["A", "A", "A"]})
        fig = plot_single_choice(df, "choice")

        ax = fig.axes[0]
        assert len(ax.patches) == 1  # One bar
        plt.close(fig)

    def test_with_nan_values(self):
        """Test handling of NaN values."""
        df = pd.DataFrame({"choice": ["A", "B", None, "A", pd.NA]})
        fig = plot_single_choice(df, "choice")

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlotMultipleChoice:
    """Tests for plot_multiple_choice function."""

    def test_basic_plot(self):
        """Test basic multiple choice plot."""
        df = pd.DataFrame(
            {
                "colors_Blue": [1, 0, 1, 1],
                "colors_Red": [0, 1, 1, 0],
                "colors_Green": [1, 1, 0, 0],
            }
        )
        columns = ["colors_Blue", "colors_Red", "colors_Green"]
        fig = plot_multiple_choice(df, columns)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_option_name_extraction(self):
        """Test that option names are correctly extracted from column names."""
        df = pd.DataFrame(
            {"colors_Blue": [1, 0], "colors_Red": [0, 1], "colors_Green": [1, 0]}
        )
        columns = ["colors_Blue", "colors_Red", "colors_Green"]
        fig = plot_multiple_choice(df, columns)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert "Blue" in labels
        assert "Red" in labels
        assert "Green" in labels
        plt.close(fig)

    def test_columns_without_prefix(self):
        """Test columns without underscore prefix."""
        df = pd.DataFrame({"Blue": [1, 0], "Red": [0, 1], "Green": [1, 0]})
        columns = ["Blue", "Red", "Green"]
        fig = plot_multiple_choice(df, columns)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert "Blue" in labels
        plt.close(fig)

    def test_sort_by_count(self):
        """Test sorting by selection count."""
        df = pd.DataFrame(
            {
                "opt_A": [1, 1, 1, 1, 1],  # 5 selections
                "opt_B": [1, 1, 1, 0, 0],  # 3 selections
                "opt_C": [1, 0, 0, 0, 0],  # 1 selection
            }
        )
        fig = plot_multiple_choice(df, ["opt_A", "opt_B", "opt_C"], sort_by="count")

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert labels[0] == "A"  # Most selections
        assert labels[1] == "B"
        assert labels[2] == "C"  # Fewest selections
        plt.close(fig)

    def test_sort_by_alphabetical(self):
        """Test alphabetical sorting."""
        df = pd.DataFrame({"opt_C": [1, 0], "opt_A": [0, 1], "opt_B": [1, 0]})
        fig = plot_multiple_choice(
            df, ["opt_C", "opt_A", "opt_B"], sort_by="alphabetical"
        )

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert labels == ["A", "B", "C"]
        plt.close(fig)

    def test_top_n_filter(self):
        """Test filtering to top N options."""
        df = pd.DataFrame(
            {
                "opt_A": [1, 1, 1, 1],  # 4 selections
                "opt_B": [1, 1, 1, 0],  # 3 selections
                "opt_C": [1, 1, 0, 0],  # 2 selections
                "opt_D": [1, 0, 0, 0],  # 1 selection
            }
        )
        fig = plot_multiple_choice(df, ["opt_A", "opt_B", "opt_C", "opt_D"], top_n=2)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert len(labels) == 2
        plt.close(fig)

    def test_show_percentages(self):
        """Test percentage display based on total respondents."""
        df = pd.DataFrame(
            {
                "colors_Blue": [1, 0, 1, 1],  # 3/4 = 75%
                "colors_Red": [0, 1, 0, 0],  # 1/4 = 25%
            }
        )
        fig = plot_multiple_choice(df, ["colors_Blue", "colors_Red"])

        ax = fig.axes[0]
        # Check that percentage labels exist
        texts = [t for t in ax.texts]
        assert len(texts) > 0
        plt.close(fig)

    def test_custom_title(self):
        """Test custom title."""
        df = pd.DataFrame({"opt_A": [1, 0], "opt_B": [0, 1]})
        fig = plot_multiple_choice(df, ["opt_A", "opt_B"], title="Favorite Colors")

        ax = fig.axes[0]
        assert ax.get_title() == "Favorite Colors"
        plt.close(fig)

    def test_respondent_count_note(self):
        """Test that note about respondent count is included."""
        df = pd.DataFrame({"opt_A": [1, 0, 1], "opt_B": [0, 1, 0]})
        fig = plot_multiple_choice(df, ["opt_A", "opt_B"])

        # Check that figure text exists (the note)
        fig_texts = fig.texts
        assert len(fig_texts) > 0
        # Check that it mentions respondents
        note_text = " ".join([t.get_text() for t in fig_texts])
        assert "respondents" in note_text.lower()
        plt.close(fig)

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({"opt_A": [], "opt_B": []})
        fig = plot_multiple_choice(df, ["opt_A", "opt_B"])

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_all_zeros(self):
        """Test when no selections are made."""
        df = pd.DataFrame({"opt_A": [0, 0, 0], "opt_B": [0, 0, 0]})
        fig = plot_multiple_choice(df, ["opt_A", "opt_B"])

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlotTopN:
    """Tests for plot_top_n function."""

    def test_basic_top_n(self):
        """Test basic top N plotting."""
        df = pd.DataFrame({"product": ["A"] * 10 + ["B"] * 5 + ["C"] * 3 + ["D"] * 1})
        fig = plot_top_n(df, "product", n=2)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert len(labels) == 2
        assert "A" in labels
        assert "B" in labels
        plt.close(fig)

    def test_default_n_value(self):
        """Test default n=10."""
        df = pd.DataFrame({"item": list("ABCDEFGHIJKLMNO")})
        fig = plot_top_n(df, "item")

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert len(labels) == 10
        plt.close(fig)

    def test_custom_title(self):
        """Test that custom title is used."""
        df = pd.DataFrame({"item": ["A", "B", "C"]})
        fig = plot_top_n(df, "item", n=2, title="Custom Title")

        ax = fig.axes[0]
        assert ax.get_title() == "Custom Title"
        plt.close(fig)

    def test_default_title_includes_n(self):
        """Test that default title mentions N."""
        df = pd.DataFrame({"item": ["A", "B", "C"]})
        fig = plot_top_n(df, "item", n=5)

        ax = fig.axes[0]
        assert "5" in ax.get_title()
        assert "item" in ax.get_title()
        plt.close(fig)

    def test_n_larger_than_categories(self):
        """Test when n is larger than number of categories."""
        df = pd.DataFrame({"choice": ["A", "B"]})
        fig = plot_top_n(df, "choice", n=10)

        ax = fig.axes[0]
        labels = [label.get_text() for label in ax.get_xticklabels()]
        assert len(labels) == 2  # Only 2 categories exist
        plt.close(fig)


class TestPlotGroupedBars:
    """Tests for plot_grouped_bars function."""

    def test_basic_grouped_bars(self):
        """Test basic grouped bar chart."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No", "Yes", "No"],
                "count": [10, 5, 8, 12],
                "gender": ["Male", "Male", "Female", "Female"],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "gender")

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_title(self):
        """Test custom title."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No"],
                "count": [10, 5],
                "gender": ["Male", "Male"],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "gender", title="Custom Title")

        ax = fig.axes[0]
        assert ax.get_title() == "Custom Title"
        plt.close(fig)

    def test_default_title(self):
        """Test default title format."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No"],
                "count": [10, 5],
                "age_group": ["Young", "Young"],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "age_group")

        ax = fig.axes[0]
        assert "response" in ax.get_title()
        assert "age_group" in ax.get_title()
        plt.close(fig)

    def test_axis_labels(self):
        """Test that axis labels are properly formatted."""
        df = pd.DataFrame(
            {
                "question_type": ["A", "B"],
                "total_count": [5, 10],
                "demographic": ["X", "X"],
            }
        )
        fig = plot_grouped_bars(df, "question_type", "total_count", "demographic")

        ax = fig.axes[0]
        xlabel = ax.get_xlabel().lower()
        ylabel = ax.get_ylabel().lower()

        assert "question" in xlabel and "type" in xlabel
        assert "total" in ylabel and "count" in ylabel
        plt.close(fig)

    def test_legend_present(self):
        """Test that legend is created for groups."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No", "Yes", "No"],
                "count": [10, 5, 8, 12],
                "gender": ["Male", "Male", "Female", "Female"],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "gender")

        ax = fig.axes[0]
        legend = ax.get_legend()
        assert legend is not None
        plt.close(fig)

    def test_custom_figsize(self):
        """Test custom figure size."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No"],
                "count": [10, 5],
                "gender": ["Male", "Male"],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "gender", figsize=(8, 4))

        assert fig.get_size_inches()[0] == 8
        assert fig.get_size_inches()[1] == 4
        plt.close(fig)

    def test_multiple_groups(self):
        """Test with multiple demographic groups."""
        df = pd.DataFrame(
            {
                "response": ["Yes", "No", "Maybe"] * 3,
                "count": [10, 5, 3, 8, 12, 4, 6, 7, 2],
                "age": [
                    "Young",
                    "Young",
                    "Young",
                    "Middle",
                    "Middle",
                    "Middle",
                    "Old",
                    "Old",
                    "Old",
                ],
            }
        )
        fig = plot_grouped_bars(df, "response", "count", "age")

        assert isinstance(fig, plt.Figure)
        ax = fig.axes[0]
        # Should have bars for each age group
        legend = ax.get_legend()
        assert len(legend.get_texts()) == 3  # Young, Middle, Old
        plt.close(fig)
