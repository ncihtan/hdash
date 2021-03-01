from hdash.validator.validation_rule import ValidationRule


class ValidationBiospecimenIds(ValidationRule):
    def __init__(self, atlas_id, meta_file_map):
        super().__init__(
            "H_BIOSPEC_IDS",
            "Biospecimen IDs reference valid Participant IDs and"
            + " follow HTAN ID Spec",
        )
        df = meta_file_map["Demographics"]
        error_list = []
        if df is None:
            error_list.append(
                "Cannot validate biospecimen IDs due to missing demographics."
            )
            self.set_status(False)
        else:
            participant_id_list = df["HTAN Participant ID"].to_list()
            df = meta_file_map["Biospecimen"]
            parent_id_list = df["HTAN Parent ID"].to_list()
            id_list = df["HTAN Biospecimen ID"].to_list()
            for parent_id in parent_id_list:
                if parent_id not in participant_id_list and parent_id not in id_list:
                    error_list.append(
                        "Biospecimen refers to parent ID:  "
                        + parent_id
                        + ", but this ID does not exist in demographics "
                        + "or biospecimen files."
                    )
            self.validate_biospecimen_id(atlas_id, error_list, id_list)
        self.set_error_list(error_list)

    def validate_biospecimen_id(self, atlas_id, error_list, id_list):
        for id in id_list:
            parts = id.split("_")
            if parts[0] != atlas_id:
                error_list.append(id + " does not match atlas ID: " + atlas_id)
            if len(parts) != 3:
                error_list.append(id + " does not match HTAN spec.")
            else:
                try:
                    int(parts[1])
                    int(parts[2])
                except ValueError:
                    error_list.append(id + " does not match HTAN spec.")
