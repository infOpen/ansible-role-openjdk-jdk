"""
Role tests
"""

import os
import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name,codenames', [
    ('openjdk-8-jdk', ['stretch']),
    ('openjdk-11-jdk', ['bionic', 'buster', 'focal']),
    ('java-11-openjdk-devel', ['7', '8']),
])
def test_repository_file(host, name, codenames):
    """
    Test packages installed
    """

    if host.system_info.distribution not in ['centos', 'debian', 'ubuntu']:
        pytest.skip('{} ({}) distribution not managed'.format(
            host.system_info.distribution, host.system_info.release))

    if host.system_info.distribution in ['debian', 'ubuntu']:
        if codenames and host.system_info.codename.lower() not in codenames:
            pytest.skip('{} package not used with {} ({})'.format(
                name, host.system_info.distribution, host.system_info.codename)
            )
    else:
        if codenames and host.system_info.release.lower() not in codenames:
            pytest.skip('{} package not used with {} ({})'.format(
                name, host.system_info.distribution, host.system_info.release))

    assert host.package(name).is_installed
