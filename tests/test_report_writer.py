"""Test Report Writer."""
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil


def test_report_writer():
    """Test Report Writer."""
    table_util = TableUtil()
    project_list = table_util.get_project_list("tests/data/projects.csv")
    table_util.annotate_project_list(project_list, "tests/data/files.csv")
    report_writer = ReportWriter(project_list)
    html = report_writer.get_index_html()
    assert html.index("Niki and Ino are actively coordinating") > 0

    atlas_html_map = report_writer.get_atlas_html_map()
    assert len(atlas_html_map) == 1
    atlas_html = atlas_html_map["syn21050481"]
    assert atlas_html.index("Metadata Files Detected") > 0
