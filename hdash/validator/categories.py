"""HTAN Data Categories."""


class Categories:
    """HTAN Data Categories."""

    # Synape Fields
    COMPONENT_COL = "Component"
    ENTITY_ID_COL = "entityId"

    # Biospecimen Categories
    BIOSPECIMEN = "Biospecimen"

    # Assay Categories
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
    OTHER_ASSAY = "OtherAssay"

    # Clinical Data Categories
    DEMOGRAPHICS = "Demographics"
    EXPOSURE = "Exposure"
    FAMILY_HISTORY = "FamilyHistory"
    FOLLOW_UP = "FollowUp"
    DIAGNOSIS = "Diagnosis"
    THERAPY = "Therapy"
    MOLECULAR_TEST = "MolecularTest"
    CLINICAL_TIER2 = "ClinicalDataTier2"
    ALL_TIER3 = "AcuteLymphoblasticLeukemiaTier3"
    BRAIN_TIER3 = "BrainCancerTier3"
    BREAST_TIER3 = "BreastCancerTier3"
    CRC_TIER3 = "ColorectalCancerTier3"
    LUNG_TIER3 = "LungCancerTier3"
    MELANOMA_TIER3 = "MelanomaTier3"
    OVARIAN_TIER3 = "OvarianCancerTier3"
    PANCREATIC_TIER3 = "PancreaticCancerTier3"
    PROSTATE_TIER3 = "ProstateCancerTier3"
    SARCOMA_TIER3 = "SarcomaTier3"

    def __init__(self):
        """Construct all new category lists."""
        self.biospecimen_list = [Categories.BIOSPECIMEN]

        self.sc_rna_list = [
            Categories.SC_RNA_SEQ_LEVEL_1,
            Categories.SC_RNA_SEQ_LEVEL_2,
            Categories.SC_RNA_SEQ_LEVEL_3,
            Categories.SC_RNA_SEQ_LEVEL_4,
        ]

        self.bulk_wes_list = [
            Categories.BULK_WES_LEVEL_1,
            Categories.BULK_WES_LEVEL_2,
            Categories.BULK_WES_LEVEL_3,
            Categories.BULK_WES_LEVEL_4,
        ]

        self.bulk_rna_list = [
            Categories.BULK_RNA_SEQ_LEVEL_1,
            Categories.BULK_RNA_SEQ_LEVEL_2,
            Categories.BULK_RNA_SEQ_LEVEL_3,
            Categories.BULK_RNA_SEQ_LEVEL_4,
        ]

        self.image_list = [
            Categories.IMAGING_LEVEL_1,
            Categories.IMAGING_LEVEL_2,
            Categories.IMAGING_LEVEL_3,
            Categories.IMAGING_LEVEL_4,
        ]

        self.sc_atac_list = [
            Categories.SC_ATAC_SEQ_LEVEL_1,
            Categories.SC_ATAC_SEQ_LEVEL_2,
            Categories.SC_ATAC_SEQ_LEVEL_3,
            Categories.SC_ATAC_SEQ_LEVEL_4,
        ]

        self.other_assay_list = [Categories.OTHER_ASSAY]

        self.clinical_tier1_2_list = [
            Categories.DEMOGRAPHICS,
            Categories.EXPOSURE,
            Categories.FAMILY_HISTORY,
            Categories.FOLLOW_UP,
            Categories.DIAGNOSIS,
            Categories.THERAPY,
            Categories.MOLECULAR_TEST,
            Categories.CLINICAL_TIER2,
        ]

        self.clinical_tier3_list = [
            Categories.ALL_TIER3,
            Categories.BRAIN_TIER3,
            Categories.BREAST_TIER3,
            Categories.CRC_TIER3,
            Categories.LUNG_TIER3,
            Categories.MELANOMA_TIER3,
            Categories.OVARIAN_TIER3,
            Categories.PANCREATIC_TIER3,
            Categories.PROSTATE_TIER3,
            Categories.SARCOMA_TIER3,
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

        self.all_assays = []
        self.all_assays.extend(self.sc_rna_list)
        self.all_assays.extend(self.sc_atac_list)
        self.all_assays.extend(self.bulk_wes_list)
        self.all_assays.extend(self.bulk_rna_list)
        self.all_assays.extend(self.image_list)
        self.all_assays.extend(self.other_assay_list)

        self.all_clinical = []
        self.all_clinical.extend(self.clinical_tier1_2_list)
        self.all_clinical.extend(self.clinical_tier3_list)

        self.all_categories = []
        self.all_categories.extend(self.all_clinical)
        self.all_categories.extend(self.biospecimen_list)
        self.all_categories.extend(self.all_assays)
