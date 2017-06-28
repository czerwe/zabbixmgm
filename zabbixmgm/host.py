import core
import interface
import group
import re

from pprint import pprint

class zbxhost(core.zbx):

    AVAILABLE_UNKNOWN = 0
    AVAILABLE_AVAILABLE = 1
    AVAILABLE_UNAVAILABLE = 2

    FLAGS_PLAIN = 0
    FLASS_DISCOVERED = 1

    INVENTORY_MODE_DISABLED = -1
    INVENTORY_MODE_MANUAL = 0
    INVENTORY_MODE_AUTOMATIC = 1

    IPMI_AUTHTYPE_DEFAULT = -1
    IPMI_AUTHTYPE_NONE = 0
    IPMI_AUTHTYPE_MD2 = 1
    IPMI_AUTHTYPE_MD5 = 2
    IPMI_AUTHTYPE_STRAIGHT = 4
    IPMI_AUTHTYPE_OEM = 5
    IPMI_AUTHTYPE_RMCP = 6

    IPMI_AVAILABLE_UNKNOWN = 0
    IPMI_AVAILABLE_AVAILABLE = 1
    IPMI_AVAILABLE_UNAVAILABLE = 2

    IPMI_PRIVILEGE_CALLBACK = 1
    IPMI_PRIVILEGE_USER = 2
    IPMI_PRIVILEGE_OPERATOR = 3
    IPMI_PRIVILEGE_ADMIN = 4
    IPMI_PRIVILEGE_OEM = 5


    JMX_AVAILABLE_UNKNOWN = 0
    JMX_AVAILABLE_AVAILABLE = 1
    JMX_AVAILABLE_UNAVAILABLE = 2

    MAINTENANCE_STATUS_DISABLED = 0
    MAINTENANCE_STATUS_ENABLE = 1

    MAINTENANCE_TYPE_WITH_DATACOL = 0
    MAINTENANCE_TYPE_NO_DATACOL = 1


    SNMP_AVAILABLE_UNKNOWN = 0
    SNMP_AVAILABLE_AVAILABLE = 1
    SNMP_AVAILABLE_UNAVAILABLE = 2


    STATUS_MONITORED = 0
    STATUS_UNMONITORED = 1


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


    @property
    def hostid(self):
        self.online_items.get('hostid', None)

    @hostid.setter
    def hostid(self, value):
        raise core.ReadOnlyField('hostid is an readonly field')


    @property
    def host(self):
        self.online_items.get('host', '')

    @host.setter
    def host(self, value):
        self.online_items['host'] = value
        if not self.host:
            self.name = value


    @property
    def name(self):
        self.online_items.get('name', None)

    @name.setter
    def name(self, value):
        self.online_items['name'] = value


    @property
    def available(self):
        self.online_items.get('available', 0)

    @available.setter
    def available(self, value):
        raise core.ReadOnlyField('available is an readonly field')


    @property
    def description(self):
        self.online_items.get('description', '')

    @description.setter
    def description(self, value):
        self.online_items['description'] = value


    @property
    def disable_until(self):
        # TODO return timestamp
        self.online_items.get('disable_until', '')

    @disable_until.setter
    def disable_until(self, value):
        raise core.ReadOnlyField('disable_until is an readonly field')


    @property
    def error(self):
        self.online_items.get('error', '')

    @error.setter
    def error(self, value):
        raise core.ReadOnlyField('error is an readonly field')


    @property
    def errors_from(self):
        # TODO return timestamp
        self.online_items.get('errors_from', '')

    @errors_from.setter
    def errors_from(self, value):
        raise core.ReadOnlyField('errors_from is an readonly field')


    @property
    def flags(self):
        self.online_items.get('flags', 0)

    @flags.setter
    def flags(self, value):
        self.online_items['flags'] = value


    @property
    def inventory_mode(self):
        self.online_items.get('inventory_mode', zbxhost.INVENTORY_MODE_MANUAL)

    @inventory_mode.setter
    def inventory_mode(self, value):
        if value in [zbxhost.INVENTORY_MODE_DISABLED, zbxhost.INVENTORY_MODE_MANUAL, zbxhost.INVENTORY_MODE_AUTOMATIC]:
            self.online_items['inventory_mode'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported inventory_mode'.format(value), status=2)


    @property
    def ipmi_authtype(self):
        self.online_items.get('ipmi_authtype', zbxhost.IPMI_AUTHTYPE_DEFAULT)

    @ipmi_authtype.setter
    def ipmi_authtype(self, value):
        if value in [zbxhost.IPMI_AUTHTYPE_DEFAULT, zbxhost.IPMI_AUTHTYPE_NONE, zbxhost.IPMI_AUTHTYPE_MD2, zbxhost.IPMI_AUTHTYPE_MD5, zbxhost.IPMI_AUTHTYPE_STRAIGHT, zbxhost.IPMI_AUTHTYPE_OEM, zbxhost.IPMI_AUTHTYPE_RMCP]:
            self.online_items['ipmi_authtype'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported ipmi_authtype'.format(value), status=2)


    @property
    def ipmi_available(self):
        self.online_items.get('ipmi_available', 0)

    @ipmi_available.setter
    def ipmi_available(self, value):
        raise core.ReadOnlyField('ipmi_available is an readonly field')


    @property
    def ipmi_disable_until(self):
        self.online_items.get('ipmi_disable_until', '')

    @ipmi_disable_until.setter
    def ipmi_disable_until(self, value):
        self.online_items['ipmi_disable_until'] = value


    @property
    def ipmi_error(self):
        self.online_items.get('ipmi_error', '')

    @ipmi_error.setter
    def ipmi_error(self, value):
        raise core.ReadOnlyField('ipmi_error is an readonly field')


    @property
    def ipmi_errors_from(self):
        self.online_items.get('ipmi_errors_from', '')

    @ipmi_errors_from.setter
    def ipmi_errors_from(self, value):
        raise core.ReadOnlyField('ipmi_errors_from is an readonly field')


    @property
    def ipmi_password(self):
        self.online_items.get('ipmi_password', '')

    @ipmi_password.setter
    def ipmi_password(self, value):
        self.online_items['ipmi_password'] = value


    @property
    def ipmi_privilege(self):
        self.online_items.get('ipmi_privilege', zbxhost.IPMI_PRIVILEGE_USER)

    @ipmi_privilege.setter
    def ipmi_privilege(self, value):
        if value in [zbxhost.IPMI_PRIVILEGE_CALLBACK, zbxhost.IPMI_PRIVILEGE_USER, zbxhost.IPMI_PRIVILEGE_OPERATOR, zbxhost.IPMI_PRIVILEGE_ADMIN, zbxhost.IPMI_PRIVILEGE_OEM]:
            self.online_items['ipmi_privilege'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported ipmi_privilege'.format(value), status=2)
        
    
    @property
    def ipmi_username(self):
        self.online_items.get('ipmi_username', '')

    @ipmi_username.setter
    def ipmi_username(self, value):
        self.online_items['ipmi_username'] = value


    @property
    def jmx_available(self):
        self.online_items.get('jmx_available', '')

    @jmx_available.setter
    def jmx_available(self, value):
        raise core.ReadOnlyField('jmx_available is an readonly field')


    @property
    def jmx_disable_until(self):
        self.online_items.get('jmx_disable_until', '')

    @jmx_disable_until.setter
    def jmx_disable_until(self, value):
        raise core.ReadOnlyField('jmx_disable_until is an readonly field')


    @property
    def jmx_error(self):
        self.online_items.get('jmx_error', zbxhost.JMX_AVAILABLE_UNKNOWN)

    @jmx_error.setter
    def jmx_error(self, value):
        raise core.ReadOnlyField('jmx_error is an readonly field')


    @property
    def jmx_errors_from(self):
        self.online_items.get('jmx_errors_from', '')

    @jmx_errors_from.setter
    def jmx_errors_from(self, value):
        raise core.ReadOnlyField('jmx_errors_from is an readonly field')


    @property
    def maintenance_from(self):
        self.online_items.get('maintenance_from', '')

    @maintenance_from.setter
    def maintenance_from(self, value):
        raise core.ReadOnlyField('maintenance_from is an readonly field')


    @property
    def maintenance_status(self):
        self.online_items.get('maintenance_status', zbxhost.MAINTENANCE_STATUS_DISABLED)

    @maintenance_status.setter
    def maintenance_status(self, value):
        raise core.ReadOnlyField('maintenance_status is an readonly field')


    @property
    def maintenance_type(self):
        self.online_items.get('maintenance_type', zbxhost.MAINTENANCE_TYPE_WITH_DATACOL)

    @maintenance_type.setter
    def maintenance_type(self, value):
        raise core.ReadOnlyField('maintenance_type is an readonly field')


    @property
    def maintenanceid(self):
        self.online_items.get('maintenanceid', '')

    @maintenanceid.setter
    def maintenanceid(self, value):
        raise core.ReadOnlyField('maintenanceid is an readonly field')


    @property
    def proxy_hostid(self):
        self.online_items.get('proxy_hostid', '')

    @proxy_hostid.setter
    def proxy_hostid(self, value):
        self.online_items['proxy_hostid'] = value


    @property
    def snmp_available(self):
        self.online_items.get('snmp_available', zbxhost.SNMP_AVAILABLE_UNKNOWN)

    @snmp_available.setter
    def snmp_available(self, value):
        raise core.ReadOnlyField('snmp_available is an readonly field')


    @property
    def snmp_disable_until(self):
        self.online_items.get('snmp_disable_until', '')

    @snmp_disable_until.setter
    def snmp_disable_until(self, value):
        raise core.ReadOnlyField('snmp_disable_until is an readonly field')


    @property
    def snmp_error(self):
        self.online_items.get('snmp_error', '')

    @snmp_error.setter
    def snmp_error(self, value):
        raise core.ReadOnlyField('snmp_error is an readonly field')


    @property
    def snmp_errors_from(self):
        self.online_items.get('snmp_errors_from', '')

    @snmp_errors_from.setter
    def snmp_errors_from(self, value):
        raise core.ReadOnlyField('snmp_errors_from is an readonly field')


    @property
    def status(self):
        self.online_items.get('status', zbxhost.STATUS_MONITORED)

    @status.setter
    def status(self, value):
        self.online_items['status'] = int(value)


    @property
    def tls_issuer(self):
        self.online_items.get('tls_issuer', '')

    @tls_issuer.setter
    def tls_issuer(self, value):
        self.online_items['tls_issuer'] = value


    @property
    def tls_subject(self):
        self.online_items.get('tls_subject', '')

    @tls_subject.setter
    def tls_subject(self, value):
        self.online_items['tls_subject'] = value


    @property
    def tls_psk_identity(self):
        self.online_items.get('tls_psk_identity', '')

    @tls_psk_identity.setter
    def tls_psk_identity(self, value):
        self.online_items['tls_psk_identity'] = value


    @property
    def tls_psk(self): 
        self.online_items.get('tls_psk', '')

    @tls_psk.setter
    def tls_psk(self, value):
        self.online_items['tls_psk'] = value






    # def get_hosts(self, filter=None):
    #     if not filter:
    #         host = self.api.do_request('host.get', {})
    #     else:
    #         host = self.api.do_request('host.get', {
    #                           'selectGroups': "extend",
    #                           'selectParentTemplates': ["name"],
    #                           'filter': filter,
    #                           'output': 'extend'
    #                       })

    #     if len(host['result']) > 0:
    #         self.online_items = host['result'][0]
    #     else:
    #         self.online_items = dict()

    #     if len(self.online_items.keys()) > 0:
    #         interfaces = self.api.do_request('hostinterface.get', {
    #                                         "output": "extend",
    #                                         "hostids": self.get_id()
    #                                     })
    #         count = 0
    #         for online_interface in interfaces['result']:
    #             count = count + 1
    #             interfaceinst = interface.zbxinterface(self.api, 'int{0}'.format(count))
                
    #             for intkey in online_interface.keys():
    #                 if not intkey in ['hostid']:
    #                     interfaceinst.add_param(intkey, online_interface[intkey])

    #             interfaceinst.write()
    #             self.add_interface(interfaceinst)


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




