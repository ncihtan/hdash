"""Command Line Interface (CLI) for generating HTAN Dashboard."""
from hdash.synapse.file_counter import FileCounter
import logging
import click
import os.path
import pandas as pd
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
import synapseclient
from hdash.synapse.credentials import SynapseCredentials

MASTER_HTAN_ID = "syn20446927"
MASTER_PROJECT_TABLE = "config/htan_projects.csv"
MASTER_HTAN_TABLE = "cache/master_htan.csv"
DASHBOARD_FILE = "htan_dashboard.xlsx"


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
    """Create HTAN Dashboard."""

    if not use_cache or not os.path.exists(MASTER_HTAN_TABLE):
        _get_master_htan_table()

    project_df = _get_project_table()
    df = pd.read_csv(MASTER_HTAN_TABLE)

    cols = [
        "ATLAS",
        "FASTQ",
        "BAM",
        "IMAGE",
        "MATRIX",
        "OTHER",
        "METADATA",
        "LIAISON",
        "NOTES",
    ]
    results_df = pd.DataFrame(columns=cols)

    for index, row in project_df.iterrows():
        target_df = df[(df.projectId == row.id) & (df.type == "file")]
        file_list = target_df.name.to_list()
        file_counter = FileCounter(file_list)
        result_row = {
            "ATLAS": row["name"],
            "FASTQ": file_counter.get_num_files(FileCounter.BAM),
            "BAM": file_counter.get_num_files(FileCounter.FASTQ),
            "IMAGE": file_counter.get_num_files(FileCounter.IMAGE),
            "MATRIX": file_counter.get_num_files(FileCounter.MATRIX),
            "OTHER": file_counter.get_num_files(FileCounter.OTHER),
            "METADATA": file_counter.get_num_files(FileCounter.METADATA),
            "LIAISON": row["liaison"],
            "NOTES": row["notes"],
        }
        results_df.loc[row["id"]] = result_row
    _write_to_excel(results_df)


@cli.command()
@click.option("--use_cache", is_flag=True, help="Use Local Synapse Cache")
def create_html(use_cache):
    """Create HTML HTAN Dashboard."""

    env = Environment(
        loader=PackageLoader("hdash", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    if not use_cache or not os.path.exists(MASTER_HTAN_TABLE):
        _get_master_htan_table()

    project_df = _get_project_table()
    df = pd.read_csv(MASTER_HTAN_TABLE)

    record_map = {}
    project_list = []
    for index, row in project_df.iterrows():
        target_df = df[(df.projectId == row.id) & (df.type == "file")]
        file_list = target_df.name.to_list()
        file_counter = FileCounter(file_list)
        record = {
            "ATLAS": row["name"],
            "FASTQ": file_counter.get_num_files(FileCounter.BAM),
            "BAM": file_counter.get_num_files(FileCounter.FASTQ),
            "IMAGE": file_counter.get_num_files(FileCounter.IMAGE),
            "MATRIX": file_counter.get_num_files(FileCounter.MATRIX),
            "OTHER": file_counter.get_num_files(FileCounter.OTHER),
            "METADATA": file_counter.get_num_files(FileCounter.METADATA),
            "LIAISON": row["liaison"],
            "NOTES": row["notes"],
        }
        record_map[row["id"]] = record
        project_list.append(row["id"])

    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    template = env.get_template("index.html")
    html = template.render(
        timestamp=dt_string, project_list=project_list, record_map=record_map
    )
    fd = open("deploy/index.html", "w")
    fd.write(html)
    fd.close()


def _write_to_excel(results_df):
    writer = pd.ExcelWriter(DASHBOARD_FILE, engine="xlsxwriter")
    results_df.to_excel(writer, sheet_name="Sheet1")

    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    cell_format = workbook.add_format({"text_wrap": True})
    worksheet.set_column("A:B", 20)
    worksheet.set_column("C:H", 10)
    worksheet.set_column("J:J", 50, cell_format)

    writer.save()
    print("HTAN Dashboard written to:  %s." % DASHBOARD_FILE)


def _get_master_htan_table():
    syn = synapseclient.Synapse()
    credentials = SynapseCredentials()
    syn.login(credentials.user, credentials.password)
    master_htan_table = syn.tableQuery("SELECT * FROM %s" % MASTER_HTAN_ID)
    df = master_htan_table.asDataFrame()
    df.to_csv(MASTER_HTAN_TABLE)


def _get_project_table():
    return pd.read_csv(MASTER_PROJECT_TABLE)
