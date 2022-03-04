"""Test Graph Util class."""
import networkx as nx
import matplotlib.pyplot as plt
from hdash.validator import htan_validator
from hdash.graph.graph_util import GraphUtil
from hdash.graph.graph import Node, Edge
from hdash.validator.categories import Categories


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
    categories = Categories()
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
    assert len(data_list) == 483

    sif_list = graph_util.sif_list
    assert sif_list[0][0] == "D_HTA3_8001"
    assert sif_list[0][1] == "B_HTA3_8001_001"

    participant_ids = graph_util.participant_ids
    assert len(participant_ids) == 6

    biospecimen_ids = graph_util.participant_2_biopsecimens["HTA3_8001"]
    assert len(biospecimen_ids) == 2
    assert biospecimen_ids[0] == "HTA3_8001_001"
    assert biospecimen_ids[1] == "HTA3_8001_002"

    biospecimens_2_assays = graph_util.biospecimens_2_assays
    category_map = biospecimens_2_assays["HTA3_8001_001"]
    assert len(category_map) == 4
    assert categories.BIOSPECIMEN in category_map
    assert categories.SC_RNA_SEQ_LEVEL_1 in category_map
    assert categories.SC_RNA_SEQ_LEVEL_2 in category_map
    assert categories.SC_RNA_SEQ_LEVEL_3 in category_map
