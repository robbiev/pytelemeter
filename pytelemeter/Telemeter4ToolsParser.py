# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter parser using the telemeter4tools service, plus caching
"""

import os
import datetime
import time
from xml.dom import minidom
from Parser import *

# constants
URL='https://telemeter4tools.services.telenet.be/TelemeterService?wsdl'
try:
    username = os.environ['USER']
except KeyError:
    username = os.path.basename(os.environ['HOME'])
CACHE = '/var/tmp/telemeter_%s.xml' % username


class Parser(TelemeterParser):
    def __init__(self, output):
        self.output = output

    def valid_cache(self):
        try:
            if not os.path.isfile(CACHE):
                return False
            mtime = os.path.getmtime(CACHE)
            cache = datetime.datetime.fromtimestamp(mtime)
            if cache.minute < 30:
                treshold = cache.replace(minute=30)
            else:
                treshold = cache.replace(hour=cache.hour+1, minute=0)
            return treshold > datetime.datetime.now()
        except:
            return False

    def clear_cache(self):
        if os.path.isfile(CACHE):
            os.remove(CACHE)

    def fetch(self, username, password):
        if self.valid_cache():
            file = open(CACHE, 'r')
            xml = file.read()
            file.close()
            if not self.output.silent:
                print 'from cache... ',
        else:
            import SOAPpy
            soap = SOAPpy.SOAPProxy(URL)
            del SOAPpy
            xml = soap.getUsage(string=username, string0=password)
            try:
                file = open(CACHE,'w')
                file.write(xml)
                file.close()
            except:
                pass
        node = _Ns1Node(minidom.parseString(xml))
        status = str(node['usage-info']['status'])
        if status != 'OK':
            self.clear_cache()
            if status.find('SYSERR_00001') >= 0:
                raise RemoteServiceError, \
                    'unexpected error in telemeter4tools application'
            if status.find('ERRTLMTLS_00001') >= 0:
                raise RemoteServiceError, \
                    'unexpected error in telemeter4tools application'
            if status.find('ERRTLMTLS_00002') >= 0:
                raise AuthenticationError, 'login or password empty'
            if status.find('ERRTLMTLS_00003') >= 0:
                raise RemoteServiceError, \
                    'exceeded number of allowed accesses'
            if status.find('ERRTLMTLS_00004') >= 0:
                raise AuthenticationError, \
                    'login or password incorrect'
        service_node = node['usage-info']['data']['service']

        usage = Usage()

        usage.down.base = int(service_node['totalusage']['down'])
        usage.down.base_max = int(service_node['limits']['max-down'])
        usage.up.base = int(service_node['totalusage']['up'])
        usage.up.base_max = int(service_node['limits']['max-up'])

        today = datetime.date.today()
        for day in service_node['usage']:
            datestring = day.node.attributes.get('day').value
            t = time.strptime(datestring, '%Y%m%d')
            date = datetime.date(t[0], t[1], t[2])
            if date <= today:
                usage.chart.append(UsageDay(date, int(day['down']),
                                                    int(day['up'])))

        return usage

class _Ns1Node:
    def __init__(self, node):
        self.node = node
    def __getitem__(self, key):
        children = self.node.getElementsByTagName('ns1:'+key)
        if len(children) == 1:
            return _Ns1Node(children[0])
        elif len(children) > 1:
            nodes = []
            for child in children:
                nodes.append(_Ns1Node(child))
            return nodes
        return None
    def __iter__(self):
        for child in self.node.childNodes:
            yield child
    def __str__(self):
        return self.node.firstChild.nodeValue
    def __int__(self):
        return int(self.node.firstChild.nodeValue.split('.')[0])
