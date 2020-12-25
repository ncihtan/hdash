"""Test Report Writer."""
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil


def test_report_writer():
    """Test Report Writer."""
    table_util = TableUtil()
    project_list = table_util.get_project_list("tests/data/projects.csv")
    table_util.annotate_project_list(project_list, "tests/data/files.csv")
    report_writer = ReportWriter(project_list)
    html = report_writer.get_html()
    assert html.index("Niki and Ino are actively coordinating") > 0
