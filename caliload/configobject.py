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

"""Interface to ~/.config/caliload/config ."""

import ConfigParser
import os

class ConfigObject:

	_shared_state = {}

	def __init__(self):
		self.__dict__ = self._shared_state
		if not hasattr(self, 'ready'):
			self.default_library = '~/Calibre Library'
			self.calibredb_cmd = 'calibredb'
			self.ebookmeta_cmd = 'ebook-meta'
			self.loglevel = 'WARN'
			self.configfile = os.path.expanduser('~/.config/caliload/config')
			if os.path.exists(self.configfile):
				self.read()
			else:
				self.write()
			self.ready = True

	def read(self):
		c = ConfigParser.RawConfigParser()
		c.read(self.configfile)
		if(c.has_option('paths', 'default_library')): self.default_library = c.get('paths', 'default_library')
		if(c.has_option('commands', 'calibredb')): self.calibredb_cmd = c.get('commands', 'calibredb')
		if(c.has_option('commands', 'ebook-meta')): self.ebookmeta_cmd = c.get('commands', 'ebook-meta')
		if(c.has_option('logging', 'level')): self.loglevel = c.get('logging', 'level')

	def write(self):
		c = ConfigParser.RawConfigParser()
		c.add_section('paths')
		c.set('paths', 'default_library', self.default_library)
		c.add_section('commands')
		c.set('commands', 'calibredb', self.calibredb_cmd)
		c.set('commands', 'ebook-meta', self.ebookmeta_cmd)
		c.add_section('logging')
		c.set('logging', 'level', 'WARN')
		with open(self.configfile, 'wb') as f:
			c.write(f)
