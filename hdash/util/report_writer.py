"""Report Writer."""
from datetime import datetime
import humanize
from jinja2 import Environment, PackageLoader, select_autoescape

from hdash.validator.categories import Categories


class ReportWriter:
    """Report Writer."""

    def __init__(self, project_list):
        """Create new Report Writer."""
        self.categories = Categories()
        self.p_list = project_list
        self.total_storage = 0
        for project in self.p_list:
            num_errors = 0
            self.total_storage += project.get_total_file_size()
            validation_list = project.validation_list
            for validation in validation_list:
                num_errors += len(validation.error_list)
            project.num_errors = num_errors

        self.env = self._get_template_env()
        self.now = datetime.now()
        self.dt = self.now.strftime("%m/%d/%Y %H:%M:%S")
        self._generate_index_html()
        self._generate_atlas_pages()
        self._generate_atlas_cytoscape_pages()

    def get_index_html(self):
        """Get Index HTML."""
        return self.index_html

    def get_atlas_html_map(self):
        """Get HTML for Atlases."""
        return self.atlas_html_map

    def get_atlas_cytoscape_html_map(self):
        """Get Cytoscape HTML for Atlases."""
        return self.atlas_cytoscape_html_map

    def _generate_index_html(self):
        template = self.env.get_template("index.html")
        storage_human = humanize.naturalsize(self.total_storage)
        self.index_html = template.render(
            now=self.dt,
            p_list=self.p_list,
            storage_human=storage_human,
        )

    def _generate_atlas_pages(self):
        self.atlas_html_map = {}
        for project in self.p_list:
            template = self.env.get_template("atlas.html")
            html = template.render(
                now=self.dt,
                project=project,
                clinical_tier1_2=self.categories.clinical_tier1_2_list,
                clinical_tier3=self.categories.clinical_tier3_list,
            )
            self.atlas_html_map[project.id] = html

    def _generate_atlas_cytoscape_pages(self):
        self.atlas_cytoscape_html_map = {}
        for project in self.p_list:
            if len(project.meta_list) > 0:
                template = self.env.get_template("atlas_cytoscape.html")
                html = template.render(now=self.dt, project=project)
                self.atlas_cytoscape_html_map[project.id] = html

    def _get_template_env(self):
        return Environment(
            loader=PackageLoader("hdash", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
