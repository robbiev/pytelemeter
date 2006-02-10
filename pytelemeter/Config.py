# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter config file handler
"""

import os
import sys
import ConfigParser

# constants
CONFIGFILE = os.path.join(os.environ['HOME'], '.pytelemeterrc')

# exceptions
class Error(Exception): pass
class MissingConfigFile(Error): pass
class MalformedConfigFile(Error): pass
class StockCredentials(Error): pass


class ConfigFile:
    def __init__(self):
        if not os.path.isfile(CONFIGFILE):
            print >> sys.stderr, 'Warning: configuration file not ' +\
                'found, this may be fatal later on'

    def read(self):
        if not os.path.isfile(CONFIGFILE):
            raise MissingConfigFile, 'unable to find config file, ' +\
                'please supply your Telenet username and password'
        if os.stat(CONFIGFILE).st_mode & 0777 != 0600:
            print >> sys.stderr, 'Warning: changing possibly ' +\
                'insecure configuration file permissions'
            os.chmod(CONFIGFILE, 0600)
        try:
            config = ConfigParser.ConfigParser()
            config.read(CONFIGFILE)
            self.username = config.get('user', 'user')
            self.password = config.get('user', 'passwd')
        except ConfigParser.Error:
            raise MalformedConfigFile, 'error parsing config file'
        if (self.username == 'foo' or self.password == 'bar'):
            raise StockCredentials, 'detected the example config ' +\
                'file, please supply your Telenet username and password'
        return self.username, self.password

    def save(self):
        config = ConfigParser.ConfigParser()
        try:
            config.read(CONFIGFILE)
        except ConfigParser.Error:
            pass
        config.remove_section('user')
        config.add_section('user')
        config.set('user', 'user', self.username)
        config.set('user', 'passwd', self.password)
        file = open(CONFIGFILE, 'w')
        config.write(file)
        file.close()
        os.chmod(CONFIGFILE, 0600)
