"""Test HTAN Validator class."""
from hdash.graph.graph_util import GraphUtil
from hdash.synapse.htan_project import HTANProject
from hdash.util.heatmap_util import HeatMapUtil
from hdash.validator import htan_validator
from hdash.stats import stats_summary
import seaborn as sns
import matplotlib.pyplot as plt
import pytest


def test_heatmap_util():
    """Test HeatMap Util."""
    file_list = [
        "tests/data/demographics.csv",
        "tests/data/biospecimens.csv",
        "tests/data/single_cell_level1.csv",
        "tests/data/single_cell_level2.csv",
        "tests/data/single_cell_level3.csv",
        "tests/data/single_cell_level4.csv",
    ]

    # Run Validator to Extract the Graph
    validator = htan_validator.HtanValidator("HTA3", file_list)
    meta_map = validator.meta_map
    graph_util = GraphUtil(validator.get_node_map(), validator.get_edge_list())
    assays_2_biospecimens = graph_util.assays_2_biospecimens

    # Run the Summary Stats
    stats = stats_summary.StatsSummary("HTA3", meta_map, assays_2_biospecimens)

    # Run HeatMap Util
    project = HTANProject()
    project.atlas_id = "HTA3"
    project.participant_id_set = stats.participant_id_set
    project.df_stats_map = stats.df_stats_map
    project.assays_2_biospecimens = assays_2_biospecimens
    project.participant_2_biopsecimens = graph_util.participant_2_biopsecimens
    heatmap_util = HeatMapUtil(project)
    heatmaps = heatmap_util.heatmaps
    assert len(heatmaps) == 5
    data0 = heatmaps[0].data
    data1 = heatmaps[1].data
    data2 = heatmaps[2].data
    assert data0[0][0] == "HTA3_8001"
    assert data0[0][1] == 0.4375
    assert data1[0][0] == "HTA3_8001"
    assert data1[0][1] == 0.0
    assert data2[0][0] == "HTA3_8001"
    assert data2[0][1] == "HTA3_8001_001"
    assert data2[0][2] == pytest.approx(0.63, 0.01)

