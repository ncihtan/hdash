"""Meta Data Categories."""


class Categories:
    """Meta Data Categories."""

    BIOSPECIMEN = "Biospecimen"
    DEMOGRAPHICS = "Demographics"
    SC_RNA_SEQ_LEVEL_1 = "ScRNA-seqLevel1"
    SC_RNA_SEQ_LEVEL_2 = "ScRNA-seqLevel2"
    SC_RNA_SEQ_LEVEL_3 = "ScRNA-seqLevel3"
    SC_RNA_SEQ_LEVEL_4 = "ScRNA-seqLevel4"

    def __init__(self):
        """Construct a new Categories Object."""
        self.category_list = []
        self.category_list.append(Categories.BIOSPECIMEN)
        self.category_list.append(Categories.DEMOGRAPHICS)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_1)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_2)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_3)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_4)

    def get_primary_category_list(self):
        """Get Primary Category List."""
        return self.category_list
