from pprint import pprint


class ReadOnlyField(Exception):
    def __init__(self, message, status=0):
        super(ReadOnlyField, self).__init__(message, status)


class InvalidFieldValue(Exception):
    def __init__(self, message, status=0):
        super(InvalidFieldValue, self).__init__(message, status)



class zbx(object):

    inventory = dict()

    def __init__(self, api):
        self.api = api
        self.objectname = None
        self.online_items = dict()
        self.difffields = list()
        self.mergediff = dict()
        self.readonlyfields = list()

    def get_objectid(self, idstring):

        if type(self.online_items) == dict and idstring in self.online_items.keys():
            return self.online_items[idstring]
        else:
            return 0


    def create_object(self, queryfunction, param={}, online_indicator=None):
        if online_indicator == None:
            online_indicator = len(self.online_items) > 0

        if not online_indicator:
            result = self.api.do_request(queryfunction, param)
            return True

        return False


    def delete_object(self, queryfunction, params):
        if len(self.online_items) > 0:
            result = self.api.do_request(queryfunction, params)

            print('----------------\n{0}: {1}\n\t{2}\n----------------'.format(queryfunction, filter, result))
            return result['result']

        return {}

    def get_query(self, queryfunction, filter=None):

        if not filter:
            query_result = self.api.do_request(queryfunction, {})
        else:
            query_result = self.api.do_request(queryfunction, {
                              'filter': filter,
                              'output': 'extend'
                          })

        print('----------------\n{0}: {1}\n\t{2}\n----------------'.format(queryfunction, filter, query_result))

        if len(query_result['result']) == 1:
            self.online_items = query_result['result'][0]
        elif len(query_result['result']) > 1:
            self.online_items = query_result['result']
        else:
            self.online_items=()

        return self.online_items


    def diff(self, iface):
        """
        Searches differences between the current zbxdata and an passed zbxdata.
        It resturns three dictionaries. Fist dictionary is the current original values
        The sedond dictironary is the passed values and the third contains only values that 
        are only exist in either of the two dictionarys.
        
        :param iface: genertated interface dictionary
        :type iface: dict
        
        :return: list of three dictionaries
        :rtype: list
        """
        diff_full = dict()
        diff_left = dict()
        diff_right = dict()
        
        for indexname in self.difffields:
            left = self.online_items.get(indexname, None)
            right = iface.get(indexname, None)
            if not left == right:
                if left:
                    diff_left[indexname] = self.online_items.get(indexname, '')
                    if not right:
                        diff_full[indexname] = self.online_items.get(indexname, '')

                if right:
                    diff_right[indexname] = iface.get(indexname, '')
                    if not left:
                        diff_full[indexname] = iface.get(indexname, '')

        return [diff_left, diff_right, diff_full]



    def merge(self, dictionary):
        left, right, total = self.diff(dictionary)
        self.mergediff = right
        for key in right.keys():
            self.online_items[key] = right[key]

    def get(self):
        return self.online_items




    # def get_hosts(self, filter=None):
    #     if not filter:
    #         host = zapi.do_request('host.get', {})
    #     else:
    #         host = zapi.do_request('host.get', {
    #                           'selectGroups': "extend",
    #                           'selectParentTemplates': ["name"],
    #                           'filter': filter,
    #                           'output': 'extend'
    #                       })
    #     return host['result']


    # def get_interfaces(self, hostid=None):
    #     if not filter:
    #         return dict()
    #     else:
    #         interfaces = zapi.do_request('hostinterface.get', {
    #                           'hostids': hostid,
    #                           'output': 'extend'
    #                       })

    #     return interfaces['result']


class zbxapplication(zbx):

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


