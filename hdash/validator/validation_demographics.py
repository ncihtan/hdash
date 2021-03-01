from hdash.validator.validation_rule import ValidationRule


class ValidationDemographics(ValidationRule):
    def __init__(self, meta_file_map):
        super().__init__("H_DEM", "Demographics File is Present")
        validation_passed = "Demographics" in meta_file_map
        self.set_status(validation_passed)
