import core

class zbxgroup(core.zbx):

    def __init__(self, api, groupname):
        super(zbxgroup, self).__init__(api)
        self.objectname = groupname
        self.update()
        self.create()

    def update(self):
        self.get_query('hostgroup.get', filter={'name': self.objectname})


    def get_id(self):
        return self.get_objectid('groupid')

    def get_name(self):
        return self.objectname


    def create(self):
        done = self.create_object('hostgroup.create', {"name": self.objectname})
        if done:
            self.update()
        return self.get_id()


    def delete(self):
        self.delete_object('hostgroup.delete', [self.get_id()])
        self.update()

