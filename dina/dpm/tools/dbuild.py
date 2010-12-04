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
import sys
import json
from optparse import OptionParser
from libdpm.control import Control

parser = OptionParser()
parser.add_option("-v", "--verbose", dest="license",
                  help="The license of package.")

option, args = parser.parse_args()


if __name__ == "__main__":

    cwd = os.getcwd()
    # Check for dina directory
    DINA = safe_join(cwd, "dina")
    if not os.path.exists(DINA):
        print "Error: 'dina' directory does not exists."
        sys.exit(1)

    conf_dict = file(safe_join(DINA, "control")).read()
    try:
        control = Control(conf_dict)
    except Config.DoesNotValid, err:
        print "Validation Error: ", str(err)
        

    
