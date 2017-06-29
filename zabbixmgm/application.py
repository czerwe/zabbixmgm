import core

from pprint import pprint

class zbxapplication(core.zbx):

    FLAGS_PLAIN = 0
    FLAGS_DISCOVERED = 1

    def __init__(self, api, name, applicationmask=None):
        super(zbxapplication, self).__init__(api)
        self.name = name
        self.host = None

        self.difffields = [
                            'applicationid',
                            'hostid',
                            'flags',
                            'name',
                            'templateids'
                        ]

        self.readonlyfields = [
                            'applicationid',
                            'flags',
                            'templateids'
                        ]

        self.apicommands = {
            "get": "application.get",
            "create": "application.create",
            "update": "application.update",
            "delete": "application.delete",
        }

        if applicationmask:
            self.merge(applicationmask)


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
        raise core.ReadOnlyField('applicationid is an readonly field')


    @property
    def hostid(self):
        return self.online_items.get('hostid', None)

    @hostid.setter
    def hostid(self, value):
        raise core.ReadOnlyField('hostid is an readonly field')


    @property
    def name(self):
        return self.online_items.get('name', None)

    @name.setter
    def name(self, value):
        self.online_items['name'] = str(value)
        self.mergediff['name'] = str(value)


    @property
    def flags(self):
        return self.online_items.get('flags', zbxapplication.FLAGS_PLAIN)

    @flags.setter
    def flags(self, value):
        raise core.ReadOnlyField('flags is an readonly field')


    @property
    def templateids(self):
        return self.online_items.get('templateids', list())

    @templateids.setter
    def templateids(self, value):
        raise core.ReadOnlyField('templateids is an readonly field')



    def add_host(self, host):
        self.host = host


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
            retval['applicationid'] = self.id

        if param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()

        if param_type in ['create', 'update']:
            retval['hostid'] = self.host.id
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'applicationid':
                        continue
                    else:
                        del retval[param]

        return [self.apicommands[param_type], retval]
