from hdash.validator.validation_rule import ValidationRule


class ValidationH2(ValidationRule):
    def __init__(self, atlas_id, meta_file_map):
        super().__init__("H2", "Demographics File Uses Correct Atlas ID")
        df = meta_file_map["Demographics"]
        participant_id_list = df["HTAN Participant ID"].to_list()
        error_list = []
        for id in participant_id_list:
            if not id.startswith(atlas_id + "_"):
                error_list.append(id + " does not match atlas ID: " + atlas_id)
        if len(error_list) == 0:
            self.set_status(True)
        else:
            self.set_status(False)
        self.set_error_list(error_list)
