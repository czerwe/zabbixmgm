import unittest2
import zabbixmgm
from mock import Mock, call
# import responses_group

from pprint import pprint

class group_tests(unittest2.TestCase):

    def setUp(self):
        self.apimock = Mock()


    def tearDown(self):
        pass


    def test_group_setname(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        self.assertEqual(tgroup.name, 'mygroup')


    def test_group_diff(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        fakegroup = {'name':'blub', 'internal': 1}

        left, right, total = tgroup.diff(fakegroup)

        self.assertEqual(len(left), 1)
        self.assertEqual(left['name'], 'mygroup')
        self.assertEqual(len(right), 2)
        self.assertEqual(right['name'], 'blub')
        self.assertEqual(right['internal'], 1)

        self.assertEqual(len(total), 1)
        self.assertEqual(total['internal'], 1)


    def test_group_merge(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        fakegroup = {'groupid': 30,'name':'blub', 'internal': 1}


        self.assertEqual(tgroup.name, 'mygroup')
        self.assertEqual(tgroup.groupid, None)

        tgroup.merge(fakegroup)

        self.assertEqual(tgroup.name, 'blub')
        self.assertEqual(tgroup.groupid, 30)
        self.assertEqual(tgroup.internal, 1)


    def test_group_create_dict(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        
        tgroup.online_items['internal'] = 1
        create_command, cr = tgroup.get('create')
        self.assertEqual(len(cr.keys()), 1)



    def test_group_update_dict(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        fakegroup = {'groupid': 30,'name':'blub', 'internal': 1}
        tgroup.merge(fakegroup)
        
        create_command, cr = tgroup.get('update')
        self.assertEqual(len(cr.keys()), 2)
        self.assertTrue('groupid' in cr.keys())
        self.assertTrue('name' in cr.keys())


    def test_group_delete_dict(self):
        tgroup = zabbixmgm.zbxgroup(self.apimock, 'mygroup')
        fakegroup = {'groupid': 30,'name':'blub', 'internal': 1}
        tgroup.merge(fakegroup)
        
        create_command, cr = tgroup.get('delete')
        self.assertEqual(len(cr), 1)
        self.assertEqual(cr[0], 30)
        



