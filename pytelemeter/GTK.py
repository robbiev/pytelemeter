#!/usr/bin/python
#
# pytelemeter GTK library 
# Contains code for the GTK frontend. 
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

# Perhaps some of these are already loaded, ignore those errors
try:
	import pygtk
	pygtk.require('2.0')
except ImportError:
	pass
except AssertionError:
	pass
try:
	import gtk
except ImportError:
        pass
except AssertionError:
        pass


from pytelemeter.Telemeter import Telemeter
from pytelemeter import VERSION
from pytelemeter.GlobalFunctions import fatalError
from pytelemeter.ConfigHandler import ConfigHandler
import sys,string,datetime,time,random

class PyTeleGui:
	def fillInfo(self, widget, fetchAgain=1, externalMeter=None):
		if self.meter == None:
			if externalMeter == None:
				self.meter = Telemeter()
				print "eigen meter"
			else:
				self.meter = externalMeter
				print "andere meter"
		if str(self.eu.get_text()) != "" and str(self.ep.get_text()) != "":
                        self.meter.username = self.eu.get_text()
                        self.meter.password = self.ep.get_text()
                        self.config.setConfig(str(self.eu.get_text()),str(self.ep.get_text()))
		#try:
		if fetchAgain == 1:
			print "fetcheu"
			self.meter.fetch()
		a,b = self.meter.getVolumeUsed(1)
		dval = float(int(a))/100
	       	uval = float(int(b))/100
       		self.dbar.set_fraction(dval)
        	self.ubar.set_fraction(uval)
        	self.dbar.set_text(str(a) + "%")
        	self.ubar.set_text(str(b) + "%")
		#self.window.show()
        	overview = self.meter.getOverview()
	        self.liststore.clear()
                for date,total,upload in overview:
               	        self.add_row(date,total,upload)
               
               	self.eu.set_text(self.meter.username)
               	self.ep.set_text(self.meter.password)

		#except:
		#	fatalError("Parent error: exiting...")
	def add_row(self, date, total, upload):
	        rand = self.rand

	        myDate = string.split(date,"/")
	        finalDate = "20" + myDate[2] + "/" + myDate[1] + "/" + myDate[0]
	        i0 = self.frameDaily.sm.get_model().append([finalDate,int(total),int(upload)])
        	sel = self.frameDaily.tv.get_selection()
        	i1 = self.frameDaily.sm.convert_child_iter_to_iter(None, i0)
        	sel.select_iter(i1)

	def show(self):
		#self.__init__(self.trayMode)
		self.window.show_all()

	def hide(self):
		self.window.hide()

	def delete_event(self, widget, event, data=None):
        	if self.trayMode == 1:
			self.window.hide()
		else:
			gtk.main_quit()
        		return gtk.FALSE

	def __init__(self, trayMode=0):
		self.trayMode = trayMode

		self.meter = None
		self.config = ConfigHandler()

		# Create a new window
        	self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(gtk.FALSE)
        	self.window.set_position(gtk.WIN_POS_CENTER)
		# Set the window title
        	self.window.set_title("pytelemeter v" + VERSION)

                pixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/pixmaps/pytele.png")
                scaled_buf = pixbuf.scale_simple(16,16,gtk.gdk.INTERP_BILINEAR)

		gtk.window_set_default_icon_list(scaled_buf)

        	# Set a handler for delete_event that immediately
        	# exits GTK.
        	self.window.connect("delete_event", self.delete_event)

        	# Sets the border width of the window.
        	self.window.set_border_width(5)
		self.window.set_size_request(-1,350)
        	vbox = gtk.VBox(homogeneous=gtk.FALSE, spacing=0)
		vbox.show()
		self.window.add(vbox)

        	# Create a new notebook, place the position of the tabs
        	notebook = gtk.Notebook()
        	notebook.set_tab_pos(gtk.POS_TOP)
        	vbox.pack_start(notebook, expand=gtk.TRUE, fill=gtk.TRUE, padding=0)
		notebook.show()
        	self.show_tabs = gtk.TRUE

        	# Let's append a bunch of pages to the notebook
        	bufferf = "Volume used"
        	bufferl = "Volume"
        	frameVolume = gtk.Frame(bufferf) #gtk.AspectFrame(label=bufferf, xalign=0.5, yalign=0.5, ratio=1.0, obey_child=gtk.TRUE)
        	frameVolume.set_border_width(20)
        	frameVolume.show()
        	label = gtk.Label(bufferl)

		# op deze tabpage voegen we de volume info toe	
                tableVolume = gtk.Table(2, 2, gtk.FALSE)

                # Put the table in the frame 
                frameVolume.add(tableVolume)

                labeld = gtk.Label("Download")
                labelu = gtk.Label("Upload")
                tableVolume.attach(labeld, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                labeld.show()
                tableVolume.attach(labelu, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=5, ypadding=5)
                labelu.show()

                # progress bars
                self.dbar = gtk.ProgressBar()
                tableVolume.attach(self.dbar, 1, 2, 0, 1,xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                self.dbar.show()

                self.ubar = gtk.ProgressBar()
                tableVolume.attach(self.ubar, 1, 2, 1, 2,xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                self.ubar.show()

                tableVolume.show()

        	notebook.append_page(frameVolume, label)

        	bufferf = "Daily statistics"
        	bufferl = "Daily history"
        	self.frameDaily = gtk.Frame(bufferf) #gtk.AspectFrame(label=bufferf, xalign=0.5, yalign=0.5, ratio=1.0, obey_child=gtk.TRUE)
        	self.frameDaily.set_border_width(20)
        	self.frameDaily.set_size_request(100, 75)
		self.frameDaily.show()
		label = gtk.Label(bufferl)
        	

	        # create a liststore with three int columns
	        self.liststore = gtk.ListStore(str, int, int)
	
	        # create a random number generator
	        self.rand = random.Random()
	        
		win = self.frameDaily
		win.tablehold = gtk.Table(0,0,gtk.FALSE)
		win.vboxDaily = gtk.VBox()
	        win.add(win.vboxDaily)
     		win.sw = gtk.ScrolledWindow()
        	win.sm = gtk.TreeModelSort(self.liststore)
        	# Set sort column
        	win.sm.set_sort_column_id(0, gtk.SORT_DESCENDING)
        	win.tv = gtk.TreeView(win.sm)
        	win.vboxDaily.pack_start(win.sw, padding=10)
		win.sw.add(win.tv)
        	win.tv.column = [None]*3
        	win.tv.column[0] = gtk.TreeViewColumn('Day')
        	win.tv.column[1] = gtk.TreeViewColumn('Total (MiB)')
        	win.tv.column[2] = gtk.TreeViewColumn('Upload (MiB)')
        	win.tv.cell = [None]*3
        	for i in range(3):
        	    win.tv.cell[i] = gtk.CellRendererText()
        	    win.tv.append_column(win.tv.column[i])
        	    win.tv.column[i].set_sort_column_id(i)
        	    win.tv.column[i].pack_start(win.tv.cell[i], True)
        	    win.tv.column[i].set_attributes(win.tv.cell[i], text=i)
        	    win.show_all()


		notebook.append_page(self.frameDaily, label)

        	bufferf = "Config"
        	bufferl = "Config"
        	frameConfig = gtk.Frame(bufferf) #gtk.AspectFrame(label=bufferf, xalign=0.5, yalign=0.5, ratio=1.0, obey_child=gtk.TRUE)
        	frameConfig.set_border_width(20)
        	frameConfig.set_size_request(100, 75)
        	frameConfig.show()
        	label = gtk.Label(bufferl)
        	

                # op deze tabpage voegen we de volume info toe  
                tableConfig = gtk.Table(2, 2, gtk.FALSE)

                # Put the table in the frame 
                frameConfig.add(tableConfig)

                labeld = gtk.Label("User")
                labelu = gtk.Label("Password")
                tableConfig.attach(labeld, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                labeld.show()
                tableConfig.attach(labelu, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=5, ypadding=5)
                labelu.show()

                # progress bars
                self.eu = gtk.Entry()
                tableConfig.attach(self.eu, 1, 2, 0, 1,xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                self.eu.show()
	
		self.ep = gtk.Entry()
                tableConfig.attach(self.ep, 1, 2, 1, 2,xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=10)
                self.ep.show()
		self.ep.set_visibility(gtk.FALSE)
		self.eu.set_text("")
		self.ep.set_text("")	


		tableConfig.show()
		notebook.append_page(frameConfig, label)

        	# Set what page to start at (page 1)
        	notebook.set_current_page(0)

        	# Create a bunch of buttons
        	Maintable = gtk.Table(1,2,gtk.FALSE)
		
	        # Button for refresh
                if trayMode == 0:
			button = gtk.Button(stock=gtk.STOCK_REFRESH)
                	button.connect("clicked", lambda w: self.fillInfo(gtk.Button,1,None))
                	Maintable.attach(button, 0, 1 , 0, 1, xpadding=5, ypadding=5)
                	button.show()

		button = gtk.Button(stock=gtk.STOCK_QUIT)
		# gtk.mainquit vs gtk.main_quit
        	# http://www.daa.com.au/pipermail/pygtk/2004-March/007142.html
		
		if self.trayMode == 1:
			button.connect("clicked", lambda w: self.hide())
		else:
			button.connect("clicked", lambda w: gtk.main_quit())
        	
		Maintable.attach(button, 1,2,0,1, xpadding=5, ypadding=5)
       		button.show()
		
		vbox.pack_start(Maintable, expand=gtk.FALSE, fill=gtk.FALSE, padding=0)	

        	Maintable.show()
