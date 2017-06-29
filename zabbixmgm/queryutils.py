

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
