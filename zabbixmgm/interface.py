import core
import re



class InvalidFieldValue(Exception):
    def __init__(self, message, status=0):
        super(InvalidFieldValue, self).__init__(message, status)


class zbxinterface(core.zbx):

    TYPE_AGENT = 1
    TYPE_SNMP = 2
    TYPE_IPMI = 3
    TYPE_JMX = 4

    BULK_OFF = 0
    BULK_ON = 1

    def __init__(self, api):
        super(zbxinterface, self).__init__(api)
        self.online_items = dict()

        self.main = 'no'
        self.host = '127.0.0.1'
        self.port = '10050'


        self.set_default_params()


    def set_default_params(self):
        self.add_param('type', zbxinterface.TYPE_AGENT)
        self.add_param('main', 0)
        self.add_param('host', '127.0.0.1')
        self.add_param('port', '10050')


    # def write(self):
    #     inerfaceid = self.online_items.get('interfaceid', False)
    #     if not inerfaceid:
    #         function = 'hostinterface.create'
    #     else:
    #         function = 'hostinterface.update'
        
    #     if self.get_interface().get('hostid', False):
    #         result = self.api.do_request(function, self.get_interface())

    #         if result['result'].get('interfaceids', None):
    #             self.add_param('interfacid', result['result']['interfaceids'])
            


    def get_name(self):
        return self.objectname

    @property
    def host(self):
        print(self.online_items)
        if len(self.online_items['ip']) > 0:
            return self.online_items['ip']

        if len(self.online_items['dns']) > 0:
            return self.online_items['dns']

        return str()

    
    @host.setter
    def host(self, value):
        ipre = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        hostregex = re.compile(ipre)

        if hostregex.match(value):
            self.add_param('useip', 1)
            self.add_param('ip', value)
            self.add_param('dns', '')
            self.online_items['ip'] = value
        else:
            self.add_param('useip', 0)
            self.add_param('dns', value)
            self.add_param('ip', '')
            self.online_items['dns'] = value
        




    @property
    def main(self):
        return self.online_items.get('main', 0) 

    @main.setter
    def main(self, value):
        if value in [1, True, 'yes']:
            self.online_items['main'] = 1
        else:
            self.online_items['main'] = 0



    @property
    def port(self):
        return self.online_items.get('port', '10050') 

    @port.setter
    def port(self, value):
        self.online_items['port'] = str(value) 


    @property
    def type(self):
        return self.online_items.get('type', zbxinterface.TYPE_AGENT) 

    @type.setter
    def type(self, value):
        if value in [zbxinterface.TYPE_AGENT, zbxinterface.TYPE_SNMP, zbxinterface.TYPE_IPMI, zbxinterface.TYPE_JMX]:
            self.online_items['type'] = value
        else:
            raise InvalidFieldValue(message='{0} is not a supported interface type'.format(value), status=2)

    @property
    def bulk(self):
        return self.online_items.get('bulk', zbxinterface.TYPE_AGENT) 

    @bulk.setter
    def bulk(self, value):
        if value in [zbxinterface.BULK_ON, zbxinterface.BULK_OFF]:
            self.online_items['bulk'] = value
        else:
            raise InvalidFieldValue(message='{0} is not a supported interface type'.format(value), status=2)








    # def add_param(self, key, value):
    #     if key == 'host':
    #         self.host = value
    #     else:
    #         self.online_items[key] = value

    # def get_param(self, key):
    #     if key == 'host':
    #         return self.host
    #     else:
    #         return self.online_items.get(key, '')

    # def set_main(self):
    #     self.add_param('main', 1)

    def get_interface(self):
        return self.online_items

