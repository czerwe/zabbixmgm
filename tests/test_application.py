import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_group

from pprint import pprint

class application_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass


    def test_application_setname(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'mygroup')
        self.assertEqual(tapplication.name, 'mygroup')


    def test_application_load_response(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'mytesthost.local')
        self.assertEqual(tapplication.id, None)
        fakeresponse = {
                        "jsonrpc": "2.0",
                        "result": {
                            "applicationids": [
                                "356"
                            ]
                        },
                        "id": 1
                    }
        tapplication.request_result = fakeresponse
        self.assertEqual(tapplication.id, '356')

    def test_application_create_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'mygroup')
        
        tapplication.online_items['internal'] = 1
        create_command, cr = tapplication.get('create')
        self.assertEqual(len(cr.keys()), 1)



    def test_application_update_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'mygroup')
        fakegroup = {'applicationid': 356, 'name': "myblub"}
        tapplication.merge(fakegroup)
        
        create_command, cr = tapplication.get('update')
        self.assertTrue(create_command == tapplication.apicommands['update'])
        self.assertEqual(create_command, 'application.update')

        self.assertEqual(len(cr.keys()), 2)
        self.assertTrue('applicationid' in cr.keys())
        self.assertTrue('name' in cr.keys())


    def test_application_delete_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'mygroup')
        fakegroup = {'applicationid': 30,'name':'blub'}
        tapplication.merge(fakegroup)
        
        create_command, cr = tapplication.get('delete')
        self.assertEqual(len(cr), 1)
        self.assertEqual(cr[0], 30)
        



