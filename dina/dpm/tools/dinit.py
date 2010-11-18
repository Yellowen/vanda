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
#
#
#    "dinit" is a tool for building a initialized environment for building
#    Dina packages.
#    Dina packages are simply any django application, but they packaged for
#    Dina Package Manager (DPM).
# -----------------------------------------------------------------------------

import os
import sys
import json
from optparse import OptionParser


# TODO: gather a complete list of licenses
# via http://www.gnu.org/licenses/license-list.html
licenses = {
    "free": {
        "1": "GNU General Public License (GPL) version 3",
        "2": "GNU General Public License (GPL) version 2",
        },
    "open": {
        },
    "nonfree": {
        }
    }

parser = OptionParser()
parser.add_option("-a", "--auto", dest="auto",\
                  help="Try to build control file automaticaly")

option, args = parser.parse_args()

if __name__ == "__main__":

    try:
        os.mkdir("dina")
    except OSError, e:
        err = e.split("]")
        print e.strip()
        os.exit(1)

    if option.auto:
        pass

    else:
        pkg = dict()
        name = raw_input("Application name: ")
        # TODO: check for illegal characters
        pkg['name'] = name.strip().replace(' ', '_')
        version = raw_input("Application version: ")
        pkg['version'] = version.strip().replace(" ", "_")
        # TODO: check for GPL compatiblity and Section
