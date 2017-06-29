import zabbixmgm
from pprint import pprint
from zabbix.api import ZabbixAPI

zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')


# Create Groups
groupname = 'autogroup'
grp = zabbixmgm.zbxgroup(zapi, groupname, zabbixmgm.query_group_by_name(zapi, groupname))
cmd, param = grp.get()
grp.request_result = zapi.do_request(cmd, param)

# Host
hostname = '52n03.s52.local'
host1_query = zabbixmgm.query_host_by_name(zapi, hostname)
host1 = zabbixmgm.zbxhost(zapi, hostname, host1_query)


if not host1.id:
    host1_inf = zabbixmgm.zbxinterface(zapi)
    host1_inf.host = host1.name
    host1.add_interface(host1_inf)
host1.add_group(grp)

# for group in host1_query.get('groups', {}):
#     sub_group = zabbixmgm.query_group_by_name(zapi, group['name'])
#     partgroup = zabbixmgm.zbxgroup(zapi, group['name'], groupmask=zabbixmgm.query_group_by_name(zapi, group['name']))
#     host1.add_group(partgroup)

# pprint(host1_query)
# for group in host1_query.get('interfaces', {}):
#     sub_group = zabbixmgm.query_group_by_name(zapi, group['name'])
#     partgroup = zabbixmgm.zbxgroup(zapi, group['name'], groupmask=zabbixmgm.query_group_by_name(zapi, group['name']))
#     host1.add_group(partgroup)


template_response = zabbixmgm.query_template_by_name(zapi,'Template OS Linux')
tpl_oslinux = zabbixmgm.zbxtemplate(zapi, 'Template OS Linux', template_response)

host1.add_template(tpl_oslinux)

cmd, param = host1.get()
# pprint(param)
host1.request_result = zapi.do_request(cmd, param)




template_response = zabbixmgm.query_template_by_name(zapi,'1blub')
tpl_blub = zabbixmgm.zbxtemplate(zapi, '1blub', template_response)
tpl_blub.add_group(grp)

# tpl_blub.add_template(tpl_oslinux)
cmd, param = tpl_blub.get()
tpl_blub.request_result = zapi.do_request(cmd, param)



app_name = 'blubapp'
app_response = zabbixmgm.query_application_by_name(zapi, app_name)
app_blub = zabbixmgm.zbxapplication(zapi, app_name, app_response)
app_blub.add_host(tpl_blub)
cmd, param = app_blub.get()
app_blub.request_result = zapi.do_request(cmd, param)




itm_heap_max = zabbixmgm.zbxitem(zapi, '{0} - heap max'.format('blub'))
itm_heap_max.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]'
itm_heap_max.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
itm_heap_max.delay = 30

itm_heap_max.add_application(app_blub)
itm_heap_max.add_host(tpl_blub)
cmd, param = itm_heap_max.get()
pprint(param)
itm_heap_max.request_result = zapi.do_request(cmd, param)