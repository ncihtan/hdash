"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.graph.graph import Node


class ValidateLinks(ValidationRule):
    """Validate all internal links."""

    SC_RNA_SEQ_LEVEL_1 = "ScRNA-seqLevel1"
    SC_RNA_SEQ_LEVEL_2 = "ScRNA-seqLevel2"
    SC_RNA_SEQ_LEVEL_3 = "ScRNA-seqLevel3"
    SC_RNA_SEQ_LEVEL_4 = "ScRNA-seqLevel4"
    BIOSPECIMEN = "Biospecimen"
    DEMOGRAPHICS = "Demographics"

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_LINKS", "Validate all internal links.")
        self.meta_map = meta_file_map
        self.node_map = {}
        self.category_list = []
        self.category_list.append(ValidateLinks.BIOSPECIMEN)
        self.category_list.append(ValidateLinks.DEMOGRAPHICS)
        self.category_list.append(ValidateLinks.SC_RNA_SEQ_LEVEL_1)
        self.category_list.append(ValidateLinks.SC_RNA_SEQ_LEVEL_2)
        self.category_list.append(ValidateLinks.SC_RNA_SEQ_LEVEL_3)
        self.category_list.append(ValidateLinks.SC_RNA_SEQ_LEVEL_4)
        error_list = []
        self.__gather_nodes()
        self.__gather_edges(error_list)
        self.set_error_list(error_list)

    def __gather_nodes(self):
        for category in self.category_list:
            self.__gather_nodes_by_category(category)

    def __gather_nodes_by_category(self, category):
        df = self.meta_map.get(category)
        if df is not None:
            primary_id = self.__get_primary_id(category)
            id_list = df[primary_id].to_list()
            for id in id_list:
                node = Node()
                node.id = id
                node.label = id
                node.category = category
                self.node_map[id] = node

    def __get_primary_id(self, category):
        if category == ValidateLinks.BIOSPECIMEN:
            return "HTAN Biospecimen ID"
        elif category == ValidateLinks.DEMOGRAPHICS:
            return "HTAN Participant ID"
        else:
            return "HTAN Data File ID"

    def __get_parent_id(self, category):
        if category == ValidateLinks.BIOSPECIMEN:
            return "HTAN Parent ID"
        elif category == ValidateLinks.DEMOGRAPHICS:
            return None
        elif category == ValidateLinks.SC_RNA_SEQ_LEVEL_1:
            return "HTAN Parent Biospecimen ID"
        else:
            return "HTAN Parent Data File ID"

    def __gather_edges(self, error_list):
        for category in self.category_list:
            self.__gather_edges_by_category(category, error_list)

    def __gather_edges_by_category(self, category, error_list):
        df = self.meta_map.get(category)
        if df is not None:
            primary_id_col = self.__get_primary_id(category)
            parent_id_col = self.__get_parent_id(category)
            if parent_id_col is not None:
                for index, row in df.iterrows():
                    chunk = row[parent_id_col]
                    id = row[primary_id_col]
                    self.__check_parents(id, chunk, category, error_list)

    def __check_parents(self, id, parent_id_chunk, category, error_list):
        # We can have multiple parents!
        parent_id_chunk = parent_id_chunk.replace(';',' ').replace(',',' ')
        parts = parent_id_chunk.split()
        for part in parts:
            parent_id = part.strip()
            parent_exists = parent_id in self.node_map
            if not parent_exists:
                m = "%s references parent ID:  %s, but no such ID exists." % (
                    category,
                    parent_id,
                )
                error_list.append(m)
