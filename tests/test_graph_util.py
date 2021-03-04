"""Test Graph Util class."""
from hdash.validator import htan_validator
import json
from hdash.graph.graph_util import GraphUtil
from hdash.graph.graph import Node, Edge


def test_graph_util():
    """Test core Graph Utility Features."""
    node1 = Node()
    node1.id = "A111"
    node1.label = "A111 Node"
    node1.category = "Biospecimen"

    node2 = Node()
    node2.id = "A112"
    node2.label = "A112 Node"
    node2.category = "Biospecimen"

    edge = Edge()
    edge.source_id = node1.id
    edge.target_id = node2.id

    node_map = {}
    node_map[node1.id] = node1
    node_map[node2.id] = node2
    edge_list = []
    edge_list.append(edge)

    graph_util = GraphUtil(node_map, edge_list)
    data_list = graph_util.data_list
    assert len(data_list) == 4


def test_real_graph():
    """Test Real Graph."""
    file_list = []
    file_list.append("tests/data/demographics.csv")
    file_list.append("tests/data/biospecimens.csv")
    file_list.append("tests/data/single_cell_level1.csv")
    file_list.append("tests/data/single_cell_level2.csv")
    file_list.append("tests/data/single_cell_level3.csv")
    file_list.append("tests/data/single_cell_level4.csv")
    validator = htan_validator.HtanValidator("HTA3", file_list)
    graph_util = GraphUtil(validator.get_node_map(), validator.get_edge_list())
    data_list = graph_util.data_list
    assert len(data_list) == 553
