import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_group

from pprint import pprint

class application_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()
        self.testhost = zabbixmgm.zbxhost(self.apimock, 'unithost', {"hostid": "12", 'name': 'unithost'})


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

    def test_application_create_dict_missing_field(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'myapp')
        
        #tapplication.online_items['internal'] = 1
        
        with self.assertRaises(zabbixmgm.core.MissingField):
            create_command, param = tapplication.get('create')
        

    def test_application_create_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, 'myapp')
        tapplication.add_host(self.testhost)
        #tapplication.online_items['internal'] = 1
        create_command, param = tapplication.get()
        pprint(param)

        self.assertEqual(create_command, 'application.create')
        self.assertEqual(create_command, tapplication.apicommands['create'])
        self.assertEqual(len(param.keys()), 2)
        self.assertTrue('name' in param.keys())
        self.assertEqual(param['name'], 'myapp')



    # def test_application_update_dict(self):
    #     tapplication = zabbixmgm.zbxapplication(self.apimock, 'myapp')
    
    #     fakegroup = {'applicationid': 356, 'name': "myblub"}
    #     tapplication.merge(fakegroup)
    #     tapplication.add_host(self.testhost)
        
    #     create_command, cr = tapplication.get('update')
    #     pprint(create_command)
    #     pprint(cr)
    #     self.assertTrue(create_command == tapplication.apicommands['update'])
    #     self.assertEqual(create_command, 'application.update')

    #     self.assertEqual(len(cr.keys()), 2)
    #     self.assertTrue('applicationid' in cr.keys())
    #     self.assertTrue('name' in cr.keys())


    # def test_application_delete_dict(self):
    #     tapplication = zabbixmgm.zbxapplication(self.apimock, 'mygroup')
    #     fakegroup = {'applicationid': 30,'name':'blub'}
    #     tapplication.merge(fakegroup)
    #     tapplication.add_host(self.testhost)
        
    #     create_command, cr = tapplication.get('delete')
    #     self.assertEqual(len(cr), 1)
    #     self.assertEqual(cr[0], 30)
        



