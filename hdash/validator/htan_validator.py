"""Core HTAN Validator."""

from typing import List
from hdash.graph.htan_graph import HtanGraph
from hdash.validator.validation_rule import ValidationRule
from hdash.validator.validate_demographics import ValidateDemographics
from hdash.validator.validate_biospecimens import ValidateBiospecimens
from hdash.validator.validate_primary_ids import ValidatePrimaryIds
from hdash.validator.validate_entity_ids import ValidateEntityIds
from hdash.validator.validate_non_demographics import ValidateNonDemographics
from hdash.validator.validate_links import ValidateLinks
from hdash.validator.validate_categories import ValidateCategories
from hdash.synapse.meta_map import MetaMap


class HtanValidator:
    """Core HTAN Validator."""

    def __init__(self, atlas_id, meta_map: MetaMap, htan_graph: HtanGraph):
        """Construct a new HTAN Validator for one atlas."""
        self.atlas_id = atlas_id
        self.meta_map = meta_map
        self.graph = htan_graph
        self.validation_list = []
        self.__validate()

    def get_validation_list(self) -> List[ValidationRule]:
        """Get the list of validation rules applied."""
        return self.validation_list

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
        links1 = ValidateLinks(self.graph)
        self.validation_list.append(links1)

        # Synapse IDs
        synapseIds1 = ValidateEntityIds(self.meta_map)
        self.validation_list.append(synapseIds1)
