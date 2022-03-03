"""Test Graph Util class."""
from hdash.validator import htan_validator
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

    node_map = {node1.id: node1, node2.id: node2}
    edge_list = [edge]

    graph_util = GraphUtil(node_map, edge_list)
    data_list = graph_util.data_list
    assert len(data_list) == 3


def test_real_graph():
    """Test Real Graph."""
    file_list = [
        "tests/data/demographics.csv",
        "tests/data/biospecimens.csv",
        "tests/data/single_cell_level1.csv",
        "tests/data/single_cell_level2.csv",
        "tests/data/single_cell_level3.csv",
        "tests/data/single_cell_level4.csv",
    ]
    validator = htan_validator.HtanValidator("HTA3", file_list)
    graph_util = GraphUtil(validator.get_node_map(), validator.get_edge_list())
    data_list = graph_util.data_list
    assert len(data_list) == 383

    sif_list = graph_util.sif_list
    assert sif_list[0][0] == "D_HTA3_8001"
    assert sif_list[0][1] == "B_HTA3_8001_1001"
