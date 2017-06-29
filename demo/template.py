
from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm




zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')

result = zabbixmgm.query_template_by_name(zapi, 'Template OS Linux')

demotpl = zabbixmgm.zbxtemplate(zapi, 'blubba')

# pprint(demotpl.get())
demotpl.merge(result)
print(demotpl.id)
pprint(demotpl.get())
print(demotpl.id)
pprint(demotpl.online_items)
pprint(result)

