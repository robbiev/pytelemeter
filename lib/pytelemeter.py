#!/usr/bin/env python
#
# Geeft download en upload statistieken van de Mijn Telenet pagina.
# door Robbie Vanbrabant <robbie.vanbrabant@pandora.be>
# en Thomas Matthijs <knu@keanu.be>  ;-)

import sys
import ClientCookie
import ConfigParser
import os
import re

#gettext
import gettext
t = gettext.translation('pytelemeter', '/usr/share/locale')
_ = t.ugettext

VERSION = "0.8"

# configuratiebestand
configfile = os.environ['HOME'] + "/.pytelemeterrc"


URL_FIRST = "https://www.telenet.be/sys/sso/exec_login.php"
URL_FIRST_DATA = "uid=%s&pwd=%s&goto=http%%3A%%2F%%2Fwww.telenet.be"
URL_MAIN = "https://www.telenet.be/sys/sso/jump.php?https://services.telenet.be/isps/MainServlet?ACTION=TELEMTR&SSOSID=%s"
URL_OVERVIEW = "https://services.telenet.be/isps/be/telenet/ebiz/ium/Histogram.jsp" 


REGEX_FIRST_SSOSID = "<!-- SSOSID => ([^ ]+) -->"


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
		
	def fetch(self):
		if (self.username == "" or self.password == ""):
			self.checkConfig()
			self.getConfig()
		# "Fetching information" in nederlands? kan op niets beter komen :p
		sys.stdout.write(_("Information aan het grijpen... "))
		sys.stdout.flush()
		 
		# lets get a cookie first, so hungry
		htmlFirst = self.getHtml(URL_FIRST, URL_FIRST_DATA % (self.username, self.password))
		# we also need the SSOSID  from that page
		ssosid = re.search(REGEX_FIRST_SSOSID, htmlFirst).group(1)
		# get the main page
		self.htmlMain = self.getHtml(URL_MAIN % ssosid)
		# get the overview page
		self.htmlOverview = self.getHtml(URL_OVERVIEW)
		
		print _("done!\n")
		
	def checkConfig(self):
		if os.path.isfile(configfile):
			mode = os.stat(configfile).st_mode
			if oct(mode & 0777) <> oct(0600 & 0777):
				fatalError(	_("\nHet configuratiebestand MOET chmod 0600 staan om veiligheidsredenen\n") +
						_("Huidige permissies: ") + oct(mode & 0777) +  "\n" +
						_("\nVoer bijvoorbeeld uit: chmod 600 ~/.pytelemeterrc\n"))
		else:
			fatalError(_("\nHet configuratiebestand is niet gevonden\n"))

	def getConfig(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(configfile)
			self.username = config.get("user", "user")
			self.password = config.get("user", "passwd")
		except ConfigParser.NoSectionError:
			fatalError(_("\nKijk of de nodige secties bestaan in het configuratiebestand.\n"))
		except ConfigParser.DuplicateSectionError:
			fatalError(_("\nTwee dezelfde configuratiesecties gevonden\n"))
		except ConfigParser.NoOptionError:
			fatalError(_("\nNiet voldoende configuratieopties gevonden\n"))
		except ConfigParser.MissingSectionHeaderError:
			fatalError(_("\nGeen configuratiesecties in het bestand\n"))
		except ConfigParser.ParsingError:
			fatalError(_("\nKan configbestand niet parsen\n"))
		except:
			fatalError(_("\nUnexpected error:") + sys.exc_info()[0])
			#If no expressions are present, raise re-raises the last expression that was active in the current scope
			#allowing a caller to handle the exception as well
			raise
		if (self.username == 'foo' or self.password == 'bar'):
			fatalError(_("\nEditeer het configuratiebestand eerst!\n"))

	def getHtml(self, url, data=""):
		try:
			if data != "":
				page = ClientCookie.urlopen(url, data)
			else: 
				page = ClientCookie.urlopen(url)
		except IOError, e:
			fatalError(_("Fout bij het openen van de Telemeter pagina: %s") %e)

		return page.read()

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
			return _("Niet over limiet")

if __name__ == "__main__":
	fatalError(_("Run dit niet rechtstreeks"))
