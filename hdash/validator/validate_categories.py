"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.validator.categories import Categories
from hdash.synapse.meta_map import MetaMap


class ValidateCategories(ValidationRule):
    """Verify that Atlas is using Categories supported by the Dashhoard."""

    def __init__(self, meta_file_map:  MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_CATEGORIES",
            "Check that all Atlas Categories are supported by the Dashboard.",
        )

        categories = Categories()
        for category in meta_file_map.get_categories():
            if category not in categories.all_categories:
                self.add_error_message(
                    f"{category} is not yet supported by the Dashboard.  "
                    "Please notify Ethan to update the code!"
                )