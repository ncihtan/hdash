"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories
from hdash.synapse.meta_map import MetaMap

class ValidateDemographics(ValidationRule):
    """Verify that Demographics File is Present."""

    def __init__(self, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__("H_DEM", "At least one Demographics file found.")
        validation_passed = meta_file_map.has_category(Categories.DEMOGRAPHICS)
        if validation_passed is False:
            self.add_error_message(f"{Categories.DEMOGRAPHICS} file was not found.")
