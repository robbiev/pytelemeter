#!/usr/bin/env python
#
# pytelemeter installatiescript
# door Robbie Vanbrabant <robbie.vanbrabant@pandora.be>



from distutils.core import setup
import os

setup(name="pytelemeter",
      version="0.8",
      description="A small Python program to check out Telenet's download/upload statistics",
      author="Robbie Vanbrabant",
      author_email="robbie.vanbrabant@pandora.be",
      url="http://users.pandora.be/vanbrabant/robbie/soft/pytelemeter.html",
      py_modules=["pytelemeter"],
      #data_files=".pytelemeterrc",
      scripts=['scripts/pytelemeter-cli', 'scripts/pytelemeter-gtk'],
      package_dir = {'': 'lib'}
)
