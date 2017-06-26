import core

class zbxinterface(core.zbx):

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

