import core
import interface
import group
import re

from pprint import pprint

class zbxhost(core.zbx):

    def __init__(self, api, hostname, group_instances=list(), interface_instance=None):
        super(zbxhost, self).__init__(api)
        self.objectname = hostname
        self.interfaces = dict()
        self.groups = dict()
        self.templates = dict()
        self.update()

        
        for passed_group in group_instances:
            if type(passed_group) == group.zbxgroup:
                self.add_group(passed_group) 

        if len(self.groups) == 0:
            autogengroup = group.zbxgroup(self.api, 'AutoGroup')
            self.add_group(autogengroup)


        if interface_instance:
            self.add_interface(interface_instance)
        else:
            if not self.interfaces.get(interface.zbxinterface.TYPE_AGENT, False):
                main_agent_interface = interface.zbxinterface(self.api, "agent")
                main_agent_interface.add_param('host', hostname)
                main_agent_interface.add_param('main', 1)
                self.add_interface(main_agent_interface)
        self.create()


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

        if len(host['result']) > 0:
            self.online_items = host['result'][0]
        else:
            self.online_items = dict()

        if len(self.online_items.keys()) > 0:
            interfaces = self.api.do_request('hostinterface.get', {
                                            "output": "extend",
                                            "hostids": self.get_id()
                                        })
            count = 0
            for online_interface in interfaces['result']:
                count = count + 1
                interfaceinst = interface.zbxinterface(self.api, 'int{0}'.format(count))
                
                for intkey in online_interface.keys():
                    if not intkey in ['hostid']:
                        interfaceinst.add_param(intkey, online_interface[intkey])

                interfaceinst.write()
                self.add_interface(interfaceinst)


    def update(self):
        self.get_hosts(filter={'name': self.objectname})

    def get_name(self):
        return self.objectname

    def get_id(self):
        return self.get_objectid('hostid')


    def add_interface(self, interface, overwrite=False):
        tid, tidx = self.serach_interface(interface.get_param('host'), interface.get_param('port'))

        if overwrite:
            self.del_interface(tid, tidx)

        if not tid or overwrite:
            idx = int(interface.get_param('type'))
            if not self.interfaces.get(idx, False):
                self.interfaces[idx] = list()
            
            interface.add_param('hostid', self.get_id())

 

            if len(self.interfaces.get(interface.get_param('type'), list())) == 0:
                interface.add_param('main', 1)
                
            interface.write()
            self.interfaces[idx].append(interface)





    def del_interface(self, tid, tidx):
        del self.interfaces[tid][tidx]
        if len(self.interfaces[tid]) == 0:
            del self.interfaces[tid]


    def serach_interface(self, host, port):
        retval_typeid = None
        retval_index = None
        for typeid in self.interfaces:
            for interfaceobject in self.interfaces[typeid]:
                if len(interfaceobject.get_param('port')) > 0:
                    if_port = int(interfaceobject.get_param('port'))
                else:
                    if_port = 0

                if interfaceobject.get_param('host') == host and if_port == int(port):
                    retval_typeid = typeid
                    retval_index  = self.interfaces[typeid].index(interfaceobject)

        return [retval_typeid, retval_index]


    def add_group(self, group):
        self.groups[group.get_name()] = group


    def add_template(self, template):
        self.templates[template.get_name()] = template


    def create(self):
        params = {
                    "host": self.objectname, 
                    "interfaces": [interface_instance.get_interface() for iftypeid in self.interfaces for interface_instance in self.interfaces[iftypeid]], 
                    'groups': [{"groupid": self.groups[groupname].get_id()} for groupname in self.groups],
                    'templates': [{"templateid": self.templates[templatename].get_id()} for templatename in self.templates], 
                    
                }
        self.create_object('host.create', params)

    # def delete(self):
    #     if self.get_id() > 0:
    #         result = self.api.do_request('host.delete', [self.hostonline['hostid']])

    #         if 'result' in result and self.hostonline['hostid'] in result['result']['hostids']:
    #             pprint("delete result: {0}".format(result))
    #     else:
    #         print ('no host on zabbix server')