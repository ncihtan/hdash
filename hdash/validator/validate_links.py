"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.graph.graph import Node, Edge
from hdash.validator.id_util import IdUtil
from hdash.validator.categories import Categories
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile
import logging


class ValidateLinks(ValidationRule):
    """Validate all internal links."""

    def __init__(self, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__("H_LINKS", "Validate all internal links.")
        self.id_util = IdUtil()
        self.meta_map = meta_file_map
        self.node_map = {}
        self.edge_list = []
        self.categories = Categories()
        self.__gather_nodes()
        self.__gather_edges()

    def __gather_nodes(self):
        self.__gather_nodes_by_category(self.categories.DEMOGRAPHICS)
        self.__gather_nodes_by_category(self.categories.BIOSPECIMEN)
        self.__gather_nodes_by_category(self.categories.SRRS_BIOSPECIMEN)
        for category in self.categories.all_assays:
            self.__gather_nodes_by_category(category)

    def __gather_nodes_by_category(self, category):
        meta_file_list = self.meta_map.get_meta_file_list(category)
        for meta_file in meta_file_list:
            df = meta_file.df
            primary_id = self.id_util.get_primary_id_column(category)
            id_list = df[primary_id].to_list()
            for current_id in id_list:
                current_id = str(current_id)
                node = Node()
                node.id = current_id
                node.label = current_id
                node.category = category
                self.node_map[current_id] = node

    def __gather_edges(self):
        for category in self.categories.all_categories:
            self.__gather_edges_by_category(category)

    def __gather_edges_by_category(self, category):
        meta_file_list = self.meta_map.get_meta_file_list(category)
        for meta_file in meta_file_list:
            logging.info("Validating links in: %s", meta_file.id)
            df = meta_file.df
            primary_id_col = self.id_util.get_primary_id_column(category)
            parent_id_col = self.id_util.get_parent_id_column(category)
            adj_id_col = self.id_util.get_adjacent_id_column(category)
            if parent_id_col is not None:
                for index, row in df.iterrows():
                    chunk = str(row[parent_id_col])

                    # Handle Special HTAPP/DFCI Cases
                    if chunk.startswith("Not Applicable"):
                        try:
                            chunk = str(row[IdUtil.HTAN_PARENT_BIOSPECIMEN_ID])
                        except KeyError:
                            chunk = "NOT_APPLICABLE"

                    id = str(row[primary_id_col])
                    self.__check_parents(meta_file, id, chunk, category)
            if adj_id_col is not None:
                if adj_id_col in df.columns:
                    for index, row in df.iterrows():
                        chunk = str(row[adj_id_col])
                        id = str(row[primary_id_col])
                        self.__check_adjacents(meta_file, id, chunk, category)
                else:
                    msg = "%s is missing column:  %s" % (category, adj_id_col)
                    self.add_error(msg, meta_file)

    def __check_parents(self, meta_file: MetaFile, id, parent_id_chunk, category):
        # We can have multiple parents!
        parent_id_chunk = parent_id_chunk.replace(";", " ").replace(",", " ")
        parts = parent_id_chunk.split()
        for part in parts:
            parent_id = part.strip()
            parent_exists = parent_id in self.node_map
            if not parent_exists:
                m = "%s references parent ID: %s, but no such ID exists" % (
                    category,
                    parent_id
                )
                self.add_error(m, meta_file)
            elif id == parent_id:
                m = "%s references itself: %s as parent." % (category, id)
                self.add_error(m, meta_file)
            else:
                edge = Edge()
                edge.source_id = parent_id
                edge.target_id = id
                self.edge_list.append(edge)

    def __check_adjacents(self, meta_file: MetaFile, id, adj_id_chunk, category):
        # We can have multiple adjacents!
        if adj_id_chunk == "nan":
            return
        adj_id_chunk = adj_id_chunk.replace(";", " ").replace(",", " ")
        parts = adj_id_chunk.split()
        for part in parts:
            adjacent_id = part.strip()
            adjacent_exists = adjacent_id in self.node_map
            if not adjacent_exists:
                m = "%s references adjacent ID: %s, but no such ID exists" % (
                    category,
                    adjacent_id
                )
                self.add_error(m, meta_file)
