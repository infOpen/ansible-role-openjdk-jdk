"""
Role tests
"""

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_packages(host):
    """
    Check if package(s) installed
    """

    package_name = ''

    if host.system_info.codename in ['trusty', 'jessie']:
        package_name = 'openjdk-7-jdk'
    elif host.system_info.codename == 'xenial':
        package_name = 'openjdk-8-jdk'

    assert host.package(package_name).is_installed
