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


    def test_intf_host_dns(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.online_items['ip'], '127.0.0.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)

        iface.host = 'test.host.local'
        self.assertEqual(iface.online_items['ip'], '')
        self.assertEqual(iface.online_items['dns'], 'test.host.local')
        self.assertEqual(iface.online_items['useip'], 0)


    def test_intf_host_ip(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.online_items['ip'], '127.0.0.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)

        iface.host = '10.0.0.1'
        self.assertEqual(iface.online_items['ip'], '10.0.0.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)


    def test_intf_host_ip2dns2ip(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        self.assertEqual(iface.online_items['ip'], '127.0.0.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)

        iface.host = '10.0.0.1'
        self.assertEqual(iface.online_items['ip'], '10.0.0.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)

        iface.host = 'test2.host.local'
        self.assertEqual(iface.online_items['ip'], '')
        self.assertEqual(iface.online_items['dns'], 'test2.host.local')
        self.assertEqual(iface.online_items['useip'], 0)

        iface.host = '10.0.1.1'
        self.assertEqual(iface.online_items['ip'], '10.0.1.1')
        self.assertEqual(iface.online_items['dns'], '')
        self.assertEqual(iface.online_items['useip'], 1)


    def test_intf_main(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        
        self.assertEqual(iface.online_items['main'], 0)
        iface.main = 1
        self.assertEqual(iface.online_items['main'], 1)

        iface.main = False
        self.assertEqual(iface.online_items['main'], 0)

        iface.main = True
        self.assertEqual(iface.online_items['main'], 1)

        iface.main = 'no'
        self.assertEqual(iface.online_items['main'], 0)

        iface.main = 'yes'
        self.assertEqual(iface.online_items['main'], 1)

        with self.assertRaises(zabbixmgm.core.InvalidFieldValue):
            iface.main = 'blub'
        


    def test_intf_port(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        
        self.assertEqual(iface.online_items['port'], '10050')
        self.assertEqual(iface.online_items['port'], iface.port)

        iface.port = 12345

        self.assertEqual(iface.online_items['port'], '12345')
        self.assertEqual(iface.online_items['port'], iface.port)
        self.assertEqual(type(iface.online_items['port']), str)



    def test_intf_type(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        
        self.assertEqual(iface.online_items['type'], 1)
        self.assertEqual(iface.online_items['type'], iface.type)
        self.assertEqual(type(iface.online_items['type']), int)

        iface.type = zabbixmgm.zbxinterface.TYPE_JMX

        self.assertEqual(iface.online_items['type'], 4)
        self.assertEqual(iface.online_items['type'], iface.type)
        self.assertEqual(type(iface.online_items['type']), int)

        iface.type = '3'
        self.assertEqual(iface.online_items['type'], 3)
        self.assertEqual(iface.online_items['type'], iface.type)
        self.assertEqual(type(iface.online_items['type']), int)

        with self.assertRaises(zabbixmgm.core.InvalidFieldValue):
            iface.type = '6'
        


    def test_intf_diff_simple(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = 1234

        command, param = iface2.get('hostcreate')
        left, right, total = iface.diff(param)
        self.assertEqual(left['port'], '10050')
        self.assertEqual(right['port'], '1234')


    def test_intf_diff_complex(self):
        iface1 = zabbixmgm.zbxinterface(self.apimock)
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface1.port = 5432
        iface2.port = 1234
        iface2.bulk = 1

        iface2.main = 0

        command, param = iface2.get('hostcreate')
        left, right, total = iface1.diff(param)
        self.assertEqual(left['port'], '5432')
        self.assertEqual(right['port'], '1234')
        self.assertEqual(right['bulk'], 1)
        self.assertEqual(total['bulk'], 1)



    def test_intf_merge_simple2(self):
        iface = zabbixmgm.zbxinterface(self.apimock)
        iface2 = zabbixmgm.zbxinterface(self.apimock)
        iface2.port = 1234

        command, param = iface2.get('hostcreate')
        left, right, total = iface.diff(param)
        self.assertEqual(left['port'], '10050')
        self.assertEqual(right['port'], '1234')

        iface.merge(iface2.get('hostcreate')[1])
        left, right, total = iface.diff(iface2.get('hostcreate')[1])

        self.assertEqual(len(left.keys()), 0)
        self.assertEqual(len(right.keys()), 0)
        self.assertEqual(len(total.keys()), 0)





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
        

