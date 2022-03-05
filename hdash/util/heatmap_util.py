"""HeatMap Utility."""
import pandas as pd
from hdash.util.heatmap import HeatMap
from hdash.validator.categories import Categories
import seaborn as sns
import matplotlib.pyplot as plt


class HeatMapUtil:
    """HeatMap Utility Class."""
    CLINICAL_TIER_1_2 = "clinical_tier1_2"
    CLINICAL_TIER_3 = "clinical_tier3"
    SINGLE_CELL = "single_cell"
    BULK = "bulk"
    IMAGE_OTHER = "image_other"

    CAPTION = "Values indicate fraction of meta-data fields that have data."

    def __init__(self, project):
        """Initialize the specified HTAN Project."""
        self.project = project
        self.heatmaps = []
        self.categories = Categories()

        # Heatmap 1
        self.__build_clinical_heatmap(
            HeatMapUtil.CLINICAL_TIER_1_2,
            self.categories.clinical_tier1_2_list,
            "Clinical Data Matrix: Tiers 1 and 2",
            "#fce1e9"
        )

        # Heatmap 2
        self.__build_clinical_heatmap(
            HeatMapUtil.CLINICAL_TIER_3,
            self.categories.clinical_tier3_list,
            "Clinical Data Matrix: Tier 3",
            "#fce1e9",
        )

        # Heatmap 3
        self.single_cell_assay_list = [self.categories.BIOSPECIMEN]
        self.single_cell_assay_list.extend(self.categories.sc_rna_list)
        self.single_cell_assay_list.extend(self.categories.sc_atac_list)
        self.__build_assay_heatmap(
            HeatMapUtil.SINGLE_CELL,
            self.single_cell_assay_list,
            "Assay Matrix: Single Cell Data",
            "#e3eeff",
        )

        # Heatmap 4
        self.bulk_assay_list = [self.categories.BIOSPECIMEN]
        self.bulk_assay_list.extend(self.categories.bulk_rna_list)
        self.bulk_assay_list.extend(self.categories.bulk_wes_list)
        self.__build_assay_heatmap(
            HeatMapUtil.BULK,
            self.bulk_assay_list,
            "Assay Matrix: Bulk Data",
            "#e3eeff",
        )

        # Heatmap 5
        self.image_assay_list = [self.categories.BIOSPECIMEN]
        self.image_assay_list.extend(self.categories.image_list)
        self.image_assay_list.extend(self.categories.other_assay_list)
        self.__build_assay_heatmap(
            HeatMapUtil.IMAGE_OTHER,
            self.image_assay_list,
            "Assay Matrix: Imaging and Other",
            "#e3eeff",
        )
        self.__create_seaborn_heatmaps()

    def __build_clinical_heatmap(self, heatmap_type, category_list, label, bg_color):
        """Build Clinical Data Heatmap."""
        headers = ["ParticipantID"]
        data = []
        for category in category_list:
            if "Tier3" in category:
                shorter = category[:8] + ".."
                headers.append(shorter)
            else:
                headers.append(category)
        for participant_id in self.project.participant_id_set:
            current_row = [participant_id]
            for category in category_list:
                key = participant_id + ":" + category
                current_row.append(self.project.df_stats_map.get(key, 0))
            data.append(current_row)
        self.__create_heatmap(heatmap_type, data, headers, label, bg_color)

    def __build_assay_heatmap(self, heatmap_type, category_list, label, bg_color):
        """Build Assay Data Heatmap."""
        participant_2_bipspecimens = self.project.participant_2_biopsecimens
        df_stats_map = self.project.df_stats_map
        headers = ["ParticipantID", "BiospecimenID"]
        data = []
        for category in category_list:
            headers.append(category)
        for participant_id in self.project.participant_id_set:
            b_ids = participant_2_bipspecimens.get(participant_id, [])
            for biospecimen_id in b_ids:
                current_row = [participant_id, biospecimen_id]
                for category in category_list:
                    key = biospecimen_id + ":" + category
                    current_row.append(df_stats_map.get(key, 0))
                data.append(current_row)
        self.__create_heatmap(heatmap_type, data, headers, label, bg_color)

    def __create_heatmap(self, heatmap_type, data, headers, label, bg_color):
        """Create Heatmap Object."""
        df = pd.DataFrame(data, columns=headers)
        df_html = df.to_html(
            index=False, justify="left", classes="table table-striped table-sm"
        )
        caption = HeatMapUtil.CAPTION
        heatmap_id = self.project.atlas_id + "_" + heatmap_type
        heatmap = HeatMap(heatmap_id, label, caption, data, df, df_html, bg_color)
        self.heatmaps.append(heatmap)

    def __create_seaborn_heatmaps(self):
        """Create Seaborn HeatMaps."""
        for heatmap in self.heatmaps:
            df = heatmap.df
            columns = list(df.columns)
            if "BiospecimenID" in columns:
                df.index = df["BiospecimenID"]
                df = df.drop(["ParticipantID", "BiospecimenID"], axis=1)
            else:
                df.index = df["ParticipantID"]
                df = df.drop(["ParticipantID"], axis=1)
            ax = sns.heatmap(df, vmin=0, vmax=1, annot=True, linewidths=0.5, cmap="Blues")
            ax.xaxis.tick_top()
            plt.xticks(rotation=90)
            ax.set_ylabel("")
            ax.figure.tight_layout()
            fig_name = "deploy/" + heatmap.id + ".png"
            plt.savefig(fig_name)
            plt.figure()
