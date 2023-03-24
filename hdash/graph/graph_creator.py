"""Graph Util Class."""

from hdash.synapse.meta_map import MetaMap
from hdash.util.id_util import IdUtil
from hdash.validator.categories import Categories
from hdash.graph.node_data import NodeData
from hdash.graph.htan_graph import HtanGraph


class GraphCreator:
    """
    Creates a Graph of Atlas Nodes.

    Given a set of MetaFiles, create an HTAN Graph.
    This enables us to link patients --> biospecimens --> assays.
    """

    def __init__(self, atlas_id, meta_map: MetaMap):
        """Default Constructor."""
        self._atlas_id = atlas_id
        self._graph = HtanGraph()
        self._meta_map = meta_map
        self._categories = Categories()
        self._id_util = IdUtil()
        self.__gather_nodes()
        self.__gather_edges()

    @property
    def htan_graph(self):
        return self._graph

    def __gather_nodes(self):
        """Gather all nodes."""
        self.__gather_nodes_by_category(self._categories.DEMOGRAPHICS)
        self.__gather_nodes_by_category(self._categories.BIOSPECIMEN)
        self.__gather_nodes_by_category(self._categories.SRRS_BIOSPECIMEN)
        for category in self._categories.all_assays:
            self.__gather_nodes_by_category(category)

    def __gather_nodes_by_category(self, category):
        """Gather all Nodes in the Specified Category."""
        meta_file_list = self._meta_map.get_meta_file_list(category)
        for meta_file in meta_file_list:
            df = meta_file.df
            primary_id = self._id_util.get_primary_id_column(category)
            id_list = df[primary_id].to_list()

            # Each Primary ID Gets its Own Node
            for current_id in id_list:
                current_id = str(current_id)
                node_data = NodeData(current_id, meta_file)
                self._graph.add_node(node_data)

    def __gather_edges(self):
        """Gather all the edges."""
        for category in self._categories.all_categories:
            self.__gather_edges_by_category(category)

    def __gather_edges_by_category(self, category):
        meta_file_list = self._meta_map.get_meta_file_list(category)
        for meta_file in meta_file_list:
            df = meta_file.df
            primary_id_col = self._id_util.get_primary_id_column(category)
            parent_id_col = self._id_util.get_parent_id_column(category)
            adj_id_col = self._id_util.get_adjacent_id_column(category)
            if parent_id_col is not None:
                self.__gather_child_parent_edges(df, primary_id_col, parent_id_col)
            if adj_id_col is not None and adj_id_col in df.columns:
                self.__gather_adjacent_edges(df, primary_id_col, adj_id_col)

    def __gather_child_parent_edges(self, df, primary_id_col, parent_id_col):
        """Gather Parent Child Edges."""
        for index, row in df.iterrows():
            primary_id = str(row[primary_id_col])
            parent_id_chunk = str(row[parent_id_col])
            parent_id_chunk = self.__handle_htapp_special_case(parent_id_chunk, row)

            # We can have multiple parents
            parent_id_chunk = parent_id_chunk.replace(";", " ").replace(",", " ")
            parts = parent_id_chunk.split()
            for part in parts:
                parent_id = part.strip()
                self._graph.add_edge(parent_id, primary_id)

    def __handle_htapp_special_case(self, parent_id_chunk, row):
        """Special case handling for HTAPP/DFCI."""
        if parent_id_chunk.startswith("Not Applicable"):
            try:
                parent_id_chunk = str(row[IdUtil.HTAN_PARENT_BIOSPECIMEN_ID])
            except KeyError:
                parent_id_chunk = "NOT_APPLICABLE"
        return parent_id_chunk

    def __gather_adjacent_edges(self, df, primary_id_col, adj_id_col):
        """Gather Adjacent Edges."""
        for index, row in df.iterrows():
            adj_id_chunk = str(row[adj_id_col])
            primary_id = str(row[primary_id_col])

            # We can have multiple adjacent nodes
            if adj_id_chunk != "nan":
                adj_id_chunk = adj_id_chunk.replace(";", " ").replace(",", " ")
                parts = adj_id_chunk.split()
                for part in parts:
                    adjacent_id = part.strip()
                    self._graph.add_adjacency_edge(primary_id, adjacent_id)
