"""Test Graph Util class."""
from hdash.graph.htan_graph import HtanGraph
from hdash.graph.node_data import NodeData
from hdash.graph.graph_flattener import GraphFlattener
from hdash.validator.categories import Categories
from hdash.synapse.meta_file import MetaFile


def test_graph_flattener():
    """"Test Graph Flattener."""

    # Create Mock Graph
    htan_graph = HtanGraph()

    p1_meta_file = __create_mock_meta_file("synapse1", Categories.DEMOGRAPHICS)
    p1 = NodeData("p1", p1_meta_file)
    htan_graph.add_node(p1)

    b1_meta_file = __create_mock_meta_file("synapse2", Categories.BIOSPECIMEN)
    b1 = NodeData("b1", b1_meta_file)
    htan_graph.add_node(b1)

    b2_meta_file = __create_mock_meta_file("synapse3", Categories.BIOSPECIMEN)
    b2 = NodeData("b2", b2_meta_file)
    htan_graph.add_node(b2)

    b3_meta_file = __create_mock_meta_file("synapse4", Categories.BIOSPECIMEN)
    b3 = NodeData("b3", b3_meta_file)
    htan_graph.add_node(b3)

    s1_meta = __create_mock_meta_file("synapse5", Categories.SC_RNA_SEQ_LEVEL_1)
    s1 = NodeData("s1", s1_meta)
    htan_graph.add_node(s1)

    s2_meta = __create_mock_meta_file("synapse6", Categories.SC_RNA_SEQ_LEVEL_2)
    s2 = NodeData("s2", s2_meta)
    htan_graph.add_node(s2)

    s3_meta = __create_mock_meta_file("synapse7", Categories.SC_RNA_SEQ_LEVEL_3)
    s3 = NodeData("s3", s3_meta)
    htan_graph.add_node(s3)

    htan_graph.add_edge("p1", "b1")
    htan_graph.add_edge("p1", "b3")
    htan_graph.add_edge("b1", "b2")
    htan_graph.add_edge("b2", "s1")
    htan_graph.add_edge("s1", "s2")
    htan_graph.add_edge("s2", "s3")
    htan_graph.add_edge("b3", "s3")

    # Now Flatten
    graph_flat = GraphFlattener(htan_graph)

    # We should have 1 patient and 3 biospecimens
    assert len(graph_flat.participant_id_set) == 1
    assert len(graph_flat.biospecimen_id_set) == 3

    # p1 should point to b1, b2, b3
    biospecimen_list = graph_flat.participant_2_biopsecimens["p1"]
    assert len(biospecimen_list) == 3
    assert "b1" in biospecimen_list
    assert "b2" in biospecimen_list
    assert "b3" in biospecimen_list

    # b1 should point to s1, s2 and s3
    assay_list = graph_flat.biospecimen_2_assays["b1"]
    assert len(assay_list) == 3
    assert "s1" in assay_list
    assert "s2" in assay_list
    assert "s3" in assay_list

    # b1 should have SCRNA-Seq Levels 1-3
    categories = Categories()
    assert graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_1)
    assert graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_2)
    assert graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_3)


def __create_mock_meta_file(id, category):
    meta_file = MetaFile()
    meta_file.id = id
    meta_file.category = category
    return meta_file
