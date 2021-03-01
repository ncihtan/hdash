from hdash.validator.validation_rule import ValidationRule


class ValidationNonDemographics(ValidationRule):
    clinical_list = []
    clinical_list.append("Exposure")
    clinical_list.append("FamilyHistory")
    clinical_list.append("FollowUp")
    clinical_list.append("Diagnosis")
    clinical_list.append("Therapy")
    clinical_list.append("ClinicalDataTier2")
    clinical_list.append("LungCancerTier3")

    def __init__(self, atlas_id, meta_map):
        super().__init__(
            "H_NON_DEM",
            "Non-Demographic Clinical Files Use Same IDs as Demographics File"
        )
        df = meta_map["Demographics"]
        error_list = []
        if df is None:
            error_list.append("Cannot assess.  No Demographics File.")
        else:
            demog_id_list = df["HTAN Participant ID"].to_list()
            for category in self.clinical_list:
                self.check_file(category, meta_map, demog_id_list, error_list)

        self.set_error_list(error_list)

    def check_file(self, category, meta_map, demog_id_list, error_list):
        if category in meta_map:
            df = meta_map[category]
            participant_id_list = df["HTAN Participant ID"].to_list()
            for id in participant_id_list:
                if id not in demog_id_list:
                    error_list.append(
                        "Clinical file:  %s" % category
                        + "contains ID:  "
                        + id
                        + ", but this ID is not in Demographics File"
                    )
