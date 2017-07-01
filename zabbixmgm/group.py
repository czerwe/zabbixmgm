import core
from pprint import pprint

class zbxgroup(core.zbx):

    FLAGS_PLAIN = 0
    FLAGS_DISCOVERED = 1

    INTERNAL_NOT_NORMAL = 0
    INTERNAL_INTERNAL = 1

    def __init__(self, api, groupmask=None, **kwargs):
        super(zbxgroup, self).__init__(api)

        self.difffields = [
                            'groupid',
                            'name',
                            'flags',
                            'internal'
                        ]

        self.readonlyfields = ['groupid', 'flags', 'internal']

        self.apicommands = {
            'get': 'hostgroup.get',
            'create': 'hostgroup.create',
            'update': 'hostgroup.update',
            'delete': 'hostgroup.delete',
        }

        if groupmask:
            self.merge(groupmask)

        for att in kwargs.keys():
            if att in self.difffields:
                setattr(self, att, kwargs[att])
            else:
                raise core.WrongType('{0} is not a valid argument'.format(att), 5)



    @property
    def id(self):
        return self.groupid
    
    @property
    def request_result(self):
        return self.groupid
    
    @request_result.setter
    def request_result(self, value):
        result = value.get('result', {})
        ids = result.get('groupids', [])
        if len(ids) >= 1:
            self.online_items['groupid'] = ids[0]


    @property
    def groupid(self):
        return self.online_items.get('groupid', None)
    
    @groupid.setter
    def groupid(self, value):
        raise core.ReadOnlyField('groupid is an readonly field')


    @property
    def name(self):
        return self.online_items.get('name', '')
    
    @name.setter
    def name(self, value):
        self.online_items['name'] = str(value)
        self.mergediff['name'] = str(value)
        

    @property
    def flags(self):
        return self.online_items.get('flags', zbxgroup.FLAGS_PLAIN)
    
    @flags.setter
    def flags(self, value):
        raise core.ReadOnlyField('flags is an readonly field')


    @property
    def internal(self):
        return self.online_items.get('internal', zbxgroup.INTERNAL_NOT_NORMAL)
    
    @internal.setter
    def internal(self, value):
        raise core.ReadOnlyField('internal is an readonly field')


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
            retval['groupid'] = self.id

        if param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()

        if param_type in ['create', 'update']:
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'groupid':
                        continue
                    else:
                        del retval[param]

        return [self.apicommands[param_type], retval]
