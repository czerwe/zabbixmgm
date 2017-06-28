import core
import re

class zbxinterface(core.zbx):

    TYPE_AGENT = 1
    TYPE_SNMP = 2
    TYPE_IPMI = 3
    TYPE_JMX = 4

    BULK_OFF = 0
    BULK_ON = 1

    def __init__(self, api, interfacemask=None):
        super(zbxinterface, self).__init__(api)
        self.difffields = ['interfaceid', 'useip', 'ip', 'dns', 'port', 'bulk', 'type']

        self.readonlyfields = ['interfaceid']
        self.online_items = dict()
        
        if interfacemask:
            self.merge(interfacemask)


        self.main = 'no'
        self.host = '127.0.0.1'
        self.port = '10050'
        self.type = zbxinterface.TYPE_AGENT
        self.main = 0




    @property
    def id(self):
        return self.interfaceid


    @property
    def interfaceid(self):
        return self.online_items.get('interfaceid', None) 

    @interfaceid.setter
    def interfaceid(self, value):
        raise core.ReadOnlyField('snmp_errors_from is an readonly field')


    @property
    def host(self):
        # print(self.online_items)
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
            self.online_items['useip'] = 1
            self.online_items['dns'] = ''
            self.online_items['ip'] = value
        else:
            self.online_items['useip'] = 0
            self.online_items['dns'] = value
            self.online_items['ip'] = ''
        

    @property
    def main(self):
        return self.online_items.get('main', 0) 


    @main.setter
    def main(self, value):
        if value in [1, True, 'yes']:
            self.online_items['main'] = 1
        elif value in [0, False, 'no']:
            self.online_items['main'] = 0
        else:
            raise core.InvalidFieldValue(message='{0} not supported to set the main value'.format(value), status=2)
            

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
        try:
            int(value)
        except:
            raise core.InvalidFieldValue(message='{0} is not a supported interface type'.format(value), status=2)
        else:
            if int(value) in [zbxinterface.TYPE_AGENT, zbxinterface.TYPE_SNMP, zbxinterface.TYPE_IPMI, zbxinterface.TYPE_JMX]:
                self.online_items['type'] = int(value)
            else:
                raise core.InvalidFieldValue(message='{0} is not a supported interface type'.format(value), status=2)

    @property
    def bulk(self):
        return self.online_items.get('bulk', zbxinterface.TYPE_AGENT) 


    @bulk.setter
    def bulk(self, value):
        if value in [zbxinterface.BULK_ON, zbxinterface.BULK_OFF]:
            self.online_items['bulk'] = value
        else:
            raise core.InvalidFieldValue(message='{0} is not a supported interface type'.format(value), status=2)


    def get(self, param_type='create'):
        if param_type == 'create':
            retval = dict(self.online_items)
        
        if param_type == 'update':
            if not self.interfaceid:
                return False

            retval = dict(self.mergediff)

        if param_type == 'delete':
            if self.interfaceid:
                retval = [self.interfaceid]
            else:
                retval = list()

        if param_type in ['create', 'update']:
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'interfaceid':
                        continue
                    else:
                        del retval[param]

        return retval

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
            
