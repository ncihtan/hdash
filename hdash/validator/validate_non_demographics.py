"""Validation Rule."""

from hdash.validator.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.validator.id_util import IdUtil


class ValidateNonDemographics(ValidationRule):
    """Verify IDs in Non-Demographics Clinical Data Files."""

    def __init__(self, meta_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_NON_DEM",
            "Non-Demographic clinical data use same IDs as demographics file.",
        )
        categories = Categories()
        df_list = meta_map.get(Categories.DEMOGRAPHICS, [])
        err_list = []
        if len(df_list) == 0:
            err_list.append("Cannot assess.  No Demographics File.")
        else:
            demog_id_list = []
            for df in df_list:
                demog_id_list.extend(df[IdUtil.HTAN_PARTICIPANT_ID].to_list())
            for category in categories.all_clinical:
                self.__check_file(category, meta_map, demog_id_list, err_list)

        self.set_error_list(err_list)

    def __check_file(self, category, meta_map, demog_id_list, err_list):
        if category in meta_map:
            df_list = meta_map.get(category, [])
            for df in df_list:
                participant_id_list = df[IdUtil.HTAN_PARTICIPANT_ID].to_list()
                for id in participant_id_list:
                    if id not in demog_id_list:
                        err_list.append(
                            "Clinical file:  %s" % category
                            + "contains ID:  "
                            + id
                            + ", but this ID is not in Demographics File"
                        )
