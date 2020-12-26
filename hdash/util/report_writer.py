"""Report Writer."""
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


class ReportWriter:
    """Report Writer."""

    def __init__(self, project_list):
        """Create new Report Writer."""
        self.p_list = project_list
        self.env = self._get_template_env()
        self.now = datetime.now()
        self.dt = self.now.strftime("%m/%d/%Y %H:%M:%S")
        self._generate_index_html()
        self._generate_atlas_pages()

    def get_index_html(self):
        """Get Index HTML."""
        return self.index_html

    def get_atlas_html_map(self):
        """Get HTML for Atlases."""
        return self.atlas_html_map

    def _generate_index_html(self):
        template = self.env.get_template("index.html")
        self.index_html = template.render(now=self.dt, p_list=self.p_list)

    def _generate_atlas_pages(self):
        self.atlas_html_map = {}
        for project in self.p_list:
            if len(project.meta_list) > 0:
                template = self.env.get_template("atlas.html")
                html = template.render(now=self.dt, project=project)
                self.atlas_html_map[project.id] = html

    def _get_template_env(self):
        return Environment(
            loader=PackageLoader("hdash", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
