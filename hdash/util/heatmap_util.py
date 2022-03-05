"""HeatMap Utility."""
import pandas as pd
from hdash.util.heatmap import HeatMap
from hdash.validator.categories import Categories


class HeatMapUtil:
    """HeatMap Utility Class."""

    CAPTION = "Values indicate fraction of meta-data fields that have data."

    def __init__(self, project):
        """Initialize the specified HTAN Project."""
        self.project = project
        self.heatmaps = []
        self.categories = Categories()

        # Heatmap 1
        self.__build_clinical_heatmap(
            self.categories.clinical_tier1_2_list,
            "Clinical Data Matrix: Tiers 1 and 2",
            "#fce1e9",
        )

        # Heatmap 2
        self.__build_clinical_heatmap(
            self.categories.clinical_tier3_list,
            "Clinical Data Matrix: Tier 3",
            "#fce1e9",
        )

        # Heatmap 3
        self.single_cell_assay_list = [self.categories.BIOSPECIMEN]
        self.single_cell_assay_list.extend(self.categories.sc_rna_list)
        self.single_cell_assay_list.extend(self.categories.sc_atac_list)
        self.__build_assay_heatmap(
            self.single_cell_assay_list,
            "Assay Matrix: Single Cell Data",
            "#e3eeff",
        )

        # Heatmap 4
        self.bulk_assay_list = [self.categories.BIOSPECIMEN]
        self.bulk_assay_list.extend(self.categories.bulk_rna_list)
        self.bulk_assay_list.extend(self.categories.bulk_wes_list)
        self.__build_assay_heatmap(
            self.bulk_assay_list,
            "Assay Matrix: Bulk Data",
            "#e3eeff",
        )

        # Heatmap 5
        self.image_assay_list = [self.categories.BIOSPECIMEN]
        self.image_assay_list.extend(self.categories.image_list)
        self.image_assay_list.extend(self.categories.other_assay_list)
        self.__build_assay_heatmap(
            self.image_assay_list,
            "Assay Matrix: Imaging and Other",
            "#e3eeff",
        )

    def __build_clinical_heatmap(self, category_list, label, bg_color):
        """Build Clinical Data Heatmap."""
        headers = ["Participant"]
        data = []
        for category in category_list:
            headers.append(category)
        for participant_id in self.project.participant_id_set:
            current_row = [participant_id]
            for category in category_list:
                key = participant_id + ":" + category
                current_row.append(self.project.df_stats_map.get(key, "NA"))
            data.append(current_row)
        self.__create_heatmap(data, headers, label, bg_color)

    def __build_assay_heatmap(self, category_list, label, bg_color):
        """Build Assay Data Heatmap."""
        participant_2_bipspecimens = self.project.participant_2_biopsecimens
        df_stats_map = self.project.df_stats_map
        headers = ["Participant", "Biospecimen"]
        data = []
        for category in category_list:
            headers.append(category)
        for participant_id in self.project.participant_id_set:
            b_ids = participant_2_bipspecimens.get(participant_id, [])
            for biospecimen_id in b_ids:
                current_row = [participant_id, biospecimen_id]
                for category in category_list:
                    key = biospecimen_id + ":" + category
                    current_row.append(df_stats_map.get(key, "NA"))
                data.append(current_row)
        self.__create_heatmap(data, headers, label, bg_color)

    def __create_heatmap(self, data, headers, label, bg_color):
        """Create Heatmap Object."""
        df = pd.DataFrame(data, columns=headers)
        df_html = df.to_html(classes="table table-stripped")
        caption = HeatMapUtil.CAPTION
        heatmap = HeatMap(label, caption, data, df, df_html, bg_color)
        self.heatmaps.append(heatmap)
