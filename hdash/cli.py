"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.graph.graph_flattener import GraphFlattener
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
from hdash.util.heatmap_util import HeatMapUtil
from hdash.util.report_writer import ReportWriter
from hdash.synapse.table_util import TableUtil
from hdash.validator.htan_validator import HtanValidator
from synapseclient.core.exceptions import SynapseHTTPError
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile
from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.graph.sif_writer import SifWriter
from hdash.stats.meta_summary import MetaDataSummary
from hdash.synapse.htan_project import HTANProject
from hdash.validator.htan_validator import ValidationRule


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
        logging.basicConfig(
            filename=log_file_name,
            filemode="w",
            level=log_level,
            format="%(levelname)s:%(message)s",
        )
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


@cli.command()
def mock():
    """Create Mock HTML Reports."""
    print("Creating Mock HTML Reports")
    report_writer = ReportWriter(_create_mock_project_list())
    _write_index_html(report_writer)
    _write_atlas_html(report_writer)


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
        # Create the Meta Map
        for meta_file in project.meta_list:
            table_util.annotate_meta_file(meta_file)
        meta_map = MetaMap()
        for meta_file in project.meta_list:
            meta_map.add_meta_file(meta_file)

        # Create the Graph and Completeness Stats
        graph_creator = GraphCreator(project.atlas_id, meta_map)
        flat_graph = GraphFlattener(graph_creator.htan_graph)
        completeness_stats = CompletenessSummary(project.atlas_id, meta_map, flat_graph)

        # Validate
        validator = HtanValidator(project.atlas_id, meta_map, graph_creator.htan_graph)

        # Create the Heat Maps
        heatmap_util = HeatMapUtil(project.atlas_id, completeness_stats)

        # Create the Network SIF
        sif_writer = SifWriter(graph_creator.htan_graph.directed_graph)
        project.sif = sif_writer.sif

        # Assess Metadata Completeness
        meta_summary = MetaDataSummary(meta_map.meta_list_sorted)

        # Store for later reference
        project.meta_map = meta_map
        project.flat_graph = flat_graph
        project.completeness_stats = completeness_stats
        project.validation_list = validator.get_validation_list()
        project.heatmap_list = heatmap_util.heatmaps
        project.percent_meta_data_complete = meta_summary.get_overall_percent_complete()

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
    _write_atlas_sif(project_list)


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


def _write_atlas_sif(project_list):
    for project in project_list:
        out_name = "deploy/%s_network.sif" % project.atlas_id
        output_message("Writing to:  %s." % out_name)
        fd = open(out_name, "w")
        fd.write(project.sif)
        fd.close()


def _create_mock_project_list():
    """Create mock project list."""
    project_list = []

    project_list.append(_create_mock_project("syn23448901", "HTA1", "HTAN MSKCC"))
    project_list.append(_create_mock_project("syn22093319", "HTA2", "HTAN OHSU"))
    project_list.append(
        _create_mock_project(
            "syn21050481",
            "HTA3",
            "HTAN Vanderbilt",
            "Vesteinn",
            "Vesteinn coordinating with XXX.",
        )
    )
    return project_list


def _create_mock_project(id, atlas_id, name, liaison="Ethan Cerami", notes=None):
    project = HTANProject()
    project.id = id
    project.size_fastq = 100000000000
    project.num_fastq = 10000
    project.atlas_id = atlas_id
    project.name = name
    project.liaison = liaison
    project.notes = notes

    validation_rule = ValidationRule("MOCK", "MOCK_VALIDATION")
    validation_rule.add_error_message("Error 1")
    validation_rule.add_error_message("Error 2")
    validation_rule.add_error_message("Error 3")
    project.validation_list = [validation_rule]

    meta_file = MetaFile()
    meta_file.id = "synapse1"
    meta_file.num_items = 4
    meta_file.percent_meta_data_complete = 0.3
    project.meta_list = [meta_file]
    project.percent_meta_data_complete = 0.3

    return project
