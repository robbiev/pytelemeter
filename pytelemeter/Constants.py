#!/usr/bin/env python
#
# pytelemeter library 
# Fetches some statistics from the "Mijn Telenet" page.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

URL_LOGIN = "https://www.telenet.be/sys/sso/signon.jsp"
URL_MAIN = "https://services.telenet.be/isps/MainServlet"
URL_OVERVIEW = "https://services.telenet.be/isps/be/telenet/ebiz/ium/Histogram.jsp"

REGEX_COOKIE = "([A-Z]+=[^;]+;)"
REGEX_COOKIE_SSOSID = "SSOSID=([^;]+);"
REGEX_FAILURE = "Authenticatie niet gelukt"

REGEX_OVERVIEW_TOTALUSED = "(?s)<(?:TD class=\"header\" align=\"right\"*)>(.*?) MB</TD>"
REGEX_OVERVIEW_DAYS = "<TR>[^<]+<TD class=\"(?:odd|even)\">[^0-9]+([0-9]{2}/[0-9]{2}/[0-9]{2})[^<]+</TD>[^<]+<TD class=\"(?:odd|even)\" align=\"right\">[^0-9]+([0-9]+)[^<]+</TD>[^<]+<TD class=\"(?:odd|even)\" align=\"right\">[^0-9]+([0-9]+)[^<]+</TD>[^<]+</TR>"
REGEX_MAIN_USED = "<b>([0-9]+)%</b><br>"

REGEX_MAIN_MAX = "Het toegelaten totaal volume op jouw product is[^<]+<b>[ ]*([0-9]+)[ ]*GB</b> per 30 dagen, waarvan[^<]+<b>[ ]*([,0-9]+)[ ]*GB</b> upstream"
REGEX_MAIN_DATEBROAD = "Door overschrijding van uw toegelaten volume werd de snelheid van uw modem beperkt. Uw snelheid wordt automatisch hersteld op<b>\n[\t]+([0-9]{2}/[0-9]{2}/[0-9]{4})"

if __name__ == "__main__":
	fatalError("Don't run this as a program, this is a module.")
