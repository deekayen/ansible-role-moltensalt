import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_saltstack_installed(host):
    assert not host.package("salt-minion").is_installed


def test_saltstack_etc(host):
    assert not host.file("/etc/salt").exists


def test_saltstack_logs(host):
    for filename in (
        ("/var/log/salt/master"),
        ("/var/log/salt/minion"),
    ):
        log = host.file(filename)
        assert not log.exists


def test_saltstack_config(host):
    for filename in (
        ("/etc/salt/master"),
        ("/etc/salt/minion"),
    ):
        config = host.file(filename)
        assert not config.exists


def test_saltstack_service(host):
    service = host.service("salt-minion")

    assert not service.is_enabled
    assert not service.is_running
