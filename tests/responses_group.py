
empty = {
           u'id': u'1',
           u'jsonrpc': u'2.0',
           u'result': []
           }

group_full_list = {
                    u'id': u'1',
                    u'jsonrpc': u'2.0',
                    u'result': [
                        {   u'flags': u'0',
                            u'groupid': u'1',
                            u'internal': u'0',
                            u'name': u'Templates'},
                         {  u'flags': u'0',
                            u'groupid': u'2',
                            u'internal': u'0',
                            u'name': u'Linux servers'},
                         {  u'flags': u'0',
                            u'groupid': u'4',
                            u'internal': u'0',
                            u'name': u'Zabbix servers'},
                         {  u'flags': u'0',
                            u'groupid': u'5',
                            u'internal': u'1',
                            u'name': u'Discovered hosts'},
                         {  u'flags': u'0',
                            u'groupid': u'6',
                            u'internal': u'0',
                            u'name': u'Virtual machines'},
                         {  u'flags': u'0',
                            u'groupid': u'7',
                            u'internal': u'0',
                            u'name': u'Hypervisors'}
                          ]
                        }


group_existing_one = {
                    u'id': u'1',
                    u'jsonrpc': u'2.0',
                    u'result': [
                         {  u'flags': u'0',
                            u'groupid': u'8',
                            u'internal': u'0',
                            u'name': u'myhosts'}
                          ]
                        }

group_created_success = {
                            u'id': u'1',
                            u'jsonrpc': u'2.0', 
                            u'result': [
                                        {
                                            u'internal': u'0', 
                                            u'flags': u'0', 
                                            u'groupid': u'8', 
                                            u'name': 
                                            u'myhosts'}
                                        ]
                    
                        }

group_delete_success = {
                            u'id': u'1',
                            u'jsonrpc': u'2.0', 
                            u'result': {
                                            u'groupids': [
                                                            u'8'
                                                        ]
                                        }
                        }