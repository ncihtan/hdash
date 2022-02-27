"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories
from hdash.validator.validate_non_demographics import ValidateNonDemographics


class ValidateCategories(ValidationRule):
    """Verify that Atlas is using Categories supported by the Dashhoard."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_CATEGORIES",
            "Verify that all Categories are supported by the Dashboard.",
        )

        categories = Categories()
        error_list = []
        for key in meta_file_map.keys():
            if (
                key not in categories.get_primary_category_list()
                and key not in ValidateNonDemographics.clinical_list
            ):
                error_list.append(
                    f"{key} is not yet supported by the Dashboard.  "
                    "Please notify Ethan to update the code!"
                )

        self.set_status(False)
        if len(self.error_list) > 0:
            self.set_status(True)
        self.set_error_list(error_list)
