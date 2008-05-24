"""
    command line output for pytelemeter
"""

import datetime
import sys


# constants
UP = {  'down': 'Download',
        'up':   ' Upload ',
        'sum':  '  Total ' }
LO = {  'down': 'download',
        'up':   'upload',
        'sum':  'transfer' }


class TelemeterOutput:
    def __init__(self, silent=False, verbose=False, debug=False,
                    daily=False, dailybars=False, remaining=False):
        self.silent = silent
        self.verbose = verbose
        self.debug = debug
        self.daily = daily
        self.dailybars = dailybars
        self.remaining = remaining

    def before_fetch(self):
        if not self.silent:
            print 'Fetching information... ',
            sys.stdout.flush()
        if self.debug:
            import httplib
            httplib.HTTPConnection.debuglevel = 1

    def after_fetch(self, usage, cached):
        if not self.silent:
            if cached:
                print 'from cache.'
            else:
                print 'done.'
            sys.stdout.flush()
        if self.verbose:
            self._print_stats(usage)
            if self.remaining:
                self._print_remaining(usage)
            if self.daily:
                self._print_daily(usage)

    def _fill_scale(self, progress, max):
        if (progress > 1):
            return 'Exceeded!'.center(max)
        return ('=' * int(round(max * progress))).ljust(max)

    def _print_stats(self, usage):
        if not self.silent:
            print ''
            print 'Telemeter statistics @ %s' \
                % datetime.date.today().strftime('%d %b %Y')
            print '----------------------------------'

        for dir, t in usage.totals.items():
            print '%s Volume:  [%s] %5s MiB (%2s%%)' % (UP[dir],
                self._fill_scale(t.float, 20), t.mib, t.pct)
        print ''

    def _print_remaining(self, usage):
        nextbill = usage.nextbill.strftime('%d/%m/%y')

        for dir, t in usage.totals.items():
            if t.mib > t.max:
                print 'You exceeded your prepaid %s volume by ' +\
                    '%i MiB.' % (LO[dir], t.mib - t.max)
            else:
                print ('Before %s, you can %s %i MiB without ' +\
                    'exceeding your prepaid %s volume.') % (
                    nextbill, LO[dir], t.max - t.mib, LO[dir])
        print ''

    def _print_daily(self, usage):
        if not self.silent:
            print 'Daily statistics:'
            print '-----------------'
        print '   Day  ',
        for dir in usage.chart[0].values.keys():
            print ' | %s' % UP[dir],
        print ''
        for day in usage.chart:
            print day.date.strftime('%d/%m/%y'),
            for mib in day.values.values():
                print ' | %8s' % mib,
            if self.dailybars:
                print '  [%s]' % '|'.join(['=' * int(round(mib / 50.0))
                                    for mib in day.values.values()]),
            print ''
        print ''
