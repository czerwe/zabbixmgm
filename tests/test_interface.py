import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_interface

from pprint import pprint


class interface_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass

    def test_intf_get_auto_create_missing_hostid(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        with self.assertRaises(zabbixmgm.core.MissingField):
            command, param = iface.get()
            # self.assertEqual(command, 'hostinterface.create')


    def test_intf_get_auto_create_dict(self):
        iface = zabbixmgm.zbxinterface(self.apimock, mask={'hostid': 777})
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.create')
        self.assertTrue(not 'interfaceid' in param)
        self.assertTrue('hostid' in param)
        self.assertTrue('main' in param)
        self.assertTrue('useip' in param)
        self.assertTrue('dns' in param)
        self.assertTrue('ip' in param)
        self.assertTrue('port' in param)
        self.assertTrue('bulk' in param)
        self.assertTrue('type' in param)


    def test_intf_get_auto_update_dict(self):
        iface = zabbixmgm.zbxinterface(self.apimock, mask={'hostid': 777, 'interfaceid': 888})
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.update')
        self.assertTrue('hostid' in param)
        self.assertTrue('main' in param)
        self.assertTrue('useip' in param)
        self.assertTrue('dns' in param)
        self.assertTrue('ip' in param)
        self.assertTrue('port' in param)
        self.assertTrue('bulk' in param)
        self.assertTrue('type' in param)
        self.assertTrue('interfaceid' in param)

    def test_intf_get_auto_hostcreate_dict(self):
        iface = zabbixmgm.zbxinterface(self.apimock, mask={'hostid': 777, 'interfaceid': 888})
        command, param = iface.get('hostcreate')
        self.assertEqual(command, 'hostinterface.create')
        self.assertTrue(not 'hostid' in param)
        self.assertTrue(not 'interfaceid' in param)
        self.assertTrue('main' in param)
        self.assertTrue('useip' in param)
        self.assertTrue('dns' in param)
        self.assertTrue('ip' in param)
        self.assertTrue('port' in param)
        self.assertTrue('bulk' in param)
        self.assertTrue('type' in param)
        
    def test_intf_get_auto_create_defaults(self):
        iface = zabbixmgm.zbxinterface(self.apimock, hostid=123)
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.create')
        self.assertTrue(not 'interfaceid' in param)
        self.assertTrue('hostid' in param)
        self.assertEqual(param['hostid'], '123')
        self.assertTrue('main' in param)
        self.assertEqual(param['main'], 0)
        self.assertTrue('useip' in param)
        self.assertEqual(param['useip'], 1)
        self.assertTrue('dns' in param)
        self.assertEqual(param['dns'], '')
        self.assertTrue('ip' in param)
        self.assertEqual(param['ip'], '127.0.0.1')
        self.assertTrue('port' in param)
        self.assertEqual(param['port'], '10050')
        self.assertTrue('bulk' in param)
        self.assertEqual(param['bulk'], 1)
        self.assertTrue('type' in param)
        self.assertEqual(param['type'], zabbixmgm.zbxinterface.TYPE_AGENT)

    def test_intf_get_auto_create_hostChanges(self):
        iface = zabbixmgm.zbxinterface(self.apimock, hostid=123, host='testhost.local')
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.create')
        self.assertTrue(not 'interfaceid' in param)
        self.assertTrue('hostid' in param)
        self.assertEqual(param['hostid'], '123')
        self.assertTrue('main' in param)
        self.assertEqual(param['main'], 0)
        self.assertTrue('useip' in param)
        self.assertEqual(param['useip'], 0)
        self.assertTrue('dns' in param)
        self.assertEqual(param['dns'], 'testhost.local')
        self.assertTrue('ip' in param)
        self.assertEqual(param['ip'], '')
        self.assertTrue('port' in param)
        self.assertEqual(param['port'], '10050')
        self.assertTrue('bulk' in param)
        self.assertEqual(param['bulk'], 1)
        self.assertTrue('type' in param)
        self.assertEqual(param['type'], zabbixmgm.zbxinterface.TYPE_AGENT)

    def test_intf_get_auto_create_changevalues(self):
        iface = zabbixmgm.zbxinterface(self.apimock, hostid=123, main=1, bulk=0, type=zabbixmgm.zbxinterface.TYPE_JMX)
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.create')
        self.assertTrue(not 'interfaceid' in param)
        self.assertTrue('hostid' in param)
        self.assertEqual(param['hostid'], '123')
        self.assertTrue('main' in param)
        self.assertEqual(param['main'], 1)
        self.assertTrue('useip' in param)
        self.assertEqual(param['useip'], 1)
        self.assertTrue('dns' in param)
        self.assertEqual(param['dns'], '')
        self.assertTrue('ip' in param)
        self.assertEqual(param['ip'], '127.0.0.1')
        self.assertTrue('port' in param)
        self.assertEqual(param['port'], '10050')
        self.assertTrue('bulk' in param)
        self.assertEqual(param['bulk'], 0)
        self.assertTrue('type' in param)
        self.assertEqual(param['type'], zabbixmgm.zbxinterface.TYPE_JMX)


    def test_intf_get_auto_update_dict_correctcheck(self):
        iface = zabbixmgm.zbxinterface(self.apimock, mask={'hostid': 777, 'interfaceid': 888})
        command, param = iface.get()
        self.assertEqual(command, 'hostinterface.update')
        self.assertTrue('hostid' in param)
        self.assertEqual(param['hostid'], '777')
        self.assertTrue('main' in param)
        self.assertTrue('useip' in param)
        self.assertTrue('dns' in param)
        self.assertTrue('ip' in param)
        self.assertTrue('port' in param)
        self.assertTrue('bulk' in param)
        self.assertTrue('type' in param)
        self.assertTrue('interfaceid' in param)
        self.assertEqual(param['interfaceid'], '888')


    
    def test_intf_host_dns(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.ip, '127.0.0.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)

        iface.host = 'test.host.local'
        self.assertEqual(iface.ip, '')
        self.assertEqual(iface.dns, 'test.host.local')
        self.assertEqual(iface.useip, 0)


    def test_intf_host_ip(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.ip, '127.0.0.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)

        iface.host = '10.0.0.1'
        self.assertEqual(iface.ip, '10.0.0.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)


    def test_intf_host_ip2dns2ip(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.ip, '127.0.0.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)

        iface.host = '10.0.0.1'
        self.assertEqual(iface.ip, '10.0.0.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)

        iface.host = 'test2.host.local'
        self.assertEqual(iface.ip, '')
        self.assertEqual(iface.dns, 'test2.host.local')
        self.assertEqual(iface.useip, 0)

        iface.host = '10.0.1.1'
        self.assertEqual(iface.ip, '10.0.1.1')
        self.assertEqual(iface.dns, '')
        self.assertEqual(iface.useip, 1)

    # DEPRICATED TESTS

    # def test_intf_main(self):
    #     iface = zabbixmgm.zbxinterface(self.apimock)
        
    #     self.assertEqual(iface.main, 0)
    #     iface.main = 1
    #     self.assertEqual(iface.main, 1)

    #     iface.main = False
    #     self.assertEqual(iface.main, 0)

    #     iface.main = True
    #     self.assertEqual(iface.main, 1)

    #     iface.main = 'no'
    #     self.assertEqual(iface.main, 0)

    #     iface.main = 'yes'
    #     self.assertEqual(iface.main, 1)

    #     with self.assertRaises(zabbixmgm.core.InvalidFieldValue):
    #         iface.main = 'blub'
        


    # def test_intf_port(self):
    #     iface = zabbixmgm.zbxinterface(self.apimock)
        
    #     self.assertEqual(iface.port, '10050')
    #     self.assertEqual(iface.port, iface.port)

    #     iface.port = 12345

    #     self.assertEqual(iface.port, '12345')
    #     self.assertEqual(iface.port, iface.port)
    #     self.assertEqual(type(iface.port), str)



    # def test_intf_type(self):
    #     iface = zabbixmgm.zbxinterface(self.apimock)
        
    #     self.assertEqual(iface.type, 1)
    #     self.assertEqual(type(iface.type), int)

    #     iface.type = zabbixmgm.zbxinterface.TYPE_JMX

    #     self.assertEqual(iface.type, 4)
    #     self.assertEqual(type(iface.type), int)

    #     iface.type = '3'
    #     self.assertEqual(iface.type, 3)
    #     self.assertEqual(type(iface.type), int)

    #     with self.assertRaises(zabbixmgm.core.InvalidFieldValue):
    #         iface.type = '6'
        


    # def test_intf_diff_simple(self):
    #     iface = zabbixmgm.zbxinterface(self.apimock)
    #     iface2 = zabbixmgm.zbxinterface(self.apimock)
    #     iface2.port = 1234

    #     command, param = iface2.get('hostcreate')
    #     left, right, total = iface.diff(param)
    #     self.assertEqual(left['port'], '10050')
    #     self.assertEqual(right['port'], '1234')


    # def test_intf_diff_complex(self):
    #     iface1 = zabbixmgm.zbxinterface(self.apimock)
    #     iface2 = zabbixmgm.zbxinterface(self.apimock)
    #     iface1.port = 5432
    #     iface2.port = 1234
    #     iface2.bulk = 1

    #     iface2.main = 0

    #     command, param = iface2.get('hostcreate')
    #     left, right, total = iface1.diff(param)
    #     self.assertEqual(left['port'], '5432')
    #     self.assertEqual(right['port'], '1234')
    #     self.assertEqual(right['bulk'], 1)
    #     self.assertEqual(total['bulk'], 1)



    # def test_intf_merge_simple2(self):
    #     iface = zabbixmgm.zbxinterface(self.apimock)
    #     iface2 = zabbixmgm.zbxinterface(self.apimock)
    #     iface2.port = 1234

    #     command, param = iface2.get('hostcreate')
    #     left, right, total = iface.diff(param)
    #     self.assertEqual(left['port'], '10050')
    #     self.assertEqual(right['port'], '1234')

    #     iface.merge(iface2.get('hostcreate')[1])
    #     left, right, total = iface.diff(iface2.get('hostcreate')[1])

    #     self.assertEqual(len(left.keys()), 0)
    #     self.assertEqual(len(right.keys()), 0)
    #     self.assertEqual(len(total.keys()), 0)



# ARTEFICIAL

    # def test_intf_index_exist(self):
    #     self.apimock.do_request.side_effect = [responses_group.group_existing_one]

    #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')

    #     self.apimock.assert_has_calls([call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})])
    #     self.assertEqual(int(grp.get_id()), 8, 'GroupID does not match')
    #     self.assertEqual(len(self.apimock.mock_calls), 1)

    
    # def test_intf_create_nonexist(self):
    #     self.apimock.do_request.side_effect = [responses_group.empty, responses_group.group_created_success, responses_group.group_existing_one]

    #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
    #     grp.create()
    #     self.apimock.assert_has_calls(
    #             [
    #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'}),
    #                 call.do_request('hostgroup.create', {'name': 'myhosts'}),
    #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
    #             ]
    #         )

    #     self.assertEqual(len(self.apimock.mock_calls), 3)
    #     self.assertEqual(int(grp.get_id()), 8)
        

    # def test_intf_create_exist(self):
    #     self.apimock.do_request.side_effect = [responses_group.group_existing_one, responses_group.group_created_success, responses_group.group_existing_one]

    #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
    #     grp.create()
    #     self.apimock.assert_has_calls(
    #             [
    #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
    #             ]
    #         )
    #     self.assertEqual(len(self.apimock.mock_calls), 1)
    #     self.assertEqual(int(grp.get_id()), 8)
        

    # def test_intf_delete_exist(self):
    #     self.apimock.do_request.side_effect = [responses_group.group_existing_one, responses_group.group_delete_success, responses_group.empty]#,, responses_group.group_existing_one]

    #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
    #     self.assertEqual(int(grp.get_id()), 8)
    #     grp.delete()
    #     self.apimock.assert_has_calls(
    #             [
    #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
    #             ]
    #         )
    #     self.assertEqual(len(self.apimock.mock_calls), 3)
    #     self.assertEqual(int(grp.get_id()), 0)
        

