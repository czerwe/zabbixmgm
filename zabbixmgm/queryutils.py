from pprint import pprint

def query_group_by_name(api, name):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name]
        }
    }
    
    result = api.do_request('hostgroup.get', params)['result']
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
    pprint(params)
    result = api.do_request('item.get', params)['result']
    pprint(result)
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

    # pprint(params)

    result = api.do_request('hostinterface.get', params)['result']
    
    return len(result)
    # if  >= 1:
    #     return result
    # else:
    #     return {}

