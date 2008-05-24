"""
    pytelemeter GTK graphical user interface
"""

import pygtk
try:
    pygtk.require('2.0')
except AssertionError:
    pass
import gtk
import gtk.glade
import sys
import os
from __init__ import *
from parser import *

# constants
ICON = '/usr/share/pixmaps/pytele_small.png'
GLADE = '/usr/share/pytelemeter/pytelemeter.glade'

# exceptions
class GladeFileNotFound(IOError): pass

# interfaces
class UpdateListener:
    def update(self):
        # should clear error messages
        raise NotImplementedError
    def error(self, msg):
        raise NotImplementedError


class TelemeterGUI:
    def __init__(self, meter=None, trayMode=False, listener=None):
        # backend
        if not meter:
            meter = Telemeter()
        self.meter = meter

        # tray mode
        self.trayMode = trayMode
        self.listener = listener

        # the gui
        self.xml = gtk.glade.XML(GLADE)
        self.xml.signal_autoconnect(self)

        # history table
        tv = self.xml.get_widget('history_treeview')
        self.history = gtk.ListStore(str, int, int)
        tms = gtk.TreeModelSort(self.history)
        tms.set_sort_column_id(0, gtk.SORT_DESCENDING)
        tv.set_model(tms)
        tv.set_model(self.history)
        columns = ['Day', 'Download', 'Upload']
        for i in range(3):
            col = gtk.TreeViewColumn(columns[i])
            cell = gtk.CellRendererText()
            col.pack_start(cell, True)
            col.add_attribute(cell, 'text', i)
            col.set_sort_column_id(i)
            tv.append_column(col)

        # main window
        self.window = self.xml.get_widget('main_window')
        self.window.set_title('pytelemeter v%s' % __version__)
        self.window.set_icon_from_file(ICON)

        self.update()

    def refresh(self):
        try:
            self.meter.fetch()
        except AuthenticationError, e:
            self.ask_credentials(e)
        except ParserError, e:
            self.error(str(e))
        self.update()
        if self.listener:
            self.listener.update()

    def ask_credentials(self, error=None):
        # -1 refers to the last page (config)
        self.xml.get_widget('main_notebook').set_current_page(-1)
        if error:
            s = str(error)
        else:
            s = 'please enter your Telenet username and password'
        self._set_errormsg(s)

    def error(self, msg):
        self._set_errormsg('Error: %s' % msg)

    def _set_errormsg(self, msg):
        for name in ('volume', 'config'):
            self.xml.get_widget('%s_errormsg' % name).set_text(msg)

    def update(self):
        "read the latest data from the telemeter"
        if not self.meter.usage:
            return
        usage = self.meter.usage
        dbar = self.xml.get_widget('download_progressbar')
        ubar = self.xml.get_widget('upload_progressbar')
        if usage.totals.has_key('down'):
            dbar.set_fraction(usage.down.float)
            dbar.set_text(str(usage.down.pct) + '%')
            ubar.set_fraction(usage.up.float)
            ubar.set_text(str(usage.up.pct) + '%')
        else:
            dbar.set_fraction(usage.sum.float)
            dbar.set_text(str(usage.sum.pct) + '%')
            ubar.hide()
            self.xml.get_widget('download_label').set_text('Transfer')
            self.xml.get_widget('upload_label').hide()
        scale = self.xml.get_widget('daysleft_scale')
        scale.set_value(usage.daysleft)
        self.history.clear()
        for day in usage.chart:
            datestring = day.date.strftime('%Y/%m/%d')
            if day.values.has_key('down'):
                self.history.prepend([datestring, day.down, day.up])
            else:
                self.history.prepend([datestring, day.sum, 0])
        uentry = self.xml.get_widget('username_entry')
        uentry.set_text(self.meter.config.account.username)
        pentry = self.xml.get_widget('password_entry')
        pentry.set_text('')
        self._set_errormsg('')

    def show(self):
        self.window.present()
    def showhide(self):
        if self.window.is_active():
            self.window.hide()
        else:
            self.window.present()

    def pass_credentials(self):
        username = self.xml.get_widget('username_entry').get_text()
        password = self.xml.get_widget('password_entry').get_text()
        if username != '' and password != '':
            self.meter.config.account = Account(username, password)
            self.meter.clear_cache()
            self.meter.clear_error()

# handlers
    def on_refresh_button_clicked(self, button=None, data=None):
        self.pass_credentials()
        self.refresh()

    def on_save_button_clicked(self, button=None, data=None):
        self.pass_credentials()
        self.meter.config.save()

    def on_close_button_clicked(self, button=None, data=None):
        if self.trayMode:
            self.window.hide()
        else:
            self.window.destroy()

    def on_main_window_delete_event(self, event=None, window=None,
                                    data=None):
        if self.trayMode:
            self.window.hide()
            return True

    def on_main_window_destroy(self, window=None):
        gtk.main_quit()
