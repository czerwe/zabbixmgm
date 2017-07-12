import sys
import zabbixmgm
import log
from pprint import pprint
from zabbix.api import ZabbixAPI



zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')

host1_inf = zabbixmgm.zbxinterface(zapi, mask={'blub': 'sdfs', 'hostid': 33434})
host1_inf.get()

# groupname = 'autogroup'
# grp = zabbixmgm.zbxgroup(zapi, groupname, zabbixmgm.query_group_by_name(zapi, groupname))
# cmd, param = grp.get()
# grp.request_result = zapi.do_request(cmd, param)



# hostname = '52n03.s52.local'
# host1_query = zabbixmgm.query_host_by_name(zapi, hostname)
# pprint(host1_query)
# host1 = zabbixmgm.zbxhost(zapi, hostname, host1_query)
# host1.add_group(grp)

# host1_inf.host = host1.name
# host1_inf.main = 1
# host1.add_interface(host1_inf)


# command, param = host1.get()
# zapi.do_request(command, param)

# host2_inf = zabbixmgm.zbxinterface(zapi)
# host2_inf.host = host1.name
# host2_inf.type = 4
# host2_inf.main = 1
# host2_inf.hostid = host1.id


# command, param = host2_inf.get()
# zapi.do_request(command, param)


# # param {filter: {
# #     "name": hostname:
# #     ""
# # }}
# pprint(zapi.do_request("host.get", param))




