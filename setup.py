#!/usr/bin/env python
#
# pytelemeter install script
#
# See COPYING for info about the license (GNU GPL)
# Check AUTHORS to see who wrote this software.

from distutils.core import setup
from pytelemeter import __version__
import sys
import glob
import re

# Check for Python < 2.2
if sys.version < '2.2':
    sys.exit('Error: Python-2.2 or newer is required. Current version:\n %s'
             % sys.version)

authors = [ ('Robbie Vanbrabant', 'climaxius@users.sourceforge.net'),
            ('Thomas Matthijs', 'axxo-@users.sourceforge.net'),
            ('Joris Patroons', 'jopa@kotnet.org') ]

lname = max([len(author[0]) for author in authors])
__author__ = '\n'.join(['%s <%s>' % (author[0].ljust(lname), author[1])
                        for author in authors])

short = 'Fetch bandwidth usage statistics from the Telenet ISP'
long = '''\
Telenet is one of the largest internet providers in Belgium. Like any
other ISP in these regions, it imposes some limits on its home user's
bandwidth usage, depending mostly on the monthly fee.
The standard way users can follow up on their usage is the ISP's
website, but that generally involves a lot of clicking.

pytelemeter provides some additional, more convenient interfaces to
access these bandwidth statistics. There is a non-interactive command
line frontend, a graphical one based on the GTK toolkit and a
freedesktop.org compliant system tray icon.'''

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP' ]

setup(name='pytelemeter',
      version=__version__,
      description=short,
      long_description=long,
      classifiers=classifiers,
      author=', '.join([author[0] for author in authors]),
      author_email=', '.join([author[1] for author in authors]),
      url='http://pytelemeter.sourceforge.net',
      packages = ['pytelemeter', 'pytelemeter/parser',
      'pytelemeter/parser/scarlet', 'pytelemeter/parser/telenet'],
      scripts=glob.glob('scripts/*'),
      data_files = [('share/pixmaps', glob.glob('images/*')),
                    ('share/pytelemeter', glob.glob('glade/*glade'))],
      license='GPL'
)
