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


    def __init__(self, api, name, hostmask=None):
        super(zbxhost, self).__init__(api)

        self.host = name

        self.interfaces = dict()
        self.groups = dict()
        self.templates = dict()
        # self.update()


        self.apicommands = {
            "get": "host.get",
            "create": "host.create",
            "update": "host.update",
            "delete": "host.delete",
        }

        self.difffields = ['hostid',
                            'host',
                            'name',
                            'available',
                            'description',
                            'disable_until',
                            'error',
                            'errors_from',
                            'flags',
                            'inventory_mode',
                            'ipmi_authtype',
                            'ipmi_available',
                            'ipmi_disable_until',
                            'ipmi_error',
                            'ipmi_errors_from',
                            'ipmi_password',
                            'ipmi_privilege',
                            'ipmi_username',
                            'jmx_available',
                            'jmx_disable_until',
                            'jmx_error',
                            'jmx_errors_from',
                            'maintenance_from',
                            'maintenance_status',
                            'maintenance_type',
                            'maintenanceid',
                            'proxy_hostid',
                            'snmp_available',
                            'snmp_disable_until',
                            'snmp_error',
                            'snmp_errors_from',
                            'status',
                            'tls_issuer',
                            'tls_subject',
                            'tls_psk_identity',
                            'tls_psk']

        self.readonlyfields = [
                                'hostid',
                                'available',
                                'disable_until',
                                'error',
                                'errors_from',
                                'flags',
                                'ipmi_available', 
                                'ipmi_disable_until',
                                'ipmi_error',
                                'ipmi_errors_from', 
                                'jmx_available',
                                'jmx_disable_until', 
                                'jmx_error', 
                                'jmx_errors_from', 
                                'maintenance_from', 
                                'maintenance_status',
                                'maintenance_type',
                                'maintenanceid',
                                'snmp_available',
                                'snmp_disable_until', 
                                'snmp_error', 
                                'snmp_errors_from',
                            ]



        if hostmask:
            self.merge(hostmask)


    @property
    def id(self):
        return self.hostid

    @property
    def request_result(self):
        return self.hostid
    
    @request_result.setter
    def request_result(self, value):
        result = value.get('result', {})
        ids = result.get('hostids', [])
        if len(ids) >= 1:
            self.online_items['hostid'] = ids[0]

    @property
    def hostid(self):
        return self.online_items.get('hostid', None)

    @hostid.setter
    def hostid(self, value):
        raise core.ReadOnlyField('hostid is an readonly field')


    @property
    def host(self):
        return self.online_items.get('host', '')

    @host.setter
    def host(self, value):
        self.online_items['host'] = value
        if not self.name:
            self.name = value

        self.mergediff['host'] = value


    @property
    def name(self):
        return self.online_items.get('name', None)

    @name.setter
    def name(self, value):
        self.online_items['name'] = value
        self.mergediff['name'] = value


    @property
    def available(self):
        return self.online_items.get('available', 0)

    @available.setter
    def available(self, value):
        raise core.ReadOnlyField('available is an readonly field')


    @property
    def description(self):
        return self.online_items.get('description', '')

    @description.setter
    def description(self, value):
        self.online_items['description'] = value
        self.mergediff['description'] = value


    @property
    def disable_until(self):
        # TODO return timestamp
        return self.online_items.get('disable_until', '')

    @disable_until.setter
    def disable_until(self, value):
        raise core.ReadOnlyField('disable_until is an readonly field')


    @property
    def error(self):
        return self.online_items.get('error', '')

    @error.setter
    def error(self, value):
        raise core.ReadOnlyField('error is an readonly field')


    @property
    def errors_from(self):
        # TODO return timestamp
        return self.online_items.get('errors_from', '')

    @errors_from.setter
    def errors_from(self, value):
        raise core.ReadOnlyField('errors_from is an readonly field')


    @property
    def flags(self):
        return self.online_items.get('flags', 0)

    @flags.setter
    def flags(self, value):
        raise core.ReadOnlyField('flags is an readonly field')
        

    @property
    def inventory_mode(self):
        return self.online_items.get('inventory_mode', zbxhost.INVENTORY_MODE_MANUAL)

    @inventory_mode.setter
    def inventory_mode(self, value):
        if value in [zbxhost.INVENTORY_MODE_DISABLED, zbxhost.INVENTORY_MODE_MANUAL, zbxhost.INVENTORY_MODE_AUTOMATIC]:
            self.online_items['inventory_mode'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported inventory_mode'.format(value), status=2)


    @property
    def ipmi_authtype(self):
        return self.online_items.get('ipmi_authtype', zbxhost.IPMI_AUTHTYPE_DEFAULT)

    @ipmi_authtype.setter
    def ipmi_authtype(self, value):
        if value in [zbxhost.IPMI_AUTHTYPE_DEFAULT, zbxhost.IPMI_AUTHTYPE_NONE, zbxhost.IPMI_AUTHTYPE_MD2, zbxhost.IPMI_AUTHTYPE_MD5, zbxhost.IPMI_AUTHTYPE_STRAIGHT, zbxhost.IPMI_AUTHTYPE_OEM, zbxhost.IPMI_AUTHTYPE_RMCP]:
            self.online_items['ipmi_authtype'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported ipmi_authtype'.format(value), status=2)


    @property
    def ipmi_available(self):
        return self.online_items.get('ipmi_available', 0)

    @ipmi_available.setter
    def ipmi_available(self, value):
        raise core.ReadOnlyField('ipmi_available is an readonly field')


    @property
    def ipmi_disable_until(self):
        return self.online_items.get('ipmi_disable_until', '')

    @ipmi_disable_until.setter
    def ipmi_disable_until(self, value):
        raise core.ReadOnlyField('ipmi_disable_until is an readonly field')


    @property
    def ipmi_error(self):
        return self.online_items.get('ipmi_error', '')

    @ipmi_error.setter
    def ipmi_error(self, value):
        raise core.ReadOnlyField('ipmi_error is an readonly field')


    @property
    def ipmi_errors_from(self):
        return self.online_items.get('ipmi_errors_from', '')

    @ipmi_errors_from.setter
    def ipmi_errors_from(self, value):
        raise core.ReadOnlyField('ipmi_errors_from is an readonly field')


    @property
    def ipmi_password(self):
        return self.online_items.get('ipmi_password', '')

    @ipmi_password.setter
    def ipmi_password(self, value):
        self.online_items['ipmi_password'] = value
        self.mergediff['ipmi_password'] = value


    @property
    def ipmi_privilege(self):
        return self.online_items.get('ipmi_privilege', zbxhost.IPMI_PRIVILEGE_USER)

    @ipmi_privilege.setter
    def ipmi_privilege(self, value):
        if value in [zbxhost.IPMI_PRIVILEGE_CALLBACK, zbxhost.IPMI_PRIVILEGE_USER, zbxhost.IPMI_PRIVILEGE_OPERATOR, zbxhost.IPMI_PRIVILEGE_ADMIN, zbxhost.IPMI_PRIVILEGE_OEM]:
            self.online_items['ipmi_privilege'] = int(value)
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported ipmi_privilege'.format(value), status=2)
        
    
    @property
    def ipmi_username(self):
        return self.online_items.get('ipmi_username', '')

    @ipmi_username.setter
    def ipmi_username(self, value):
        self.online_items['ipmi_username'] = value
        self.mergediff['ipmi_username'] = value


    @property
    def jmx_available(self):
        return self.online_items.get('jmx_available', '')

    @jmx_available.setter
    def jmx_available(self, value):
        raise core.ReadOnlyField('jmx_available is an readonly field')


    @property
    def jmx_disable_until(self):
        return self.online_items.get('jmx_disable_until', '')

    @jmx_disable_until.setter
    def jmx_disable_until(self, value):
        raise core.ReadOnlyField('jmx_disable_until is an readonly field')


    @property
    def jmx_error(self):
        return self.online_items.get('jmx_error', zbxhost.JMX_AVAILABLE_UNKNOWN)

    @jmx_error.setter
    def jmx_error(self, value):
        raise core.ReadOnlyField('jmx_error is an readonly field')


    @property
    def jmx_errors_from(self):
        return self.online_items.get('jmx_errors_from', '')

    @jmx_errors_from.setter
    def jmx_errors_from(self, value):
        raise core.ReadOnlyField('jmx_errors_from is an readonly field')


    @property
    def maintenance_from(self):
        return self.online_items.get('maintenance_from', '')

    @maintenance_from.setter
    def maintenance_from(self, value):
        raise core.ReadOnlyField('maintenance_from is an readonly field')


    @property
    def maintenance_status(self):
        return self.online_items.get('maintenance_status', zbxhost.MAINTENANCE_STATUS_DISABLED)

    @maintenance_status.setter
    def maintenance_status(self, value):
        raise core.ReadOnlyField('maintenance_status is an readonly field')


    @property
    def maintenance_type(self):
        return self.online_items.get('maintenance_type', zbxhost.MAINTENANCE_TYPE_WITH_DATACOL)

    @maintenance_type.setter
    def maintenance_type(self, value):
        raise core.ReadOnlyField('maintenance_type is an readonly field')


    @property
    def maintenanceid(self):
        return self.online_items.get('maintenanceid', '')

    @maintenanceid.setter
    def maintenanceid(self, value):
        raise core.ReadOnlyField('maintenanceid is an readonly field')


    @property
    def proxy_hostid(self):
        return self.online_items.get('proxy_hostid', '')

    @proxy_hostid.setter
    def proxy_hostid(self, value):
        self.online_items['proxy_hostid'] = value
        self.mergediff['proxy_hostid'] = value


    @property
    def snmp_available(self):
        return self.online_items.get('snmp_available', zbxhost.SNMP_AVAILABLE_UNKNOWN)

    @snmp_available.setter
    def snmp_available(self, value):
        raise core.ReadOnlyField('snmp_available is an readonly field')


    @property
    def snmp_disable_until(self):
        return self.online_items.get('snmp_disable_until', '')

    @snmp_disable_until.setter
    def snmp_disable_until(self, value):
        raise core.ReadOnlyField('snmp_disable_until is an readonly field')


    @property
    def snmp_error(self):
        return self.online_items.get('snmp_error', '')

    @snmp_error.setter
    def snmp_error(self, value):
        raise core.ReadOnlyField('snmp_error is an readonly field')


    @property
    def snmp_errors_from(self):
        return self.online_items.get('snmp_errors_from', '')

    @snmp_errors_from.setter
    def snmp_errors_from(self, value):
        raise core.ReadOnlyField('snmp_errors_from is an readonly field')


    @property
    def status(self):
        return self.online_items.get('status', zbxhost.STATUS_MONITORED)

    @status.setter
    def status(self, value):
        self.online_items['status'] = int(value)
        self.mergediff['status'] = value


    @property
    def tls_issuer(self):
        return self.online_items.get('tls_issuer', '')

    @tls_issuer.setter
    def tls_issuer(self, value):
        self.online_items['tls_issuer'] = value
        self.mergediff['tls_issuer'] = value


    @property
    def tls_subject(self):
        return self.online_items.get('tls_subject', '')

    @tls_subject.setter
    def tls_subject(self, value):
        self.online_items['tls_subject'] = value
        self.mergediff['tls_subject'] = value


    @property
    def tls_psk_identity(self):
        return self.online_items.get('tls_psk_identity', '')

    @tls_psk_identity.setter
    def tls_psk_identity(self, value):
        self.online_items['tls_psk_identity'] = value
        self.mergediff['tls_psk_identity'] = value


    @property
    def tls_psk(self): 
        return self.online_items.get('tls_psk', '')

    @tls_psk.setter
    def tls_psk(self, value):
        self.online_items['tls_psk'] = value
        self.mergediff['tls_psk'] = value


    def interface_inventory(self, interfaces):
        for single_interface in interfaces:
            tmpint = interface.zbxinterface(self.api, single_interface['name'], single_interface)
            self.add_interface(tmpint)


    def interface_mains(self):
        for itype in self.interfaces.keys():
            if not 1 in [ifac.main for ifac in self.interfaces[itype]] and len(self.interfaces[itype]) >= 1:
                self.interfaces[itype][0].main = 1



    def add_interface(self, interface):
        tid, tidx = self.search_interface(host=interface.host, port=interface.port)



        idx = interface.type
        if not tid :
            if not self.interfaces.get(idx, False):
                self.interfaces[idx] = list()
        
            self.interfaces[idx].append(interface)
            interface.hostid = self.id





    def del_interface(self, tid, tidx):
        del self.interfaces[tid][tidx]
        if len(self.interfaces[tid]) == 0:
            del self.interfaces[tid]


    def search_interface(self, host=None, port=None, searchtype='both'):
        retval_typeid = None
        retval_index = None
        for typeid in self.interfaces.keys():
            for interfaceobject in self.interfaces[typeid]:
                ok = False
                if searchtype == 'both':
                    ok = interfaceobject.host == host and interfaceobject.port == str(port)
                elif searchtype == 'port':
                    ok = interfaceobject.port == str(port)
                elif searchtype == 'host':
                    ok = interfaceobject.host == host

                if ok:
                    retval_typeid = typeid
                    retval_index  = self.interfaces[typeid].index(interfaceobject)
                    break

            if retval_typeid:
                break

        return [retval_typeid, retval_index]


    def add_group(self, group):
        self.groups[group.name] = group

    def add_template(self, template):
        self.templates[template.name] = template

    def get(self, param_type=None):
        retval = dict()
        if not param_type:
            if self.id:
                param_type = 'update'
            else:
                param_type = 'create'


        if param_type == 'create':
            if self.id:
                return [False, retval]
            
            self.interface_mains()

            retval = dict(self.online_items)
            retval['interfaces'] = [interface_instance.get('hostcreate')[1] for iftypeid in self.interfaces for interface_instance in self.interfaces[iftypeid]]
            retval['groups'] = [{"groupid": self.groups[groupname].id} for groupname in self.groups]
            retval['templates'] = [{"templateid": self.templates[templatename].id} for templatename in self.templates]

        if param_type == 'update':
            if not self.id:
                return [False, retval]
            retval = dict(self.mergediff)
            retval['hostid'] = self.id
            retval['groups'] = [{"groupid": self.groups[groupname].id} for groupname in self.groups]
            retval['templates'] = [{"templateid": self.templates[templatename].id} for templatename in self.templates]




        if param_type in ['create', 'update']:
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'hostid':
                        continue
                    else:
                        del retval[param]


        elif param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()

        pprint(retval)

        return [self.apicommands[param_type], retval]