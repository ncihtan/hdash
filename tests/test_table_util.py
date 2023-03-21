"""Test Table Utilities."""
import pandas as pd
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.table_util import TableUtil


def test_project_list():
    """Test Project List."""
    table_util = TableUtil()
    project_df = pd.read_csv("tests/data/projects.csv")
    project_list = table_util.get_project_list(project_df)
    assert len(project_list) == 4
    project0 = project_list[0]
    assert project0.id == "syn23448901"
    assert project0.name == "HTAN MSK"
    assert project0.liaison == "Niki"
    assert project0.notes.startswith("Niki and Ino are")


def test_project_annotation(init_project_list):
    """Test Project Annotation."""
    table_util = TableUtil()
    project_list = init_project_list
    table_util.annotate_project_list(project_list, "tests/data/files.csv")

    project0 = project_list[1]
    assert len(project0.meta_list) == 0

    project2 = project_list[2]
    assert project2.num_fastq == 31
    assert project2.num_bam == 0
    assert project2.num_image == 0
    assert project2.num_other == 0
    assert project2.num_matrix == 23
    assert project2.num_meta == 6
    assert len(project2.meta_list) == 6

    assert project2.size_fastq == 3100
    assert project2.size_bam == 0
    assert project2.size_image == 0
    assert project2.size_other == 0
    assert project2.size_matrix == 2300

    assert project2.meta_list[0].id == "syn23636452"
    assert project2.meta_list[1].id == "syn23636563"


def test_meta_file_annotation():
    """Test Meta File Annotation."""
    table_util = TableUtil()
    meta_file = MetaFile()
    meta_file.path = "tests/data/manifest.csv"
    table_util.annotate_meta_file(meta_file)
    assert meta_file.category == "Demographics"
    assert meta_file.num_items == 3
