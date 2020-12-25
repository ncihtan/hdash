"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil
import logging
import click
import os.path
import synapseclient
from hdash.synapse.credentials import SynapseCredentials

MASTER_HTAN_ID = "syn20446927"
MASTER_PROJECT_TABLE = "config/htan_projects.csv"
MASTER_HTAN_TABLE = "cache/master_htan.csv"


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

    if not use_cache or not os.path.exists(MASTER_HTAN_TABLE):
        _get_master_htan_table()

    table_util = TableUtil()
    project_list = table_util.get_project_list(MASTER_PROJECT_TABLE)
    table_util.annotate_project_list(project_list, MASTER_HTAN_TABLE)
    _write_html(project_list)


def _get_master_htan_table():
    syn = synapseclient.Synapse()
    credentials = SynapseCredentials()
    syn.login(credentials.user, credentials.password)
    master_htan_table = syn.tableQuery("SELECT * FROM %s" % MASTER_HTAN_ID)
    df = master_htan_table.asDataFrame()
    df.to_csv(MASTER_HTAN_TABLE)


def _write_html(project_list):
    if not os.path.exists("deploy"):
        os.makedirs("deploy")
    out_name = "deploy/index.html"
    print("Writing to:  %s." % out_name)
    report_writer = ReportWriter(project_list)
    fd = open(out_name, "w")
    fd.write(report_writer.get_html())
    fd.close()
