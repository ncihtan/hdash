"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule


class ValidateDemographicsIds(ValidationRule):
    """Validate IDs in Demographics File."""

    def __init__(self, atlas_id, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_DEM_IDS",
            "Demographics file uses correct "
            + " atlas ID and adheres to the HTAN ID Spec.",
        )
        df = meta_file_map["Demographics"]
        id_list = df["HTAN Participant ID"].to_list()
        error_list = []
        self.__validate_ids(atlas_id, id_list, error_list)
        self.set_error_list(error_list)

    def __validate_ids(self, atlas_id, id_list, error_list):
        for id in id_list:
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
