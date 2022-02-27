"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule


class ValidateEntityIds(ValidationRule):
    """Verify that Entity Ids are Specified."""

    ENTITY_ID_COL = "entityId"

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_ENTITY_ID", "Synapse Entity IDs are Specified.")
        error_list = []
        for key in meta_file_map:
            df_list = meta_file_map[key]
            for df in df_list:
                try:
                    synapse_ids = df[ValidateEntityIds.ENTITY_ID_COL].to_list()
                    self.__check_synapse_ids(key, synapse_ids, error_list)
                except KeyError:
                    msg = "%s does not have %s column." % (
                        key,
                        ValidateEntityIds.ENTITY_ID_COL,
                    )
                    error_list.append(msg)
        self.set_error_list(error_list)

    def __check_synapse_ids(self, key, synapse_ids, error_list):
        for synapse_id in synapse_ids:
            if not synapse_id.startswith("syn"):
                msg = "%s has invalid Synapse ID: %s." % (key, synapse_id)
                error_list.append(msg)
