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

from gladegui import *
from parser import *
from __init__ import *


# constants
UP = {  'down': 'Download:',
        'up':   'Upload:\t',
        'sum':  'Transfer:\t'
}


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
        self.area.connect_after('realize', self.on_realize_area)

        eventbox = gtk.EventBox()
        eventbox.connect('button_press_event', self.on_tray_clicked)
        eventbox.add(self.area)
        self.tray.add(eventbox)

        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.tray,'Pytelemeter v%s' % __version__)

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
        bars = []
        if self.meter.usage:
            totals = self.meter.usage.totals
            for dir in ('down', 'up', 'sum'):
                if totals.has_key(dir):
                    bars.append(totals[dir])

        # blank the area
        gc = self.area.get_style().bg_gc[gtk.STATE_NORMAL]
        self.buffer.draw_rectangle(gc, True, 0, 0, 24, 24)
        # draw the bars and tag on the text
        if len(bars) >= 1:
            if len(bars) >= 2:
                self._drawbar(bars[0], 0)
                self._drawbar(bars[1], 11)
            else:
                self._drawbar(bars[0], 5)
        else:
            pass #TODO draw the logo
        # we updated the buffer, now force redrawing
        self.area.queue_draw()
        # finally, the tooltip
        tip = ''
        line = '%s\t%s MiB (%s%%)\n'
        for bar in bars:
            tip += line % (UP[bar.constraint], bar.mib, bar.pct)
        tip += '\npytelemeter v%s' % __version__
        self.tooltips.set_tip(self.tray, tip)

    def _drawbar(self, usage, offset):
        colormap = gtk.gdk.colormap_get_system()
        color = self._status_color(usage.pct)
        self.gc.foreground = colormap.alloc_color(color)
        width = int(round(20 * usage.float))
        self.buffer.draw_rectangle(self.gc, True, 2, 2+offset, width, 8)

        layout = self.area.create_pango_layout('%i%%' % usage.pct)
        layout.set_font_description(self.smallfont)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_width(20)
        black = self.area.get_style().black_gc
        self.buffer.draw_layout(black, 12, 1+offset, layout)

        self.buffer.draw_rectangle(black, False, 1, 1+offset, 21, 9)

    def _status_color(self, pct):
        if pct <= 70: return 'green'
        if pct <= 80: return 'yellow'
        if pct <= 90: return 'orange'
        return 'red'

# signal handlers
    def on_realize_area(self, area):
        # we suppose the tray area is 24x24
        self.buffer = gtk.gdk.Pixmap(area.window, 24, 24)
        background = area.get_style().bg_gc[gtk.STATE_NORMAL]
        self.buffer.draw_rectangle(background, True, 0, 0, 24, 24)
        self.gc = area.window.new_gc()

        # actual font size depends on screen dpi
        screen = area.get_screen()
        dpi = 25.4 * screen.get_height() / screen.get_height_mm()
        size = int(round(675 / dpi))
        self.smallfont = pango.FontDescription('FreeSans,sans %i' % size)

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
