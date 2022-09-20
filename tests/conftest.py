"""PyTest Fixtures."""
import pytest
from hdash.synapse.htan_project import HTANProject, MetaFile


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
