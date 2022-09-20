"""Test Report Writer."""
from hdash.util.report_writer import ReportWriter


def test_report_writer(init_annotated_project_list):
    """Test Report Writer."""
    report_writer = ReportWriter(init_annotated_project_list)
    html = report_writer.index_html
    assert html.index("Vesteinn") > 0

    atlas_html_map = report_writer.atlas_html_map
    assert len(atlas_html_map) == 3
    atlas_html = atlas_html_map["HTA1"]
    assert atlas_html.index("No metadata detected") > 0
