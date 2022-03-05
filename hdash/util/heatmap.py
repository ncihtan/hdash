"""HeatMap Class."""


class HeatMap:
    """HeatMap Class."""

    def __init__(self, label, caption, data, df, df_html, bg_color):
        """Initialize HeatMap Object."""
        self.label = label
        self.caption = caption
        self.data = data
        self.df = df
        self.df_html = df_html
        self.bg_color = bg_color

    def __repr__(self):
        """Return summary of object."""
        return f"Heatmap:: {self.label}."
