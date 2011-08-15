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

"""Interface to calibre command line tools."""

from caliload.configobject import ConfigObject
from caliload.db import Db
from caliload.optionsobject import OptionsObject
import subprocess

config = ConfigObject()
options = OptionsObject()

import logging
log = logging.getLogger(__name__)

class Calibre():

	def __init__(self):
		pass
	
	def insert(self, metadata):
		"""Insert an ebook file into Calibre."""
		log.info("Creating Calibre record.")
		cmd = [
			config.calibredb_cmd, "add",
			"--library-path=%s" % options.library, metadata.bookfile
		]
		subprocess.check_output(cmd)
		calibreid = Db().get_last_id()

		self.updateMetadata(calibreid, metadata)

	def update_metadata(self, calibreid, metadata):
		"""Update an ebook's metadata in Calibre."""
		log.info("Setting Calibre metadata.")
		cmd = [
			config.calibredb_cmd, 'set_metadata',
			"--library-path=%s" % options.library, calibreid, metadata.xmlfilename
		]
		subprocess.check_output(cmd)

	def update_content(self, calibreid, file):
		"""Update an ebook's content in Calibre."""
		log.info("Inserting content into Calibre.")
		cmd = [
			config.calibredb_cmd, 'add_format',
			"--library-path=%s" % options.library, calibreid, file
		]
		subprocess.check_output(cmd)

	def write_metadata_file(self, calibreid, xmlfile):
		"""Write metadata to file from Calibre's database."""
		log.info("Retrieving metadata from Calibre.")
		cmd = [
			config.calibredb_cmd, 'show_metadata',
			"--library-path=%s" % options.library, '--as-opf', calibreid
		]
		output = subprocess.check_output(cmd)

		f = open(xmlfile, "w")
		f.write(output)
		f.close()
