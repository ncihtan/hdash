"""Report Writer."""
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


class ReportWriter:
    """Report Writer."""

    def __init__(self, project_list):
        """Create new Report Writer."""
        self.project_list = project_list
        self.env = self._get_template_env()

    def get_html(self):
        """Generate HTML Report."""
        now = datetime.now()
        dt = now.strftime("%m/%d/%Y %H:%M:%S")
        template = self.env.get_template("index.html")
        html = template.render(timestamp=dt, project_list=self.project_list)
        return html

    def _get_template_env(self):
        return Environment(
            loader=PackageLoader("hdash", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
