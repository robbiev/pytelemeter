#!/usr/bin/env python
#
# Geeft download en upload statistieken van de Mijn Telenet pagina.
# door Robbie Vanbrabant <robbie.vanbrabant@pandora.be>
# alot of changes by Thomas M <knu@keanu.be>  ;-)

import sys
import ClientCookie
import ConfigParser
import os
import re

VERSION = "0.8"

# configuratiebestand
configfile = os.environ['HOME'] + "/.pytelemeterrc"

def fatalError(errormsg):
	print errormsg
	sys.exit(1)


def checkConfig():
	if os.path.isfile(configfile):
		mode = os.stat(configfile).st_mode
        	if oct(mode & 0777) <> oct(0600 & 0777):
			fatalError(	"\nHet configuratiebestand MOET chmod 0600 staan om veiligheidsredenen\n" +
					"Huidige permissies: " + oct(mode & 0777) +  "\n" +
					"\nVoer bijvoorbeeld uit: chmod 600 ~/.pytelemeterrc\n")
	else:
		fatalError("\nHet configuratiebestand is niet gevonden\n")

def getConfig():
	global user
	global passwd
	try:
		config = ConfigParser.ConfigParser()
		config.read(configfile)
		user= config.get("user","user")
		passwd= config.get("user","passwd")
	except ConfigParser.NoSectionError:
		fatalError("\nKijk of de nodige secties bestaan in het configuratiebestand.\n")
	except ConfigParser.DuplicateSectionError:
		fatalErro("\nTwee dezelfde configuratiesecties gevonden\n")
	except ConfigParser.NoOptionError:
		fatalErro("\nNiet voldoende configuratieopties gevonden\n")
	except ConfigParser.MissingSectionHeaderError:
		fatalError("\nGeen configuratiesecties in het bestand\n")
	except ConfigParser.ParsingError:
		fatalError("\nKan configbestand niet parsen\n")
	except:
		fatalError("\nUnexpected error:", sys.exc_info()[0])
		#wat doet raise?
		#If no expressions are present, raise re-raises the last expression that was active in the current scope
		#allowing a caller to handle the exception as well
		raise
	if user == 'foo' or passwd == 'bar':
		fatalError("\nEditeer het configuratiebestand eerst!\n")

#def setDebug():
	# TODO: minder lelijk uitwerken
	#print "Python %s" % sys.version[0:5]
	#print "ClientCookie %s\n" % ClientCookie.VERSION

	# debug mode
	#hh = ClientCookie.HTTPHandler()
	#sh = ClientCookie.HTTPSHandler()
	#for h in [hh, sh]:
	#    h.set_http_debuglevel(1)
	#ClientCookie.install_opener(ClientCookie.build_opener(hh, sh))

def getInfo():
	global htmlMain
	global htmlOverzicht
	cookieUrl = "https://www.telenet.be/sys/sso/exec_login.php"
	goto = "http%3A%2F%2Fwww.telenet.be"

	# openen van telenet website voor het verkrijgen van een sessie id
	try:
		data = "uid=" + user + "&pwd=" + passwd + "&goto=" + goto
		r = ClientCookie.urlopen(cookieUrl, data)
		output = r.read()
	except IOError, e:
		fatalError("Fout bij het verkrijgen van een SSOSID: %s" %e)
        
	# het SSOSID 
        SSOSID = re.search("<!-- SSOSID => ([^ ]+) -->",output).group(1)
	
	# telemeter pagina openen
	try:
		meterurl = 'https://www.telenet.be/sys/sso/jump.php?https://services.telenet.be/isps/MainServlet?ACTION=TELEMTR&SSOSID=' + SSOSID
		pagina = ClientCookie.urlopen(meterurl)
		htmlMain = pagina.read()
	except IOError, e:
		fatalError("Fout bij het openen van de Telemeter pagina: %s" %e)

	# gedetailleerde info opvragen
	try:
		detail = ClientCookie.urlopen("https://services.telenet.be/isps/be/telenet/ebiz/ium/Histogram.jsp")
		htmlOverzicht = detail.read()
	except IOError, e:
		fatalError("Fout bij het openen van de dagoverzicht pagina: %s" %e)
		
def getVolumeUsed():
	#Totaal verbruikt,upload verbuikt in MiB
	regex = re.compile(r'<(?:TD class="header" align="right"*)>(.*?) MB</TD>', re.M)
	match = regex.findall(htmlOverzicht)

	totmb = int(match[0])
	upmb = int(match[1])
	return totmb,upmb
	
def getOverzicht():
	# Overzicht
	dagOverzicht = re.findall('<TR>[^<]+<TD class="(?:odd|even)">[^0-9]+([0-9]{2}/[0-9]{2}/[0-9]{2})[^<]+</TD>[^<]+<TD class="(?:odd|even)" align="right">[^0-9]+([0-9]+)[^<]+</TD>[^<]+<TD class="(?:odd|even)" align="right">[^0-9]+([0-9]+)[^<]+</TD>[^<]+</TR>',htmlOverzicht)
	return dagOverzicht
	
def getVolumeUsedProcent():
	# % verbruikt
 	volumeTotaal = re.search('Totaal verbruikt volume \(downstream \+ upstream\)</a>[^<]+<b>([0-9]+)%</b><br>',htmlMain).group(1)
	volumeUpload = re.search('Upstream verbruikt volume\</a>[^<]+<b>([0-9]+)%</b><br>',htmlMain).group(1)
	return int(volumeTotaal),int(volumeUpload)
	
def getMaxVolume():
	# zoek maximum volume dat toegestaan is
	# deze regex werkt voor mij, zou bij iedereen moeten werken, maar staat paar rare spacies in, die van plaats en aantal bljiken te verandere soms,daarom een aantal [ ]*
	volumeMax = re.search('Het toegelaten totaal volume op jouw product is[^<]+<b>[ ]*([0-9]+)[ ]*GB</b> per 30 dagen, waarvan[^<]+<b>[ ]*([,0-9]+)[ ]*GB</b> upstream',htmlMain)
	volumeDownMax = int(volumeMax.group(1))
	volumeUpMax = float(volumeMax.group(2).replace(",","."))
	return volumeDownMax,volumeUpMax

def getDatumTerugBreedband():
	#datum dat je terug op breedband komt
	terugBreed = re.search('Door overschrijding van uw toegelaten volume werd de snelheid van uw modem beperkt. Uw snelheid wordt automatisch hersteld op <b>[^0-9]+([0-9]{2}/[0-9]{2}/[0-9]{4})[^<]+</b>',htmlMain)
	if terugBreed:
		return terugBreed.group(1)
	else:
		return "Not Found"

def main():
	checkConfig()
	getConfig()
	#setDebug()
	getInfo()

if __name__ == "__main__":
	main()
	sys.exit(0)
