# Copyright 2011 Brendan Kidwell <brendan@glump.net>.
#
# This file is part of caliload.
#
# caliload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# caliload is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with caliload.  If not, see <http://www.gnu.org/licenses/>.

"""Interface to command line options."""

from caliload import VERSION
from caliload.configobject import ConfigObject
import caliload
import getopt
import os
import sys

config = ConfigObject()

import logging
log = logging.getLogger(__name__)

HELPTEXT = '''\
Usage: %s COMMAND [options] [arguments]

caliload is a wrapper script for various Calibre command line tools that
allows you to add and update books from an offline library.

Commands:

db_add         Adds an ebook to Calibre.
db_update      Updates ebook in Calibre.
db_readmeta    Read metadata from Calibre to metadata.opf .
db_tags        List tags from database.
db_meta_pull   Pull metadata from DB to metadata.opf, ebook file, and
               Calibre's copy of the ebook file.
readmeta       Read metadata from ebook file to metadata.opf .
writemeta      Write metadata from metadata.opf to ebook file.
config         Edit configuration file.

Options:

--dir=DIR       Work with book in DIR.
--library=DIR   Work with Calibre library in DIR (default ~/Calibre
                Library).
--debug         Display debug messages.

Exit Codes (general):
  0   Command completed successfully.
'''

ACTIONS = '''
	help version db_add db_update db_readmeta db_tags db_meta_pull readmeta writemeta config
'''.strip().split(' ')

class OptionsObject:

	_shared_state = {}

	def __init__(self, argv=None):
		self.__dict__ = self._shared_state
		if hasattr(self, 'ready'): return

		if argv is None: argv = sys.argv
		self.scriptname = os.path.basename(argv[0])
		self.calibredb = 'calibredb'
		self.set_library(os.path.expanduser(config.default_library))
		self.ebookmeta = 'ebook-meta'
		self.action = 'help'
		self.exitcode = 0
		self.argv = argv
		self.dir = os.getcwd()

		if(argv is None or len(argv) < 1):
			self.exitcode = 1
			self.action = 'help'
			return

		self.optlist, self.args = getopt.getopt(argv[1:], '', ['version', 'help', 'dir=', 'debug'])
		if len(self.args) > 0: self.action = self.args[0] # action is first unnamed argument
		if len(self.args) > 1: self.args = self.args[1:] # remove first unnamed argument

		if self.action == '--version':
			self.action = 'version'
	
		if self.action in ('help', '-h', '-?', '--help'):
			self.action = 'help'
		
		if self.action not in ACTIONS:
			self.exitcode = 1
			self.action = 'help'
		
		logging.basicConfig(level=config.loglevel)

		for (key, value) in self.optlist:
			if key == '--dir': self.dir = value
			if key == '--library': self.set_library(value)
			if key == '--debug':
				logging.basicConfig(level=logging.DEBUG)
			if key in ('--help', '-h'): self.action = 'help'
			if key in ('--version', '-v'): self.action = 'version'
		
		log.info('Using Calibre library:\n   %s' % self.get_library())
		log.info('Working folder for book files:\n   %s' % self.dir)

		self.ready = True
	
	def set_library(self, value):
		self._library = value
		self.dbfile = os.path.join(self._library, 'metadata.db')
	
	def get_library(self):
		return self._library
	
	def get_help(self):
		return HELPTEXT % self.scriptname
	
	library = property(get_library, set_library)
