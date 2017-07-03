import core
import host

from pprint import pprint

class zbxapplication(core.zbx):

    FLAGS_PLAIN = 0
    FLAGS_DISCOVERED = 1

    def __init__(self, api, **kwargs):
        super(zbxapplication, self).__init__(api)
        self.host = None



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
        return None

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
        if type(hostinstance) == host.zbxhost:
            self.host = hostinstance
            self.hostid = hostinstance.id
        else:
            raise core.WrongType("expect zabbixmgm.zbxhost as argument not {0}".format(type(hostinstance)))


    def get(self, param_type=None):

        if not param_type:
            if self.id:
                param_type = 'update'
            else:
                param_type = 'create'

        if param_type in ['create', 'update']:
            retval = dict(self.online_items)

            if param_type == 'create':
                if self.id:
                    return [False, {}]
            
            if param_type == 'update':
                if not self.id:
                    raise core.MissingField('id field is missing', '4')
                            
                retval['applicationid'] = self.id

            if self.host and self.host.id:
                retval['hostid'] = self.host.id

            for reqfield in self.required_fields:
                if not reqfield in retval:
                    raise core.MissingField('{0} is missing'.format(reqfield), '3')
            
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'applicationid':
                        continue
                    else:
                        del retval[param]

            # retval2 = self.get_attrs(withreadonly=True, verify=True)
            print '\n{0} ----------------'.format(param_type)
            pprint(retval)
            pprint(self.get_attrs(withreadonly=True, verify=False))
            print '----------------\n'



        elif param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()



        return [self.apicommands[param_type], retval]