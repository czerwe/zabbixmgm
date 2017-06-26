from setuptools import setup

import zabbixmgm
setup(
    name='zabbixmgm',
    version=zabbixmgm.__version__,
    packages=['zabbixmgm'],
    test_suite="tests",
    install_requires=['py-zabbix==1.1.3']
)
