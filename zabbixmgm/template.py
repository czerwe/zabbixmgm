import core
import item

class zbxtemplate(core.zbx):

    def __init__(self, api, templatename):
        super(zbxtemplate, self).__init__(api)
        self.objectname = templatename
        self.update()
        self.items = dict()
        self.applications = dict()

    def update(self):
        self.get_query('template.get', filter={'host': self.objectname})


    def get_name(self):
        return self.objectname

    def get_id(self):
        return self.get_objectid('templateid')


    def create(self, groups=list(), hosts=list()):
        params = {
                    'host': self.objectname, 
                    'groups': dict(("groupid", groupid) for groupid in groups), 
                    'hosts': dict(("hostid", hostid) for hostid in hosts)
                }
        self.create_object('template.create', params)
        
        for application in self.applications.keys():
            self.applications[application].create()

        for item in self.items.keys():
            self.items[item].create()


        self.update()
        return self.get_id()


    def delete(self):
        for item in self.items.keys():
            self.items[item].delete()

        for application in self.applications.keys():
            self.applications[application].delete()

        self.delete_object('template.delete', [self.get_id()])


    def create_application(self, applicationname, groups):
        self.create(groups)
        if not applicationname in self.applications:
            self.applications[applicationname] = core.zbxapplication(self.api, applicationname=applicationname, hostid=self.get_id())
        
        return self.applications[applicationname]


    def create_item(self, itemname, applicationname):
        self.create()
        if not itemname in self.items:
            self.items[itemname] = item.zbxitem(self.api, itemname=itemname, hostid=self.get_id())
        
        if applicationname in self.applications:
            self.items[itemname].set_params('applications', [self.applications[applicationname].get_id()])
        else:
            #TODO
            # error
            print 'does nto exist'

        return self.items[itemname]
