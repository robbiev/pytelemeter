#!/usr/bin/env python
#
# pytelemeter library 
# Fetches some statistics from the "Mijn Telenet" page.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

import sys
import os
import re
import urllib
import urllib2
import Constants
from ConfigHandler import ConfigHandler
from GlobalFunctions import fatalError
from httplib import HTTPConnection

class Telemeter:
	def __init__(self,debug="false"):
		if debug == "true":
			# verbose debug
			#import httplib
			HTTPConnection.debuglevel = 1  

		config = ConfigHandler()
		config.checkConfig()
		config.getConfig()
		self.username = config.username 
		self.password = config.password 

		self.htmlMain = ""
		self.htmlOverview = ""

		self.cookie = ""
		self.jsessionid = ""
	
	def fetch(self,silent=0):
		if (self.username == "" or self.password == ""):
			self.checkConfig()
			self.getConfig()
                if silent == 0:
                    sys.stdout.write("Fetching information... ")
                    sys.stdout.flush()
#		try:		 
		self.getCookie()
		self.htmlMain = self.getMainHtml()
	
		self.htmlOverview = self.getOverviewHtml()
                
		if silent == 0:
	    		sys.stdout.write("done!\n")
#		except:
#			fatalError("\nUnexpected error! Maybe username and/or password incorrect?")

	def getCookie(self):
		try:
			resp = urllib.URLopener().open(Constants.URL_LOGIN,urllib.urlencode({'goto': 'http://www.telenet.be/mijntelenet/index.php?content=https%3A%2F%2Fwww.telenet.be%2Fsys%2Fsso%2Fjump.php%3Fhttps%3A%2F%2Fservices.telenet.be%2Fisps%2FMainServlet%3FACTION%3DTELEMTR%26SSOSID%3D%24SSOSID%24','alt': '/mijntelenet/login.php','uid': self.username,'pwd': self.password}))
		
			cook =  re.findall(Constants.REGEX_COOKIE,resp.info()["Set-Cookie"])
			for i in cook:
                                self.cookie += i + " "

		except IOError, values:
			for i in values:
				print i
				
				#match = re.search(Constants.REGEX_ERROR,i)
				#if match:
				#	fatalError("\nUnexpected error: " + match.group(1))
			#if not match:
			#	fatalError("\nUnexpected error while fetching cookie")
	def getMainHtml(self):
		req = urllib2.Request(Constants.URL_MAIN)
		req.add_header("Cookie",self.cookie)
		ssosid = re.search(Constants.REGEX_COOKIE_SSOSID,self.cookie).group(1)
		page = urllib2.urlopen(req,urllib.urlencode({'ACTION': 'TELEMTR','SSOSID': ssosid}))
		# there is a jsessionid sent, catch it for the overview
		self.jsessionid = re.search(Constants.REGEX_COOKIE,page.info()["Set-Cookie"]).group(1)
		return page.read()

	def getOverviewHtml(self):
		req = urllib2.Request(Constants.URL_OVERVIEW)
		req.add_header("Cookie",self.jsessionid)
		page = urllib2.urlopen(req)
		return page.read()

	def getVolumeUsed(self, procent):
		if (procent == 1):
	 		total = int(re.findall(Constants.REGEX_MAIN_USED, self.htmlMain)[0])
			upload = int(re.findall(Constants.REGEX_MAIN_USED, self.htmlMain)[1])
		else:
			match = re.findall(Constants.REGEX_OVERVIEW_TOTALUSED, self.htmlOverview)
			total = int(match[0])
			upload = int(match[1])
		return total, upload
	
	def getOverview(self):
		# Overview
		return re.findall(Constants.REGEX_OVERVIEW_DAYS, self.htmlOverview)
	
	def getVolumeMax(self):
		# allowed volume
		volumeMax = re.search(Constants.REGEX_MAIN_MAX, self.htmlMain)
		totalMax = int(volumeMax.group(1))
		uploadMax = float(volumeMax.group(2).replace(",", "."))
		return totalMax, uploadMax

	def getDateBroad(self):
		# date you return to broadband
		date = re.search(Constants.REGEX_MAIN_DATEBROAD, self.htmlMain)
		if date:
			return date.group(1)
		else:
			return "Within volume limits"

if __name__ == "__main__":
	fatalError("Don't run this as a program, this is a module.")
