"""Test HTAN Validator class."""
from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.table_util import TableUtil
from hdash.util.heatmap_util import HeatMapUtil


def test_heatmap_util(sample_meta_map):
    """Test HeatMap Util."""
    meta_map = sample_meta_map
    graph_creator = GraphCreator("HTA1", meta_map)
    graph_flat = GraphFlattener(graph_creator.htan_graph)

    stats = CompletenessSummary("HTA1", meta_map, graph_flat)

    # Run HeatMap Util
    heatmap_util = HeatMapUtil("HTA1", stats)

    heatmaps = heatmap_util.heatmaps
    assert len(heatmaps) == 6
    data0 = heatmaps[0].data
    data1 = heatmaps[1].data
    data2 = heatmaps[2].data

    # Validate Clinical Tiers 1,2
    assert data0[0][0] == "HTA3_8001"
    assert data0[0][1] == 1

    # Validate Clinical Tier 3
    assert data1[0][0] == "HTA3_8001"
    assert data1[0][1] == 0

    # Validate Single Cell Data
    assert data2[0][0] == "HTA3_8001_001"
    assert data2[0][1] == 1
    assert data2[0][2] == 1
    assert data2[0][3] == 1
    assert data2[0][4] == 1
