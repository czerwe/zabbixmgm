from pprint import pprint
from zabbix.api import ZabbixAPI
import zabbixmgm

import re


class zbxappmonitor(object):

    def __init__(self, api, applicationname, groups, host, port):
        self.api = api
        self.applicationname = applicationname
        self.groups = groups
        self.app_host = host
        self.app_port = port
        self.app_interface = None

        self.apptemplate = zabbixmgm.zbxtemplate(api, '1Template {0}'.format(applicationname), self.groups)
        self.apptemplate.create_application(applicationname)

        self.defaults = dict()
        self.defaults['interface.type'] = zabbixmgm.zbxinterface.TYPE_AGENT

        self.interface(self.app_host.get_name(), port)
        self.app_host.add_interface(self.app_interface)


    def create(self):
        self.apptemplate.create(groups=[self.groups.get_id()])
 
    def interface(self, host, port, interface_type=None):
        """
        Configure the interface for this service
        
        :param host: ip or fqdn of the host
        :type host: str
        :param port: ip or fqdn of the port
        :type port: str
        :param interface_type: interface type
        :type interface_type: int
        
        :return: None
        :rtype: None
        """
        if not interface_type:
            interface_type = self.defaults['interface.type']

        if not self.app_interface:
            self.app_interface = zabbixmgm.zbxinterface(self.api, self.applicationname)

        self.app_interface.add_param('host', host)
        self.app_interface.add_param('type', self.defaults['interface.type'])
        self.app_interface.add_param('port', str(port))

        self.app_interface.add_param('hostid', self.app_host.get_id())
        self.app_interface.write()



class zbxjmxappmonitor(zbxappmonitor):

    def __init__(self, api, applicationname, groups, host, port):
        super(zbxjmxappmonitor, self).__init__(api, applicationname, groups, host, port)
        
        self.defaults['interface.type'] = zabbixmgm.zbxinterface.TYPE_JMX
    
        self.java_commons()
        self.appSpecificItems()

 

    def java_commons(self):
        heap_max = self.apptemplate.create_item('{0} - heap max'.format(self.applicationname), applicationname=self.applicationname)
        heap_max.set_params('key_', 'jmx[java.lang:type=Memory, HeapMemoryUsage.max]')
        heap_max.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

        heap_used = self.apptemplate.create_item('{0} - heap used'.format(self.applicationname), applicationname=self.applicationname)
        heap_used.set_params('key_', 'jmx[java.lang:type=Memory, HeapMemoryUsage.used]')
        heap_used.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

        nonheap_max = self.apptemplate.create_item('{0} - nonheap max'.format(self.applicationname), applicationname=self.applicationname)
        nonheap_max.set_params('key_', 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.max]')
        nonheap_max.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

        nonheap_used = self.apptemplate.create_item('{0} - nonheap used'.format(self.applicationname), applicationname=self.applicationname)
        nonheap_used.set_params('key_', 'jmx[java.lang:type=Memory, NonHeapMemoryUsage.used]')
        nonheap_used.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

        java_threads = self.apptemplate.create_item('{0} - java threads'.format(self.applicationname), applicationname=self.applicationname)
        java_threads.set_params('key_', 'jmx[java.lang:type=Threading, ThreadCount]')
        java_threads.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)


    def appSpecificItems(self):
        pass



class zbxMcngEventCorrelator(zbxjmxappmonitor):

    def __init__(self, api, applicationname, groups, host, port):
        super(zbxMcngEventCorrelator, self).__init__(api, applicationname, groups, host, port)

 
    def appSpecificItems(self):
        ec_totalnumber_of_intercepts_created = self.apptemplate.create_item('{0} -  Total intercepts created'.format(self.applicationname), applicationname=self.applicationname)
        ec_totalnumber_of_intercepts_created.set_params('key_', 'jmx[EC:type=InterceptCounters, TotalNumberOfInterceptsCreated]')
        ec_totalnumber_of_intercepts_created.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

        ec_One_minute_creation_rate = self.apptemplate.create_item('{0} -  One minute creation rate'.format(self.applicationname), applicationname=self.applicationname)
        ec_One_minute_creation_rate.set_params('key_', 'jmx[EC:type=InterceptCounters, OneMinuteInterceptCreationRate]')
        ec_One_minute_creation_rate.set_params('type', zabbixmgm.zbxitem.TYPE_JMX_AGENT)

 

class zbxMcngDtu(zbxjmxappmonitor):

    def __init__(self, api, applicationname, groups, host, port):
        super(zbxMcngDtu, self).__init__(api, applicationname, groups, host, port)


import sys


zapi = ZabbixAPI(url='http://192.168.52.10:91', user='Admin', password='zabbix')

mcgroup = zabbixmgm.zbxgroup(zapi, '3MCng')


n03 = zabbixmgm.zbxhost(zapi, '52n03.s52.local', [mcgroup])
app = zbxMcngEventCorrelator(zapi, 'EventCorrelator', [mcgroup], n03, '40002')

