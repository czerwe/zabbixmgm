import core
# import item
import host

from pprint import pprint

class zbxtemplate(host.zbxhost):

    def __init__(self, api, name, templatemask=None):
        super(zbxtemplate, self).__init__(api, name)
        self.name = name

        self.difffields[self.difffields.index('hostid')] = 'templateid'
        self.readonlyfields[self.readonlyfields.index('hostid')] = 'templateid'

        self.apicommands = {
            "get": "template.get",
            "create": "template.create",
            "update": "template.update",
            "delete": "template.delete",
        }

        if templatemask:
            self.merge(templatemask)


    @property
    def id(self):
        return self.templateid

    @property
    def hostid(self):
        return self.templateid

    @property
    def request_result(self):
        return self.groupid
    
    @request_result.setter
    def request_result(self, value):
        result = value.get('result', {})
        ids = result.get('templateids', [])
        if len(ids) >= 1:
            self.online_items['templateid'] = ids[0]

    @property
    def templateid(self):
        return self.online_items.get('templateid', None)

    @templateid.setter
    def templateid(self):
        raise core.ReadOnlyField('templateid is an readonly field')


    def get(self, param_type=None):
        retval = dict()
        if not param_type:
            if self.id:
                param_type = 'update'
            else:
                param_type = 'create'


        if param_type == 'create':
            if self.id:
                return [False, retval]
            # pprint(self.templates['Template OS Linux'].get())
            # pprint(self.templates['Template OS Linux'].online_items)
            retval = dict(self.online_items)
            retval['groups'] = [{"groupid": self.groups[groupname].id} for groupname in self.groups]
            retval['templates'] = [{"templateid": self.templates[templatename].id} for templatename in self.templates]
            
        if param_type == 'update':
            if not self.id:
                return [False, retval]
            retval = dict(self.mergediff)
            retval['templateid'] = self.id
            retval['groups'] = [{"groupid": self.groups[groupname].id} for groupname in self.groups]
            retval['templates'] = [{"templateid": self.templates[templatename].id} for templatename in self.templates]
            

        if param_type in ['create', 'update']:
            for param in retval.keys():
                if param in self.readonlyfields:
                    if param_type == 'update' and param == 'templateid':
                        continue
                    else:
                        del retval[param]
        elif param_type == 'delete':
            if self.id:
                retval = [self.id]
            else:
                retval = list()

        return [self.apicommands[param_type], retval]