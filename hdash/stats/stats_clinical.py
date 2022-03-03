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
            num_fields = 0
            num_completed_fields = 0
            participant_id = row[IdUtil.HTAN_PARTICIPANT_ID]
            self.participant_id_set.add(participant_id)

            # Iterate through all the fields
            # and count number of fields, and number of completed fields
            for key, value in row.items():
                if key not in StatsClinical.IGNORED_FIELDS:
                    num_fields += 1
                    value = str(value).lower()
                    if value not in StatsClinical.NA_VALUES:
                        num_completed_fields += 1

            key = participant_id + ":" + clinical_category
            percent_complete = num_completed_fields / num_fields
            self.participant_map[key] = f"{percent_complete:.0%}"
