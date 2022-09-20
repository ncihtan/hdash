"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories


class ValidateDemographics(ValidationRule):
    """Verify that Demographics File is Present."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_DEM", "At least one Demographics file found.")
        validation_passed = Categories.DEMOGRAPHICS in meta_file_map
        self.set_status(validation_passed)
        if validation_passed is False:
            error_list = []
            error_list.append(f"{Categories.DEMOGRAPHICS} file was not found.")
            self.set_error_list(error_list)
