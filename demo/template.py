
from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm




# zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')
zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')

result = zabbixmgm.query_items_from_host(zapi, '10145')
pprint(result)


print(len(result))