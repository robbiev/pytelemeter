#!/usr/bin/env python
#
# pytelemeter library 
# Fetches some statistics from the "Mijn Telenet" page.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

import sys
import ConfigParser
import os
import re
import urllib
import urllib2

VERSION = "0.8"

# config file
configfile = os.environ['HOME'] + "/.pytelemeterrc"

URL_LOGIN = "https://www.telenet.be/sys/sso/exec_login.php"
URL_MAIN = "https://services.telenet.be/isps/MainServlet"
URL_OVERVIEW = "https://services.telenet.be/isps/be/telenet/ebiz/ium/Histogram.jsp"

REGEX_COOKIE = "([A-Z]+=[^;]+;)"
REGEX_COOKIE_SSOSID = "SSOSID=([^;]+);"
REGEX_FAILURE = "Authenticatie niet gelukt"

REGEX_OVERVIEW_TOTALUSED = "(?s)<(?:TD class=\"header\" align=\"right\"*)>(.*?) MB</TD>"
REGEX_OVERVIEW_DAYS = "<TR>[^<]+<TD class=\"(?:odd|even)\">[^0-9]+([0-9]{2}/[0-9]{2}/[0-9]{2})[^<]+</TD>[^<]+<TD class=\"(?:odd|even)\" align=\"right\">[^0-9]+([0-9]+)[^<]+</TD>[^<]+<TD class=\"(?:odd|even)\" align=\"right\">[^0-9]+([0-9]+)[^<]+</TD>[^<]+</TR>"
REGEX_MAIN_USED_TOTAL = "Totaal verbruikt volume \(downstream \+ upstream\)</a>[^<]+<b>([0-9]+)%</b><br>"
REGEX_MAIN_USED_UPLOAD = "Upstream verbruikt volume\</a>[^<]+<b>([0-9]+)%</b><br>"
REGEX_MAIN_MAX = "Het toegelaten totaal volume op jouw product is[^<]+<b>[ ]*([0-9]+)[ ]*GB</b> per 30 dagen, waarvan[^<]+<b>[ ]*([,0-9]+)[ ]*GB</b> upstream"
REGEX_MAIN_DATEBROAD = "Door overschrijding van uw toegelaten volume werd de snelheid van uw modem beperkt. Uw snelheid wordt automatisch hersteld op <b>[^0-9]+([0-9]{2}/[0-9]{2}/[0-9]{4})[^<]+</b>"

def fatalError(errormsg):
	print errormsg
	sys.exit(1)


class Telemeter:
	def __init__(self):
		self.username = ""
		self.password = ""

		self.htmlMain = ""
		self.htmlOverview = ""

		self.cookie = ""
		
	def fetch(self,silent=0):
		if (self.username == "" or self.password == ""):
			self.checkConfig()
			self.getConfig()
                if silent == 0:
                    sys.stdout.write("Fetching information... ")
                    sys.stdout.flush()
		 
		self.getCookie()
		self.htmlMain = self.getMainHtml()
		self.htmlOverview = self.getOverviewHtml()

                if silent == 0:
		    sys.stdout.write("done!\n")
	
	def getCookie(self):
		try:
			urllib.URLopener().open(URL_LOGIN,urllib.urlencode({'goto': 'www.telenet.be','alt': '/mijntelenet/login.php','uid': self.username,'pwd': self.password}))
		except IOError, (ignored,ignored,ignored,headers):
                        #find a better way!
                        if re.search(REGEX_FAILURE,headers["Location"]):
                            fatalError("\nUsername/password combination incorrect.")

			cookies = headers["Set-Cookie"]
			for i in re.findall(REGEX_COOKIE,cookies):
				self.cookie += i + " "

	def getMainHtml(self):
		req = urllib2.Request(URL_MAIN)
		req.add_header("Cookie",self.cookie)
		ssosid = re.search(REGEX_COOKIE_SSOSID,self.cookie).group(1)
		page = urllib2.urlopen(req,urllib.urlencode({'ACTION': 'TELEMTR','SSOSID': ssosid}))
		self.cookie = re.search(REGEX_COOKIE,page.info()["Set-Cookie"]).group(1)
		return page.read()

	def getOverviewHtml(self):
		req = urllib2.Request(URL_OVERVIEW)
		req.add_header("Cookie",self.cookie)
		page = urllib2.urlopen(req)
		return page.read()

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
			fatalError("\nUnexpected error:" + sys.exc_info()[0])
			#If no expressions are present, raise re-raises the last expression that was active in the current scope
			#allowing a caller to handle the exception as well
			raise
		if (self.username == 'foo' or self.password == 'bar'):
			fatalError("\nEdit the configuration file first!\n")

	def getVolumeUsed(self, procent):
		if (procent == 1):
	 		total = int(re.search(REGEX_MAIN_USED_TOTAL, self.htmlMain).group(1))
			upload = int(re.search(REGEX_MAIN_USED_UPLOAD, self.htmlMain).group(1))
		else:
			match = re.findall(REGEX_OVERVIEW_TOTALUSED, self.htmlOverview)

			total = int(match[0])
			upload = int(match[1])
		return total, upload
	
	def getOverview(self):
		# Overview
		return re.findall(REGEX_OVERVIEW_DAYS, self.htmlOverview)
	
	def getVolumeMax(self):
		# allowed volume
		volumeMax = re.search(REGEX_MAIN_MAX, self.htmlMain)
		totalMax = int(volumeMax.group(1))
		uploadMax = float(volumeMax.group(2).replace(",", "."))
		return totalMax, uploadMax

	def getDateBroad(self):
		#date you return to broadband
		date = re.search(REGEX_MAIN_DATEBROAD, self.htmlMain)
		if date:
			return date.group(1)
		else:
			return "Within volume limits"

if __name__ == "__main__":
	fatalError("Don't run this as a program, this is a module.")
