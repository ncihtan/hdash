"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories


class ValidateBiospecimens(ValidationRule):
    """Verify that Biospecimen File is Present."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_BIOSPEC", "At least one Biospecimen file found.")
        check1 = Categories.BIOSPECIMEN in meta_file_map
        check2 = Categories.SRRS_BIOSPECIMEN in meta_file_map
        final_check = check1 or check2
        self.set_status(final_check)
        if final_check is False:
            error_list = []
            error_list.append(f"{Categories.BIOSPECIMEN} file was not found.")
            self.set_error_list(error_list)
