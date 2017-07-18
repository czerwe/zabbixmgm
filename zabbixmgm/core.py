from pprint import pprint
import logging


class ReadOnlyField(Exception):
    def __init__(self, message, status=0):
        super(ReadOnlyField, self).__init__(message, status)


class InvalidFieldValue(Exception):
    def __init__(self, message, status=0):
        super(InvalidFieldValue, self).__init__(message, status)

class MissingField(Exception):
    def __init__(self, message, status=0):
        super(MissingField, self).__init__(message, status)


class WrongType(Exception):
    def __init__(self, message, status=0):
        super(WrongType, self).__init__(message, status)


class zbx(object):

    inventory = dict()

    def __init__(self, api):
        self.logger = logging.getLogger(__name__)
        self.api = api
        self.objectname = None
        self.online_items = dict()
        self.difffields = list()
        self.mergediff = dict()
        self.readonlyfields = list()
        self.required_fields = list()

    @property
    def mask(self):
        self.logger.debug('mask.get called')
        return self.get_attrs(withreadonly=True, verify=False)

    @mask.setter
    def mask(self, value):
        for passed_key in value.keys():
            self.logger.debug('mask.set contains {0} with value {1}({2})'.format(passed_key, value[passed_key], type(value[passed_key])))
            setattr(self, passed_key, value[passed_key])


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
        self.logger.error('DEPRICATED diff called')
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
        self.logger.error('DEPRICATED merge called')
        left, right, total = self.diff(dictionary)
        self.mergediff = right
        for key in right.keys():
            # setattr(self, key, right[key])
            self.online_items[key] = right[key]


    def get_update_modifier(self, value):
        self.logger.debug('empty update modifier called')
        return value

    def get_create_modifier(self, value):
        self.logger.debug('empty create modifier called')
        return value



    def get_attrs(self, withreadonly=False, verify=False):
        self.logger.debug('get_attrs called  withreadonly={0} verify={1}'.format(withreadonly, verify))
        all_attrs = dict((attr, getattr(self, attr)) 
                        for attr in self.difffields  
                        if not getattr(self, attr) == None)

        if not withreadonly:
            for key in all_attrs.keys():
                if key in self.readonlyfields:
                    self.logger.debug('Readonlyfield {0} removed, value was {1}'.format(key, all_attrs[key]))
                    del all_attrs[key]

        if verify:
            for key in self.required_fields:
                if not key in all_attrs.keys():
                    self.logger.critical('Missing attribute named {0}'.format(key))
                    raise MissingField('missing field {0}'.format(key), 5)
              
        return all_attrs


    def get(self, param_type=None):

        if not param_type:
            self.logger.debug('Did not recieved query type, evaluating')
            if self.id:
                param_type = 'update'
            else:
                param_type = 'create'
        
        self.logger.info('Generating query dict for {0}'.format(param_type))

        if param_type == 'create':
            if self.id:
                self.logger.error('{0} not possible, existing id'.format(param_type))
                return [None, {}]
            retval = self.get_create_modifier(self.get_attrs(withreadonly=False, verify=True))

        if param_type == 'update':
            if not self.id:
                self.logger.error('{0} not possible, missing id'.format(param_type))
                return [None, {}]
            retval = self.get_update_modifier(self.get_attrs(withreadonly=False, verify=True))

        if param_type == 'delete':
            if self.id:
                self.logger.info('{0} possible existing id'.format(param_type))
                retval = [self.id]
            else:
                self.logger.error('{0} not possible, missing id'.format(param_type))
                retval = list()



        return [self.apicommands[param_type], retval]