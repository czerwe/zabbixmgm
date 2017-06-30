import sys
import zabbixmgm
from pprint import pprint
from zabbix.api import ZabbixAPI



zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')
# zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')


# Create Groups
groupname = 'autogroup'
grp = zabbixmgm.zbxgroup(zapi, groupname, zabbixmgm.query_group_by_name(zapi, groupname))
cmd, param = grp.get()
grp.request_result = zapi.do_request(cmd, param)

# Host
hostname = '52n03.s52.local'
host1_query = zabbixmgm.query_host_by_name(zapi, hostname)
host1 = zabbixmgm.zbxhost(zapi, hostname, host1_query)

res = zabbixmgm.query_interfaces_by_host(zapi, host1.id)
# pprint(res)
# sys.exit(0)

host1.add_group(grp)

if not host1.id:
    host1_inf = zabbixmgm.zbxinterface(zapi)
    host1_inf.host = host1.name
    host1.add_interface(host1_inf)

    host1_inf2 = zabbixmgm.zbxinterface(zapi)
    host1_inf2.host = host1.name
    host1_inf2.port = '40001'
    host1_inf2.type = zabbixmgm.zbxinterface.TYPE_JMX
    host1.add_interface(host1_inf2)

for group in host1_query.get('groups', {}):
    sub_group = zabbixmgm.query_group_by_name(zapi, group['name'])
    partgroup = zabbixmgm.zbxgroup(zapi, group['name'], groupmask=zabbixmgm.query_group_by_name(zapi, group['name']))
    host1.add_group(partgroup)

# pprint(host1_query)
for interface in host1_query.get('interfaces', {}):
    sub_interface = zabbixmgm.query_interfaces_by_id(zapi, interface['interfaceid'])
    partinterface = zabbixmgm.zbxinterface(zapi, interfacemask=zabbixmgm.query_group_by_name(zapi, group['name']))
    host1.add_interface(partinterface)

pprint(host1.online_items)
pprint(host1.interfaces)


template_response = zabbixmgm.query_template_by_name(zapi,'Template OS Linux')
tpl_oslinux = zabbixmgm.zbxtemplate(zapi, 'Template OS Linux', template_response)


template_response = zabbixmgm.query_template_by_name(zapi,'1blub')
tpl_blub = zabbixmgm.zbxtemplate(zapi, '1blub', template_response)
tpl_blub.add_group(grp)

# tpl_blub.add_template(tpl_oslinux)
cmd, param = tpl_blub.get()
tpl_blub.request_result = zapi.do_request(cmd, param)


# host1.add_template(tpl_oslinux)
host1.add_template(tpl_blub)

cmd, param = host1.get()
host1.request_result = zapi.do_request(cmd, param)


app_name = 'blubapp'
app_response = zabbixmgm.query_application_by_name(zapi, app_name)
app_blub = zabbixmgm.zbxapplication(zapi, app_name, app_response)
app_blub.add_host(tpl_blub)
cmd, param = app_blub.get()
app_blub.request_result = zapi.do_request(cmd, param)


itm_heap_max_name = '{0} - heap max'.format('blub')
itm_heap_max_result = zabbixmgm.query_item_by_name_and_host(zapi, itm_heap_max_name, host1.id)
# print('-------------')
# pprint(itm_heap_max_result)
itm_heap_max = zabbixmgm.zbxitem(zapi, itm_heap_max_name, itm_heap_max_result)
itm_heap_max.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]'
itm_heap_max.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
itm_heap_max.value_type = zabbixmgm.zbxitem.VAL_TYPE_NUMERIC_FLOAT
itm_heap_max.delay = 30

itm_heap_max.add_application(app_blub)
itm_heap_max.add_host(tpl_blub)
cmd, param = itm_heap_max.get()
itm_heap_max.request_result = zapi.do_request(cmd, param)



itm_heap_min_name = '{0} - heap min'.format('blub')
itm_heap_min_result = zabbixmgm.query_item_by_name_and_host(zapi, itm_heap_min_name, host1.id)
# print('-------------')
# pprint(itm_heap_min_result)
itm_heap_min = zabbixmgm.zbxitem(zapi, itm_heap_min_name, itm_heap_min_result)
itm_heap_min.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.min]'
itm_heap_min.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
itm_heap_min.value_type = zabbixmgm.zbxitem.VAL_TYPE_NUMERIC_FLOAT
itm_heap_min.delay = 30

itm_heap_min.add_application(app_blub)
itm_heap_min.add_host(tpl_blub)
cmd, param = itm_heap_min.get()
itm_heap_min.request_result = zapi.do_request(cmd, param)


