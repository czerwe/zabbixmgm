import logging

from pprint import pprint

logger = logging.getLogger(__name__)

def query_group_by_name(api, name):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name]
        }
    }
    
    result = api.do_request('hostgroup.get', params)['result']
    logger.debug('query_group_by_name querys for group {0} with {1} results'.format(name, len(result)))
    if len(result) >= 1:
        return result[0]
    else:
        return {}


def query_host_by_name(api, name):
    params = {
        'output': 'extend',
        'selectGroups': ["name"],
        'selectInterfaces': ["interfaceid"],
        'selectParentTemplates': ["name"],
        'filter': {
            'name': [name]
        }
    }
    
    result = api.do_request('host.get', params)['result']
    logger.debug('query_host_by_name querys for host {0} with {1} results'.format(name, len(result)))
    if len(result) >= 1:
        return result[0]
    else:
        return {}

def query_template_by_name(api, name):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name]
        }
    }
    result = api.do_request('template.get', params)['result']
    logger.debug('query_template_by_name querys for template {0} with {1} results'.format(name, len(result)))
    if len(result) >= 1:
        return result[0]
    else:
        return {}

def query_application_by_name(api, name):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name]
        }
    }
    
    result = api.do_request('application.get', params)['result']
    logger.debug('query_application_by_name querys for application {0} with {1} results'.format(name, len(result)))
    if len(result) >= 1:
        return result[0]
    else:
        return {}



def query_interfaces_by_host(api, host):
    params = {
        'output': 'extend',
        'hostids': host,
    }

    result = api.do_request('hostinterface.get', params)['result']
    logger.debug('query_interfaces_by_host querys for interfaces {0} with {1} results'.format(name, len(result)))
    if len(result) >= 1:
        return result
    else:
        return {}


def query_interfaces_by_id(api, interfaceid):
    params = {
        'output': 'extend',
        'interfaceids': interfaceid,
    }

    result = api.do_request('hostinterface.get', params)['result']
    logger.debug('query_interfaces_by_id querys for interface {0} with {1} results'.format(interfaceid, len(result)))
    if len(result) >= 1:
        return result[0]
    else:
        return {}




def query_item_by_name_and_host(api, name, host):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name],
            'hostid': host
            
        },
    }
    result = api.do_request('item.get', params)['result']
    logger.debug('query_item_by_name_and_host querys for item {0} and host {2} with {1} results'.format(name, len(result), host))
    if len(result) >= 1:
        return result[0]
    else:
        return {}



def query_items_from_hostid(api, host):
    params = {
        'output': 'extend',
        'hostids': [host]
        # 'filter': {
        # },
    }

    # pprint(params)

    result = api.do_request('item.get', params)['result']
    logger.debug('query_items_from_hostid querys for items from host {0} with {1} results'.format(host, len(result)))
    if len(result) >= 1:
        return result
    else:
        return {}

def query_num_of_interface_types(api, host, itype):
    params = {
        'output': 'extend',
        'hostids': [host],
        'filter': {
            'type': itype,
        },
    }

    logger.debug('query_num_of_interface_types querys for interfaces from host {0} of type {2} with {1} results'.format(host, len(result), itype))
    result = api.do_request('hostinterface.get', params)['result']
    
    return len(result)

