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

    def __init__(self, api, itemname, hostid):
        super(zbxitem, self).__init__(api)

        self.objectname = itemname
        self.objecthost = hostid
        self.update()
        


    def set_default_params(self):
        self.online_items = dict()

        self.online_items['name'] = self.objectname
        self.online_items['type'] = zbxitem.TYPE_ZABBIX_AGENT
        self.online_items['value_type'] = zbxitem.VAL_TYPE_NUMERIC_FLOAT
        self.online_items['delay'] = 30
        self.online_items['hostid'] = self.objecthost


    def get_items(self, hostid=None, name=None):

        parameters = {'output': 'extend'}
        
        if hostid:
            parameters['hostids'] = hostid
        
        if name:
            parameters['search'] ={'name': name}

        query_result = self.api.do_request('item.get', parameters)

        if len(query_result['result']) == 1:
            self.online = True
            self.online_items = query_result['result'][0]
        else:
            self.set_default_params()
            self.online = False
        
        return self.online_items


    def update(self):
        self.get_items(hostid=self.objecthost, name=self.objectname)


    def get_id(self):
        return self.get_objectid('itemid')


    def create(self):
        if not self.online:
            self.create_object('item.create', param=self.online_items, online_indicator=self.online)
            self.update()
        return self.get_id()

    def set_params(self, key, value):
        self.online_items[key] = value


    def delete(self):
        if self.online:

            self.delete_object('item.delete', [self.get_id()])

