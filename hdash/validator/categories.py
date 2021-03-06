"""Meta Data Categories."""


class Categories:
    """Meta Data Categories."""

    BIOSPECIMEN = "Biospecimen"
    DEMOGRAPHICS = "Demographics"
    SC_RNA_SEQ_LEVEL_1 = "ScRNA-seqLevel1"
    SC_RNA_SEQ_LEVEL_2 = "ScRNA-seqLevel2"
    SC_RNA_SEQ_LEVEL_3 = "ScRNA-seqLevel3"
    SC_RNA_SEQ_LEVEL_4 = "ScRNA-seqLevel4"
    BULK_WES_LEVEL_1 = "BulkWESLevel1"
    BULK_RNA_SEQ_LEVEL_1 = "BulkRNA-seqLevel1"
    IMAGING_LEVEL_2 = "ImagingLevel2"

    def __init__(self):
        """Construct a new Categories Object."""
        self.category_list = []
        self.category_list.append(Categories.BIOSPECIMEN)
        self.category_list.append(Categories.DEMOGRAPHICS)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_1)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_2)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_3)
        self.category_list.append(Categories.SC_RNA_SEQ_LEVEL_4)
        self.category_list.append(Categories.BULK_WES_LEVEL_1)
        self.category_list.append(Categories.BULK_RNA_SEQ_LEVEL_1)
        self.category_list.append(Categories.IMAGING_LEVEL_2)
        self.abbrev_category_map = {}
        self.abbrev_category_map[Categories.BIOSPECIMEN] = "B"
        self.abbrev_category_map[Categories.DEMOGRAPHICS] = "D"
        self.abbrev_category_map[Categories.SC_RNA_SEQ_LEVEL_1] = "SC1"
        self.abbrev_category_map[Categories.SC_RNA_SEQ_LEVEL_2] = "SC2"
        self.abbrev_category_map[Categories.SC_RNA_SEQ_LEVEL_3] = "SC3"
        self.abbrev_category_map[Categories.SC_RNA_SEQ_LEVEL_4] = "SC4"
        self.abbrev_category_map[Categories.BULK_WES_LEVEL_1] = "WES1"
        self.abbrev_category_map[Categories.BULK_RNA_SEQ_LEVEL_1] = "RNA1"
        self.abbrev_category_map[Categories.IMAGING_LEVEL_2] = "I2"

    def get_primary_category_list(self):
        """Get Primary Category List."""
        return self.category_list
