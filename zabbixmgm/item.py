import core


class zbxitem(core.zbx):

    TYPE_ZABBIX_AGENT = 0
    TYPE_SNMPV1_AGENT = 1
    TYPE_ZABBIX_TRAPPER = 2
    TYPE_SIMPLE_CHECK = 3
    TYPE_SNMPV2_AGENT = 4
    TYPE_ZABBIX_INTERNAL = 5
    TYPE_SNMPV3_AGENT = 6
    TYPE_ZABBIX_AGENT_ACTIVE = 7
    TYPE_ZABBIX_AGGREGATE = 8
    TYPE_WEB_ITEM = 9
    TYPE_EXTERNAL_CHECK = 10
    TYPE_DATABASE_MONITOR = 11
    TYPE_IPMI_AGENT = 12
    TYPE_SSH_AGENT = 13
    TYPE_TELNET_AGENT = 14
    TYPE_CALCULATED = 15
    TYPE_JMX_AGENT = 16
    TYPE_SNMP_TRAP = 17

    VAL_TYPE_NUMERIC_FLOAT = 0
    VAL_TYPE_CHARACTER = 1
    VAL_TYPE_LOG = 2
    VAL_TYPE_NUMERIC_UNSIGNED = 3
    VAL_TYPE_TEXT = 4

    AUTHTYPE_PASSWORD = 0
    AUTHTYPE_KEY =1

    DATA_TYPE_DECIMAL = 0
    DATA_TYPE_OCTAL = 1
    DATA_TYPE_DEXADECIMAL = 2
    DATA_TYPE_BOOLEAN = 3

    DELTA_ASIS =  0
    DELTA_PERSECOND = 1
    DELTA_SIMPLECHANGE = 2 

    FLAGS_PLAIN = 0
    FLASS_DISCOVERED = 1

    STATE_NORMAL = 0
    STATE_NOTSUPPORTED = 1

    STATUS_ENABLED = 0
    STATUS_DISABLED = 1

    SNMPV3_AUTHPROTOCOL_DES = 0
    SNMPV3_AUTHPROTOCOL_SHA = 1

    SNMPV3_PRIVROTOCOL_DES = 0
    SNMPV3_PRIVROTOCOL_SHA = 1

    SNMPV3_SECURITYLEVEL_NOAUTHNOPRIV = 0
    SNMPV3_SECURITYLEVEL_AUTHNOPRIV = 1
    SNMPV3_SECURITYLEVEL_AUTHPRIV = 2



    def __init__(self, api, name, itemmask=None):
        super(zbxitem, self).__init__(api)

        self.name = name
        self.applications = dict()
        self.host = None


        self.apicommands = {
            "get": "item.get",
            "create": "item.create",
            "update": "item.update",
            "delete": "item.delete",
        }

        self.difffields = [
            'itemid',
            'delay',
            'interfaceid',
            'key',
            'name',
            'type',
            'value_type',
            'data_type',
            'delay_flex',
            'delta',
            'description',
            'error',
            'flags',
            'formula',
            'history',
            'inventory_link',
            'ipmi_sensor',
            'lastclock',
            'lastns',
            'lastvalue',
            'logtimefmt',
            'mtime',
            'multiplier',
            'params',
            'password',
            'port',
            'prevvalue',
            'privatekey',
            'publickey',
            'snmp_community',
            'snmp_oid',
            'snmpv3_authpassphrase',
            'snmpv3_authprotocol',
            'snmpv3_contextname',
            'snmpv3_privprotocol',
            'snmpv3_securityname',
            'state',
            'status',
            'templateid',
            'trapper_hosts',
            'trends',
            'units',
            'username',
            'valuemapid'
        ]

        self.readonlyfields = [
            'itemid',
            'error',
            'flags',
            'lastclock',
            'lastns',
            'lastvalue',
            'prevvalue',
            'templateid',

        ]


        if itemmask:
            self.merge(itemmask)


    @property
    def id(self):
        return self.itemid

    @property
    def request_result(self):
        return self.itemid
    
    @request_result.setter
    def request_result(self, value):
        result = value.get('result', {})
        ids = result.get('itemids', [])
        if len(ids) >= 1:
            self.online_items['itemid'] = ids[0]

    @property
    def itemid(self):
        return self.online_items.get('itemid', None)

    @itemid.setter
    def itemid(self, value):
        raise core.ReadOnlyField('itemid is an readonly field')


    @property
    def delay(self):
        return self.online_items.get('delay', 30)

    @delay.setter
    def delay(self, value):
        self.online_items['delay'] = int(value)
        self.mergediff['delay'] = int(value)


    @property
    def interfaceid(self):
        return self.online_items.get('interfaceid', None)

    @interfaceid.setter
    def interfaceid(self, value):
        self.online_items['interfaceid'] = str(value)
        self.mergediff['interfaceid'] = str(value)
        

    @property
    def key(self):
        return self.online_items.get('key_', '')

    @key.setter
    def key(self, value):
        self.online_items['key_'] = str(value)
        self.mergediff['key_'] = str(value)
        

    @property
    def name(self):
        return self.online_items.get('name', '')

    @name.setter
    def name(self, value):
        self.online_items['name'] = str(value)
        self.mergediff['name'] = str(value)


    @property
    def type(self):
        return self.online_items.get('type', zbxitem.TYPE_ZABBIX_AGENT)

    @type.setter
    def type(self, value):
        self.online_items['type'] = int(value)
        self.mergediff['type'] = int(value)


    @property
    def value_type(self):
        return self.online_items.get('value_type', zbxitem.VAL_TYPE_NUMERIC_FLOAT)

    @value_type.setter
    def value_type(self, value):
        self.online_items['value_type'] = int(value)
        self.mergediff['value_type'] = int(value)


    @property
    def authtype(self):
        return self.online_items.get('authtype', zbxitem.AUTHTYPE_PASSWORD)

    @authtype.setter
    def authtype(self, value):
        self.online_items['authtype'] = int(value)
        self.mergediff['authtype'] = int(value)


    @property
    def data_type(self):
        return self.online_items.get('data_type', zbxitem.DATA_TYPE_DECIMAL)

    @data_type.setter
    def data_type(self, value):
        self.online_items['data_type'] = int(value)
        self.mergediff['data_type'] = int(value)


    @property
    def delay_flex(self):
        return self.online_items.get('delay_flex', '')

    @delay_flex.setter
    def delay_flex(self, value):
        self.online_items['delay_flex'] = str(value)
        self.mergediff['delay_flex'] = str(value)


    @property
    def delta(self):
        return self.online_items.get('delta', '')

    @delta.setter
    def delta(self, value):
        self.online_items['delta'] = str(value)
        self.mergediff['delta'] = str(value)


    @property
    def description(self):
        return self.online_items.get('description', '')

    @description.setter
    def description(self, value):
        self.online_items['description'] = str(value)
        self.mergediff['description'] = str(value)



    @property
    def error(self):
        return self.online_items.get('error', '')

    @itemid.setter
    def error(self, value):
        raise core.ReadOnlyField('error is an readonly field')


    @property
    def flags(self):
        return self.online_items.get('flags', zbxitem.FLAGS_PLAIN)

    @itemid.setter
    def flags(self, value):
        raise core.ReadOnlyField('flags is an readonly field')


    @property
    def formula(self):
        return self.online_items.get('formula', 1)

    @formula.setter
    def formula(self, value):
        self.online_items['formula'] = float(value)
        self.mergediff['formula'] = float(value)


    @property
    def history(self):
        return self.online_items.get('history', 90)

    @history.setter
    def history(self, value):
        self.online_items['history'] = int(value)
        self.mergediff['history'] = int(value)


    @property
    def inventory_link(self):
        return self.online_items.get('inventory_link', 0)

    @inventory_link.setter
    def inventory_link(self, value):
        self.online_items['inventory_link'] = int(value)
        self.mergediff['inventory_link'] = int(value)


    @property
    def ipmi_sensor(self):
        return self.online_items.get('ipmi_sensor', 0)

    @ipmi_sensor.setter
    def ipmi_sensor(self, value):
        self.online_items['ipmi_sensor'] = str(value)
        self.mergediff['ipmi_sensor'] = str(value)


    @property
    def lastclock(self):
        return self.online_items.get('lastclock', '')

    @lastclock.setter
    def lastclock(self, value):
        raise core.ReadOnlyField('lastclock is an readonly field')
        

    @property
    def lastns(self):
        return self.online_items.get('lastns', 0)

    @lastns.setter
    def lastns(self, value):
        raise core.ReadOnlyField('lastns is an readonly field')
        

    @property
    def lastvalue(self):
        return self.online_items.get('lastvalue', '')

    @lastvalue.setter
    def lastvalue(self, value):
        raise core.ReadOnlyField('lastvalue is an readonly field')
        

    @property
    def logtimefmt(self):
        return self.online_items.get('logtimefmt', '')

    @logtimefmt.setter
    def logtimefmt(self, value):
        self.online_items['logtimefmt'] = str(value)
        self.mergediff['logtimefmt'] = str(value)
        

    @property
    def mtime(self):
        return self.online_items.get('mtime', '')

    @mtime.setter
    def mtime(self, value):
        self.online_items['mtime'] = str(value)
        self.mergediff['mtime'] = str(value)
        

    @property
    def multiplier(self):
        return self.online_items.get('multiplier', '')

    @multiplier.setter
    def multiplier(self, value):
        self.online_items['multiplier'] = str(value)
        self.mergediff['multiplier'] = str(value)
        

    @property
    def params(self):
        return self.online_items.get('params', '')

    @params.setter
    def params(self, value):
        self.online_items['params'] = str(value)
        self.mergediff['params'] = str(value)
        

    @property
    def password(self):
        return self.online_items.get('password', '')

    @password.setter
    def password(self, value):
        self.online_items['password'] = str(value)
        self.mergediff['password'] = str(value)
        

    @property
    def port(self):
        return self.online_items.get('port', '')

    @port.setter
    def port(self, value):
        self.online_items['port'] = str(value)
        self.mergediff['port'] = str(value)
        

    @property
    def prevvalue(self):
        return self.online_items.get('prevvalue', '')

    @prevvalue.setter
    def prevvalue(self, value):
        raise core.ReadOnlyField('prevvalue is an readonly field')
        

    @property
    def privatekey(self):
        return self.online_items.get('privatekey', '')

    @privatekey.setter
    def privatekey(self, value):
        self.online_items['privatekey'] = str(value)
        self.mergediff['privatekey'] = str(value)
        

    @property
    def publickey(self):
        return self.online_items.get('publickey', '')

    @publickey.setter
    def publickey(self, value):
        self.online_items['publickey'] = str(value)
        self.mergediff['publickey'] = str(value)
        

    @property
    def snmp_community(self):
        return self.online_items.get('snmp_community', '')

    @snmp_community.setter
    def snmp_community(self, value):
        self.online_items['snmp_community'] = str(value)
        self.mergediff['snmp_community'] = str(value)
        

    @property
    def snmp_oid(self):
        return self.online_items.get('snmp_oid', '')

    @snmp_oid.setter
    def snmp_oid(self, value):
        self.online_items['snmp_oid'] = str(value)
        self.mergediff['snmp_oid'] = str(value)
        

    @property
    def snmpv3_authpassphrase(self):
        return self.online_items.get('snmpv3_authpassphrase', '')

    @snmpv3_authpassphrase.setter
    def snmpv3_authpassphrase(self, value):
        self.online_items['snmpv3_authpassphrase'] = str(value)
        self.mergediff['snmpv3_authpassphrase'] = str(value)
        

    @property
    def snmpv3_authprotocol(self):
        return self.online_items.get('snmpv3_authprotocol', zbxitem.SNMPV3_AUTHPROTOCOL_DES)

    @snmpv3_authprotocol.setter
    def snmpv3_authprotocol (self, value):
        self.online_items['snmpv3_authprotocol'] = item(value)
        self.mergediff['snmpv3_authprotocol'] = item(value)
        

    @property
    def snmpv3_contextname(self):
        return self.online_items.get('snmpv3_contextname', '')

    @snmpv3_contextname.setter
    def snmpv3_contextname (self, value):
        self.online_items['snmpv3_contextname'] = str(value)
        self.mergediff['snmpv3_contextname'] = str(value)
        

    @property
    def snmpv3_privpassphrase(self):
        return self.online_items.get('snmpv3_privpassphrase', '')

    @snmpv3_privpassphrase.setter
    def snmpv3_privpassphrase (self, value):
        self.online_items['snmpv3_privpassphrase'] = str(value)
        self.mergediff['snmpv3_privpassphrase'] = str(value)
        

    @property
    def snmpv3_privprotocol(self):
        return self.online_items.get('snmpv3_privprotocol', zbxitem.SNMPV3_PRIVROTOCOL_DES)

    @snmpv3_privprotocol.setter
    def snmpv3_privprotocol (self, value):
        self.online_items['snmpv3_privprotocol'] = item(value)
        self.mergediff['snmpv3_privprotocol'] = item(value)
        

    @property
    def snmpv3_securitylevel(self):
        return self.online_items.get('snmpv3_securitylevel', zbxitem.SNMPV3_SECURITYLEVEL_NOAUTHNOPRIV)

    @snmpv3_securitylevel.setter
    def snmpv3_securitylevel (self, value):
        self.online_items['snmpv3_securitylevel'] = item(value)
        self.mergediff['snmpv3_securitylevel'] = item(value)
        

    @property
    def snmpv3_securityname(self):
        return self.online_items.get('snmpv3_securityname', '')

    @snmpv3_securityname.setter
    def snmpv3_securityname (self, value):
        self.online_items['snmpv3_securityname'] = str(value)
        self.mergediff['snmpv3_securityname'] = str(value)
        

    @property
    def state(self):
        return self.online_items.get('state', zbxitem.STATE_NORMAL)

    @state.setter
    def state (self, value):
        self.online_items['state'] = str(value)
        self.mergediff['state'] = str(value)
        

    @property
    def status(self):
        return self.online_items.get('status', zbxitem.STATUS_ENABLED)

    @status.setter
    def status (self, value):
        self.online_items['status'] = str(value)
        self.mergediff['status'] = str(value)
        
    @property
    def templateid(self):
        return self.online_items.get('templateid', '')

    @templateid.setter
    def templateid(self, value):
        raise core.ReadOnlyField('templateid is an readonly field')
        
        
    @property
    def trapper_hosts(self):
        return self.online_items.get('trapper_hosts', '')

    @trapper_hosts.setter
    def trapper_hosts(self, value):
        self.online_items['trapper_hosts'] = str(value)
        self.mergediff['trapper_hosts'] = str(value)
        

    @property
    def trends(self):
        return self.online_items.get('trends', 365)

    @trends.setter
    def trends(self, value):
        self.online_items['trends'] = int(value)
        self.mergediff['trends'] = int(value)
        

    @property
    def units(self):
        return self.online_items.get('units', '')

    @units.setter
    def units(self, value):
        self.online_items['units'] = str(value)
        self.mergediff['units'] = str(value)
        

    @property
    def username(self):
        return self.online_items.get('username', '')

    @username.setter
    def username(self, value):
        self.online_items['username'] = str(value)
        self.mergediff['username'] = str(value)
        

    @property
    def valuemapid(self):
        return self.online_items.get('valuemapid', '')

    @valuemapid.setter
    def valuemapid(self, value):
        self.online_items['valuemapid'] = str(value)
        self.mergediff['valuemapid'] = str(value)
        


    def add_host(self, host):
        self.host = host

    def add_application(self, application):
        self.applications[application.name] = application




    def get(self, param_type=None):
        
        if not param_type:
            if self.id:
                param_type = 'update'
            else:
                param_type = 'create'
        
        if param_type == 'create':
            if self.id:
                return [False, {}]
            retval = dict(self.online_items)
        
        if param_type == 'update':
            if not self.id:
                return [False, {}]
            retval = dict(self.mergediff)
            retval['itemid'] = self.id

        if param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()

        if param_type in ['create', 'update']:
            retval['hostid'] = self.host.id
            retval['applications'] = [self.applications[applicationname].id for applicationname in self.applications]
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'itemid':
                        continue
                    else:
                        del retval[param]

        return [self.apicommands[param_type], retval]
