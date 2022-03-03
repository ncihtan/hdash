"""Summary Clinical Data Stats."""
from hdash.validator.htan_validator import HtanValidator
from hdash.validator.id_util import IdUtil
from hdash.validator.categories import Categories
from natsort import natsorted


class StatsClinical:
    """Summary Clinical Data Stats."""

    NA_VALUES = ["na", "nan", "unknown", "not applicable"]
    IGNORED_FIELDS = [
        IdUtil.HTAN_PARTICIPANT_ID,
        Categories.COMPONENT_COL,
        Categories.ENTITY_ID_COL,
    ]

    def __init__(self, atlas_id, meta_map):
        """Init with Atlas ID and Map of all DataFrames."""
        self.atlas_id = atlas_id
        self.meta_map = meta_map
        self.participant_id_set = set()
        self.participant_map = {}
        self.categories = Categories()
        self.participant_num_fields = {}
        self.participant_num_completed_fields = {}
        self.__walk_clinical_data_categories()
        self.participant_id_set = natsorted(self.participant_id_set)

    def __walk_clinical_data_categories(self):
        """Walk through all the clinical meta data categories."""
        for clinical_category in self.categories.all_clinical:
            if clinical_category in self.meta_map:
                # We can have multiple clinical data files of each type
                df_list = self.meta_map.get(clinical_category, [])
                for df in df_list:
                    self.inspect_clinical_df(clinical_category, df)

    def inspect_clinical_df(self, clinical_category, df):
        """Inspect Clinical Data Data Frame."""
        for index, row in df.iterrows():
            participant_id = row[IdUtil.HTAN_PARTICIPANT_ID]
            self.participant_id_set.add(participant_id)

            # Iterate through all the fields
            # and count number of fields, and number of completed fields
            key = participant_id + ":" + clinical_category
            for field_name, field_value in row.items():
                if field_name not in StatsClinical.IGNORED_FIELDS:
                    self.__increment_num_fields(key)
                    field_value = str(field_value).lower()
                    if field_value not in StatsClinical.NA_VALUES:
                        self.__increment_num_completed_fields(key)

            percent_complete = self.__calculate_percent_complete_fields(key)
            self.participant_map[key] = f"{percent_complete:.0%}"

    def __increment_num_fields(self, key):
        if key in self.participant_num_fields:
            self.participant_num_fields[key] = self.participant_num_fields[key] + 1
        else:
            self.participant_num_fields[key] = 1

    def __increment_num_completed_fields(self, key):
        if key in self.participant_num_completed_fields:
            self.participant_num_completed_fields[key] = (
                self.participant_num_completed_fields[key] + 1
            )
        else:
            self.participant_num_completed_fields[key] = 1

    def __calculate_percent_complete_fields(self, key):
        num_complete_fields = self.participant_num_completed_fields.get(key, 0)
        num_fields = self.participant_num_fields.get(key, 1)
        return num_complete_fields / num_fields
