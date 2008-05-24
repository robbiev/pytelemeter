"""
    pytelemeter parser using the data for the telemeter flash graphs
"""

import re
import urllib
import urllib2
import datetime
from xml.dom import minidom
from pytelemeter.parser import *

# constants
URL_LOGIN='https://www.telenet.be/sys/sso/signon.jsp'
URL_VALIDATE='https://www.telenet.be/sys/sso/checksession.jsp?appid=telemeter_prod'
URL_XML='https://services.telenet.be/lngtlm/telemeter/%sdata.xml?graphType=%s'
DIRECTIONS = ['down', 'up']
MONTHS = {  'januari': 1,
            'februari': 2,
            'maart': 3,
            'april': 4,
            'mei': 5,
            'juni': 6,
            'juli': 7,
            'augustus': 8,
            'september': 9,
            'oktober': 10,
            'november': 11,
            'december': 12 }
AUTHFAIL = re.compile('errcode=sso\.login\.authfail\.([^&]+)&')

class FlashXMLParser(Parser):
    def __init__(self):
        try:
            import cookielib
            o = urllib2
        except ImportError:
            import ClientCookie
            cookielib = ClientCookie
            o = ClientCookie
        self.opener = o.build_opener(o.HTTPCookieProcessor(cookielib.CookieJar()))

    def fetch(self, account):
        self._get_cookie(account.username, account.password)

        usage = Usage(DIRECTIONS)
        for dir in DIRECTIONS:
            xml = self._get_totals(dir)
            month = usage.totals[dir]
            for node in xml.documentElement.childNodes:
                if node.nodeName in ('base','baseextension'):
                    month.mib += int(node.attributes.get('used').value)
                    month.max += int(node.attributes.get('available').value)
                elif node.nodeName in ('postpaid'):
                    month.mib += int(node.attributes.get('used').value)

            xml = self._get_chart(dir)
            if len(usage.chart) == 0: # initialize the dates
                for elem in xml.getElementsByTagName('category'):
                    attr =  elem.attributes.get('hoverText')
                    day, month = attr.value.split()
                    today = datetime.date.today()
                    date = datetime.date(today.year, MONTHS[month], int(day))
                    diff = today - date
                    if diff.days < -31:
                        date = datetime.date(today.year - 1, MONTHS[month], int(day))
                    if diff.days > 31:
                        date = datetime.date(today.year + 1, MONTHS[month], int(day))
                    if diff.days >= 0: # we ignore the future
                        values = {}
                        for d in DIRECTIONS:
                            values[d] = 0
                        usage.chart.append(UsageDay(date, values))
            for node in xml.getElementsByTagName('dataset'):
                for elem, index in zip(node.getElementsByTagName('set'),
                                    xrange(len(usage.chart))):
                    mb = int(elem.attributes.get('value').value)
                    day = usage.chart[index]
                    usage.chart[index].values[dir] += mb

        return usage

    def _get_cookie(self, username, password):
        try:
            post = urllib.urlencode({'uid': username, 'pwd': password})
            resp = self.opener.open(URL_LOGIN, post)
            match = AUTHFAIL.search(resp.geturl())
            if match:
                raise AuthenticationError, \
                    'authentication failure: %' % match.group(1)
            resp = self.opener.open(URL_VALIDATE)
        except urllib2.HTTPError, e:
            raise RemoteServiceError, \
                'unexpected http response: %i' % e.code
        except IOError, e:
            raise ConnectionError, \
                'could not connect to the Telemeter service'

    def _get_totals(self, dir):
        return self._get_xml(URL_XML % ('overview', dir))

    def _get_chart(self, dir):
        return self._get_xml(URL_XML % ('chart', dir))

    def _get_xml(self, url):
        try:
            resp = self.opener.open(url)
            return minidom.parseString(resp.read())
        except urllib2.HTTPError, e:
            raise RemoteServiceError, \
                'unexpected http response: %i' % e.code
        except IOError, e:
            raise ConnectionError, \
                'could not connect to the Telemeter service'
