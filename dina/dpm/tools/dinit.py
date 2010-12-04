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
#    dinit will build a basic dina packaging environment for easy development
#    dinit make some files inside a folder with the name of "dina" inside of
#    application source tree.
# TODO: build dinit development documentation in Sphinx

import os
import sys
import json
from optparse import OptionParser

from libdpm.control import Control
from libdpm.utils import safe_join


# TODO: gather a complete list of licenses
# via http://www.gnu.org/licenses/license-list.html
licenses = {
    "compatibel": {
        "1": "GNU General Public License (GPL) version 3",
        "2": "GNU General Public License (GPL) version 2",
        },
    "non-compatible": {
        },
    "nonfree": {
        }
    }


parser = OptionParser()
# TODO: add license option
parser.add_option("-l", "--license", dest="license",
                  help="The license of package.")

option, args = parser.parse_args()


if __name__ == "__main__":

    try:
        os.mkdir("dina")
    except OSError, e:
        err = str(e).split("]")
        print str(e).strip()
        sys.exit(1)

    # TODO: retrive version and name of the package
    # from the parent directory just like debian
    # package building system
    dirname = os.getcwd().split("/")[-1].split("-")
    config = Control(safe_join(os.getcwd(), "dina"), new=True)
    if len(dirname) < 2:
        print "Error: Your project directory name shoud be in NAME-VERSION format."
        os.rmdir("dina")
        sys.exit(1)
    name = dirname[0]
    version = dirname[1:].replace(" ", "_")
    config._control["Source"] = name.capitalize().replace(" ", "_")
    config._control["Package"] = name.lower().replace(" ", "_")
    if len(version.split(".")) == 3:
        config._control["Version"] = version
        print "Version should be a 3 section type"
        os.rmdir("dina")
        sys.exit(1)

    config.flush()
    # TODO: add changelog
    # TODO: add copyright file
    # TODO: add watch file
    # TODO: add patch folder
    # TODO: add README.dina
    # TODO: add preintall.py
    # TODO: add postinstall.py
    # TODO: add prerm.py
    # TODO: add postrm.py
    print "Done"
