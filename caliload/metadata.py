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

"""Interface to metadata.opf ."""

from caliload.configobject import ConfigObject
from caliload.optionsobject import OptionsObject
from glob import glob
from uuid import uuid1
from xml.dom import minidom
import os
import subprocess

config = ConfigObject()
options = OptionsObject()

import logging
log = logging.getLogger(__name__)

def get_text(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

def get_book_filename(dir):
	file = None
	for ext in ("epub", "pdf"):
		if not file is None: break
		for n in glob(os.path.join(dir, "*.%s" % ext)):
			if not n[0] == '_':
				file = n
				filetype = ext
				break
	if file is None:
		raise RuntimeError("Can't find an ebook file.")
	return (file, filetype)

class Metadata:

	def __init__(self, useCached=True):
		self.xmlfilename = os.path.join(options.dir, 'metadata.opf')

		self.bookfile, self.type = get_book_filename(options.dir)

		if not useCached or not os.path.exists(self.xmlfilename):
			if useCached:
				log.info("metadata.opf not found. Extracting from %s." % os.path.basename(self.bookfile))
			else:
				log.info("Loading metadata.opf from %s." % os.path.basename(self.bookfile))
			cmd = [
				config.ebookmeta_cmd, self.bookfile, '--to-opf=%s' % self.xmlfilename
			]
			subprocess.check_output(cmd)

		log.info("Reading %s." % os.path.basename(self.xmlfilename))
		self.xml = minidom.parse(self.xmlfilename)
		self.metadata = self.xml.getElementsByTagName('metadata')[0]
		self.uuidfile = os.path.join(options.dir, 'uuid')

		self.id = None
		for e in self.metadata.getElementsByTagName('dc:identifier'):
			scheme = e.getAttribute('opf:scheme')
			if scheme.lower() == 'caliload': self.id = get_text(e.childNodes)

		if self.id is None:
			self.recover_or_generateId()
		
		if not os.path.exists(self.uuidfile):
			f = open(self.uuidfile, 'w')
			f.write(self.id + '\n')
			f.close()

	def recover_or_generateId(self):
		"""Load UUID from uuid file or generate a new UUID; store UUID in metadata.opf ."""
		if os.path.exists(self.uuidfile):
			log.info("Found ID in uuid file. Writing to %s." % os.path.basename(self.xmlfilename))
			f = open(self.uuidfile, 'r')
			self.id = f.read().strip()
			f.close()
		else:
			log.info("ID not found. Creating and saving a new ID.")
			self.id = str(uuid1())
			f = open(self.uuidfile, 'w')
			f.write(self.id + '\n')
			f.close()

		# write data to XML doc
		e = self.xml.createElement('dc:identifier')
		e.setAttribute('opf:scheme', 'caliload')
		textNode = self.xml.createTextNode(str(self.id))
		e.appendChild(textNode)
		self.metadata.appendChild(e)

		# save metadata.opf
		f = open(self.xmlfilename, 'w')
		f.write(self.xml.toprettyxml(indent='', newl='', encoding='utf-8'))
		f.close()

	def write_to_book(self):
		"""Write metadata.opf to ebook file."""
		log.info("Writing metadata.opf to book file.")

		# erase old tags
		cmd = [
			config.ebookmeta_cmd, self.bookfile, "--tags="
		]
		subprocess.check_output(cmd)

		# write all metadata from opf file
		cmd = [
			config.ebookmeta_cmd, self.bookfile, '--from-opf=%s' % self.xmlfilename
		]
		subprocess.check_output(cmd)
