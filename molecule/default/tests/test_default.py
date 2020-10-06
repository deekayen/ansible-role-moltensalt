import os
import http.client
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_saltstack_installed(host):
    assert host.package("salt-minion").is_installed == False


def test_saltstack_etc(host):
    assert host.file("/etc/salt").exists == False


def test_saltstack_logs(host):
    for filename in (
        ("/var/log/salt/master"),
        ("/var/log/salt/minion"),
    ):
        log = host.file(filename)
        assert log.exists == False


def test_saltstack_config(host):
    for filename in (
        ("/etc/salt/master"),
        ("/etc/salt/minion"),
    ):
        config = host.file(filename)
        assert config.exists == False


def test_saltstack_service(host):
    service = host.service("salt-minion")

    assert service.is_enabled == False
    assert service.is_running == False

