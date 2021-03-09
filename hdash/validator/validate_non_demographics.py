"""Validation Rule."""

from hdash.validator.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.validator.id_util import IdUtil


class ValidateNonDemographics(ValidationRule):
    """Verify IDs in Non-Demographics Clinical Data Files."""

    # This list will need to be expanded in the future...
    clinical_list = []
    clinical_list.append("Exposure")
    clinical_list.append("FamilyHistory")
    clinical_list.append("FollowUp")
    clinical_list.append("Diagnosis")
    clinical_list.append("Therapy")
    clinical_list.append("MolecularTest")
    clinical_list.append("ClinicalDataTier2")
    clinical_list.append("LungCancerTier3")
    clinical_list.append("BreastCancerTier3")

    def __init__(self, meta_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_NON_DEM",
            "Non-Demographic clinical data use same IDs as demographics file.",
        )
        df = meta_map[Categories.DEMOGRAPHICS]
        err_list = []
        if df is None:
            err_list.append("Cannot assess.  No Demographics File.")
        else:
            demog_id_list = df[IdUtil.HTAN_PARTICIPANT_ID].to_list()
            for category in self.clinical_list:
                self.__check_file(category, meta_map, demog_id_list, err_list)

        self.set_error_list(err_list)

    def __check_file(self, category, meta_map, demog_id_list, err_list):
        if category in meta_map:
            df = meta_map[category]
            participant_id_list = df[IdUtil.HTAN_PARTICIPANT_ID].to_list()
            for id in participant_id_list:
                if id not in demog_id_list:
                    err_list.append(
                        "Clinical file:  %s" % category
                        + "contains ID:  "
                        + id
                        + ", but this ID is not in Demographics File"
                    )
