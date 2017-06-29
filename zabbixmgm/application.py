import core

class zbxapplication(core.zbx):

    def __init__(self, api, applicationname, hostid):
        super(zbxapplication, self).__init__(api)
        self.objectname = applicationname
        self.objecthost = hostid
        self.update()


    def get_applications(self, hostid=None, name=None):

        if (hostid and name) or (not hostid and not name):
            #TODO exception
            return False

        else:
            parameters = {'output': 'extend'}
            if hostid:
                parameters['hostids'] = hostid
            else:
                parameters['names'] = name

            query_result = self.api.do_request('application.get', parameters)

        if len(query_result['result']) == 1:
            self.online_items = query_result['result'][0]
        elif len(query_result['result']) > 1:
            self.online_items = query_result['result']
        else:
            self.online_items=()

        return self.online_items


    def update(self):
        self.get_applications(hostid=self.objecthost)

        if type(self.online_items) == dict():
            if not self.online_items['name'] == self.objectname:
                self.online_items == dict()

    def get_id(self):
        return self.get_objectid('applicationid')


    def create(self):
        params = {'name': self.objectname, 'hostid': self.objecthost}
        self.create_object('application.create', params)
        self.update()
        return self.get_id()


    def delete(self):
        self.delete_object('application.delete', [self.get_id()])


