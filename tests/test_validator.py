"""Test HTAN Validator class."""
from hdash.validator import htan_validator
from hdash.synapse.table_util import TableUtil
from hdash.synapse.meta_file import MetaFile

def test_validator():
    """Test core HTAN Validator."""
    path_list = ["tests/data/demographics.csv", "tests/data/biospecimens.csv"]
    meta_file_list = _create_meta_file_list(path_list)
    validator = htan_validator.HtanValidator("HTA3", meta_file_list)
    validation_list = validator.get_validation_list()

    assert len(validation_list) == 7
    assert validation_list[0].validation_passed()
    assert validation_list[1].validation_passed()
    assert validation_list[2].validation_passed()
    assert validation_list[3].validation_passed()
    assert validation_list[4].validation_passed()
    assert not validation_list[5].validation_passed()
    error_list = validation_list[5].error_list
    assert error_list[0].startswith("Biospecimen references adjacent ID: ")
    assert validation_list[6].validation_passed()


def test_graph():
    """Test Links and Graph Creation."""
    path_list = [
        "tests/data/demographics.csv",
        "tests/data/biospecimens.csv",
        "tests/data/single_cell_level1.csv",
        "tests/data/single_cell_level2.csv",
        "tests/data/single_cell_level3.csv",
        "tests/data/single_cell_level4.csv",
    ]
    meta_file_list = _create_meta_file_list(path_list)

    validator = htan_validator.HtanValidator("HTA3", meta_file_list)
    node_map = validator.get_node_map()
    edge_list = validator.get_edge_list()
    assert len(node_map) == 213
    assert len(edge_list) == 270


def _create_meta_file_list(path_list: list[str]):
    meta_file_list = []
    tableUtil = TableUtil()
    for path in path_list:
        meta_file = MetaFile()
        meta_file.path = path
        tableUtil.annotate_meta_file(meta_file)
        meta_file_list.append(meta_file)
    return meta_file_list