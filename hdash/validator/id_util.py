"""ID Utility Class."""
from hdash.validator.categories import Categories


class IdUtil:
    """ID Utility Class."""

    HTAN_PARTICIPANT_ID = "HTAN Participant ID"

    def get_primary_id_column(self, category):
        """Get Primary ID Column for the specified category of data."""
        if category == Categories.BIOSPECIMEN:
            return "HTAN Biospecimen ID"
        elif category == Categories.DEMOGRAPHICS:
            return IdUtil.HTAN_PARTICIPANT_ID
        else:
            return "HTAN Data File ID"

    def get_parent_id_column(self, category):
        """Get Parent ID Column for the specified category of data."""
        if category == Categories.BIOSPECIMEN:
            return "HTAN Parent ID"
        elif category == Categories.DEMOGRAPHICS:
            return None
        elif category == Categories.SC_RNA_SEQ_LEVEL_1:
            return "HTAN Parent Biospecimen ID"
        else:
            return "HTAN Parent Data File ID"
