# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter parser programming interface
"""

import datetime

# exceptions
class Error(Exception): pass
class ConnectionError(Error): pass
class RemoteServiceError(Error): pass
class AuthenticationError(Error): pass


class Output:
    "the output level"
    def __init__(self, silent=False, verbose=False, debug=False,
                    daily=False, remaining=False):
        self.silent = silent
        self.verbose = verbose
        self.debug = debug
        self.daily = daily
        self.remaining = remaining

class TelemeterParser:
    "the parser interface"
    def fetch(self, username, password):
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

class Usage:
    "an object containing all the telemeter readings"
    # up, down -> UsageMonth
    # chart -> list of UsageDays
    def __init__(self):
        self.chart = []
        self.down = UsageMonth()
        self.up = UsageMonth()
    def __getattr__(self, name):
        if name == 'nextbill':
            last = self.chart[0].date
            if last.month == 12:
                return datetime.date(last.year+1, 1, last.day)
            else:
                return datetime.date(last.year, last.month+1, last.day)
        if name == 'daysleft':
            diff = self.nextbill - datetime.date.today()
            return diff.days
        else:
            return getattr(Usage, name)

class UsageMonth:
    "the bandwidth usage (so far) this month, either upload or download"
    # base, base_max, extended, extended_max, postpaid -> int
    def __init__(self):
        self.base = 0
        self.base_max = 0
        self.extended = 0
        self.extended_max = 0
        self.postpaid = 0
    def __getattr__(self, name):
        "compute the attributes for total usage on the fly"
        expr = {
            'total': 'self.base + self.extended + self.postpaid',
            'total_max': 'self.base_max + self.extended_max',
            'base_pct': '100 * self.base / self.base_max',
            'base_float': 'float(self.base) / float(self.base_max)',
            'extended_pct': '100 * self.extended / self.extended_max',
            'extended_float':
                'float(self.extended) / float(self.extended_max)',
            'total_pct': '100 * self.total / self.total_max',
            'total_float': 'float(self.total) / float(self.total_max)'
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
    # up, down -> int
    def __init__(self, date=None, down=0, up=0):
        self.date = date
        self.down = down
        self.up = up
