#!/usr/bin/env python

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

"""Launch script"""

from caliload import commands
from caliload.optionsobject import OptionsObject
import caliload
import sys

options = OptionsObject()

cmd = getattr(commands, options.action)
(exitcode, output) = cmd()
if output: print output
sys.exit(exitcode)
