from hdash.validator.validation_rule import ValidationRule


class ValidationH1(ValidationRule):
    def __init__(self, meta_file_map):
        super().__init__("H1", "Demographics File is Present")
        validation_passed = "Demographics" in meta_file_map
        self.set_status(validation_passed)
