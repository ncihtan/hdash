"""Summary Stats Across all Data Categories."""
from hdash.validator.id_util import IdUtil
from hdash.validator.categories import Categories
from natsort import natsorted


class StatsSummary:
    """Summary Stats across all data categories."""

    NA_VALUES = ["na", "nan", "unknown", "not applicable"]
    IGNORED_FIELDS = [
        IdUtil.HTAN_PARTICIPANT_ID,
        IdUtil.HTAN_PARENT_ID,
        IdUtil.HTAN_BIOSPECIMEN_ID,
        Categories.COMPONENT_COL,
        Categories.ENTITY_ID_COL,
    ]

    def __init__(self, atlas_id, meta_map, assays_2_biospecimens):
        """Init with Atlas ID and Map of all DataFrames."""
        self.atlas_id = atlas_id
        self.meta_map = meta_map
        self.assays_2_biospecimens = assays_2_biospecimens
        self.participant_id_set = set()
        self.df_stats_map = {}
        self.categories = Categories()
        self.num_fields = {}
        self.num_completed_fields = {}
        self.id_util = IdUtil()
        self.__walk_clinical_data_categories()
        self.participant_id_set = natsorted(self.participant_id_set)
        self.__walk_category(self.categories.BIOSPECIMEN)
        self.__walk_assay_categories()

    def __walk_clinical_data_categories(self):
        """Walk through all the clinical categories."""
        for clinical_category in self.categories.all_clinical:
            self.__walk_category(clinical_category)

    def __walk_assay_categories(self):
        """Walk through all the assay categories."""
        for clinical_category in self.categories.all_assays:
            self.__walk_category(clinical_category)

    def __walk_category(self, category):
        """Walk through specified data category."""
        df_list = self.meta_map.get(category, [])
        for df in df_list:
            self.inspect_df(category, df)

    def inspect_df(self, category, df):
        """Inspect Data Frame for completed/missing fields."""
        for index, row in df.iterrows():
            primary_id_column = self.id_util.get_primary_id_column(category)
            primary_id = row[primary_id_column]

            # Inspect Primary ID:  If this is an assay type, we need
            # to link to the root biopsecimen.
            if primary_id_column == IdUtil.HTAN_PARTICIPANT_ID:
                self.participant_id_set.add(primary_id)
            elif primary_id_column == IdUtil.HTAN_DATA_FILE_ID:
                primary_id = self.assays_2_biospecimens.get(primary_id, "NA")

            # Iterate through all the fields
            # and count number of fields, and number of completed fields
            key = primary_id + ":" + category
            for field_name, field_value in row.items():
                if field_name not in StatsSummary.IGNORED_FIELDS:
                    self.__increment_num_fields(key)
                    field_value = str(field_value).lower()
                    if field_value not in StatsSummary.NA_VALUES:
                        self.__increment_num_completed_fields(key)

            percent_complete = self.__calculate_percent_complete_fields(key)
            # self.df_stats_map[key] = f"{percent_complete:.0%}"
            self.df_stats_map[key] = percent_complete

    def __increment_num_fields(self, key):
        if key in self.num_fields:
            self.num_fields[key] = self.num_fields[key] + 1
        else:
            self.num_fields[key] = 1

    def __increment_num_completed_fields(self, key):
        if key in self.num_completed_fields:
            self.num_completed_fields[key] = self.num_completed_fields[key] + 1
        else:
            self.num_completed_fields[key] = 1

    def __calculate_percent_complete_fields(self, key):
        num_complete_fields = self.num_completed_fields.get(key, 0)
        num_fields = self.num_fields.get(key, 1)
        return num_complete_fields / num_fields
