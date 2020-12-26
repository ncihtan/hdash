"""Command Line Interface (CLI) for generating HTAN Dashboard."""
import logging
import emoji
import click
import os.path
from hdash.synapse.synapse_util import SynapseUtil
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil

MASTER_PROJECT_TABLE = "config/htan_projects.csv"


@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose mode")
def cli(verbose):
    """Run HTAN Dashboard Builder."""
    log_level = logging.FATAL
    if verbose:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s:%(message)s")


@cli.command()
@click.option("--use_cache", is_flag=True, help="Use Local Synapse Cache")
def create(use_cache):
    """Create HTML HTAN Dashboard."""
    output_header("Creating HTAN Dashboard.")
    synapse_util = SynapseUtil()
    if not use_cache or not os.path.exists(SynapseUtil.MASTER_HTAN_TABLE):
        synapse_util.retrieve_master_htan_table()

    table_util = TableUtil()
    p_list = table_util.get_project_list(MASTER_PROJECT_TABLE)
    table_util.annotate_project_list(p_list, SynapseUtil.MASTER_HTAN_TABLE)

    for project in p_list:
        for meta_file in project.meta_list:
            meta_file.path = synapse_util.retrieve_file(meta_file.id)
            table_util.annotate_meta_file(meta_file)

    _write_html(p_list)
    output_header(emoji.emojize("Done! :beer:", use_aliases=True))


def _write_html(project_list):
    if not os.path.exists("deploy"):
        os.makedirs("deploy")
    report_writer = ReportWriter(project_list)
    _write_index_html(report_writer)
    _write_atlas_html(report_writer)


def _write_index_html(report_writer):
    out_name = "deploy/index.html"
    print("Writing to:  %s." % out_name)
    fd = open(out_name, "w")
    fd.write(report_writer.get_index_html())
    fd.close()
    return report_writer


def _write_atlas_html(report_writer):
    atlas_html_map = report_writer.get_atlas_html_map()
    for id in atlas_html_map:
        html = atlas_html_map[id]
        out_name = "deploy/%s.html" % id
        print("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write(html)
        fd.close()


def output_header(msg):
    """Output header with emphasis."""
    click.echo(click.style(msg, fg="green"))
