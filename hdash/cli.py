"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.graph.graph_util import GraphUtil
import logging
import emoji
import click
import os.path
import time
import json
import subprocess
import pandas as pd
from shutil import copyfile
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

    for project in p_list:
        meta_file_list = []
        for meta_file in project.meta_list:
            meta_file_list.append(meta_file.path)
            table_util.annotate_meta_file(meta_file)
        validator = HtanValidator(project.atlas_id, meta_file_list)
        project.validation_list = validator.get_validation_list()
        node_map = validator.get_node_map()
        edge_list = validator.get_edge_list()
        graph_util = GraphUtil(node_map, edge_list)
        project.data_list = graph_util.data_list
        project.node_map = validator.get_node_map()
        project.sif_list = graph_util.sif_list

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
    _write_atlas_cytoscape_html(report_writer)
    _write_atlas_cytoscape_json_sif(project_list)


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


def _write_atlas_cytoscape_html(report_writer):
    copyfile("static/cy-style.json", "deploy/cy-style.json")
    atlas_html_map = report_writer.get_atlas_cytoscape_html_map()
    for id in atlas_html_map:
        html = atlas_html_map[id]
        out_name = "deploy/%s_cytoscape.html" % id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write(html)
        fd.close()


def _write_atlas_cytoscape_json_sif(project_list):
    for project in project_list:
        out_name = "deploy/%s_data.json" % project.id
        output_message("Writing to:  %s." % out_name)
        json_dump_str = json.dumps(project.data_list, indent=4)
        fd = open(out_name, "w")
        fd.write(json_dump_str)
        fd.close()

        out_name = "deploy/%s_network.sif" % project.id
        output_message("Writing to:  %s." % out_name)
        sif_list = project.sif_list
        fd = open(out_name, "w")
        for edge in sif_list:
            fd.write("%s\tconnect\t%s\n" % (edge[0], edge[1]))
        fd.close()

        out_name = "deploy/%s_nodes.txt" % project.id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write("ID\tCATEGORY\n")
        for key in project.node_map:
            node = project.node_map[key]
            fd.write("%s\t%s\n" % (node.sif_id, node.category))
        fd.close()


def output_header(msg):
    """Output header with emphasis."""
    click.echo(click.style(msg, fg="green"))


def output_message(msg):
    """Output message to console."""
    click.echo(msg)


def _deploy_with_surge():
    subprocess.run(["surge", "deploy", "http://htan_dashboard.surge.sh/"])
