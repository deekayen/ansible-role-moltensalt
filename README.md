[![Build Status](https://travis-ci.org/deekayen/ansible-role-moltensalt.svg?branch=main)](https://travis-ci.org/deekayen/ansible-role-moltensalt) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

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

Example Playbook
----------------

    - hosts: servers
      roles:
         - deekayen.moltensalt

License
-------

BSD
