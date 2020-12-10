"""Command Line Interface (CLI) for generating HTAN Dashboard."""
import logging
import click
import os.path
import pandas as pd
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
def dashboard(use_cache):
    """Create HTAN Dashboard."""
    if not use_cache or not os.path.exists(MASTER_HTAN_TABLE):
        _get_master_htan_table()

    project_df = _get_project_table()
    df = pd.read_csv(MASTER_HTAN_TABLE)

    for index, row in project_df.iterrows():
        print(row.id, row.name)
        target_df = df[(df.projectId == row.id) & (df.type == "file")]
        file_list = target_df.name.to_list()
        print(file_list)


def _get_master_htan_table():
    syn = synapseclient.Synapse()
    credentials = SynapseCredentials()
    syn.login(credentials.user, credentials.password)
    master_htan_table = syn.tableQuery("SELECT * FROM %s" % MASTER_HTAN_ID)
    df = master_htan_table.asDataFrame()
    df.to_csv(MASTER_HTAN_TABLE)


def _get_project_table():
    return pd.read_csv(MASTER_PROJECT_TABLE)
