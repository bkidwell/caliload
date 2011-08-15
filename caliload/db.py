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

"""Interface to Calibre's sqlite database file."""

from caliload.optionsobject import OptionsObject
import sqlite3

options = OptionsObject()

conn = None

class Db:

	def __init__(self):
		global conn
		conn = sqlite3.connect(options.dbfile)

	def get_id(self, uuid):
		"""Get a Calibre database book id for a given caliload UUID."""
		cursor = conn.cursor()
		cursor.execute(
			'''SELECT book FROM identifiers
			WHERE type=? AND val=?''',
			('caliload', uuid)
		)
		row = cursor.fetchone()
		if row: return str(row[0])
		return None

	def get_last_id(self):
		"""Get last inserted Calibre database book id."""
		cursor = conn.cursor()
		cursor.execute('SELECT Max(id) FROM books')
		return str(cursor.fetchone()[0])

	def get_all_tags(self):
		"""Get a list of tags in the Calibre database."""
		cursor = conn.cursor()
		cursor.execute('SELECT name FROM tags ORDER BY name')
		return cursor.fetchall()
