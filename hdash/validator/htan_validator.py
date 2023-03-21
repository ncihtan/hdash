"""Core HTAN Validator."""

import pandas as pd

from typing import List
from hdash.validator.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.validator.validate_demographics import ValidateDemographics
from hdash.validator.validate_biospecimens import ValidateBiospecimens
from hdash.validator.validate_primary_ids import ValidatePrimaryIds
from hdash.validator.validate_entity_ids import ValidateEntityIds
from hdash.validator.validate_non_demographics import ValidateNonDemographics
from hdash.validator.validate_links import ValidateLinks
from hdash.validator.validate_categories import ValidateCategories
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile


class HtanValidator:
    """Core HTAN Validator."""

    def __init__(self, atlas_id, meta_data_file_list: List[MetaFile]):
        """Construct a new HTAN Validator for one atlas."""
        self.atlas_id = atlas_id
        self.validation_list = []
        self.node_map = {}
        self.meta_map = MetaMap()

        # Review all the metadata files and bin them within the MetaMap
        for meta_file in meta_data_file_list:
            self.meta_map.add_meta_file(meta_file)

        # Then validate
        self.__validate()

    def get_validation_list(self) -> List[ValidationRule]:
        """Get the list of validation rules applied."""
        return self.validation_list

    def get_node_map(self):
        """Get the graph map of all nodes."""
        return self.links1.node_map

    def get_edge_list(self):
        """Get the list of all edges."""
        return self.links1.edge_list

    def __validate(self):
        # Categories Validation
        c0 = ValidateCategories(self.meta_map)
        self.validation_list.append(c0)

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

        # Synapse IDs
        self.synapseIds1 = ValidateEntityIds(self.meta_map)
        self.validation_list.append(self.synapseIds1)
