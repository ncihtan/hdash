"""Synapse Utilities."""


import synapseclient
import logging
import os
import glob
from hdash.synapse.credentials import SynapseCredentials


class SynapseUtil:
    """Core Synapse Utility Class."""

    CACHE = "cache"
    MASTER_HTAN_TABLE = CACHE + "/master_htan.csv"
    MASTER_HTAN_ID = "syn20446927"

    def __init__(self, use_cache):
        """Construct a new Synapse Utility Class."""
        if not use_cache:
            self.__clear_synapse_cache()

        self.syn = synapseclient.Synapse()
        self.cred = SynapseCredentials()
        self.syn.login(self.cred.user, self.cred.password, silent=True)

    def __clear_synapse_cache(self):
        file_list = glob.glob(SynapseUtil.CACHE + "/*.csv")
        for file_path in file_list:
            logging.info("Deleting cached file:  " + file_path)
            os.remove(file_path)

    def retrieve_master_htan_table(self):
        """Retrieve the Master HTAN Table from Synapse."""
        master_htan_table = self.syn.tableQuery(
            "SELECT * FROM %s" % SynapseUtil.MASTER_HTAN_ID
        )
        df = master_htan_table.asDataFrame()
        df.to_csv(SynapseUtil.MASTER_HTAN_TABLE)

    def retrieve_file(self, synapse_id):
        """Retrieve the specified file from Synapse."""
        syn_link = self.syn.get(
            entity=synapse_id,
            downloadLocation=SynapseUtil.CACHE,
        )
        new_file_path = SynapseUtil.CACHE + "/" + synapse_id + ".csv"
        logging.info("Renaming:  %s --> %s" % (syn_link.path, new_file_path))
        os.rename(syn_link.path, new_file_path)
        return new_file_path
