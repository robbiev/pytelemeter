# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter public interface
"""

import Config
from Parser import *


class Telemeter:
    """ the public pytelemeter interface """
    def __init__(self, output=None):
        if not output:
            output = Output()
        self.output = output
        self.usage = None
        self.parsers=[]
        try:
            import Telemeter4ToolsParser
            self.parsers.append(Telemeter4ToolsParser.Parser(output))
        except:
            pass # SOAPpy is probably not installed, silent skip it
        try:
            import FlashXMLParser
            self.parsers.append(FlashXMLParser.Parser(output))
        except:
            pass # should not happen, but no real harm
        self.config = Config.ConfigFile()
        try:
            self.read_config()
        except Config.Error, e:
            self.username = ''
            self.password = ''
            self.configerror = str(e)

    def fetch(self):
        self.usage = None
        if not self.username or not self.password:
            if self.configerror:
                raise AuthenticationError, self.configerror
            else:
                raise AuthenticationError, 'login or password empty'
        if not self.output.silent:
            print 'Fetching information... ',
        last = Exception('no parsers could be initialized')
        for parser in self.parsers:
            try:
                self.usage = parser.fetch(self.username, self.password)
                if not self.output.silent:
                    print 'done!'
                if self.output.verbose:
                    self._print_stats()
                    if self.output.remaining:
                        self._print_remaining()
                    if self.output.daily:
                        self._print_daily()
                return self.usage
            except AuthenticationError, e:
                raise
            except Exception, e:
                last = e
        raise last

    def clear_cache(self):
        for parser in self.parsers:
            try:
                parser.clear_cache()
            except:
                pass

    def read_config(self):
        self.configerror = None
        self.username, self.password = self.config.read()

    def save_config(self):
        self.configerror = None
        self.config.username = self.username
        self.config.password = self.password
        self.config.save()

    def _fill_scale(self, progress, max):
        if (progress > 1):
            return 'Exceeded!'.center(max)
        return ('=' * int(round(max * progress))).ljust(max)

    def _print_stats(self):
        d = self.usage.down
        u = self.usage.up

        if not self.output.silent:
            print ''
            print 'Telemeter statistics @ %s' \
                % datetime.date.today().strftime('%d %b %Y')
            print '----------------------------------'

        print '%s [%s] %5s MiB (%2s%%)' % ('Download Volume: ', 
            self._fill_scale(d.total_float, 20), d.total, d.total_pct)
        print '%s [%s] %5s MiB (%2s%%)' % (' Upload  Volume: ',
            self._fill_scale(u.total_float, 20), u.total, u.total_pct)
        print ''

    def _print_remaining(self):
        down = self.usage.down
        up = self.usage.up
        nextbill = self.usage.nextbill.strftime('%d/%m/%y')

        if down.total > down.total_max:
            print 'You exceeded your prepaid download volume by ' +\
                '%i MiB.' % (down.total - down.total_max)
        else:
            print ('Before %s, you can download %i MiB without ' +\
                'exceeding your prepaid download volume.') % (
                nextbill, down.total_max - down.total)

        if up.total > up.total_max:
            print 'You exceeded your prepaid upload volume by ' +\
                '%i MiB.' % (up.total - up.total_max)
        else:
            print ('Before %s, you can upload %i MiB without ' +\
                'exceeding your prepaid upload volume.') % (
                nextbill, up.total_max - up.total)
        print ''

    def _print_daily(self):
        if not self.output.silent:
            print 'Daily statistics:'
            print '-----------------'
        print '   Day   | Download |  Upload'
        if self.output.dailybars:
            for day in self.usage.chart:
                print '%s | %8s | %8s  [%s|%s]' % (
                    day.date.strftime('%d/%m/%y'),
                    day.down, day.up,
                    self._print_daybar(day.down),
                    self._print_daybar(day.up))
        else:
            for day in self.usage.chart:
                print '%s | %8s | %8s' % (
                    day.date.strftime('%d/%m/%y'), day.down, day.up)
        print ''

    def _print_daybar(self, mib):
        return '=' * int(round(mib / 50.0))
