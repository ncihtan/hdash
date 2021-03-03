"""Synapse Tests."""
import pytest
from hdash.synapse.credentials import SynapseCredentials
from pytest import MonkeyPatch


def test_valid_env():
    """Test Valid Environment."""
    monkey_patch = MonkeyPatch()
    monkey_patch.setenv("SYNAPSE_USER", "user")
    monkey_patch.setenv("SYNAPSE_PASSWORD", "password")
    credentials = SynapseCredentials()
    assert credentials.user == "user"
    assert credentials.password == "password"


def test_missing_user():
    """Test Missing User Environment Variable."""
    monkey_patch = MonkeyPatch()
    monkey_patch.delenv("SYNAPSE_USER", raising=False)

    with pytest.raises(EnvironmentError):
        SynapseCredentials()


def test_missing_password():
    """Test Missing Password Environment Variable."""
    monkey_patch = MonkeyPatch()
    monkey_patch.setenv("SYNAPSE_USER", "user")
    monkey_patch.delenv("SYNAPSE_PASSWORD", raising=False)

    with pytest.raises(EnvironmentError):
        SynapseCredentials()
