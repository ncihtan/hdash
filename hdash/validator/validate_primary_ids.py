"""Validation Rule."""

from hdash.validator.id_util import IdUtil
from hdash.validator.categories import Categories
from hdash.validator.validation_rule import ValidationRule


class ValidatePrimaryIds(ValidationRule):
    """Validate Primary IDs in all Files."""

    def __init__(self, atlas_id, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__(
            "H_ID_SPEC",
            "Verify that primary IDs follow HTAN ID Spec.",
        )
        self.meta_file_map = meta_file_map
        self.categories = Categories()
        self.id_util = IdUtil()
        self.category_list = self.categories.get_primary_category_list()
        error_list = []
        for category in self.category_list:
            self.__validate_ids(atlas_id, category, error_list)
        self.set_error_list(error_list)

    def __validate_ids(self, atlas_id, category, e_list):
        if category in self.meta_file_map:
            df = self.meta_file_map[category]
            primary_id_col = self.id_util.get_primary_id_column(category)
            id_list = df[primary_id_col].to_list()
            for id in id_list:
                id = str(id)
                if primary_id_col == IdUtil.HTAN_PARTICIPANT_ID:
                    self.__check_participant_id(category, id, atlas_id, e_list)
                else:
                    self.__check_primary_id(category, id, atlas_id, e_list)

    def __check_participant_id(self, category, id, atlas_id, error_list):
        parts = id.split("_")
        label = category + ": " + id
        if parts[0] != atlas_id:
            error_list.append(label + " does not match atlas ID: " + atlas_id)
        if len(parts) != 2:
            error_list.append(label + " does not match HTAN spec.")
        else:
            try:
                int(parts[1])
            except ValueError:
                error_list.append(label + " does not match HTAN spec.")

    def __check_primary_id(self, category, id, atlas_id, error_list):
        parts = id.split("_")
        label = category + ": " + id
        if parts[0] != atlas_id:
            error_list.append(label + " does not match atlas ID: " + atlas_id)
        if len(parts) != 3:
            error_list.append(label + " does not match HTAN spec.")
        else:
            try:
                int(parts[1])
                int(parts[2])
            except ValueError:
                error_list.append(label + " does not match HTAN spec.")
