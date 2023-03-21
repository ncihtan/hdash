"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories
from hdash.synapse.meta_map import MetaMap


class ValidateBiospecimens(ValidationRule):
    """Verify that Biospecimen File is Present."""

    def __init__(self, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__("H_BIOSPEC", "At least one Biospecimen file found.")
        check1 = meta_file_map.has_category(Categories.BIOSPECIMEN)
        check2 = meta_file_map.has_category(Categories.SRRS_BIOSPECIMEN)
        final_check = check1 or check2
        if final_check is False:
            self.add_error_message(f"{Categories.BIOSPECIMEN} file was not found.")
