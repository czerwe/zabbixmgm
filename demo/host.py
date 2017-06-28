from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm




zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')

result = zabbixmgm.query_group_by_name(zapi, 'yu')
yugroup = zabbixmgm.zbxgroup(zapi, 'yu')
yugroup.merge(result)
pprint(yugroup.id)

result = zabbixmgm.query_group_by_name(zapi, 'yi')
yigroup = zabbixmgm.zbxgroup(zapi, 'yi')
yigroup.merge(result)
pprint(yigroup.id)

command, param = yigroup.get()
zapi.do_request(command, param)

myhost_result = zabbixmgm.query_host_by_name(zapi, '52n05.s52.local')
myhost3 = zabbixmgm.zbxhost(zapi, '52n05.s52.local')
myhost3.merge(myhost_result)


if not myhost3.id:
    inf = zabbixmgm.zbxinterface(zapi)
    inf.host = myhost3.name
    myhost3.add_interface(inf)

myhost3.add_group(yugroup)

# pprint(myhost_result)
# pprint(myhost_result.get('groups', {}))
for group in myhost_result.get('groups', {}):
    print(group)
    grpresult = zabbixmgm.query_group_by_name(zapi, group['name'])
    partgroup = zabbixmgm.zbxgroup(zapi, grpresult['name'], groupmask=grpresult)
    pprint(partgroup.id)
    myhost3.add_group(partgroup)


myhost3.add_group(yigroup)
command, param = myhost3.get()
# pprint(param)
zapi.do_request(command, param)


