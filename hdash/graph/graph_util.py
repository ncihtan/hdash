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
        self.__init_participants_to_biospecimens()
        self.__init_biospecimens_to_assays()

    def __init_networkx(self):
        self.graph = nx.DiGraph()
        for node_id, node in self.node_map.items():
            self.graph.add_node(node_id)

        for edge in self.edge_list:
            self.graph.add_edge(edge.source_id, edge.target_id)

    def __init_participants_to_biospecimens(self):
        """Determine Participant IDs and all Downstream Biospecimen IDs."""
        self.participant_ids = []
        self.biospecimen_ids = []
        self.participant_2_biopsecimens = {}
        for node_id, node in self.node_map.items():
            if node.category == self.categories.DEMOGRAPHICS:
                self.participant_ids.append(node_id)
        for participant_id in self.participant_ids:
            current_biospecimen_ids = list(self.graph.successors(participant_id))
            self.biospecimen_ids.extend(current_biospecimen_ids)
            self.participant_2_biopsecimens[participant_id] = current_biospecimen_ids

    def __init_biospecimens_to_assays(self):
        """For each biospecimen, identify all downstream assays."""
        self.biospecimens_2_assays = {}
        for biospecimen_id in self.biospecimen_ids:
            self.__downstream_nodes = []
            self.__walk_node(self.graph, biospecimen_id)
            category_map = {}
            for downstream_node in self.__downstream_nodes:
                category = self.node_map[downstream_node].category
                category_map[category] = 1
            self.biospecimens_2_assays[biospecimen_id] = category_map

    def __walk_node(self, graph, node_id):
        """Walk the graph and gather all downstream nodes."""
        successors = graph.successors(node_id)
        for successor in successors:
            self.__downstream_nodes.append(node_id)
            self.__walk_node(graph, successor)
