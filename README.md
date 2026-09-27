Molten Salt
===========

[![CI](https://github.com/deekayen/ansible-role-moltensalt/workflows/CI/badge.svg)](https://github.com/deekayen/ansible-role-moltensalt/actions?query=workflow%3ACI) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

Remove SaltStack, all leftover files, and directories, including Salt 3006+
onedir installs from the Salt Project repositories.

Tested with Molecule on EL 9/10, Amazon Linux 2023, Ubuntu 22.04/24.04/26.04,
and Debian 12/13 by installing a current Salt minion and removing it. The
Windows tasks are linted but not exercised in CI.

Dependencies
------------

None.

Default Variables
-----------------

    # Purge configuration files on Debian and Ubuntu.
    debian_purge: false

    saltstack_keys:
      - 754A1A7AE731F165D5E6D4BD0E08A149DE57BFBE

    saltstack_packages:
      - salt
      - salt-minion
      - salt-repo
      - salt-master
      - salt-ssh
      - salt-syndic
      - salt-cloud

    saltstack_paths:
      - /etc/bash_completion/salt.bash
      - /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7-Salt
      - /etc/pki/rpm-gpg/saltstack-signing-key
      - /etc/salt
      - /etc/yum.repos.d/salt-2016.11.repo
      - /usr/bin/spm
      - /usr/bin/salt-call
      - /usr/bin/salt-minion
      - /usr/bin/salt-proxy
      - /usr/lib/systemd/system/salt-minion.service
      - /var/cache/salt
      - /var/log/salt
      - /usr/lib/python2.7/site-packages/salt
      - /usr/share/man/man1/salt-call.1.gz
      - /usr/share/man/man1/salt-minion.1.gz
      - /usr/share/man/man1/salt-proxy.1.gz
      # Salt 3006+ onedir packages and the Salt Project repositories.
      - /opt/saltstack
      - /etc/yum.repos.d/salt.repo
      - /etc/apt/sources.list.d/salt.sources
      - /etc/apt/sources.list.d/salt.list
      - /etc/apt/keyrings/salt-archive-keyring.pgp
      - /etc/apt/keyrings/salt-archive-keyring.gpg

    windows_remove_instdir: false

Example Playbook
----------------

    - hosts: servers
      roles:
         - deekayen.moltensalt

License
-------

BSD
