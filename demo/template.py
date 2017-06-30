
from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm




# zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')
zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')

result = zabbixmgm.query_template_by_name(zapi, 'Template OS Linux')
result = zabbixmgm.query_host_by_name(zapi, '52n03.s52.local')
pprint(result)
demotpl = zabbixmgm.zbxtemplate(zapi, 'blubba')
result = zabbixmgm.query_interfaces_by_id(zapi, '38')

# pprint(demotpl.get())
demotpl.merge(result)
print(demotpl.id)
pprint(demotpl.get())
print(demotpl.id)
pprint(demotpl.online_items)
pprint(result)

