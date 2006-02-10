# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.
"""
    pytelemeter freedesktop.org compliant system tray icon
"""

import pygtk
try:
    pygtk.require('2.0')
except AssertionError:
    pass
import gtk
import egg.trayicon
import pango

from Telemeter import Telemeter
from GTK import *
from Parser import *
from __init__ import VERSION


class TelemeterTray(UpdateListener):
    def __init__(self, meter=None, gui=None):
        if not meter:
            meter = Telemeter()
        self.meter = meter
        self.gui = gui

        self.tray = egg.trayicon.TrayIcon('pytelemeter');

        self.area = gtk.DrawingArea()
        self.area.set_size_request(24,24)
        self.area.connect('expose-event', self.on_expose_event)
        self.area.connect('configure-event', self.on_configure_event)

        eventbox = gtk.EventBox()
        eventbox.connect('button_press_event', self.on_tray_clicked)
        eventbox.add(self.area)
        self.tray.add(eventbox)

        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.tray,'Pytelemeter v%s' % VERSION)

        self.menu = gtk.Menu()

        # Create the menu items
        refresh_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_REFRESH,
                                                    accel_group=None)
        open_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_OPEN,
                                                    accel_group=None)
        quit_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT,
                                                    accel_group=None)
        # Add them to the menu
        self.menu.append(refresh_item)
        self.menu.append(open_item)
        self.menu.append(quit_item)
        # Connect the signals
        refresh_item.connect('activate', lambda x: self.refresh())
        open_item.connect('activate', lambda x: self.showGUI())
        quit_item.connect('activate', gtk.main_quit)

        self.menu.show_all()
        self.tray.show_all()

        self.update()

    def showGUI(self, switch=False):
        if not self.gui:
            self.gui = TelemeterGUI(self.meter, 1, self)
        if switch:
            self.gui.showhide()
        else:
            self.gui.show()

    def refresh(self):
        try:
            self.meter.fetch()
        except AuthenticationError, e:
            self.showGUI()
            self.gui.ask_credentials(e)
        except RemoteServiceError:
            self.error('remote telemeter service failure')
        except ConnectionError:
            self.error('could not connect to telemeter service')
        self.update()
        if self.gui:
            self.gui.update()

    def error(self, msg):
        self.tooltips.set_tip(self.tray, 'Error: %s' % msg)

    def update(self):
        "read the latest data from the telemeter"
        if not self.meter.usage:
            return
        dn = self.meter.usage.down
        up = self.meter.usage.up
        offset = 11 # vertical distance between the 2 bars
        # blank the area
        gc = self.area.get_style().bg_gc[gtk.STATE_NORMAL]
        self.buffer.draw_rectangle(gc, True, 0, 0, 24, 24)
        # draw the outline
        gc = self.area.get_style().black_gc
        self.buffer.draw_rectangle(gc, False, 1, 1, 21, 9)
        self.buffer.draw_rectangle(gc, False, 1, 1+offset, 21, 9)
        # fill the bars and tag on the text
        self._drawbar(dn, 0)
        self._drawbar(up, offset)
        # we updated the buffer, now force redrawing
        self.area.queue_draw()
        # finally, the tooltip
        tip = 'Download:\t%s MiB (%s%%)\n' % (dn.total, dn.total_pct)
        tip += 'Upload\t\t%s MiB (%s%%)\n' % (up.total, up.total_pct)
        tip += '\npytelemeter v%s' % VERSION
        self.tooltips.set_tip(self.tray, tip)

    def _drawbar(self, usage, offset):
        colormap = gtk.gdk.colormap_get_system()
        color = self._status_color(usage.total_pct)
        self.gc.foreground = colormap.alloc_color(color)
        width = int(round(20 * usage.total_float))
        self.buffer.draw_rectangle(self.gc, True, 2, 2+offset, width, 8)

        layout = self.area.create_pango_layout('%i%%' % usage.total_pct)
        layout.set_font_description(self.smallfont)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_width(20)
        black = self.area.get_style().black_gc
        self.buffer.draw_layout(black, 13, offset, layout)

    def _status_color(self, pct):
        if pct <= 70: return 'green'
        if pct <= 80: return 'yellow'
        if pct <= 90: return 'orange'
        return 'red'

# signal handlers
    def on_configure_event(self, area, event=None):
        # we suppose the tray area is 24x24
        self.buffer = gtk.gdk.Pixmap(area.window, 24, 24)
        background = area.get_style().bg_gc[gtk.STATE_NORMAL]
        self.buffer.draw_rectangle(background, True, 0, 0, 24, 24)
        self.gc = self.area.window.new_gc()

        # actual font size depends on screen dpi
        screen = area.get_screen()
        dpi = 25.4 * screen.get_height() / screen.get_height_mm()
        size = int(round(600 / dpi))
        self.smallfont = pango.FontDescription('Sans Serif %i' % size)

    def on_expose_event(self, area, event):
        x , y, width, height = event.area
        gc = area.get_style().fg_gc[gtk.STATE_NORMAL]
        area.window.draw_drawable(gc, self.buffer, x, y, x, y, width,
                                                                height)
        return False

    def on_tray_clicked(self, signal, event):
        if event.button == 1: # left
            if event.type == gtk.gdk.BUTTON_PRESS:
                self.showGUI(True)
        elif event.button == 2: # middle
            pass
        elif event.button == 3: # right
            if event.type == gtk.gdk.BUTTON_PRESS:
                self.menu.popup(None, None,
                    lambda x: self._menupos(x, event),
                    event.button, event.time)

    def _menupos(self, menu, event):
        x = int(event.x_root - event.x)
        y = int(event.y_root - event.y)
        monitor = menu.get_screen().get_monitor_at_point(x,y)
        rect = menu.get_screen().get_monitor_geometry(monitor)
        space_above = y - rect.y
        space_below = rect.y + rect.height - y

        width, height = menu.size_request()
        if height <= space_below:
            y += 24 # prefer just beneath
        elif height <= space_above:
            y -= height # just above
        elif space_below >= space_above:
            y += space_below - height # screen bottom
        else:
            y = rect.y # screen top
        return int(x), int(y), 1
