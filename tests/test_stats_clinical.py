"""Test HTAN Validator class."""
from hdash.validator import htan_validator
from hdash.stats import stats_clinical


def test_stats_clinical():
    """Test Clinical Data Stats."""
    file_list = ["tests/data/demographics.csv", "tests/data/biospecimens.csv"]
    validator = htan_validator.HtanValidator("HTA3", file_list)
    meta_map = validator.meta_map
    stats = stats_clinical.StatsClinical("HTA3", meta_map)
    participant_id_list = stats.participant_id_set
    participant_map = stats.participant_map
    assert "HTA3_8001" in participant_id_list
    assert "HTA3_8004" in participant_id_list
    assert "HTA3_8001:Demographics" in participant_map
    value = participant_map.get("HTA3_8001:Demographics")

    # 44% is based on manual inspection of HTA3_8001
    assert value == "44%"

    # 38% is based on manual inspection of HTA3_8004
    value = participant_map.get("HTA3_8004:Demographics")
    assert value == "38%"
