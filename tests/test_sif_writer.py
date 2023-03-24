"""Test Graph Creator."""
from hdash.graph.graph_creator import GraphCreator
from hdash.graph.sif_writer import SifWriter


def test_sif_writer(sample_meta_map):
    """Test SIF Writer."""
    meta_map = sample_meta_map
    graph_creator = GraphCreator("HTA1", meta_map)
    directed_graph = graph_creator.htan_graph.directed_graph
    sif_writer = SifWriter(directed_graph)

    # Check for Specific Edges
    sif = sif_writer.sif
    assert "B_HTA3_8001_002\tconnect\tSC1_HTA3_8001_4651918348" in sif
    assert "B_HTA3_8001_001	connect	SC1_HTA3_8001_7837535366" in sif
