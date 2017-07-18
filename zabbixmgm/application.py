import core
import host
import host
import logging
from pprint import pprint

class zbxapplication(core.zbx):

    FLAGS_PLAIN = 0
    FLAGS_DISCOVERED = 1

    def __init__(self, api, **kwargs):
        super(zbxapplication, self).__init__(api)
        self.host = None

        self.logger = logging.getLogger(__name__)
        self.difffields = ['applicationid',
                           'hostid',
                           'flags',
                           'name',
                           'templateids']

        self.readonlyfields = ['applicationid', 'flags', 'templateids']
        self.required_fields = ['hostid', 'name']

        self.apicommands = {
            'get': 'application.get',
            'create': 'application.create',
            'update': 'application.update',
            'delete': 'application.delete',
        }

        for att in kwargs.keys():
            if att in self.difffields + ['mask']:
                setattr(self, att, kwargs[att])
            else:
                raise core.WrongType('{0} is not a valid argument'.format(att), 5)



    @property
    def id(self):
        return self.applicationid

    @property
    def request_result(self):
        return self.applicationid
    
    @request_result.setter
    def request_result(self, value):
        result = value.get('result', {})
        ids = result.get('applicationids', [])
        if len(ids) >= 1:
            self.online_items['applicationid'] = ids[0]

    @property
    def applicationid(self):
        return self.online_items.get('applicationid', None)

    @applicationid.setter
    def applicationid(self, value):
        self.online_items['applicationid'] = int(value)
        # raise core.ReadOnlyField('applicationid is an readonly field')


    @property
    def hostid(self):
        if self.host:
            return self.host.id
        else:
            return self.online_items.get('hostid', None)
            
    @hostid.setter
    def hostid(self, value):
        self.online_items['hostid'] = str(value)
        # raise core.ReadOnlyField('hostid is an readonly field')


    @property
    def name(self):
        return self.online_items.get('name', None)

    @name.setter
    def name(self, value):
        self.online_items['name'] = str(value)


    @property
    def flags(self):
        return self.online_items.get('flags', zbxapplication.FLAGS_PLAIN)

    @flags.setter
    def flags(self, value):
        self.online_items['flags'] = int(value)
        # raise core.ReadOnlyField('flags is an readonly field')


    @property
    def templateids(self):
        return self.online_items.get('templateids', list())

    @templateids.setter
    def templateids(self, value):
        self.online_items['templateids'] = value
        # raise core.ReadOnlyField('templateids is an readonly field')
        
    @property
    def mask(self):
        return self.get_attrs(withreadonly=True, verify=False)

    @mask.setter
    def mask(self, value):
        self.merge(value)


    def merge(self, dictionary):
        left, right, total = self.diff(dictionary)
        self.mergediff = right
        for key in right.keys():
            setattr(self, key, right[key])
            # self.online_items[key] = right[key]


    def add_host(self, hostinstance):
        if type(hostinstance) == host.zbxhost or type(hostinstance) == host.zbxtemplate :
            self.host = hostinstance
            self.hostid = hostinstance.id
        else:
            raise core.WrongType("expect zabbixmgm.zbxhost as argument not {0}".format(type(hostinstance)))


    def get_update_modifier(self, value):
        if self.applicationid:
            value['applicationid'] = self.applicationid
        return value

    def get_create_modifier(self, value):
        return value

