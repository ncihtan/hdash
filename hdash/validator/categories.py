"""Meta Data Categories."""


class Categories:
    """Meta Data Categories."""

    OTHER_ASSAY = "OtherAssay"
    BIOSPECIMEN = "Biospecimen"
    DEMOGRAPHICS = "Demographics"
    SC_RNA_SEQ_LEVEL_1 = "ScRNA-seqLevel1"
    SC_RNA_SEQ_LEVEL_2 = "ScRNA-seqLevel2"
    SC_RNA_SEQ_LEVEL_3 = "ScRNA-seqLevel3"
    SC_RNA_SEQ_LEVEL_4 = "ScRNA-seqLevel4"
    BULK_WES_LEVEL_1 = "BulkWESLevel1"
    BULK_WES_LEVEL_2 = "BulkWESLevel2"
    BULK_WES_LEVEL_3 = "BulkWESLevel3"
    BULK_WES_LEVEL_4 = "BulkWESLevel4"
    BULK_RNA_SEQ_LEVEL_1 = "BulkRNA-seqLevel1"
    BULK_RNA_SEQ_LEVEL_2 = "BulkRNA-seqLevel2"
    BULK_RNA_SEQ_LEVEL_3 = "BulkRNA-seqLevel3"
    BULK_RNA_SEQ_LEVEL_4 = "BulkRNA-seqLevel4"
    SC_ATAC_SEQ_LEVEL_1 = "ScATAC-seqLevel1"
    SC_ATAC_SEQ_LEVEL_2 = "ScATAC-seqLevel2"
    SC_ATAC_SEQ_LEVEL_3 = "ScATAC-seqLevel3"
    SC_ATAC_SEQ_LEVEL_4 = "ScATAC-seqLevel4"
    IMAGING_LEVEL_1 = "ImagingLevel1"
    IMAGING_LEVEL_2 = "ImagingLevel2"
    IMAGING_LEVEL_3 = "ImagingLevel3"
    IMAGING_LEVEL_4 = "ImagingLevel3"

    def __init__(self):
        """Construct a new Categories Object."""
        self.category_list = [
            Categories.OTHER_ASSAY,
            Categories.BIOSPECIMEN,
            Categories.DEMOGRAPHICS,
            Categories.SC_RNA_SEQ_LEVEL_1,
            Categories.SC_RNA_SEQ_LEVEL_2,
            Categories.SC_RNA_SEQ_LEVEL_3,
            Categories.SC_RNA_SEQ_LEVEL_4,
            Categories.BULK_WES_LEVEL_1,
            Categories.BULK_WES_LEVEL_2,
            Categories.BULK_WES_LEVEL_3,
            Categories.BULK_WES_LEVEL_4,
            Categories.BULK_RNA_SEQ_LEVEL_1,
            Categories.BULK_RNA_SEQ_LEVEL_2,
            Categories.BULK_RNA_SEQ_LEVEL_3,
            Categories.BULK_RNA_SEQ_LEVEL_4,
            Categories.IMAGING_LEVEL_1,
            Categories.IMAGING_LEVEL_2,
            Categories.IMAGING_LEVEL_3,
            Categories.IMAGING_LEVEL_4,
            Categories.SC_ATAC_SEQ_LEVEL_1,
            Categories.SC_ATAC_SEQ_LEVEL_2,
            Categories.SC_ATAC_SEQ_LEVEL_3,
            Categories.SC_ATAC_SEQ_LEVEL_4,
        ]
        self.abbrev_category_map = {
            Categories.OTHER_ASSAY: "O",
            Categories.BIOSPECIMEN: "B",
            Categories.DEMOGRAPHICS: "D",
            Categories.SC_RNA_SEQ_LEVEL_1: "SC1",
            Categories.SC_RNA_SEQ_LEVEL_2: "SC2",
            Categories.SC_RNA_SEQ_LEVEL_3: "SC3",
            Categories.SC_RNA_SEQ_LEVEL_4: "SC4",
            Categories.BULK_WES_LEVEL_1: "WES1",
            Categories.BULK_WES_LEVEL_2: "WES2",
            Categories.BULK_WES_LEVEL_3: "WES3",
            Categories.BULK_WES_LEVEL_4: "WES4",
            Categories.BULK_RNA_SEQ_LEVEL_1: "RNA1",
            Categories.BULK_RNA_SEQ_LEVEL_2: "RNA2",
            Categories.BULK_RNA_SEQ_LEVEL_3: "RNA3",
            Categories.BULK_RNA_SEQ_LEVEL_4: "RNA4",
            Categories.IMAGING_LEVEL_1: "I1",
            Categories.IMAGING_LEVEL_2: "I2",
            Categories.IMAGING_LEVEL_3: "I3",
            Categories.IMAGING_LEVEL_4: "I4",
            Categories.SC_ATAC_SEQ_LEVEL_1: "SCATAC1",
            Categories.SC_ATAC_SEQ_LEVEL_2: "SCATAC2",
            Categories.SC_ATAC_SEQ_LEVEL_3: "SCATAC3",
            Categories.SC_ATAC_SEQ_LEVEL_4: "SCATAC4",
        }

    def get_primary_category_list(self):
        """Get Primary Category List."""
        return self.category_list
