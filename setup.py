#!/usr/bin/env python
#
# pytelemeter installatiescript
# door Robbie Vanbrabant <robbie.vanbrabant@pandora.be>



from distutils.core import setup

setup(name="pytelemeter",
      version="0.8",
      description="A small Python 'Telemeter' application to check out Telenet's download/upload statistics",
      author="Robbie Vanbrabant",
      author_email="climaxius@users.sourceforge.net",
      url="http://pytelemeter.sourceforge.net",
      py_modules=["pytelemeter"],
      scripts=['scripts/pytelemeter-cli', 'scripts/pytelemeter-gtk'],
      package_dir = {'': 'lib'}
)
