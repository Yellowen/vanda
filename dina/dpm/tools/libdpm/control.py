#! /usr/bin/env python
# -----------------------------------------------------------------------------
#    Dina Project
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

import json
from libdpm.utils import safe_join

class Control (object):
    """
    Control class is a interface to dina/control file.
    """

    def __init__(self, cwd):
        self._control = json.loads(file(safe_join(cwd, "control")))

    def validate(self):
        if "package" not in self._control:
            raise 
