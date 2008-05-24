"""
    pytelemeter parser programming interface
    this package has a subdirectory for each provider
"""

import datetime

# exceptions
class ParserError(Exception): pass
class ConnectionError(ParserError): pass
class RemoteServiceError(ParserError): pass
class AuthenticationError(ParserError): pass

class Provider:
    "an ISP, offering online bandwidth usage statistics"
    def parsers(self):
        raise NotImplementedException
    def name(self, capital=False):
        raise NotImplementedException

class Account:
    "an account with your ISP, most likely a Telenet account"
    def __init__(self, id, username, password, provider=None):
        self.id = id
        self.username = username
        self.password = password
        if not provider:
            provider = 'telenet'
        self.provider = provider
    def parsers(self):
        try:
            p = __import__('pytelemeter.parser.%s' % self.provider)
            p = getattr(p.parser, self.provider)
            return p.parsers()
        except ImportError:
            raise ParserError, \
                'no parser found for provider: %s' % providername

class Parser:
    "the parser interface"
    def fetch(self, account):
        """
          fetch the data
          returns a Usage object
        """
        raise NotImplementedError
    def clear_cache(self):
        """
          if the parser keeps a cache, clear it
        """
        pass
    def was_cached(self):
        """
          did the last fetch come from cache?
        """
        return False

class Usage:
    "an object containing all the telemeter readings"
    # totals -> dictionary of UsageMonths
    # chart -> list of UsageDays
    def __init__(self, constraints=[]):
        self.chart = []
        self.totals = {}
        for constraint in constraints:
            self.totals[constraint] = UsageMonth(constraint)
    def __getattr__(self, name):
        if name == 'nextbill':
            last = self.chart[0].date
            if last.month == 12:
                return datetime.date(last.year+1, 1, last.day)
            else:
                return datetime.date(last.year, last.month+1, last.day)
        elif name == 'daysleft':
            diff = self.nextbill - datetime.date.today()
            return diff.days
        else:
            try:
                return self.totals[name]
            except KeyError:
                return getattr(Usage, name)

class UsageMonth:
    """the bandwidth usage (so far) this month,
        for one of the constraints (either upload, download or total)
    """
    # max, mib -> int
    def __init__(self, constraint=''):
        self.mib = 0
        self.max = 0
        self.constraint = constraint
    def __getattr__(self, name):
        "compute the attributes for total usage on the fly"
        expr = {
            'pct': '100 * self.mib / self.max',
            'float': 'float(self.mib) / float(self.max)'
            }
        try:
            return eval(expr[name])
        except ZeroDivisionError:
            return 0
        except KeyError:
            return getattr(UsageMonth, name)

class UsageDay:
    "the bandwidth usage of a particular day"
    # date -> datetime.date
    # values -> dictionary of ints
    def __init__(self, date=None, values={}):
        self.date = date
        self.values = values
    def __getattr__(self, name):
        try:
            return self.values[name]
        except KeyError:
            return getattr(UsageDay, name)
