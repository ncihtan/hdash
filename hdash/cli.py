"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.synapse.synapse_util import SynapseUtil
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil
import logging
import click
import os.path

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

    synapse_util = SynapseUtil()
    if not use_cache or not os.path.exists(SynapseUtil.MASTER_HTAN_TABLE):
        synapse_util.retrieve_master_htan_table()

    table_util = TableUtil()
    p_list = table_util.get_project_list(MASTER_PROJECT_TABLE)
    table_util.annotate_project_list(p_list, SynapseUtil.MASTER_HTAN_TABLE)
    _write_html(p_list)


def _write_html(project_list):
    if not os.path.exists("deploy"):
        os.makedirs("deploy")
    out_name = "deploy/index.html"
    print("Writing to:  %s." % out_name)
    report_writer = ReportWriter(project_list)
    fd = open(out_name, "w")
    fd.write(report_writer.get_html())
    fd.close()
