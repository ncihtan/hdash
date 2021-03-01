from hdash.validator.validation_rule import ValidationRule


class ValidationH3(ValidationRule):
    def __init__(self, meta_file_map):
        super().__init__("H3", "Biospecimen File is Present")
        validation_passed = "Biospecimen" in meta_file_map
        self.set_status(validation_passed)
