"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.graph.graph_util import GraphUtil
import logging
import emoji
import click
import os.path
import time
import subprocess
import pandas as pd
from datetime import datetime

from hdash.stats import stats_summary
from hdash.synapse.synapse_util import SynapseUtil
from hdash.google.gsheet_util import GoogleSheetUtil
from hdash.util.heatmap_util import HeatMapUtil
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil
from hdash.validator.htan_validator import HtanValidator
from synapseclient.core.exceptions import SynapseHTTPError

# Local Project Table, Used when google option is not enabled.
MASTER_PROJECT_TABLE = "config/htan_projects.csv"
SLEEP_INTERVAL = 7200  # 2 hours


@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose mode")
def cli(verbose):
    """Run HTAN Dashboard Builder."""
    log_level = logging.FATAL
    if verbose:
        log_level = logging.INFO
        log_file_name = "hdash.log"
        print(f"Logging to:  {log_file_name}.")
        logging.basicConfig(filename=log_file_name, filemode='w', level=log_level, format="%(levelname)s:%(message)s")
    else:
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

    if not os.path.exists("deploy"):
        os.makedirs("deploy")
    if not os.path.exists("deploy/images"):
        os.makedirs("deploy/images")

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

    # Annotate all HTAN projects with files obtained from Synapse.
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
        for meta_file in project.meta_list:
            table_util.annotate_meta_file(meta_file)
        validator = HtanValidator(project.atlas_id, project.meta_list)
        project.validation_list = validator.get_validation_list()
        node_map = validator.get_node_map()
        edge_list = validator.get_edge_list()
        graph_util = GraphUtil(node_map, edge_list)
        project.data_list = graph_util.data_list
        project.node_map = validator.get_node_map()
        project.sif_list = graph_util.sif_list
        assays_2_biospecimens = graph_util.assays_2_biospecimens
        stats = stats_summary.StatsSummary(
            project.atlas_id, validator.meta_map, assays_2_biospecimens
        )
        project.participant_id_set = stats.participant_id_set
        project.df_stats_map = stats.df_stats_map
        project.participant_2_biopsecimens = graph_util.participant_2_biopsecimens
        project.assays_2_biospecimens = graph_util.assays_2_biospecimens
        heatmap_util = HeatMapUtil(project)
        project.heatmap_list = heatmap_util.heatmaps

    _write_html(p_list)

    if surge:
        output_header("Deploying to Surge...")
        _deploy_with_surge()

    if google:
        output_header("Appending to Google Sheet...")
        gsheet_util.write(p_list)

    output_header(emoji.emojize("Done! :beer:", use_aliases=True))


def _write_html(project_list):
    report_writer = ReportWriter(project_list)
    _write_index_html(report_writer)
    _write_atlas_html(report_writer)
    _write_matrix_html(report_writer)
    _write_atlas_cytoscape_json_sif(project_list)


def _write_index_html(report_writer):
    out_name = "deploy/index.html"
    output_message("Writing to:  %s." % out_name)
    fd = open(out_name, "w")
    fd.write(report_writer.index_html)
    fd.close()
    return report_writer


def _write_atlas_html(report_writer):
    atlas_html_map = report_writer.atlas_html_map
    for atlas_id in atlas_html_map:
        html = atlas_html_map[atlas_id]
        out_name = "deploy/%s.html" % atlas_id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write(html)
        fd.close()


def _write_matrix_html(report_writer):
    matrix_html_map = report_writer.matrix_html_map
    for atlas_id in matrix_html_map:
        for heatmap_id, html in matrix_html_map[atlas_id].items():
            out_name = "deploy/%s.html" % heatmap_id
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


def _write_atlas_cytoscape_json_sif(project_list):
    for project in project_list:
        out_name = "deploy/%s_network.sif" % project.atlas_id
        output_message("Writing to:  %s." % out_name)
        sif_list = project.sif_list
        fd = open(out_name, "w")
        for edge in sif_list:
            fd.write("%s\tconnect\t%s\n" % (edge[0], edge[1]))
        fd.close()

        out_name = "deploy/%s_nodes.txt" % project.atlas_id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write("ID\tCATEGORY\n")
        for key in project.node_map:
            node = project.node_map[key]
            fd.write("%s\t%s\n" % (node.sif_id, node.category))
        fd.close()
