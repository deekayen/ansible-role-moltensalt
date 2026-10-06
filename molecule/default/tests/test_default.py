"""Testinfra checks for the moltensalt role."""

import os

import pytest
import yaml

DEFAULTS = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "defaults", "main.yml"
)
with open(DEFAULTS) as defaults_file:
    ROLE_DEFAULTS = yaml.safe_load(defaults_file)


@pytest.mark.parametrize("name", ["salt", "salt-common", "salt-minion"])
def test_packages_removed(host, name):
    assert not host.package(name).is_installed


def test_salt_commands_gone(host):
    assert not host.exists("salt-call")
    assert not host.exists("salt-minion")


def test_minion_service_gone(host):
    # Newer systemd exits 4 for a removed unit, which testinfra's
    # Service.is_enabled rejects, so read the state directly.
    cmd = host.run("systemctl is-enabled salt-minion.service")
    assert cmd.stdout.strip() in ("", "not-found", "disabled")
    assert not host.service("salt-minion").is_running


@pytest.mark.parametrize("path", ROLE_DEFAULTS["saltstack_paths"])
def test_paths_removed(host, path):
    assert not host.file(path).exists
