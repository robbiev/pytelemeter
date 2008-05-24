"""
    pytelemeter config file handler
"""

import os
import sys
import ConfigParser
from parser import Account

# exceptions
class ConfigError(Exception): pass
class MissingConfigFile(ConfigError): pass
class MalformedConfigFile(ConfigError): pass
class StockCredentials(ConfigError): pass
class NoSuchAccount(ConfigError): pass


class ConfigFile:
    def __init__(self, location):
        if not location:
            location = DEFAULT_LOCATION
        self.location = location
        if not os.path.isfile(self.location):
            print >> sys.stderr, ('Warning: configuration file not '
                'found, this may be fatal later on')

    def read(self, account=None):
        if not os.path.isfile(self.location):
            raise MissingConfigFile, ('unable to find config file, '
                'please supply your username and password')
        if os.stat(self.location).st_mode & 0777 != 0600:
            print >> sys.stderr, ('Warning: changing possibly '
                'insecure configuration file permissions')
            os.chmod(self.location, 0600)
        try:
            config = self._get_config()
            sections = config.sections()

            if account:
                if account in sections:
                    id = account
                else:
                    raise NoSuchAccount, ('unable to find the '
                        'specified account in the config file')
            else:
                if 'default' in sections:
                    id = 'default'
                elif 'user' in sections:
                    id = 'user'
                elif len(sections):
                    id = sections[0]
                else:
                    raise MalformedConfigFile, ('no accounts specified '
                        'in the configuration file')

            try:
                username = config.get(id, 'user')
            except ConfigParser.NoOptionError:
                username = config.get(id, 'username')
            try:
                password = config.get(id, 'passwd')
            except ConfigParser.NoOptionError:
                password = config.get(id, 'password')
            try:
                provider = config.get(id, 'provider')
            except ConfigParser.NoOptionError:
                provider = None     # will use default = telenet

            self.account = Account(id, username, password, provider)
        except ConfigParser.Error:
            raise MalformedConfigFile, 'error parsing config file'

    def check(self):
        a = self.account
        if (a.username == 'foo' or a.password == 'bar'):
            raise StockCredentials, ('detected the example config '
                'file, please supply your username and password')

    def save(self, account='user'):
        config = self._get_config(false)
        config.remove_section(account)
        config.add_section(account)
        config.set(account, 'username', self.account.username)
        config.set(account, 'password', self.account.password)
        config.set(account, 'provider', self.account.provider)
        self._save_config(config)

    def delete(self, account):
        config = self._get_config()
        config.remove_section(account)
        self._save_config(config)

    def _get_config(self, fail=True):
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.location)
        except ConfigParser.Error:
            if fail:
                raise
            else:
                pass
        return config

    def _save_config(self, config):
        file = open(self.location, 'w')
        config.write(file)
        file.close()
        os.chmod(self.location, 0600)

