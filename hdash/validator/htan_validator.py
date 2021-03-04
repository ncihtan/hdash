"""Core HTAN Validator."""

import pandas as pd

from hdash.validator.validate_demographics import ValidateDemographics
from hdash.validator.validate_biospecimens import ValidateBiospecimens
from hdash.validator.validate_primary_ids import ValidatePrimaryIds
from hdash.validator.validate_non_demographics import ValidateNonDemographics
from hdash.validator.validate_links import ValidateLinks


class HtanValidator:
    """Core HTAN Validator."""

    def __init__(self, atlas_id, meta_data_file_list):
        """Construct a new HTAN Validator for one atlas."""
        self.atlas_id = atlas_id
        self.validation_list = []
        self.node_map = {}

        # First step is to read in all the metadata files and caterogize them
        self.meta_map = {}
        for path in meta_data_file_list:
            current_df = pd.read_csv(path)
            component_list = current_df["Component"].to_list()
            try:
                component = component_list[0]
            except IndexError:
                component = "Empty"
            self.meta_map[component] = current_df

        # Then validate
        self.__validate()

    def get_validation_list(self):
        """Get the list of validation rules applied."""
        return self.validation_list

    def get_node_map(self):
        """Get the graph map of all nodes."""
        return self.links1.node_map

    def get_edge_list(self):
        """Get the list of all edges."""
        return self.links1.edge_list

    def __validate(self):

        # Clinical Validation
        c1 = ValidateDemographics(self.meta_map)
        self.validation_list.append(c1)

        if c1.validation_passed:
            c2 = ValidateNonDemographics(self.meta_map)
            self.validation_list.append(c2)

        # Biospecimen Validation
        b1 = ValidateBiospecimens(self.meta_map)
        self.validation_list.append(b1)

        # ID Checks
        id1 = ValidatePrimaryIds(self.atlas_id, self.meta_map)
        self.validation_list.append(id1)

        # Link Integrity
        self.links1 = ValidateLinks(self.meta_map)
        self.validation_list.append(self.links1)
