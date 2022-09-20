"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories


class ValidateBiospecimens(ValidationRule):
    """Verify that Biospecimen File is Present."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_BIOSPEC", "At least one Biospecimen file found.")
        validation_passed = (Categories.BIOSPECIMEN in meta_file_map) or (
            Categories.SRRS_BIOSPECIMEN in meta_file_map
        )
        self.set_status(validation_passed)
