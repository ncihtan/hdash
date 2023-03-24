"""Graph Flattener Class."""
import networkx as nx
from natsort import natsorted
from hdash.graph.htan_graph import HtanGraph
from hdash.validator.categories import Categories
from hdash.graph.key import KeyUtil


class GraphFlattener:
    """Graph Flattener Class.

    Given an HTAN Graph, flatten it so that we can map:
    1) Participant --> All Derived Biospecimens.
    2) Biospecimen --> All Derived Assays.
    """

    def __init__(self, htan_graph: HtanGraph):
        """Default Constructor."""
        self.htan_graph = htan_graph
        self.directed_graph = htan_graph.directed_graph
        self.categories = Categories()
        self.participant_2_biopsecimens = {}
        self.biospecimen_2_assays = {}
        self.assay_map = set()
        self.__bin_nodes()
        self.__gather_downstream_biospecimens()
        self.__gather_downstream_assays()

    def biospecimen_has_assay(self, biospecimen_id, category):
        """Determine if the specified biospecimen has the specified assay."""
        key = KeyUtil.create_key(biospecimen_id, category)
        return key in self.assay_map

    def __bin_nodes(self):
        """Bin Participants and Biospecimens."""
        self.participant_id_set = set()
        self.biospecimen_id_set = set()
        for node_id in self.directed_graph.nodes:
            data = self.directed_graph.nodes[node_id][HtanGraph.DATA_KEY]
            category = data.meta_file.category
            if category == self.categories.DEMOGRAPHICS:
                self.participant_id_set.add(node_id)
            elif category in self.categories.biospecimen_list:
                self.biospecimen_id_set.add(node_id)

        # Sort the Participants
        self.participant_id_set = natsorted(self.participant_id_set)

    def __gather_downstream_biospecimens(self):
        """Given a Participant, find *all* Downstream Biospecimens."""
        for participant_id in self.participant_id_set:
            nodes = nx.descendants(self.directed_graph, participant_id)

            # Filter Descendents for Biospecimens Only
            filtered_list = self.__filter_nodes(nodes, self.categories.biospecimen_list)
            self.participant_2_biopsecimens[participant_id] = filtered_list

    def __gather_downstream_assays(self):
        """Given a Biospecimen, find *all* Downstream Assays."""
        for biospecimen_id in self.biospecimen_id_set:
            nodes = nx.descendants(self.directed_graph, biospecimen_id)

            # Filter Descendents for Assays Only
            filtered_list = self.__filter_nodes(nodes, self.categories.all_assays)
            self.biospecimen_2_assays[biospecimen_id] = filtered_list

            # Add to assay map for easy look-up
            for node_id in filtered_list:
                data = self.directed_graph.nodes[node_id][HtanGraph.DATA_KEY]
                key = KeyUtil.create_key(biospecimen_id, data.meta_file.category)
                self.assay_map.add(key)

    def __filter_nodes(self, nodes, target_categories):
        """Filter Node List to Only those in the Target Categories."""
        filtered_list = []
        for node_id in nodes:
            data = self.directed_graph.nodes[node_id][HtanGraph.DATA_KEY]
            if data.meta_file.category in target_categories:
                filtered_list.append(node_id)
        return filtered_list
