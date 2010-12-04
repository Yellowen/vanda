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

import os

from control import Control
from utils import safe_join


class Package (object):
    """
    DPM package base class. an interface to DPM packages.
    """

    def __init__(self, path=None):
        if path:
            # package exists
            # initialize Package from a tarball file

            # TODO: package class should initilized from a tarball
        else:
            # initialize a empty package shell
            self._path = safe_join(path, "dina")
            if os.path.exists(self._path):
                try:
                    self.control = Control(self._path)
                except Control.DoesNotExist():
                    raise

