

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
        'selectInterfaces': ["name"],
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



def query_item_by_name_and_host(api, name, host):
    params = {
        'output': 'extend',
        'filter': {
            'name': [name],
            'hosts': [host]
        },
    }

    result = api.do_request('item.get', params)['result']
    if len(result) >= 1:
        return result[0]
    else:
        return {}



def query_items_from_host(api, host):
    params = {
        'output': 'extend',
        'filter': {
            'hosts': [host]
        },
    }

    result = api.do_request('item.get', params)['result']
    if len(result) >= 1:
        return result[0]
    else:
        return {}
