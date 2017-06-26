from pprint import pprint

class zbx(object):

    inventory = dict()

    def __init__(self, api):
        self.api = api
        self.objectname = None
        self.online_items = dict()


    def get_objectid(self, idstring):
        if idstring in self.online_items.keys():
            return self.online_items[idstring]
        else:
            return 0


    def create_object(self, queryfunction, param={}, online_indicator=None):
        if online_indicator == None:
            online_indicator = len(self.online_items) > 0

        if not online_indicator:
            result = self.api.do_request(queryfunction, param)
            return True

        return False


    def delete_object(self, queryfunction, params):
        if len(self.online_items) > 0:
            result = self.api.do_request(queryfunction, params)

            print('----------------\n{0}: {1}\n\t{2}\n----------------'.format(queryfunction, filter, result))
            return result['result']

        return {}

    def get_query(self, queryfunction, filter=None):

        if not filter:
            query_result = self.api.do_request(queryfunction, {})
        else:
            query_result = self.api.do_request(queryfunction, {
                              'filter': filter,
                              'output': 'extend'
                          })

        print('----------------\n{0}: {1}\n\t{2}\n----------------'.format(queryfunction, filter, query_result))

        if len(query_result['result']) == 1:
            self.online_items = query_result['result'][0]
        elif len(query_result['result']) > 1:
            self.online_items = query_result['result']
        else:
            self.online_items=()

        return self.online_items


    # def get_hosts(self, filter=None):
    #     if not filter:
    #         host = zapi.do_request('host.get', {})
    #     else:
    #         host = zapi.do_request('host.get', {
    #                           'selectGroups': "extend",
    #                           'selectParentTemplates': ["name"],
    #                           'filter': filter,
    #                           'output': 'extend'
    #                       })
    #     return host['result']


    # def get_interfaces(self, hostid=None):
    #     if not filter:
    #         return dict()
    #     else:
    #         interfaces = zapi.do_request('hostinterface.get', {
    #                           'hostids': hostid,
    #                           'output': 'extend'
    #                       })

    #     return interfaces['result']


class zbxinterface(zbx):

    TYPE_AGENT = 1
    TYPE_SNMP = 2
    TYPE_IPMI = 3
    TYPE_JMX = 4

    def __init__(self, api, interfacename):
        super(zbxinterface, self).__init__(api)
        self.online_items  = dict()
        self.objectname = interfacename
        self.set_default_params()

    def get_name(self):
        return self.objectname

    def set_default_params(self):
        self.add_param('type', zbxinterface.TYPE_AGENT)
        self.add_param('main', 0)
        self.add_param('useip', 1)
        self.add_param('dns', '')
        self.add_param('ip', '')
        self.add_param('port', '10050')


    def add_param(self, key, value):
        self.online_items[key] = value

    def set_main(self):
        self.add_param('main', 1)

    def get_interface(self):
        return self.online_items


class zbxhost(zbx):

    def __init__(self, api, hostname):
        super(zbxhost, self).__init__(api)
        self.objectname = hostname
        self.interfaces = dict()
        self.groups = dict()
        self.templates = dict()
        self.update()
        pprint(self.online_items)

    def get_hosts(self, filter=None):
        if not filter:
            host = self.api.do_request('host.get', {})
        else:
            host = self.api.do_request('host.get', {
                              'selectGroups': "extend",
                              'selectParentTemplates': ["name"],
                              'filter': filter,
                              'output': 'extend'
                          })

        self.online_items = host['result']

    def update(self):
        self.get_hosts(filter={'name': self.objectname})


    def get_name(self):
        return self.objectname

    def get_id(self):
        return self.get_objectid('hostid')


    def add_interface(self, interface):
        self.interfaces[interface.get_name()] = interface

    def add_group(self, group):
        self.groups[group.get_name()] = group


    def add_template(self, template):
        self.templates[template.get_name()] = template


    def create(self):
        params = {
                    "host": self.objectname, 
                    "interfaces": [self.interfaces[interf].get_interface() for interf in self.interfaces], 
                    'groups': [{"groupid": self.groups[groupname].get_id()} for groupname in self.groups], 
                    # 'groups': dict(("groupid", self.groups[groupname].get_id()) for groupname in self.groups), 
                    'templates': [{"templateid": self.templates[templatename].get_id()} for templatename in self.templates], 
                    
                }
        pprint(params)
        self.create_object('host.create', params)

    # def delete(self):
    #     if self.get_id() > 0:
    #         result = self.api.do_request('host.delete', [self.hostonline['hostid']])

    #         if 'result' in result and self.hostonline['hostid'] in result['result']['hostids']:
    #             pprint("delete result: {0}".format(result))
    #     else:
    #         print ('no host on zabbix server')




class zbxapplication(zbx):

    def __init__(self, api, applicationname, hostid):
        super(zbxapplication, self).__init__(api)
        self.objectname = applicationname
        self.objecthost = hostid
        self.update()


    def get_applications(self, hostid=None, name=None):

        if (hostid and name) or (not hostid and not name):
            #TODO exception
            return False

        else:
            parameters = {'output': 'extend'}
            if hostid:
                parameters['hostids'] = hostid
            else:
                parameters['names'] = name

            query_result = self.api.do_request('application.get', parameters)

        if len(query_result['result']) == 1:
            self.online_items = query_result['result'][0]
        elif len(query_result['result']) > 1:
            self.online_items = query_result['result']
        else:
            self.online_items=()

        return self.online_items


    def update(self):
        self.get_applications(hostid=self.objecthost)

        if type(self.online_items) == dict():
            if not self.online_items['name'] == self.objectname:
                self.online_items == dict()

    def get_id(self):
        return self.get_objectid('applicationid')


    def create(self):
        params = {'name': self.objectname, 'hostid': self.objecthost}
        self.create_object('application.create', params)
        self.update()
        return self.get_id()


    def delete(self):
        self.delete_object('application.delete', [self.get_id()])


