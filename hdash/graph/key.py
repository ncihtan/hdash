"""Key Util."""


class KeyUtil:
    """Key Utilities Class."""

    @staticmethod
    def create_key(primary_id, category):
        """Create key of primary_id + category."""
        return f"{primary_id}__{category}"
