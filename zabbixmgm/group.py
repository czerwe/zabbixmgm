import core

class zbxgroup(core.zbx):

    FLAGS_PLAIN = 0
    FLAGS_DISCOVERED = 1

    INTERNAL_NOT_NORMAL = 0
    INTERNAL_INTERNAL = 1

    def __init__(self, api, name):
        super(zbxgroup, self).__init__(api)
        self.name = name

        self.difffields = [
                            'groupid',
                            'name',
                            'flags',
                            'internal'
                        ]

        apicommands = {
            "get": "hostgroup.get",
            "create": "hostgroup.create",
            "update": "hostgroup.update",
        }


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



    def get(self):
        return self.online_items



    # def update(self):
    #     self.get_query('hostgroup.get', filter={'name': self.objectname})


    # def get_id(self):
    #     return self.get_objectid('groupid')

    # def get_name(self):
    #     return self.objectname


    # def create(self):
    #     done = self.create_object('hostgroup.create', {"name": self.objectname})
    #     if done:
    #         self.update()
    #     return self.get_id()


    # def delete(self):
    #     self.delete_object('hostgroup.delete', [self.get_id()])
    #     self.update()

