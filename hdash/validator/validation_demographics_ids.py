from hdash.validator.validation_rule import ValidationRule


class ValidationDemographicsIds(ValidationRule):
    def __init__(self, atlas_id, meta_file_map):
        super().__init__(
            "H_DEM_IDS",
            "Demographics File Uses Correct "
            + " Atlas ID and adheres to the HTAN ID Spec",
        )
        df = meta_file_map["Demographics"]
        participant_id_list = df["HTAN Participant ID"].to_list()
        error_list = []
        for id in participant_id_list:
            parts = id.split("_")
            if parts[0] != atlas_id:
                error_list.append(id + " does not match atlas ID: " + atlas_id)
            if len(parts) > 2:
                error_list.append(id + " does not match HTAN spec.")
            else:
                try:
                    int(parts[1])
                except ValueError:
                    error_list.append(id + " does not match HTAN spec.")

        self.set_error_list(error_list)
