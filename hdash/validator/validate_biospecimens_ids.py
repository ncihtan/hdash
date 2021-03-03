"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule


class ValidateBiospecimenIds(ValidationRule):
    """Validate Biospecimend IDs."""

    def __init__(self, atlas_id, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_BIOSPEC_IDS",
            "Biospecimen IDs follow HTAN ID Spec.",
        )
        df = meta_file_map["Demographics"]
        error_list = []
        df = meta_file_map["Biospecimen"]
        id_list = df["HTAN Biospecimen ID"].to_list()
        self.__validate_biospecimen_id(atlas_id, error_list, id_list)
        self.set_error_list(error_list)

    def __validate_biospecimen_id(self, atlas_id, error_list, id_list):
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
