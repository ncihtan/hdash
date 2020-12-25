"""Synapse Credentials."""
import os
import logging


class SynapseCredentials:
    """Synapse Credentials obtained via Environment Variables."""

    user = None
    password = None

    def __init__(self):
        """Construct Synapse Credentials."""
        self.user = os.getenv("SYNAPSE_USER")
        if self.user is None:
            raise EnvironmentError("SYNAPSE_USER is not set.")

        self.password = os.getenv("SYNAPSE_PASSWORD")
        if self.password is None:
            raise EnvironmentError("SYNAPSE_PASSWORD is not set.")

        logging.info("Using Synapse ID:  %s." % self.user)
