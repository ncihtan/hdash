"""SIF Writer."""
import networkx as nx
from hdash.graph.htan_graph import HtanGraph


class SifWriter:
    """SIF Network Writer for Cytoscape."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.sif = ""
        self._create_sif()


    def _create_sif(self):
        """Create the SIF Network."""
        edge_list = self.graph.edges
        for edge in edge_list:
            node0_id = edge[0]
            node1_id = edge[1]
            sif_id0 = self.graph.nodes[node0_id][HtanGraph.DATA_KEY].sif_id
            sif_id1 = self.graph.nodes[node1_id][HtanGraph.DATA_KEY].sif_id
            self.sif += f"{sif_id0}\tconnect\t{sif_id1}\n"
