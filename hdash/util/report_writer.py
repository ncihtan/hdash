"""Report Writer."""
from datetime import datetime
import humanize
from jinja2 import Environment, PackageLoader, select_autoescape

from hdash.validator.categories import Categories


class ReportWriter:
    """Report Writer."""

    def __init__(self, project_list):
        """Create new Report Writer."""
        self.atlas_html_map = {}
        self.index_html = None
        self.matrix_html_map = {}
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
        self._generate_matrix_pages()

    def _generate_index_html(self):
        template = self.env.get_template("index.html")
        storage_human = humanize.naturalsize(self.total_storage)
        self.index_html = template.render(
            now=self.dt,
            p_list=self.p_list,
            storage_human=storage_human,
        )

    def _generate_atlas_pages(self):
        for project in self.p_list:
            project.meta_list = sorted(project.meta_list, key=lambda d: d.category)
            template = self.env.get_template("atlas.html")
            html = template.render(now=self.dt, project=project)
            self.atlas_html_map[project.atlas_id] = html

    def _generate_matrix_pages(self):
        for project in self.p_list:
            current_map = {}
            if len(project.meta_list) > 0:
                for heatmap in project.heatmap_list:
                    template = self.env.get_template("matrix.html")
                    html = template.render(
                        now=self.dt, project=project, heatmap=heatmap
                    )
                    current_map[heatmap.id] = html
            self.matrix_html_map[project.id] = current_map

    def _get_template_env(self):
        return Environment(
            loader=PackageLoader("hdash", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
