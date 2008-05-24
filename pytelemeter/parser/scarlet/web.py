"""
    pytelemeter parser for Scarlet bandwidth usage web page
"""

import os
import re
import urllib
import urllib2
import datetime
from pytelemeter.parser import *

# constants
URL_COOKIE='http://customercare.scarlet.be/index.jsp?language=nl'
URL_LOGIN='http://customercare.scarlet.be/logon.do'
URL_USAGE='http://customercare.scarlet.be/usage/dispatch.do'
MONTHS = {  'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12 }
try:
    username = os.environ['USER']
except KeyError:
    username = os.path.basename(os.environ['HOME'])
CACHE = '/var/tmp/scarletmeter_%s.html' % username


class ScarletWebParser(Parser):
    def __init__(self):
        self.wascached = False

    def was_cached(self):
        return self.wascached

    def valid_cache(self):
        try:
            if not os.path.isfile(CACHE):
                return False
            mtime = os.path.getmtime(CACHE)
            cache = datetime.datetime.fromtimestamp(mtime)
            treshold = cache + datetime.timedelta(minutes=30)
            return treshold > datetime.datetime.now()
        except:
            return False

    def clear_cache(self):
        return # for testing purposes, no cache clearing
        if os.path.isfile(CACHE):
            os.remove(CACHE)

    def fetch(self, account):
        if self.valid_cache():
            file = open(CACHE,'r')
            html = file.read()
            file.close()
            self.wascached = True
        else:
            html = self._get_usage(account.username, account.password)
            try:
                file = open(CACHE,'w')
                file.write(html)
                file.close()
            except:
                pass
            self.wascached = False

        usage = Usage(['sum'])
        usage.chart = []

        REGEX_TOTAL='<param name="FlashVars" value="language=nl&used=([0-9]+)\|([0-9]+)" />'
        maxGb, usageMb = re.findall(REGEX_TOTAL,html)[0]
        usage.totals['sum'].mib = int(usageMb)
        usage.totals['sum'].max = 1024 * int(maxGb)

        REGEX_DAILY_LINE = '\s*<td class="digit">([^<>]*)</td>'
        REGEX_DAILY = '(?s)<tr>' + 4 * REGEX_DAILY_LINE + '\s*</tr>'

        matches = re.findall(REGEX_DAILY,html)
        for match in matches:
            day, month, year = match[0].split()
            date = datetime.date(int(year), MONTHS[month], int(day))
            values = {}
            def count_megabytes(text): # expected input like '123 MB'
                sizes = {'MB': 1, 'GB': 1024, 'kB': 0.001}
                s = text.split()
                return int(round(float(s[0]) * sizes[s[1]]))
            values['down'] = count_megabytes(match[1])
            values['up'] = count_megabytes(match[2])
            usage.chart.append(UsageDay(date, values))

        return usage

    def _get_usage(self, username, password):
        REGEX_COOKIE = '([A-Z]+=[^;]+;)'
        try:
            resp = urllib2.urlopen(URL_COOKIE)
            self.cookie = ' '.join(re.findall(REGEX_COOKIE,
                                    resp.info()['Set-Cookie']))

            post = urllib.urlencode({'username': username,'password': password})
            req = urllib2.Request(URL_LOGIN)
            req.add_header('Cookie',self.cookie)
            resp = urllib2.urlopen(req, post)
            req = urllib2.Request(URL_USAGE)
            req.add_header('Cookie',self.cookie)
            resp = urllib2.urlopen(req)
            return resp.read()
        except urllib2.HTTPError, e:
            raise RemoteServiceError, \
                'unexpected http response: %i' % e.code
        except IOError, e:
            raise ConnectionError, \
                'could not connect to the telemeter service'
