#!/usr/bin/env python
#
# pytelemeter install script 
# Installs all files needed.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

from distutils.core import setup
from pytelemeter import VERSION
import sys

try:
    from dsextras import TemplateExtension, getoutput, GLOBAL_MACROS
except ImportError:
    try:
        from gtk.dsextras import TemplateExtension, getoutput, GLOBAL_MACROS
    except ImportError:
        sys.exit('Error: Can not find dsextras or gtk.dsextras')

#Stuff for dsextras to work properly
sys.path.insert(0, getoutput('pkg-config --variable=codegendir pygtk-2.0'))
GLOBAL_MACROS+=[('GETTEXT_PACKAGE','"pytelemeter"')]
	
# Check for Python < 2.1
if sys.version < '2.2':
    sys.exit('Error: Python-2.2 or newer is required. Current version:\n %s'
             % sys.version)

def modules_check():
    '''Check if necessary modules is installed.
    The function is executed by distutils (by the install command).'''
    try:
        import pygtk
        pygtk.require('2.0')
        imp.find_module('gtk')
    except AssertionError:
        # We ignore this because gtk must be present to build"
        pass
    except:
        sys.exit('Error: PyGTK 2 or newer is required.')

setup(name="pytelemeter",
      version=VERSION,
      description="A small Python 'Telemeter' application to check out Telenet's download/upload statistics",
      author="Robbie Vanbrabant, Thomas Matthijs",
      author_email="climaxius@users.sourceforge.net, axxo-@users.sourceforge.net",
      url="http://pytelemeter.sourceforge.net",
      scripts=['scripts/pytelemeter-cli', 'scripts/pytelemeter-gtk', 'scripts/pytelemeter-tray'],
      packages = ['pytelemeter'],
      ext_modules = [TemplateExtension(name='trayicon',
			pkc_name='pygtk-2.0 gtk+-2.0',
			pkc_version='2.0.0',
			output='pytelemeter.pytrayicon',
			defs='eggtray/trayicon.defs',
			sources=['eggtray/trayiconmodule.c',
				'eggtray/trayicon.c',
				'eggtray/eggtrayicon.c'],
			register=['eggtray/trayicon.defs'],
			override='eggtray/trayicon.override')]
)
