"""Test HTAN Validator class."""
from hdash.stats.meta_summary import MetaDataSummary
from hdash.synapse.meta_map import MetaMap
import pytest


def test_meta_summary(sample_meta_map: MetaMap):
    """Test Meta Summary."""
    meta_map = sample_meta_map
    meta_list = meta_map.meta_list_sorted
    MetaDataSummary(meta_list)
    assert meta_list[0].percent_meta_data_complete == pytest.approx(0.427, 0.01)
    assert meta_list[2].percent_meta_data_complete == pytest.approx(0.82, 0.01)
