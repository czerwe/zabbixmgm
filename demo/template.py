
from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm


zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')
blub = zabbixmgm.zbxinterface(zapi, {'interfaceid': '232'}, host='hollei')
pprint(blub.get_attrs(True))

# pprint(blub.get_attrs())
# pprint(blub.get_attrs(True))

blub = zabbixmgm.zbxhost(zapi, "test", {'hostid': '232'})
pprint(blub.get_attrs(True))


# class blub(object):

#     def __init__(self):
#         self.bu = None


#     @property
#     def id(self):
#         return 'Value: {0}'.format(self.bu)

#     @id.setter
#     def id(self, val):
#         self.bu = val
    

# g = blub()

# g.id = "test"
# print g.id


# setattr(g, 'id', 'hollei')
# print g.id
# g.id = '34'
# print getattr(g, 'id')

# # zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')
# zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')

# result = zabbixmgm.query_items_from_host(zapi, '10145')
# pprint(result)


# print(len(result))