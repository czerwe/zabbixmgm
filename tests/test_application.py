import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_group

from pprint import pprint


app30 = {'applicationid': 30,'name':'blub'}
app356 = {'applicationid': 356, 'name': "myblub", 'hostid': '4444'}

class application_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()
        self.testhost = zabbixmgm.zbxhost(self.apimock, {"hostid": "12", 'name': 'unithost'}, name='unithost')
       

    def tearDown(self):
        pass


    def test_application_setname(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='myapp')
        self.assertEqual(tapplication.name, 'myapp')


    def test_application_load_response(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='mytesthost.local')
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
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='myapp')
        
        #tapplication.online_items['internal'] = 1
        
        with self.assertRaises(zabbixmgm.core.MissingField):
            create_command, param = tapplication.get('create')
        

    def test_application_create_missing_field(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='myapp')
        
        with self.assertRaises(zabbixmgm.core.MissingField):
            tapplication.get()



    def test_application_create(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='myapp')
        
        tapplication.add_host(self.testhost)
        command, param = tapplication.get()

        self.assertEqual(command, tapplication.apicommands['create'])
        self.assertEqual(command, 'application.create')

        self.assertEqual(len(param.keys()), 2)
        self.assertTrue('hostid' in param.keys())
        self.assertEqual(param['hostid'], '12')
        self.assertTrue('name' in param.keys())
        self.assertEqual(param['name'], 'myapp')
        self.assertTrue(not 'applicationid' in param.keys())



    def test_application_update_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, name='myapp')
    
        tapplication.merge(app356)

        command, param = tapplication.get()
        self.assertEqual(command, tapplication.apicommands['update'])
        self.assertEqual(command, 'application.update')

        self.assertEqual(len(param.keys()), 3)
        self.assertTrue('applicationid' in param.keys())
        self.assertEqual(param['applicationid'], 356)
        self.assertTrue('name' in param.keys())
        self.assertEqual(param['name'], 'myblub')
        self.assertTrue('hostid' in param.keys())
        self.assertEqual(param['hostid'], '4444')


        # adding an other host to see if values changed correctly
        tapplication.add_host(self.testhost)
        
        command, param = tapplication.get()
        self.assertEqual(command, tapplication.apicommands['update'])
        self.assertEqual(command, 'application.update')

        self.assertEqual(len(param.keys()), 3)

        self.assertTrue('applicationid' in param.keys())
        self.assertEqual(param['applicationid'], 356)
        self.assertTrue('name' in param.keys())
        self.assertEqual(param['name'], 'myblub')
        self.assertTrue('hostid' in param.keys())
        self.assertEqual(param['hostid'], '12')


    def test_application_delete_dict(self):
        tapplication = zabbixmgm.zbxapplication(self.apimock, mask=app30, name='myapp')

        command, param = tapplication.get('delete')
        self.assertEqual(command, tapplication.apicommands['delete'])
        self.assertEqual(command, 'application.delete')
        self.assertEqual(len(param), 1)
        self.assertEqual(param[0], 30)