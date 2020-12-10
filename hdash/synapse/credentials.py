"""Synapse Credentials."""
import os
import logging


class SynapseCredentials:
    """Synapse Credentials obtained via Environment Variables."""

    user = None
    password = None

    def __init__(self):
        """Construct Synapse Credentials."""
        self.user = os.getenv('SYNAPSE_USER')
        self.password = os.getenv('SYNAPSE_PASSWORD')
        logging.info("Using Synapse ID:  %s." % self.user)
