"""Summary Stats across all metadata files."""
from hdash.util.id_util import IdUtil
from hdash.validator.categories import Categories
from typing import List
from hdash.synapse.meta_file import MetaFile


class MetaDataSummary:
    """Summary Stats across all metadata files."""

    NA_VALUES = ["na", "nan", "unknown", "not applicable", "not reported"]
    IGNORED_FIELDS = [
        IdUtil.HTAN_PARTICIPANT_ID,
        IdUtil.HTAN_PARENT_ID,
        IdUtil.HTAN_BIOSPECIMEN_ID,
        Categories.COMPONENT_COL,
        Categories.ENTITY_ID_COL,
    ]

    def get_overall_percent_complete(self):
        """Get overall metadata completeness metric."""
        if self._total_num_complete_fields == 0:
            return 0
        else:
            return self._total_num_complete_fields / self._total_num_fields


    def __init__(self, meta_list: List[MetaFile]):
        """Default Constructor."""
        self._total_num_fields = 0
        self._total_num_complete_fields = 0
        self.categories = Categories()
        for meta_file in meta_list:
            percent_complete = self._calculate_percent_complete(meta_file.df)
            meta_file.percent_meta_data_complete = percent_complete

    def _calculate_percent_complete(self, df):
        """Inspect Data Frame for completed/missing fields."""
        num_fields = 0
        num_completed_fields = 0
        for index, row in df.iterrows():
            for field_name, field_value in row.items():
                if field_name not in self.IGNORED_FIELDS:
                    num_fields += 1
                    field_value = str(field_value).lower()
                    if field_value not in self.NA_VALUES:
                        num_completed_fields += 1
        self._total_num_fields += num_fields
        self._total_num_complete_fields += num_completed_fields
        return num_completed_fields / num_fields
