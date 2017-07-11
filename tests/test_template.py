import unittest2
import zabbixmgm
from mock import Mock, call

from pprint import pprint


class template_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass


    def test_template_init(self):
        ttemplate = zabbixmgm.zbxtemplate(self.apimock, name='mytemplate')

        self.assertTrue('templateid' in ttemplate.difffields)
        self.assertTrue('templateid' in ttemplate.readonlyfields)


    def test_template_new(self):
        ttemplate = zabbixmgm.zbxtemplate(self.apimock, name='mytemplate')

        self.assertEqual(ttemplate.id, None)
        self.assertEqual(ttemplate.templateid, None)


    def test_template_masking(self):
        mask = {'available': u'0', 'status': u'3', 'templateid': u'10001'}

        ttemplate = zabbixmgm.zbxtemplate(self.apimock, mask=mask, name='mytemplate')

        self.assertEqual(ttemplate.id, '10001')
        self.assertEqual(ttemplate.templateid, '10001')





