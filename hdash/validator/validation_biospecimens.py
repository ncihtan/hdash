from hdash.validator.validation_rule import ValidationRule


class ValidationBiospecimens(ValidationRule):
    def __init__(self, meta_file_map):
        super().__init__("H_BIOSPEC", "Biospecimen File is Present")
        validation_passed = "Biospecimen" in meta_file_map
        self.set_status(validation_passed)
