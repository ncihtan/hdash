"""Test HTAN Validator class."""
from hdash.graph.graph_util import GraphUtil
from hdash.validator import htan_validator
from hdash.stats import stats_summary


def test_stats_summary():
    """Test Summary Stats."""
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
    participant_id_set = stats.participant_id_set
    stats_map = stats.df_stats_map

    # Verify Participant ID Set
    assert "HTA3_8001" in participant_id_set
    assert "HTA3_8004" in participant_id_set

    # Verify Completeness of HTA3_8001:Demographics
    # 44% is based on manual inspection of HTA3_8001
    assert stats_map.get("HTA3_8001:Demographics") == "44%"

    # Verify Completeness of HTA3_8004:Demographics
    # 38% is based on manual inspection of HTA3_8004
    assert stats_map.get("HTA3_8004:Demographics") == "38%"

    # Verify Completeness of HTA3_8001_001:Biospecimen
    assert stats_map.get("HTA3_8001_001:Biospecimen") == "63%"

    # Verify Completeness of Downstream Assays
    assert stats_map.get("HTA3_8001_001:ScRNA-seqLevel1") == "82%"
    assert stats_map.get("HTA3_8001_001:ScRNA-seqLevel2") == "67%"
    assert stats_map.get("HTA3_8001_001:ScRNA-seqLevel3") == "79%"
    assert stats_map.get("HTA3_8001_001:ScRNA-seqLevel4") == "80%"
