"""Validation Rule."""

from hdash.util.id_util import IdUtil
from hdash.validator.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile


class ValidatePrimaryIds(ValidationRule):
    """Validate Primary IDs in all Files."""

    def __init__(self, atlas_id, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_ID_SPEC",
            "Verify that primary IDs follow HTAN ID Spec.",
        )

        # List of Files to Exclude from Validation
        self._exclude_list = ["syn42292434"]  # HTAP Ex-Seq Data Set

        self.meta_file_map = meta_file_map
        self.categories = Categories()
        self.id_util = IdUtil()
        for category in self.categories.all_assays:
            self.__validate_ids(atlas_id, category)

    def __validate_ids(self, atlas_id, category):
        if self.meta_file_map.has_category(category):
            meta_file_list = self.meta_file_map.get_meta_file_list(category)
            for meta_file in meta_file_list:
                if meta_file.id not in self._exclude_list:
                    df = meta_file.df
                    primary_id_col = self.id_util.get_primary_id_column(category)
                    id_list = df[primary_id_col].to_list()
                    for current_id in id_list:
                        current_id = str(current_id)
                        if primary_id_col == IdUtil.HTAN_PARTICIPANT_ID:
                            self.__check_participant_id(
                                meta_file, category, current_id, atlas_id
                            )
                        else:
                            self.__check_primary_id(
                                meta_file, category, current_id, atlas_id
                            )

    def __check_participant_id(self, meta_file: MetaFile, category, id, atlas_id):
        parts = id.split("_")
        label = category + ": " + id
        if parts[0] != atlas_id:
            msg = label + " does not match atlas ID: " + atlas_id
            self.add_error(msg, meta_file)
        if len(parts) != 2:
            msg = label + " does not match HTAN spec."
            self.add_error(msg, meta_file)
        else:
            try:
                int(parts[1])
            except ValueError:
                msg = label + " does not match HTAN spec."
                self.add_error(msg, meta_file)

    def __check_primary_id(self, meta_file: MetaFile, category, id, atlas_id):
        parts = id.split("_")
        label = category + ": " + id
        if parts[0] != atlas_id:
            msg = label + " does not match atlas ID: " + atlas_id
            self.add_error(msg, meta_file)
        if len(parts) != 3:
            msg = label + " does not match HTAN spec."
            self.add_error(msg, meta_file)
        else:
            try:
                if parts[1] != "xxxx":
                    int(parts[1])
                int(parts[2])
            except ValueError:
                msg = label + " does not match HTAN spec."
                self.add_error(msg, meta_file)
