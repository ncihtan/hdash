"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.graph.graph import Node, Edge
from hdash.validator.id_util import IdUtil
from hdash.validator.categories import Categories


class ValidateLinks(ValidationRule):
    """Validate all internal links."""

    def __init__(self, meta_file_map):
        """Construct new Validation Rule."""
        super().__init__("H_LINKS", "Validate all internal links.")
        self.id_util = IdUtil()
        self.meta_map = meta_file_map
        self.node_map = {}
        self.edge_list = []
        self.categories = Categories()
        error_list = []
        self.__gather_nodes()
        self.__gather_edges(error_list)
        self.set_error_list(error_list)

    def __gather_nodes(self):
        self.__gather_nodes_by_category(self.categories.DEMOGRAPHICS)
        self.__gather_nodes_by_category(self.categories.BIOSPECIMEN)
        self.__gather_nodes_by_category(self.categories.SRRS_BIOSPECIMEN)
        for category in self.categories.all_assays:
            self.__gather_nodes_by_category(category)

    def __gather_nodes_by_category(self, category):
        df_list = self.meta_map.get(category, [])
        for df in df_list:
            primary_id = self.id_util.get_primary_id_column(category)
            id_list = df[primary_id].to_list()
            for current_id in id_list:
                current_id = str(current_id)
                node = Node()
                node.id = current_id
                node.label = current_id
                node.category = category
                self.node_map[current_id] = node

    def __gather_edges(self, error_list):
        for category in self.categories.all_categories:
            self.__gather_edges_by_category(category, error_list)

    def __gather_edges_by_category(self, category, e_list):
        df_list = self.meta_map.get(category, [])
        for df in df_list:
            primary_id_col = self.id_util.get_primary_id_column(category)
            parent_id_col = self.id_util.get_parent_id_column(category)
            adj_id_col = self.id_util.get_adjacent_id_column(category)
            if parent_id_col is not None:
                for index, row in df.iterrows():
                    chunk = str(row[parent_id_col])
                    id = str(row[primary_id_col])
                    self.__check_parents(id, chunk, category, e_list)
            if adj_id_col is not None:
                if adj_id_col in df.columns:
                    for index, row in df.iterrows():
                        chunk = str(row[adj_id_col])
                        id = str(row[primary_id_col])
                        self.__check_adjacents(id, chunk, category, e_list)
                else:
                    msg = "%s is missing column:  %s" % (category, adj_id_col)
                    e_list.append(msg)

    def __check_parents(self, id, parent_id_chunk, category, error_list):
        # We can have multiple parents!
        parent_id_chunk = parent_id_chunk.replace(";", " ").replace(",", " ")
        parts = parent_id_chunk.split()
        for part in parts:
            parent_id = part.strip()
            parent_exists = parent_id in self.node_map
            if not parent_exists:
                m = "%s references parent ID: %s, but no such ID exists." % (
                    category,
                    parent_id,
                )
                error_list.append(m)
            elif id == parent_id:
                m = "%s references itself: %s as parent." % (category, id)
                error_list.append(m)
            else:
                edge = Edge()
                edge.source_id = parent_id
                edge.target_id = id
                self.edge_list.append(edge)

    def __check_adjacents(self, id, adj_id_chunk, category, error_list):
        # We can have multiple adjacents!
        if adj_id_chunk == "nan":
            return
        adj_id_chunk = adj_id_chunk.replace(";", " ").replace(",", " ")
        parts = adj_id_chunk.split()
        for part in parts:
            adjacent_id = part.strip()
            adjacent_exists = adjacent_id in self.node_map
            if not adjacent_exists:
                m = "%s references adjacent ID: %s, but no such ID exists." % (
                    category,
                    adjacent_id,
                )
                error_list.append(m)
