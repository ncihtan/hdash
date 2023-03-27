"""HeatMap Class."""


class HeatMap:
    """HeatMap Class."""

    def __init__(
        self, heatmap_id, label, caption, data, df, df_html, counts_html, bg_color
    ):
        """Initialize HeatMap Object."""
        self.id = heatmap_id
        self.label = label
        self.caption = caption
        self.data = data
        self.df = df
        self.df_html = df_html
        self.counts_html = counts_html
        self.bg_color = bg_color

    def __repr__(self):
        """Return summary of object."""
        return f"Heatmap:: {self.label}."
