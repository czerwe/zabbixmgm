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





