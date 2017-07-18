# import unittest2
# import zabbixmgm
# from mock import Mock, call
# import responses_interface

# from pprint import pprint


# class interface_tests(unittest2.TestCase):

#     def setUp(self):
#         self.apimock = Mock()


#     def tearDown(self):
#         pass


#     def test_index_nonexist(self):
#         self.apimock.do_request.side_effect = [responses_group.empty, responses_group.group_existing_one]

#         grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')

#         self.apimock.assert_has_calls([call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})])
#         self.assertEqual(len(self.apimock.mock_calls), 1)

    



    
#     # def test_index_exist(self):
#     #     self.apimock.do_request.side_effect = [responses_group.group_existing_one]

#     #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')

#     #     self.apimock.assert_has_calls([call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})])
#     #     self.assertEqual(int(grp.get_id()), 8, 'GroupID does not match')
#     #     self.assertEqual(len(self.apimock.mock_calls), 1)

    
#     # def test_create_nonexist(self):
#     #     self.apimock.do_request.side_effect = [responses_group.empty, responses_group.group_created_success, responses_group.group_existing_one]

#     #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
#     #     grp.create()
#     #     self.apimock.assert_has_calls(
#     #             [
#     #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'}),
#     #                 call.do_request('hostgroup.create', {'name': 'myhosts'}),
#     #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
#     #             ]
#     #         )

#     #     self.assertEqual(len(self.apimock.mock_calls), 3)
#     #     self.assertEqual(int(grp.get_id()), 8)
        

#     # def test_create_exist(self):
#     #     self.apimock.do_request.side_effect = [responses_group.group_existing_one, responses_group.group_created_success, responses_group.group_existing_one]

#     #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
#     #     grp.create()
#     #     self.apimock.assert_has_calls(
#     #             [
#     #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
#     #             ]
#     #         )
#     #     self.assertEqual(len(self.apimock.mock_calls), 1)
#     #     self.assertEqual(int(grp.get_id()), 8)
        

#     # def test_delete_exist(self):
#     #     self.apimock.do_request.side_effect = [responses_group.group_existing_one, responses_group.group_delete_success, responses_group.empty]#,, responses_group.group_existing_one]

#     #     grp = zabbixmgm.zbxgroup(self.apimock, 'myhosts')
#     #     self.assertEqual(int(grp.get_id()), 8)
#     #     grp.delete()
#     #     self.apimock.assert_has_calls(
#     #             [
#     #                 call.do_request('hostgroup.get', {'filter': {'name': 'myhosts'}, 'output': 'extend'})
#     #             ]
#     #         )
#     #     self.assertEqual(len(self.apimock.mock_calls), 3)
#     #     self.assertEqual(int(grp.get_id()), 0)
        

