#!/usr/bin/env python
#
# pytelemeter install script 
# Installs all files needed.
# 
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.



from distutils.core import setup
from pytelemeter import VERSION

setup(name="pytelemeter",
      version=VERSION,
      description="A small Python 'Telemeter' application to check out Telenet's download/upload statistics",
      author="Robbie Vanbrabant, Thomas Matthijs",
      author_email="climaxius@users.sourceforge.net, axxo-@users.sourceforge.net",
      url="http://pytelemeter.sourceforge.net",
      scripts=['scripts/pytelemeter-cli', 'scripts/pytelemeter-gtk'],
      packages = ['pytelemeter']
)
