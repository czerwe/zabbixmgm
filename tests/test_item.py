import unittest2
import zabbixmgm
from mock import Mock, call

from pprint import pprint


class item_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass


    def test_item_setname(self):
        titem = zabbixmgm.zbxhost(self.apimock, name='myitem')
