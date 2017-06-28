from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm




zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')
result = zabbixmgm.query_group_by_name(zapi, 'yu')

yugroup = zabbixmgm.zbxgroup(zapi, 'yu')
pprint(yugroup.online_items)


yugroup.merge(result)

yugroup.name = 'blub'
pprint(yugroup.online_items)
g = yugroup.get('update')

pprint(g)




