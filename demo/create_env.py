import sys
import zabbixmgm
from pprint import pprint
from zabbix.api import ZabbixAPI

# zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')
zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')



def create_group(groupname):
    resp = zabbixmgm.query_group_by_name(zapi, groupname)
    pprint(resp)
    grp = zabbixmgm.zbxgroup(zapi, name=groupname, mask=resp)

    if not grp.id:
        cmd, param = grp.get()
        grp.request_result = zapi.do_request(cmd, param)

    return grp


def create_application(appname, host):
    resp = zabbixmgm.query_application_by_name(zapi, appname)
    retApp = zabbixmgm.zbxapplication(zapi, name=appname, mask=resp)
    if not retApp.id:
        retApp.add_host(host)
        cmd, param = retApp.get()
        retApp.request_result = zapi.do_request(cmd, param)
    return retApp


def get_template(templatename, group, subtemplates=list()):
    resp = zabbixmgm.query_template_by_name(zapi, name=templatename)
    retTemplate = zabbixmgm.zbxtemplate(zapi, name=templatename, mask=resp)
    retTemplate.add_group(group)
    for i in subtemplates:
        retTemplate.add_template(i)

    
    commit_template(retTemplate)

    return retTemplate

def get_interface(host, port, itype):
    retInf = zabbixmgm.zbxinterface(zapi)
    retInf.hostid = host.id
    retInf.host = host.name
    retInf.port = port
    retInf.type = itype
    # retInf.main = main
    
    commit_interface(retInf)
    return retInf

def commit_interface(inf):
    if zabbixmgm.query_num_of_interface_types(zapi, inf.hostid, inf.type) == 0:
        inf.main = 1

    cmd, param = inf.get()
    inf.request_result = zapi.do_request(cmd, param)


def commit_template(tempalte):
    cmd, param = tempalte.get()
    tempalte.request_result = zapi.do_request(cmd, param)





def commit_host(host):
    cmd, param = host.get()
    host.request_result = zapi.do_request(cmd, param)

def get_host(hostname, group):
    resp = zabbixmgm.query_host_by_name(zapi, hostname)
    retHost = zabbixmgm.zbxhost(zapi, name=hostname, mask=resp)
    retHost.add_group(group)
    
    if not retHost.id:
        inf = zabbixmgm.zbxinterface(zapi)
        inf.host = retHost.name
        retHost.add_interface(inf)
    else:
        for interface in resp.get('interfaces', {}):
            sub_interface = zabbixmgm.query_interfaces_by_id(zapi, interface['interfaceid'])
            partinterface = zabbixmgm.zbxinterface(zapi, mask=sub_interface)
            retHost.add_interface(partinterface)

    commit_host(retHost)

    return retHost


class apptemplate(object):

    def __init__(self, shortname, longname, groupname):
        self.items = list()
        self.corecounter(self)
        self.app_short_name = shortname
        self.group = create_group(groupname)
        self.template = get_template("Template {0}".format(longname), self.group, []) 
        self.application = create_application(longname, self.template)
        self.corecounter()

    def corecounter(self):
        pass

    def get_item(self, itemname):
        res = zabbixmgm.query_item_by_name_and_host(zapi, itemname, self.template.id)
        retItem = zabbixmgm.zbxitem(zapi, name=itemname, mask=res, delay=30, value_type=zabbixmgm.zbxitem.VAL_TYPE_NUMERIC_FLOAT)
        retItem.add_host(self.template)
        retItem.add_application(self.app)
        return retItem

    def commit_item(self, item):
        cmd, param = item.get()
        item.request_result = zapi.do_request(cmd, param)



class jmxapptemplate(apptemplate):

    def __init__(self, shortname, longname, groupname):
        super(jmxapptemplate, self).__init__(self, shortname, longname, groupname)

    def get_item(self, itemname):
        itm = super(jmxapptemplate, self).get_item(itemname)
        itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
        return itm

    def corecounter(self):
        itm = self.get_item('{0} - heap max'.format(self.app_short_name))
        itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]'
        self.commit_item(itm)
        self.items.append(itm)

        itm = self.get_item('{0} - heap used'.format(self.app_short_name))
        itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.used]'
        self.commit_item(itm)
        self.items.append(itm)

        itm = self.get_item('{0} - nonheap max'.format(self.app_short_name))
        itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.max]'
        self.commit_item(itm)
        self.items.append(itm)

        itm = self.get_item('{0} - nonheap used'.format(self.app_short_name))
        itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.used]'
        self.commit_item(itm)
        self.items.append(itm)

        itm = self.get_item('{0} - java threads'.format(self.app_short_name))
        itm.key = 'jmx[java.lang:type=Threading, ThreadCount]'
        self.commit_item(itm)
        self.items.append(itm)



# class eventCorrelator(object):

#     def __init__(self):
#         self.app_short_name = 'EC'
#         # template_response = zabbixmgm.query_template_by_name(zapi,'Template OS Linux')
#         # tpl_oslinux = zabbixmgm.zbxtemplate(zapi, mask=template_response, name='blub')


#         self.group = create_group("MCng Backend")
#         self.template = get_template("Template MCng EventCorrelator", self.group, []) 
#         self.application = create_application('MCng Event Correlator', self.template)
#         self.items = list()
#         self.add_items()


#     def add_items(self):
#         itm = get_item('{0} - heap max'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - heap used'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.used]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - nonheap max'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.max]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - nonheap used'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.used]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - java threads'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Threading, ThreadCount]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)
        
#     def assign_to_host(self, host, port):
#         host.add_template(self.template)
#         intf = get_interface(host, port, itype=zabbixmgm.zbxinterface.TYPE_JMX)
#         # intf.type = 
#         host.add_interface(intf)
#         commit_host(host)


# class applicationservice(object):

#     def __init__(self):
#         self.app_short_name = 'AG'
#         # template_response = zabbixmgm.query_template_by_name(zapi,'Template OS Linux')
#         # tpl_oslinux = zabbixmgm.zbxtemplate(zapi, mask=template_response, name='blub')


#         self.group = create_group("MCng Backend")
#         self.template = get_template("Template MCng ApplicationServie", self.group) 
#         self.application = create_application('MCng Application Service', self.template)
#         self.items = list()
#         self.add_items()


#     def add_items(self):
#         itm = get_item('{0} - heap max'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - heap used'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, HeapMemoryUsage.used]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - nonheap max'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.max]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - nonheap used'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.used]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)

#         itm = get_item('{0} - java threads'.format(self.app_short_name), self.template, self.application)
#         itm.key = 'jmx[java.lang:type=Threading, ThreadCount]'
#         itm.type = zabbixmgm.zbxitem.TYPE_JMX_AGENT
#         commit_item(itm)
#         self.items.append(itm)
        
#     def assign_to_host(self, host, port):
#         host.add_template(self.template)
#         intf = get_interface(host, port, itype=zabbixmgm.zbxinterface.TYPE_JMX)
#         # intf.type = 
#         host.add_interface(intf)
#         commit_host(host)



ec = eventCorrelator()
ag = applicationservice()

n3 = get_host('52n03.s52.local', create_group("MCng Backend"))

# ec.assign_to_host(n3, '40002')
# ag.assign_to_host(n3, '40003')