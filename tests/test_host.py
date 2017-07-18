import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_interface

from pprint import pprint



host_search_response = {
 u'available': u'0',
 u'groups': [{u'groupid': u'32', u'name': u'autogroup'}],
 u'host': u'52n03.s52.local',
 u'hostid': u'10142',
 u'interfaces': [{u'interfaceid': u'38'}],
 u'name': u'52n03.s52.local',
 u'parentTemplates': [],
 u'status': u'0'}

inf38_response = {u'bulk': u'1',
 u'dns': u'',
 u'hostid': u'10142',
 u'interfaceid': u'38',
 u'ip': u'127.0.0.1',
 u'main': u'1',
 u'port': u'10050',
 u'type': u'1',
 u'useip': u'1'}

inf39_response = {u'bulk': u'1',
 u'dns': u'',
 u'hostid': u'10142',
 u'interfaceid': u'39',
 u'ip': u'127.0.0.1',
 u'main': u'1',
 u'port': u'10051',
 u'type': u'4',
 u'useip': u'1'
}

inf40_response = {u'bulk': u'1',
 u'dns': u'',
 u'hostid': u'10142',
 u'interfaceid': u'40',
 u'ip': u'127.0.0.1',
 u'main': u'0',
 u'port': u'10053',
 u'type': u'4',
 u'useip': u'1'
}


fullhost = {u'available': u'0',
 u'description': u'',
 u'disable_until': u'0',
 u'error': u'',
 u'errors_from': u'0',
 u'flags': u'0',
 u'groups': [{u'groupid': u'2', u'name': u'Linux servers'}],
 u'host': u'myhost.local',
 u'hostid': u'10105',
 u'interfaces': [{u'interfaceid': u'2'}],
 u'ipmi_authtype': u'-1',
 u'ipmi_available': u'0',
 u'ipmi_disable_until': u'0',
 u'ipmi_error': u'',
 u'ipmi_errors_from': u'0',
 u'ipmi_password': u'',
 u'ipmi_privilege': u'2',
 u'ipmi_username': u'',
 u'jmx_available': u'0',
 u'jmx_disable_until': u'0',
 u'jmx_error': u'',
 u'jmx_errors_from': u'0',
 u'lastaccess': u'0',
 u'maintenance_from': u'0',
 u'maintenance_status': u'0',
 u'maintenance_type': u'0',
 u'maintenanceid': u'0',
 u'name': u'myhost.local',
 u'parentTemplates': [],
 u'proxy_hostid': u'0',
 u'snmp_available': u'0',
 u'snmp_disable_until': u'0',
 u'snmp_error': u'',
 u'snmp_errors_from': u'0',
 u'status': u'0',
 u'templateid': u'0',
 u'tls_accept': u'1',
 u'tls_connect': u'1',
 u'tls_issuer': u'',
 u'tls_psk': u'',
 u'tls_psk_identity': u'',
 u'tls_subject': u''}





