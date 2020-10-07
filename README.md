[![Build Status](https://travis-ci.org/deekayen/ansible-role-moltensalt.svg?branch=main)](https://travis-ci.org/deekayen/ansible-role-moltensalt) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

Molten Salt
===========

Remove SaltStack, all leftover files, and directories.

Dependencies
------------

None.

Default Variables
-----------------

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

    windows_remove_instdir: false

Example Playbook
----------------

    - hosts: servers
      roles:
         - deekayen.moltensalt

License
-------

BSD
