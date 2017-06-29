import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_interface

from pprint import pprint


class host_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass


    def test_host_setname(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'myhost')
        self.assertEqual(thost.host, 'myhost')
        self.assertEqual(thost.name, 'myhost')

        thost.name = 'myhostname'
        self.assertEqual(thost.host, 'myhost')
        self.assertEqual(thost.name, 'myhostname')

        thost.host = 'myhostnchange'
        self.assertEqual(thost.host, 'myhostnchange')
        self.assertEqual(thost.name, 'myhostname')


    def test_host_add_interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface = zabbixmgm.zbxinterface(self.apimock)
        iface.port = '3000'
        iface.host = 'mytesthost.local'
        thost.add_interface(iface)
        create_command, create_params = thost.get('create')

        self.assertEqual(create_params['host'], 'mytesthost.local')
        self.assertEqual(len(create_params['interfaces']), 1)
        interface_1 = create_params['interfaces'][0]
        self.assertEqual(interface_1['main'], 1)
        


    def test_host_add_2interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3000'
        iface1.host = 'mytesthost.local'
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3001'
        iface2.host = '127.0.0.1'
        thost.add_interface(iface1)
        thost.add_interface(iface2)
        create_command, create_params = thost.get('create')
        pprint(create_params)

        self.assertEqual(create_params['host'], 'mytesthost.local')
        self.assertEqual(len(create_params['interfaces']), 2)
        interface_1 = create_params['interfaces'][0]
        self.assertEqual(interface_1['main'], 1)
        interface_2 = create_params['interfaces'][1]
        self.assertEqual(interface_2['main'], 0)
        

    def test_host_add_2interface_diff_types(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3001'
        iface1.host = 'mytesthost.local'
        

        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3002'
        iface2.host = '127.0.0.1'

        iface3 = zabbixmgm.zbxinterface(self.apimock)
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface3.port = '3003'
        iface3.host = 'mytesthost.local'
        

        iface4 = zabbixmgm.zbxinterface(self.apimock)
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4.port = '3004'
        iface4.host = '127.0.0.1'
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
        create_command, create_params = thost.get('create')
        # pprint(create_params)
        self.assertEqual(len(create_params['interfaces']), 4)

        int1, int2 = [interf for interf in create_params['interfaces'] if interf['type'] == 1]
        self.assertEqual(int1['main'], 1)
        self.assertEqual(int2['main'], 0)

        int1, int2 = [interf for interf in create_params['interfaces'] if interf['type'] == 4]
        self.assertEqual(int1['main'], 1)
        self.assertEqual(int2['main'], 0)
        

    def test_host_searchintercept_both(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3001'
        iface1.host = 'mytesthost.local'
        
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3002'
        iface2.host = '127.0.0.1'

        iface3 = zabbixmgm.zbxinterface(self.apimock)
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface3.port = '3003'
        iface3.host = 'mytesthost.local'
        

        iface4 = zabbixmgm.zbxinterface(self.apimock)
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4.port = '3004'
        iface4.host = '127.0.0.1'
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        tpid, idx = thost.search_interface(host='mytesthost.local', port='3001', searchtype='both')

        self.assertEqual(tpid, 1)
        self.assertEqual(idx, 0)

        

    def test_host_searchintercept_port(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3001'
        iface1.host = 'mytesthost.local'
        
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3002'
        iface2.host = '127.0.0.1'

        iface3 = zabbixmgm.zbxinterface(self.apimock)
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface3.port = '3003'
        iface3.host = 'mytesthost.local'
        

        iface4 = zabbixmgm.zbxinterface(self.apimock)
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4.port = '3004'
        iface4.host = '127.0.0.1'
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        tpid, idx = thost.search_interface(port='3004', searchtype='port')

        self.assertEqual(tpid, 4)
        self.assertEqual(idx, 1)
        



    def test_host_searchintercept_host(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3001'
        iface1.host = 'mytesthost.local'
        
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3002'
        iface2.host = '127.0.0.1'

        iface3 = zabbixmgm.zbxinterface(self.apimock)
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface3.port = '3003'
        iface3.host = 'mytesthost2.local'
        

        iface4 = zabbixmgm.zbxinterface(self.apimock)
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4.port = '3004'
        iface4.host = '127.0.0.1'
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        tpid, idx = thost.search_interface(host='mytesthost2.local', searchtype='host')

        self.assertEqual(tpid, 4)
        self.assertEqual(idx, 0)
        


    def test_host_rm_interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = '3001'
        iface1.host = 'mytesthost.local'
        
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = '3002'
        iface2.host = '127.0.0.1'

        iface3 = zabbixmgm.zbxinterface(self.apimock)
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface3.port = '3003'
        iface3.host = 'mytesthost2.local'
        

        iface4 = zabbixmgm.zbxinterface(self.apimock)
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4.port = '3004'
        iface4.host = '127.0.0.1'
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        create_command, create_params = thost.get('create')
        self.assertEqual(len(create_params['interfaces']), 4)
        self.assertEqual(len(thost.interfaces[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaces[zabbixmgm.zbxinterface.TYPE_JMX]), 2)

        tpid, idx = thost.search_interface(host='mytesthost2.local', searchtype='host')
        thost.del_interface(tpid, idx)

        create_command, create_params = thost.get('create')
        self.assertEqual(len(thost.interfaces[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaces[zabbixmgm.zbxinterface.TYPE_JMX]), 1)
        self.assertEqual(len(create_params['interfaces']), 3)


        tpid, idx = thost.search_interface(host='127.0.0.1', port='3004')
        thost.del_interface(tpid, idx)

        create_command, create_params = thost.get('create')
        self.assertEqual(len(thost.interfaces[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaces.keys()), 1)
        self.assertFalse(zabbixmgm.zbxinterface.TYPE_JMX in thost.interfaces.keys())
        self.assertEqual(len(create_params['interfaces']), 2)


    def test_host_load_response(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        self.assertEqual(thost.id, None)
        fakeresponse = {
                        "jsonrpc": "2.0",
                        "result": {
                            "hostids": [
                                "107819"
                            ]
                        },
                        "id": 1
                    }
        thost.request_result = fakeresponse
        self.assertEqual(thost.id, '107819')



    def test_host_get_create(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        command, param = thost.get()
        self.assertEqual(thost.apicommands['create'], command)



    def test_host_get_update(self):
        thost = zabbixmgm.zbxhost(self.apimock, 'mytesthost.local')
        command, param = thost.get('update')
        self.assertFalse(command)

        fakeresponse = {
                        "jsonrpc": "2.0",
                        "result": {
                            "hostids": [
                                "107819"
                            ]
                        },
                        "id": 1
                    }
        thost.request_result = fakeresponse
        self.assertEqual(thost.id, '107819')
        command, param = thost.get()
        self.assertEqual(thost.apicommands['update'], command)
        self.assertEqual(param['hostid'], '107819')
        
        command, param = thost.get('create')
        self.assertFalse(command)