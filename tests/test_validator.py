"""Test HTAN Validator class."""
from hdash.validator import htan_validator


def test_validator():
    """Test core HTAN Validator."""
    file_list = []
    file_list.append("tests/data/demographics.csv")
    file_list.append("tests/data/biospecimens.csv")
    validator = htan_validator.HtanValidator("HTA3", file_list)
    validation_list = validator.get_validation_list()
    assert len(validation_list) == 5
    assert validation_list[0].validation_passed is True
    assert validation_list[1].validation_passed is True
    assert validation_list[2].validation_passed is True
    assert validation_list[3].validation_passed is True
    assert validation_list[4].validation_passed is False
    error_list = validation_list[4].error_list
    assert error_list[0].startswith("Biospecimen references adjacent ID: ")


def test_graph():
    """Test Links and Graph Creation."""
    file_list = []
    file_list.append("tests/data/demographics.csv")
    file_list.append("tests/data/biospecimens.csv")
    file_list.append("tests/data/single_cell_level1.csv")
    file_list.append("tests/data/single_cell_level2.csv")
    file_list.append("tests/data/single_cell_level3.csv")
    file_list.append("tests/data/single_cell_level4.csv")
    validator = htan_validator.HtanValidator("HTA3", file_list)
    node_map = validator.get_node_map()
    edge_list = validator.get_edge_list()
    assert len(node_map) == 213
    assert len(edge_list) == 170
