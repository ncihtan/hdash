"""Graph Util Class."""
import networkx as nx
from hdash.validator.categories import Categories


class GraphUtil:
    """Graph Utilities Class."""

    def __init__(self, node_map, edge_list):
        """Construct a new Graph Utility Class."""
        self.node_map = node_map
        self.edge_list = edge_list
        self.sif_list = []
        self.categories = Categories()
        self.participant_id_set = set()
        self.biospecimen_id_set = set()
        self.participant_2_biopsecimens = {}
        self.assays_2_biospecimens = {}
        abbrev_map = self.categories.abbrev_category_map

        self.data_list = []
        for node_id in node_map:
            node = node_map[node_id]
            node.sif_id = abbrev_map[node.category] + "_" + node.label
            current_node = {
                "id": node.id,
                "label": node.sif_id,
                "category": node.category,
            }
            node_dict = {"data": current_node}
            self.data_list.append(node_dict)

        edge_id = 0
        for edge in edge_list:
            current_edge = {
                "id": "e" + str(edge_id),
                "source": edge.source_id,
                "target": edge.target_id,
            }
            node_dict = {"data": current_edge}
            self.data_list.append(node_dict)

            s_node = self.node_map[edge.source_id]
            t_node = self.node_map[edge.target_id]
            self.sif_list.append([s_node.sif_id, t_node.sif_id])
            edge_id += 1
        self.__init_networkx()
        self.__gather_participants_biospecimens()
        self.__gather_downstream_assays()

    def __init_networkx(self):
        self.graph = nx.DiGraph()
        for node_id, node in self.node_map.items():
            self.graph.add_node(node_id)

        for edge in self.edge_list:
            self.graph.add_edge(edge.source_id, edge.target_id)

    def __gather_participants_biospecimens(self):
        """Gather Participant IDs and all Downstream Biospecimen IDs."""
        for node_id, node in self.node_map.items():
            if node.category == self.categories.DEMOGRAPHICS:
                self.participant_id_set.add(node_id)
        for participant_id in self.participant_id_set:
            self.__downstream_nodes = []
            self.__walk_non_assay_node(self.graph, participant_id)

            downstream_biospecimens = []
            for downstream_node in self.__downstream_nodes:
                downstream_biospecimens.append(downstream_node)

            for biospecimen_id in downstream_biospecimens:
                self.biospecimen_id_set.add(biospecimen_id)
            self.participant_2_biopsecimens[participant_id] = downstream_biospecimens

    def __gather_downstream_assays(self):
        """For each biospecimen, gather all downstream assays."""
        for biospecimen_id in self.biospecimen_id_set:
            self.__downstream_nodes = []
            self.__walk_node(self.graph, biospecimen_id)
            for downstream_id in self.__downstream_nodes:
                assay_id = self.node_map[downstream_id].id
                self.assays_2_biospecimens[assay_id] = biospecimen_id

    def __walk_node(self, graph, node_id):
        """Walk the graph and gather all downstream nodes."""
        successors = graph.successors(node_id)
        for successor_id in successors:
            node = self.node_map[successor_id]
            # if this is not a biospecimen, keeping walking
            if not node.sif_id.startswith("B"):
                self.__downstream_nodes.append(successor_id)
                self.__walk_node(graph, successor_id)

    def __walk_non_assay_node(self, graph, node_id):
        """Walk the graph and gather all downstream biospecimens."""
        successors = graph.successors(node_id)
        for successor_id in successors:
            node = self.node_map[successor_id]
            # if this is a biospecimen, keeping walking
            if node.sif_id.startswith("B"):
                self.__downstream_nodes.append(successor_id)
                self.__walk_non_assay_node(graph, successor_id)
