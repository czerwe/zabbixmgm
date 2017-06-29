from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm

import sys


# zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')
zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')

result = zabbixmgm.query_group_by_name(zapi, 'yu')
grp_meine = zabbixmgm.zbxgroup(zapi, 'meinehosts', zabbixmgm.query_group_by_name(zapi, 'meinehosts'))
grp_meine2 = zabbixmgm.zbxgroup(zapi, 'meinehosts2', zabbixmgm.query_group_by_name(zapi, 'meinehosts2'))

command, param = grp_meine.get()
grp_meine.request_result = zapi.do_request(command, param)

command, param = grp_meine2.get()
grp_meine2.request_result = zapi.do_request(command, param)

myhost1_result = zabbixmgm.query_host_by_name(zapi, '52n05.s52.local')
myhost1 = zabbixmgm.zbxhost(zapi, '52n05.s52.local', myhost1_result)


if not myhost1.id:
    inf = zabbixmgm.zbxinterface(zapi)
    inf.host = myhost1.name
    myhost1.add_interface(inf)

myhost1.add_group(grp_meine)

for group in myhost1_result.get('groups', {}):
    grpresult = zabbixmgm.query_group_by_name(zapi, group['name'])
    partgroup = zabbixmgm.zbxgroup(zapi, grpresult['name'], groupmask=zabbixmgm.query_group_by_name(zapi, group['name']))
    myhost1.add_group(partgroup)


myhost1.add_group(grp_meine2)
command, param = myhost1.get()
# pprint(command)
# pprint(param)
myhost1.request_result = zapi.do_request(command, param)

import time
time.sleep(10)
for dev in [myhost1, grp_meine2, grp_meine]:
    command, param = dev.get('delete')
    zapi.do_request(command, param)



