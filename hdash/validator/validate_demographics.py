"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule


class ValidateDemographics(ValidationRule):
    """Verify that Demographics File is Present."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_DEM", "At least one Demographics file found.")
        validation_passed = "Demographics" in meta_file_map
        self.set_status(validation_passed)
