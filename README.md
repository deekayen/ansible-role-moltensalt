# deekayen.moltensalt

[![CI](https://github.com/deekayen/ansible-role-moltensalt/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-moltensalt/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.moltensalt-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/moltensalt/) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that uninstalls SaltStack from Linux and Windows hosts and deletes what the packages leave behind. It covers older Salt packages as well as Salt 3006+ onedir builds from the Salt Project repositories, which install under `/opt/saltstack` on top of a `salt-common` base package.

On Linux, the role removes the Salt packages with apt or the system package manager, removes a pip-installed `salt` if `python3 -m pip show salt` finds one, removes the Salt signing keys from the apt keyring or RPM database, and deletes every path in `saltstack_paths`. That list includes `/etc/salt`, `/var/cache/salt`, `/var/log/salt`, `/opt/saltstack`, and the Salt Project repository and keyring files. On Windows, it removes the `salt-minion` and `salt-master` services, `uninst.exe`, `ssm.exe`, `vcredist.exe`, `bin`, and `salt*` from the Salt install directory (`C:\salt`), and the App Paths, uninstall, and `salt-minion` service registry keys listed in `vars/main.yml`. The Windows steps follow what the [Salt minion NSIS uninstaller](https://github.com/saltstack/salt/blob/983d20e3bd4cee61ca12a699e43afc2bc0add451/pkg/windows/installer/Salt-Minion-Setup.nsi#L801) does, since running `uninst.exe /S` did not remove the 2014 and 2016 releases.

## Requirements

- ansible-core 2.15 or newer on the controller.
- The `ansible.windows` collection for Windows targets: `ansible-galaxy collection install ansible.windows`.
- Privilege escalation on Linux targets. Run the play with `become: true`; the role removes packages and deletes paths under `/etc`, `/usr`, `/var`, and `/opt`.
- A WinRM or SSH connection with administrative rights on Windows targets, since the role removes services and `HKLM` registry keys.
- Fact gathering left on. The role picks its task files from `ansible_facts.os_family`.

## Supported platforms

| Platform | Versions |
| --- | --- |
| EL (Rocky Linux in CI) | 9, 10 |
| Amazon Linux | 2023 |
| Debian | 12 (bookworm), 13 (trixie) |
| Ubuntu | 22.04 (jammy), 24.04 (noble), 26.04 (resolute) |
| Windows | 2016, 2019, 2022 |

CI installs a Salt minion from the Salt Project repositories on each Linux platform in the table, then removes it with Molecule. The Windows tasks are linted but never applied to a Windows host in CI.

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.moltensalt
ansible-galaxy collection install ansible.windows
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.moltensalt
    src: https://github.com/deekayen/ansible-role-moltensalt.git
    scm: git
    version: main

collections:
  - name: ansible.windows
```

```bash
ansible-galaxy install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `debian_purge` | `false` | Purge configuration files when removing Debian packages. |
| `saltstack_keys` | `[754A1A7AE731F165D5E6D4BD0E08A149DE57BFBE]` | Fingerprints of Salt signing keys to remove from the apt keyring or RPM database. The role asserts that every entry is a full 40-hex-digit fingerprint. |
| `saltstack_packages` | `salt`, `salt-minion`, `salt-repo`, `salt-master`, `salt-ssh`, `salt-syndic`, `salt-cloud` | Packages removed on RedHat-family hosts only. Debian-family hosts use a fixed list in `tasks/debian.yml`: `salt-master`, `salt-minion`, `salt-ssh`, `salt-syndic`, `salt-cloud`, `salt-api`, and `salt-common`. |
| `saltstack_paths` | 22 paths, see `defaults/main.yml` | Files and directories deleted on Linux after package removal. The role asserts that every entry is an absolute path. Overriding the list replaces it. |
| `windows_remove_instdir` | `false` | Also delete the whole Salt install directory on Windows, after the targeted file and registry cleanup. |

`vars/main.yml` holds the Windows install directory (`salt_instdir`, `C:\salt`) and the list of registry keys to delete.

## Behavior

- On Debian-family hosts, apt key removal runs only when both `/usr/bin/apt-key` and `/usr/bin/gpg` exist. Debian 13 and Ubuntu 26.04 no longer ship `apt-key`, so the role skips it there. The role also deletes `/etc/apt/sources.list.d/saltstack.list`.
- The pip check runs `python3 -m pip show salt` and tolerates a missing pip, so hosts without pip or without a pip-installed `salt` skip the pip removal.
- On Windows, the role asserts that `C:\salt\bin\Scripts` exists before removing anything, and fails the play otherwise. See [Known issues](#known-issues).
- Unless `windows_remove_instdir` is `true`, `C:\salt` stays on Windows hosts with anything that did not match `uninst.exe`, `ssm.exe`, `vcredist.exe`, `bin`, or `salt*`.

## Dependencies

None. The `ansible.windows` collection is a requirement, not a role dependency.

## Example playbook

Use separate plays, with `become` only on the Linux one:

```yaml
---
- name: Remove SaltStack from Linux hosts.
  hosts: salt_minions_linux
  become: true

  vars:
    debian_purge: true

  roles:
    - deekayen.moltensalt

- name: Remove SaltStack from Windows hosts.
  hosts: salt_minions_windows

  vars:
    windows_remove_instdir: true

  roles:
    - deekayen.moltensalt
```

## Tags

| Tag | Tasks |
| --- | --- |
| `packages` | Package and pip removal. |
| `key` | Signing key removal. |
| `files` | Path cleanup on Linux, and file and directory removal on Windows. |
| `service` | Windows service removal, and on Linux stopping the minion service and reloading systemd. |
| `registry` | Windows registry cleanup. |
| `validation` | The Windows install directory assert. |
| `debug` | The Windows success message. |

Input validation in `tasks/assert.yml` is tagged `always`. Only `--skip-tags` works reliably with these tags. See [Known issues](#known-issues).

## Known issues

- The `include_tasks` calls in `tasks/main.yml:31`, `:35`, `:39`, and `:61` have no tags. Under `--tags`, Ansible skips an untagged dynamic include, so the tagged tasks inside `debian.yml`, `redhat.yml`, `pip.yml`, and `windows.yml` never run. `--tags files` runs only the Linux path cleanup in `tasks/main.yml`. `--skip-tags` behaves as expected.
- The Windows assert in `tasks/windows.yml:14-22` requires `C:\salt\bin\Scripts`, and `tasks/windows.yml:40-48` deletes `C:\salt\bin`. A second run against the same host, or a run against a Windows host that never had Salt, fails the assert.
- That assert's message tells the user to adjust `salt_instdir`, but `salt_instdir` is set in `vars/main.yml:3`. The [variable precedence list](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence) puts role vars above inventory, `group_vars`, and play `vars`, so changing it takes a role parameter set directly on the `roles:` entry, or `-e`.

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint: installs `molecule/default/requirements.yml`, then runs `ansible-lint --profile production` and `flake8 molecule/`.
2. Molecule: `prepare.yml` adds the Salt Project apt source or yum repository and installs `salt-minion`, then Molecule runs converge, idempotence, and testinfra verification in Docker against each Linux distribution in the table above.

To run the same checks locally with Docker available:

```bash
pip3 install ansible-core ansible-lint flake8 molecule "molecule-plugins[docker]" docker pytest-testinfra
ansible-galaxy install -r molecule/default/requirements.yml
ansible-lint --profile production
flake8 molecule/
MOLECULE_DISTRO=rockylinux9 molecule test
```

`MOLECULE_DISTRO` selects a `geerlingguy/docker-<distro>-ansible` image. The values CI uses are `rockylinux9`, `rockylinux10`, `amazonlinux2023`, `ubuntu2204`, `ubuntu2404`, `ubuntu2604`, `debian12`, and `debian13`. The testinfra checks in `molecule/default/tests/test_default.py` read `defaults/main.yml` and confirm that `salt`, `salt-common`, and `salt-minion` are not installed, `salt-call` and `salt-minion` are gone from the path, the `salt-minion` unit is not enabled or running, and every path in `saltstack_paths` is absent.

The repository also has a `.pre-commit-config.yaml`; run `pre-commit run --all-files` before pushing.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Input validation, the per-family includes, and Linux path cleanup. |
| `tasks/assert.yml` | Checks `saltstack_paths` and `saltstack_keys`, tagged `always`. |
| `tasks/debian.yml` | apt package, key, and source removal. |
| `tasks/redhat.yml` | Package and RPM key removal. |
| `tasks/pip.yml` | Removal of a pip-installed `salt`. |
| `tasks/windows.yml` | Windows service, file, and registry removal. |
| `defaults/main.yml` | Every user-facing variable. |
| `vars/main.yml` | Windows install directory and registry key list. |
| `meta/argument_specs.yml` | Argument spec for the user-facing variables. |
| `molecule/default/` | Molecule scenario: `prepare.yml` installs Salt, `converge.yml` applies the role, and testinfra tests check the result. |
| `.github/workflows/` | `ci.yml` for lint and Molecule, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.moltensalt`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen). Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).
