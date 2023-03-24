"""PyTest Fixtures."""
import pytest
from hdash.synapse.htan_project import HTANProject
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.table_util import TableUtil


@pytest.fixture
def init_project_list():
    """Init project list."""
    return _init_project_list()


@pytest.fixture
def init_annotated_project_list():
    """Init annotated project list."""
    project_list = _init_project_list()
    project = project_list[2]
    project.num_meta = 1
    meta_file = MetaFile()
    meta_file.id = "syn2105048111"
    project.meta_list.append(meta_file)
    return project_list

@pytest.fixture
def sample_meta_map():
    path_list = [
        "tests/data/demographics.csv",
        "tests/data/biospecimens.csv",
        "tests/data/single_cell_level1.csv",
        "tests/data/single_cell_level2.csv",
        "tests/data/single_cell_level3.csv",
        "tests/data/single_cell_level4.csv",
    ]
    meta_file_list = _create_meta_file_list(path_list)

    meta_map = MetaMap()
    for meta_file in meta_file_list:
        meta_map.add_meta_file(meta_file)
    return meta_map

def _create_meta_file_list(path_list: list[str]):
    meta_file_list = []
    tableUtil = TableUtil()
    synapse_id = 1
    for path in path_list:
        meta_file = MetaFile()
        meta_file.path = path
        meta_file.id = f"synapse_{synapse_id}"
        tableUtil.annotate_meta_file(meta_file)
        meta_file_list.append(meta_file)
        synapse_id += 1
    return meta_file_list


def _init_project_list():
    project_list = []

    project_list.append(_create_project("syn23448901", "HTA1", "HTAN MSKCC"))
    project_list.append(_create_project("syn22093319", "HTA2", "HTAN OHSU"))
    project_list.append(
        _create_project(
            "syn21050481",
            "HTA3",
            "HTAN Vanderbilt",
            "Vesteinn",
            "Vesteinn coordinating with XXX.",
        )
    )
    return project_list


def _create_project(id, atlas_id, name, liaison=None, notes=None):
    project = HTANProject()
    project.id = id
    project.atlas_id = atlas_id
    project.name = name
    project.liaison = liaison
    project.notes = notes
    return project
