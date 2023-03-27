"""HTAN Graph."""
import networkx as nx
from hdash.graph.node_data import NodeData
from hdash.validator.categories import Categories


class HtanGraph:
    """HTAN Graph.

    This class leverages the networkx Python package.
    """

    DATA_KEY = "data"

    def __init__(self):
        """Default Constructor."""
        self.directed_graph = nx.DiGraph()
        self.edge_list = []
        self.adjacent_list = []
        self.participant_list = set()
        self.biospecimen_list = set()
        self._categories = Categories()

    def add_node(self, node_data: NodeData):
        """Add node to the graph."""
        self.directed_graph.add_node(node_data.id)
        self.directed_graph.nodes[node_data.id][self.DATA_KEY] = node_data

    def add_edge(self, source_id, target_id):
        """Add edge to the graph."""
        # Only Add the Edge if both nodes exist
        if (
            target_id in self.directed_graph.nodes
            and source_id in self.directed_graph.nodes
        ):
            self.directed_graph.add_edge(source_id, target_id)

        # Store all the original edges for later validation
        self.edge_list.append([source_id, target_id])

    def add_adjacency_edge(self, source_id, target_id):
        """Add adjacency edge to its own list."""
        self.adjacent_list.append([source_id, target_id])

    def __repr__(self):
        """Get edge summary."""
        return "HTAN Graph [%s nodes, %s edges]" % (
            len(self.directed_graph.nodes),
            len(self.directed_graph.edges),
        )
