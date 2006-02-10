# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter parser using the data for the telemeter flash graphs
"""

import re
import urllib
import urllib2
import datetime
from xml.dom import minidom
from Parser import *

# constants
URL_LOGIN='https://www.telenet.be/sys/sso/signon.jsp'
URL_VALIDATE='https://www.telenet.be/sys/sso/checksession.jsp?appid=telemeter_prod&goto=/sso/valid.html'
URL_XML_TOTALS='https://services.telenet.be/lngtlm/overviewdata.xml?graphType='
URL_XML_CHART='https://services.telenet.be/lngtlm/chartdata.xml?graphType='
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


class Parser(TelemeterParser):
    def __init__(self, output):
        self.output = output

    def fetch(self, username, password):
        self._get_cookie(username, password)
        usage = Usage()
        for dir in 'down', 'up':
            xml = self._get_totals(dir)
            month = getattr(usage, dir)
            for node in xml.documentElement.childNodes:
                if node.nodeName == 'base':
                    month.base = int(node.attributes.get('used').value)
                    month.base_max = \
                        int(node.attributes.get('available').value)
                elif node.nodeName == 'baseextension':
                    month.extended = int(node.attributes.get('used').value)
                    month.extended_max = \
                        int(node.attributes.get('available').value)
                elif node.nodeName == 'postpaid':
                    month.postpaid = int(node.attributes.get('used').value)

            xml = self._get_chart(dir)

            if len(usage.chart) == 0: # initialize the dates
                for elem in xml.getElementsByTagName('category'):
                    attr =  elem.attributes.get('hoverText')
                    day, month = attr.value.split()
                    today = datetime.date.today()
                    date = datetime.date(today.year, MONTHS[month], int(day))
                    diff = today - date
                    if diff.days < -31:
                        date = datetime.date(today.year - 1, months[month], int(day))
                    if diff.days > 31:
                        date = datetime.date(today.year + 1, months[month], int(day))
                    if diff.days >= 0: # we ignore the future
                        usage.chart.append(UsageDay(date))

            for node in xml.getElementsByTagName('dataset'):
                for elem, index in zip(node.getElementsByTagName('set'),
                                    xrange(len(usage.chart))):
                    mb = int(elem.attributes.get('value').value)
                    day = usage.chart[index]
                    setattr(day, dir, getattr(day, dir) + mb)

        return usage

    def _get_cookie(self, username, password):
        REGEX_COOKIE = '([A-Z]+=[^;]+;)'
        try:
            post = urllib.urlencode({'uid': username,'pwd': password})
            resp = urllib2.urlopen(URL_LOGIN, post)
            self.cookie = ' '.join(re.findall(REGEX_COOKIE,
                                    resp.info()['Set-Cookie']))
            req = urllib2.Request(URL_VALIDATE)
            req.add_header('Cookie',self.cookie)
            resp = urllib2.urlopen(req)
            self.cookie = re.search(REGEX_COOKIE,
                                    resp.info()['Set-Cookie']).group(1)
        except urllib2.HTTPError, e:
            raise RemoteServiceError, \
                'unexpected http response: %i' % e.code
        except IOError, e:
            self._parse_IOError(e)

    def _get_totals(self, dir):
        return self._get_xml(URL_XML_TOTALS+dir)

    def _get_chart(self, dir):
        return self._get_xml(URL_XML_CHART+dir)

    def _get_xml(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header('Cookie',self.cookie)
            page = urllib2.urlopen(req)
            return minidom.parseString(page.read())
        except urllib2.HTTPError, e:
            raise RemoteServiceError, \
                'unexpected http response: %i' % e.code
        except IOError, e:
            self._parse_IOError(e)

    def _parse_IOError(self, ioerror):
        REGEX_ERROR = 'errcode=([^&]+)&'
        for resp in ioerror:
            try:
                if resp.has_key('location'):
                    header = resp.getheaders('location')
                    match = re.search(Constants.REGEX_ERROR,
                                                    str(header))
                    if match:
                        error = match.group(1)
                        known_errors = {
                            'sso.login.authfail.PasswordNOK':
                              AuthenticationError('password incorrect'),
                            'sso.login.authfail.LoginDoesNotExist':
                              AuthenticationError('login incorrect')
                        }
                        try:
                            raise known_errors[error]
                        except KeyError:
                            raise RemoteServiceError, \
                                'telemeter failure code %s' % error
            except:
                pass
        raise ConnectionError, \
            'could not connect to the telemeter service'
