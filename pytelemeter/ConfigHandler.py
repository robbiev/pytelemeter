#!/usr/bin/env python
#
# pytelemeter library 
# Fetches some statistics from the "Mijn Telenet" page.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

import ConfigParser
import os
from GlobalFunctions import fatalError

# config file
configfile = os.environ['HOME'] + "/.pytelemeterrc"

class ConfigHandler:
	def __init__(self):
		self.username = ""
		self.password = ""
	
	def checkConfig(self):
		if os.path.isfile(configfile):
			mode = os.stat(configfile).st_mode
			if oct(mode & 0777) <> oct(0600 & 0777):
				fatalError(	"\nConfiguration file needs to be chmod 0600 for security reasons.\n" +
						"Current permissions: " + oct(mode & 0777) +  "\n" +
						"\nTry this: chmod 600 ~/.pytelemeterrc\n")
		else:
			fatalError("\nConfiguration file not found.\n")

	def getConfig(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(configfile)
			self.username = config.get("user", "user")
			self.password = config.get("user", "passwd")
		except ConfigParser.NoSectionError:
			fatalError("\nCheck if the sections needed exist in the config file.\n")
		except ConfigParser.DuplicateSectionError:
			fatalError("\nFound sections that are the same in the config file. Only create one entry/section.\n")
		except ConfigParser.NoOptionError:
			fatalError("\nNot eneough sections found in config file\n")
		except ConfigParser.MissingSectionHeaderError:
			fatalError("\nNo sections found in config file.\n")
		except ConfigParser.ParsingError:
			fatalError("\nError parsing config file\n")
		except:
			fatalError("\nUnexpected error:" + str(sys.exc_info()[0]))
			#If no expressions are present, raise re-raises the last expression that was active in the current scope
			#allowing a caller to handle the exception as well
			raise
		if (self.username == 'foo' or self.password == 'bar'):
			fatalError("\nEdit the configuration file first!\n")

	def setConfig(self,user,passwd):
		try:
			config = ConfigParser.ConfigParser()
			#config.read(configfile)
			config.add_section("user")
			config.set("user","user",user)
			config.set("user","passwd",passwd)
			file = open(configfile, 'w') 
			config.write(file)
			file.close()		
              	except ConfigParser.NoSectionError:
        	        fatalError("\nCheck if the sections needed exist in the config file.\n")
		except ConfigParser.NoOptionError:
                        fatalError("\nNot eneough sections found in config file\n")
                except ConfigParser.MissingSectionHeaderError:
                        fatalError("\nNo sections found in config file.\n")
                except ConfigParser.ParsingError:
                        fatalError("\nError parsing config file\n")
                except: 
                        fatalError("\nUnexpected error:" + str(sys.exc_info()[0]))
                        #If no expressions are present, raise re-raises the last expression that was active in the current scope
                        #allowing a caller to handle the exception as well
                        raise

if __name__ == "__main__":
	fatalError("Don't run this as a program, this is a module.")
