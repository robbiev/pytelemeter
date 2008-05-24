"""
    pytelemeter
    Fetch bandwidth usage statistics from the Belgian ISP Telenet
"""

__version__ = "1.4.99beta1"
__all__ = ['__version__', 'Telemeter', 'TelemeterOutput']

import os
import config
from parser import *
from output import *

# constants
DEFAULT_CONFIGFILE = os.path.join(os.environ['HOME'], '.pytelemeterrc')

class Telemeter:
    """ the public pytelemeter interface """
    def __init__(self, output=None, configfile=None, account=None):
        if not output:
            output = TelemeterOutput()
        self.output = output
        self.usage = None
        if not configfile:
            configfile = DEFAULT_CONFIGFILE
        self.account = account
        self.config = config.ConfigFile(configfile)
        self.configerror = None
        try:
            self.config.read(account)
        except config.ConfigError, e:
            self.configerror = str(e)
        # guess provider
        self.parsers = self.config.account.parsers()

    def fetch(self):
        self.usage = None
        if self.configerror:
            raise AuthenticationError, self.configerror
        elif not self.config.account.username or not self.config.account.password:
            raise AuthenticationError, 'login or password empty'
        self.output.before_fetch()
        last = Exception('no parsers could be initialized')
        for parser in self.parsers:
            try:
                self.usage = parser.fetch(self.config.account)
                self.output.after_fetch(self.usage, parser.was_cached())
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

    def clear_error(self):
        self.configerror = None
