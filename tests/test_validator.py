"""Test HTAN Validator class."""
from hdash.validator import htan_validator
from hdash.graph.graph_creator import GraphCreator
from hdash.synapse.meta_map import MetaMap
from conftest import _create_meta_file_list


def test_validator():
    """Test core HTAN Validator."""
    path_list = ["tests/data/demographics.csv", "tests/data/biospecimens.csv"]
    meta_file_list = _create_meta_file_list(path_list)

    # Create the MetaMap
    meta_map = MetaMap()
    for meta_file in meta_file_list:
        meta_map.add_meta_file(meta_file)

    # Create the Graph
    graph_creator = GraphCreator("HTA3", meta_map)
    htan_graph = graph_creator.htan_graph

    validator = htan_validator.HtanValidator("HTA3", meta_map, htan_graph)
    validation_list = validator.get_validation_list()

    assert len(validation_list) == 7
    assert validation_list[0].validation_passed()
    assert validation_list[1].validation_passed()
    assert validation_list[2].validation_passed()
    assert validation_list[3].validation_passed()
    assert validation_list[4].validation_passed()
    assert not validation_list[5].validation_passed()
    error_list = validation_list[5].error_list
    assert error_list[0].startswith(
        "HTA3_8001_001 references adjacent ID=HTA3_8001_1002"
    )
    assert validation_list[6].validation_passed()
