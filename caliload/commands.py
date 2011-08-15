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

"""Command actions."""

from caliload.calibre import Calibre
from caliload.configobject import ConfigObject
from caliload.db import Db
from caliload.metadata import Metadata
from caliload.optionsobject import OptionsObject
import caliload
import subprocess

conf = ConfigObject()
options = OptionsObject()

import logging
log = logging.getLogger(__name__)

def help():
	help = options.get_help()
	if options.exitcode: help = 'Invalid command line options specified.\n\n' + help
	return options.exitcode, help

def version():
	return 0, '%s %s' % (caliload.APPNAME, caliload.VERSION)

def db_add():
	metadata = Metadata()
	db = Db()
	calibreid = db.get_id(metadata.id)
	if calibreid is None:
		c = Calibre()
		c.insert(metadata)
		return 0, 'Finished inserting %s.' % options.dir
	else:
		return 1, 'Book already exists in Calibre: %s' % options.dir

def db_update():
	metadata = Metadata()
	db = Db()
	calibreid = db.get_id(metadata.id)
	if calibreid is None:
		return 1, 'Book not found in Calibre: %s' % options.dir
	
	c = Calibre()
	c.update_content(calibreid, metadata.bookfile)
	c.update_metadata(calibreid, metadata)

	return 0, 'Finished updating in Calibre: %s' % options.dir

def readmeta():
	metadata = Metadata(useCached=False)

	return 0, 'Finished reading metadata from book file in %s.' % options.dir

def db_readmeta():
	metadata = Metadata()
	db = Db()
	calibreid = db.get_id(metadata.id)

	if calibreid is None:
		return 1, 'Book not found in Calibre: %s' % options.dir

	c = Calibre()
	c.write_metadata_file(calibreid, metadata.xmlfilename)

	return 0, 'Finished reading metadata from Calibre for %s.' % options.dir

def writemeta():
	metadata = Metadata()
	metadata.write_to_book()

	return 0, 'Finished writing metadata from book file in %s.' % options.dir

def db_tags():
	tags = Db().get_all_tags()
	return 0, "\n".join(t[0] for t in tags)

def db_meta_pull():
	metadata = Metadata()
	db = Db()
	calibreid = db.get_id(metadata.id)

	if calibreid is None:
		return 1, 'Book not found in Calibre: %s' % options.dir

	# save metadata from Calibre to metadata.opf
	c = Calibre()
	c.write_metadata_file(calibreid, metadata.xmlfilename)

	# reload metadata from metadata.opf
	metadata = Metadata()
	metadata.write_to_book()

	# push book file with new metadata to Calibre
	c.update_content(calibreid, metadata.bookfile)

	return 0, "Finished updating content and metadata file from Calibre's metadata for %s." % options.dir

def config():
	cmd = ['sensible-editor', conf.configfile]
	subprocess.call(cmd)

	return 0, ''