class host_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass

    def create_host_4_interfaces(self):
        self.thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        self.iface1 = zabbixmgm.zbxinterface(self.apimock, port=3001, host=self.thost.name)
        self.iface2 = zabbixmgm.zbxinterface(self.apimock, port=3002, host='127.0.0.1')
        
        self.iface3 = zabbixmgm.zbxinterface(self.apimock, port=3003, host=self.thost.name)
        self.iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        self.iface4 = zabbixmgm.zbxinterface(self.apimock, port=3004, host='127.0.0.1')
        self.iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        
        self.thost.add_interface(self.iface1)
        self.thost.add_interface(self.iface3)
        self.thost.add_interface(self.iface2)
        self.thost.add_interface(self.iface4)



    def test_host_setname(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='myhost')
        self.assertEqual(thost.host, 'myhost')
        self.assertEqual(thost.name, 'myhost')

        thost.name = 'myhostname'
        self.assertEqual(thost.host, 'myhost')
        self.assertEqual(thost.name, 'myhostname')

        thost.host = 'myhostnchange'
        self.assertEqual(thost.host, 'myhostnchange')
        self.assertEqual(thost.name, 'myhostname')


    def test_host_add_interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        iface = zabbixmgm.zbxinterface(self.apimock, port=3000, host=thost.name)
        thost.add_interface(iface)
        create_command, create_params = thost.get('create')

        self.assertEqual(create_params['host'], 'mytesthost.local')
        self.assertEqual(len(create_params['interfaces']), 1)
        interface_1 = create_params['interfaces'][0]
        self.assertEqual(interface_1['main'], 1)
        self.assertEqual(interface_1['dns'], 'mytesthost.local')
        self.assertEqual(interface_1['useip'], 0)
        self.assertEqual(interface_1['port'], '3000')
        


    def test_host_add_2interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock, port=3000, host=thost.name)
        iface2 = zabbixmgm.zbxinterface(self.apimock, port=3001, host=thost.name)

        thost.add_interface(iface1)
        thost.add_interface(iface2)

        create_command, create_params = thost.get('create')

        self.assertEqual(create_params['host'], 'mytesthost.local')
        self.assertEqual(len(create_params['interfaces']), 2)
        interface_1 = create_params['interfaces'][0]
        self.assertEqual(interface_1['main'], 1)
        interface_2 = create_params['interfaces'][1]
        self.assertEqual(interface_2['main'], 0)
        

    def test_host_add_2interface_diff_types(self):
        self.create_host_4_interfaces()
        create_command, create_params = self.thost.get()
        
        self.assertEqual(create_command, 'host.create')
        self.assertEqual(len(create_params['interfaces']), 4)

        int1, int2 = [interf for interf in create_params['interfaces'] if interf['type'] == 1]
        self.assertEqual(int1['main'], 1)
        self.assertEqual(int2['main'], 0)

        int1, int2 = [interf for interf in create_params['interfaces'] if interf['type'] == 4]
        self.assertEqual(int1['main'], 1)
        self.assertEqual(int2['main'], 0)
        

    def test_host_searchinterface_both_parameters(self):
        self.create_host_4_interfaces()
        tpid, idx = self.thost.search_interface(host='mytesthost.local', port='3001', searchtype='both')

        self.assertEqual(tpid, 1)
        self.assertEqual(idx, 0)

        

    def test_host_searchintercept_port(self):
        self.create_host_4_interfaces()
        tpid, idx = self.thost.search_interface(port='3004', searchtype='port')

        self.assertEqual(tpid, 4)
        self.assertEqual(idx, 1)



    def test_host_searchintercept_host(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock, port=3001, host=thost.name)
        iface2 = zabbixmgm.zbxinterface(self.apimock, port=3002, host='127.0.0.1')
        
        iface3 = zabbixmgm.zbxinterface(self.apimock, port=3003, host='mytesthost2.local')
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4 = zabbixmgm.zbxinterface(self.apimock, port=3004, host='127.0.0.1')
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        tpid, idx = thost.search_interface(port='3004', searchtype='port')

        self.assertEqual(tpid, 4)
        self.assertEqual(idx, 1)
        
       
        tpid, idx = thost.search_interface(host='mytesthost2.local', searchtype='host')

        self.assertEqual(tpid, 4)
        self.assertEqual(idx, 0)
        


    def test_host_rm_interface(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        iface1 = zabbixmgm.zbxinterface(self.apimock, port=3001, host=thost.name)
        iface2 = zabbixmgm.zbxinterface(self.apimock, port=3002, host='127.0.0.1')
        
        iface3 = zabbixmgm.zbxinterface(self.apimock, port=3003, host='mytesthost2.local')
        iface3.type = zabbixmgm.zbxinterface.TYPE_JMX
        iface4 = zabbixmgm.zbxinterface(self.apimock, port=3004, host='127.0.0.1')
        iface4.type = zabbixmgm.zbxinterface.TYPE_JMX
        
        thost.add_interface(iface1)
        thost.add_interface(iface3)
        thost.add_interface(iface2)
        thost.add_interface(iface4)
       
        create_command, create_params = thost.get('create')
        self.assertEqual(len(create_params['interfaces']), 4)

        self.assertEqual(len(thost.interfaceobjects[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaceobjects[zabbixmgm.zbxinterface.TYPE_JMX]), 2)

        tpid, idx = thost.search_interface(host='mytesthost2.local', searchtype='host')
        thost.del_interface(tpid, idx)

        create_command, create_params = thost.get('create')
        self.assertEqual(len(thost.interfaceobjects[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaceobjects[zabbixmgm.zbxinterface.TYPE_JMX]), 1)
        self.assertEqual(len(create_params['interfaces']), 3)

        tpid, idx = thost.search_interface(host='127.0.0.1', port='3004')
        thost.del_interface(tpid, idx)

        create_command, create_params = thost.get('create')
        self.assertEqual(len(thost.interfaceobjects[zabbixmgm.zbxinterface.TYPE_AGENT]), 2)
        self.assertEqual(len(thost.interfaceobjects.keys()), 1)
        self.assertFalse(zabbixmgm.zbxinterface.TYPE_JMX in thost.interfaceobjects.keys())
        self.assertEqual(len(create_params['interfaces']), 2)


    def test_host_load_response(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
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
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        command, param = thost.get()
        self.assertEqual(thost.apicommands['create'], command)



    def test_host_get_update(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
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



    def test_host_interface_upon_creation_1inf(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')


        tinterface1 = zabbixmgm.zbxinterface(self.apimock)
        tinterface1.host = thost.name
        thost.add_interface(tinterface1)
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertEqual(len(param['interfaces']), 1, 'interface should be filled with just 1')
        
        interface = param['interfaces'][0]

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        self.assertFalse('hostid' == interface.keys())
        self.assertFalse('interfaceid' == interface.keys())


    def test_host_interface_upon_creation_2inf_same_type(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')


        tinterface1 = zabbixmgm.zbxinterface(self.apimock)
        tinterface1.host = thost.name
        thost.add_interface(tinterface1)
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertEqual(len(param['interfaces']), 1, 'interface should be filled with just 1')
        
        interface = param['interfaces'][0]

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        
        tinterface2 = zabbixmgm.zbxinterface(self.apimock)
        tinterface2.host = thost.name
        tinterface2.port = '1110'
        thost.add_interface(tinterface2)
        command, param = thost.get()

        self.assertEqual(len(param['interfaces']), 2, 'interface should be filled with 2')
        
        interface = param['interfaces'][0]

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        self.assertEqual(interface['port'], '10050')
        self.assertEqual(interface['type'], zabbixmgm.zbxinterface.TYPE_AGENT)

        interface = param['interfaces'][1]

        self.assertEqual(interface['main'], 0, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        self.assertEqual(interface['port'], '1110')
        self.assertEqual(interface['type'], zabbixmgm.zbxinterface.TYPE_AGENT)


    def test_host_interface_upon_creation_2inf_diff_type(self):
        thost = zabbixmgm.zbxhost(self.apimock, name='mytesthost.local')
        # pprint(thost.interfaceobjects)
        # self.interfaces = thost.interfaceobjects
        # ss = [interface_instance.get('hostcreate')[1] for iftypeid in self.interfaces.keys() for interface_instance in self.interfaces[iftypeid]]
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')


        tinterface1 = zabbixmgm.zbxinterface(self.apimock)
        tinterface1.host = thost.name
        thost.add_interface(tinterface1)
        command, param = thost.get()
        self.assertEqual(command, 'host.create')
        self.assertEqual(command, thost.apicommands['create'])
        self.assertTrue('interfaces' in param.keys())
        self.assertEqual(len(param['interfaces']), 1, 'interface should be filled with just 1')
        
        interface = param['interfaces'][0]

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        
        tinterface2 = zabbixmgm.zbxinterface(self.apimock)
        tinterface2.host = thost.name
        tinterface2.port = '4002'
        tinterface2.type = zabbixmgm.zbxinterface.TYPE_JMX
        thost.add_interface(tinterface2)
        command, param = thost.get()

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        self.assertEqual(interface['port'], '10050')
        self.assertEqual(interface['type'], zabbixmgm.zbxinterface.TYPE_AGENT)

        interface = param['interfaces'][1]

        self.assertEqual(interface['main'], 1, 'main should be one, it is set automatically')
        self.assertEqual(interface['dns'], 'mytesthost.local')
        self.assertEqual(interface['port'], '4002')
        self.assertEqual(interface['type'], zabbixmgm.zbxinterface.TYPE_JMX)


    def test_host_interface_upon_update_1inf(self):

        thost = zabbixmgm.zbxhost(self.apimock, mask=host_search_response, name='mytesthost.local')
        command, param = thost.get()

        self.assertEqual(command, 'host.update')
        self.assertTrue('hostid' in param.keys())
        self.assertEqual(param['hostid'], '10142')
        self.assertEqual(command, thost.apicommands['update'])
        self.assertFalse('interfaces' in param.keys())
        # self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')
        
        inf38 = zabbixmgm.zbxinterface(self.apimock, mask=inf38_response)
        thost.add_interface(inf38)
        command, param = thost.get()

        self.assertTrue('interfaces' in param.keys())
        self.assertEqual(len(param['interfaces']), 1, 'interface should be 1 but isn\'t')
        self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'Wrong interface listed')


    def test_host_mask_all(self):
        thost = zabbixmgm.zbxhost(self.apimock, mask=fullhost)

        

    def test_host_add_faulty_interfaces(self):
        thost = zabbixmgm.zbxhost(self.apimock, mask=fullhost)
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_interface(24)

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_interface('24')

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_interface(zabbixmgm.zbxhost(self.apimock, name='fake'))




    def test_host_add_faulty_groups(self):
        thost = zabbixmgm.zbxhost(self.apimock, mask=fullhost)
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_group(24)

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_group('24')

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_group(zabbixmgm.zbxhost(self.apimock, name='fake'))


    def test_host_add_faulty_templates(self):
        thost = zabbixmgm.zbxhost(self.apimock, mask=fullhost)
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_template(24)

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_template('24')

        
        with self.assertRaises(zabbixmgm.core.WrongType):
            thost.add_template(zabbixmgm.zbxhost(self.apimock, name='fake'))



    # def test_host_interface_upon_update_2inf(self):

    #     thost = zabbixmgm.zbxhost(self.apimock, host_search_response, name='mytesthost.local')
    #     command, param = thost.get()
    #     self.assertEqual(command, 'host.update')
    #     self.assertTrue('hostid' in param.keys())
    #     self.assertEqual(param['hostid'], '10142')
    #     self.assertEqual(command, thost.apicommands['update'])
    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')
        
    #     inf38 = zabbixmgm.zbxinterface(self.apimock, mask=inf38_response)
    #     thost.add_interface(inf38)
    #     command, param = thost.get()

    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertEqual(len(param['interfaces']), 1, 'interface should be 1 but isn\'t')
    #     self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'Wrong interface listed')


    #     inf39 = zabbixmgm.zbxinterface(self.apimock, mask=inf39_response)
    #     thost.add_interface(inf39)
    #     command, param = thost.get()

    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertEqual(len(param['interfaces']), 2, 'interface should be 2 but isn\'t')
    #     self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'interface 38 not listed')
    #     self.assertTrue({'interfaceid': '39'} in param['interfaces'], 'interface 39 not listed')




    # def test_host_interface_upon_update_3inf_onesametype(self):

    #     thost = zabbixmgm.zbxhost(self.apimock, host_search_response, name='mytesthost.local')
    #     command, param = thost.get()
    #     self.assertEqual(command, 'host.update')
    #     self.assertTrue('hostid' in param.keys())
    #     self.assertEqual(param['hostid'], '10142')
    #     self.assertEqual(command, thost.apicommands['update'])
    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertTrue(len(param['interfaces']) == 0, 'interface should be empty but isn\'t')
        
    #     inf38 = zabbixmgm.zbxinterface(self.apimock, inf38_response)
    #     thost.add_interface(inf38)
    #     command, param = thost.get()

    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertEqual(len(param['interfaces']), 1, 'interface should be 1 but isn\'t')
    #     self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'Wrong interface listed')


    #     inf39 = zabbixmgm.zbxinterface(self.apimock, inf39_response)
    #     thost.add_interface(inf39)
    #     command, param = thost.get()

    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertEqual(len(param['interfaces']), 2, 'interface should be 2 but isn\'t')
    #     self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'interface 38 not listed')
    #     self.assertTrue({'interfaceid': '39'} in param['interfaces'], 'interface 39 not listed')

    #     inf40 = zabbixmgm.zbxinterface(self.apimock, inf40_response)
    #     thost.add_interface(inf40)
    #     command, param = thost.get()
        
    #     self.assertTrue('interfaces' in param.keys())
    #     self.assertEqual(len(param['interfaces']), 3, 'interface should be 3 but isn\'t')
    #     self.assertTrue({'interfaceid': '38'} in param['interfaces'], 'interface 38 not listed')
    #     self.assertTrue({'interfaceid': '39'} in param['interfaces'], 'interface 39 not listed')
    #     self.assertTrue({'interfaceid': '40'} in param['interfaces'], 'interface 40 not listed')


