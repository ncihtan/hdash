"""Test Graph Util class."""
import networkx as nx
import matplotlib.pyplot as plt
from hdash.validator import htan_validator
from hdash.graph.graph_util import GraphUtil
from hdash.graph.graph import Node, Edge
from hdash.validator.categories import Categories
from hdash.synapse.table_util import TableUtil
from hdash.synapse.meta_file import MetaFile


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

    path_list = [
        "tests/data/demographics.csv",
        "tests/data/biospecimens.csv",
        "tests/data/single_cell_level1.csv",
        "tests/data/single_cell_level2.csv",
        "tests/data/single_cell_level3.csv",
        "tests/data/single_cell_level4.csv",
    ]
    meta_file_list = []
    tableUtil = TableUtil()
    for path in path_list:
        meta_file = MetaFile()
        meta_file.path = path
        tableUtil.annotate_meta_file(meta_file)
        meta_file_list.append(meta_file)

    validator = htan_validator.HtanValidator("HTA3", meta_file_list)
    graph_util = GraphUtil(validator.get_node_map(), validator.get_edge_list())
    data_list = graph_util.data_list
    assert len(data_list) == 483

    sif_list = graph_util.sif_list
    assert sif_list[0][0] == "D_HTA3_8001"
    assert sif_list[0][1] == "B_HTA3_8001_001"

    # Verify Participant Set
    participant_ids = graph_util.participant_id_set
    assert len(participant_ids) == 6

    # Verify Biospecimen Set
    biospecimen_ids = graph_util.participant_2_biopsecimens["HTA3_8001"]
    assert len(biospecimen_ids) == 2
    assert biospecimen_ids[0] == "HTA3_8001_001"
    assert biospecimen_ids[1] == "HTA3_8001_002"

    # Verify Downstream Assays are Linked to Parent Biospecimens
    biospecimens_2_assays = graph_util.assays_2_biospecimens
    assert biospecimens_2_assays["HTA3_8001_4651918348"] == "HTA3_8001_002"
    assert biospecimens_2_assays["HTA3_8001_3257504874"] == "HTA3_8001_002"
