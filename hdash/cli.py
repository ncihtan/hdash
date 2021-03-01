"""Command Line Interface (CLI) for generating HTAN Dashboard."""
import logging
import emoji
import click
import os.path
import time
import subprocess
import pandas as pd
from datetime import datetime
from hdash.synapse.synapse_util import SynapseUtil
from hdash.google.gsheet_util import GoogleSheetUtil
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil
from hdash.validator.htan_validator import HtanValidator
from synapseclient.core.exceptions import SynapseHTTPError

MASTER_PROJECT_TABLE = "config/htan_projects.csv"
SLEEP_INTERVAL = 7200  # 2 hours


@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose mode")
def cli(verbose):
    """Run HTAN Dashboard Builder."""
    log_level = logging.FATAL
    if verbose:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s:%(message)s")


@cli.command()
@click.option("--use_cache", is_flag=True, help="Use Local Synapse Cache.")
@click.option("--repeat", is_flag=True, help="Repeat every N hours.")
@click.option("--surge", is_flag=True, help="Deploy HTML with surge.")
@click.option("--google", is_flag=True, help="Read/write to Google sheets.")
def create(use_cache, repeat, surge, google):
    """Create HTML HTAN Dashboard."""
    if repeat:
        while True:
            _create_dashboard(use_cache, surge, google)
            time.sleep(SLEEP_INTERVAL)
    else:
        _create_dashboard(use_cache, surge, google)


def _create_dashboard(use_cache, surge, google):
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    output_header("Creating HTAN Dashboard:  %s" % dt)
    if not use_cache:
        output_message("Connecting to Synapse...")
        synapse_util = SynapseUtil(use_cache)
    if google:
        output_message("Connecting to Google...")
        gsheet_util = GoogleSheetUtil()

    if not use_cache or not os.path.exists(SynapseUtil.MASTER_HTAN_TABLE):
        synapse_util.retrieve_master_htan_table()

    table_util = TableUtil()
    project_df = pd.read_csv(MASTER_PROJECT_TABLE)
    if google:
        project_df = gsheet_util.project_df
    p_list = table_util.get_project_list(project_df)
    table_util.annotate_project_list(p_list, SynapseUtil.MASTER_HTAN_TABLE)

    if not use_cache:
        for project in p_list:
            for meta_file in project.meta_list:
                try:
                    output_message("Downloading file:  %s" % meta_file.id)
                    meta_file.path = synapse_util.retrieve_file(meta_file.id)
                except SynapseHTTPError:
                    output_message("Could not retrieve:  %s" % meta_file.id)

    meta_file_list = []
    for project in p_list:
        for meta_file in project.meta_list:
            meta_file_list.append(meta_file.path)
            table_util.annotate_meta_file(meta_file)
        validator = HtanValidator(project.atlas_id, meta_file_list)
        project.validation_list = validator.get_validation_list()

    _write_html(p_list)

    if surge:
        output_header("Deploying to Surge...")
        _deploy_with_surge()

    if google:
        output_header("Appending to Google Sheet...")
        gsheet_util.write(p_list)

    output_header(emoji.emojize("Done! :beer:", use_aliases=True))


def _write_html(project_list):
    if not os.path.exists("deploy"):
        os.makedirs("deploy")
    report_writer = ReportWriter(project_list)
    _write_index_html(report_writer)
    _write_atlas_html(report_writer)


def _write_index_html(report_writer):
    out_name = "deploy/index.html"
    output_message("Writing to:  %s." % out_name)
    fd = open(out_name, "w")
    fd.write(report_writer.get_index_html())
    fd.close()
    return report_writer


def _write_atlas_html(report_writer):
    atlas_html_map = report_writer.get_atlas_html_map()
    for id in atlas_html_map:
        html = atlas_html_map[id]
        out_name = "deploy/%s.html" % id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write(html)
        fd.close()


def output_header(msg):
    """Output header with emphasis."""
    click.echo(click.style(msg, fg="green"))


def output_message(msg):
    """Output message to console."""
    click.echo(msg)


def _deploy_with_surge():
    subprocess.run(["surge", "deploy", "http://htan_dashboard.surge.sh/"])
